-- Roles de usuario para el sistema
do $$
begin
  if not exists (
    select 1
    from pg_type t
    join pg_namespace n on n.oid = t.typnamespace
    where t.typname = 'user_role'
      and n.nspname = 'public'
  ) then
    create type public.user_role as enum ('director', 'jefe_seccion', 'archivero');
  end if;
end;
$$;

-- Perfil asociado al usuario de auth
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text not null unique,
  full_name text not null,
  role public.user_role not null default 'archivero',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Timestamp de actualizacion
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists profiles_set_updated_at on public.profiles;
create trigger profiles_set_updated_at
before update on public.profiles
for each row
execute procedure public.set_updated_at();

-- Funcion para saber si el usuario autenticado es director
create or replace function public.is_director()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.profiles p
    where p.id = auth.uid()
      and p.role = 'director'
      and p.is_active = true
  );
$$;

-- Crear perfil automaticamente al registrarse
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  metadata_name text;
begin
  metadata_name := coalesce(new.raw_user_meta_data ->> 'full_name', split_part(new.email, '@', 1));

  insert into public.profiles (id, email, full_name, role)
  values (new.id, new.email, metadata_name, 'archivero')
  on conflict (id) do update
  set email = excluded.email,
      full_name = excluded.full_name;

  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row
execute procedure public.handle_new_user();

-- Exposicion al Data API y permisos basicos
grant usage on schema public to authenticated;
grant select, insert, update, delete on table public.profiles to authenticated;

-- Seguridad de filas
alter table public.profiles enable row level security;

-- Cada usuario ve su propio perfil
drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
on public.profiles
for select
to authenticated
using ((select auth.uid()) = id);

-- Cada usuario puede editar su perfil sin cambiarse el rol
drop policy if exists "profiles_update_own_without_role_change" on public.profiles;
create policy "profiles_update_own_without_role_change"
on public.profiles
for update
to authenticated
using ((select auth.uid()) = id)
with check (
  (select auth.uid()) = id
  and role = (
    select p.role
    from public.profiles p
    where p.id = (select auth.uid())
  )
);

-- Director puede ver y administrar todos los perfiles
drop policy if exists "profiles_director_select_all" on public.profiles;
create policy "profiles_director_select_all"
on public.profiles
for select
to authenticated
using (public.is_director());

drop policy if exists "profiles_director_insert_all" on public.profiles;
create policy "profiles_director_insert_all"
on public.profiles
for insert
to authenticated
with check (public.is_director());

drop policy if exists "profiles_director_update_all" on public.profiles;
create policy "profiles_director_update_all"
on public.profiles
for update
to authenticated
using (public.is_director())
with check (public.is_director());

drop policy if exists "profiles_director_delete_all" on public.profiles;
create policy "profiles_director_delete_all"
on public.profiles
for delete
to authenticated
using (public.is_director());
