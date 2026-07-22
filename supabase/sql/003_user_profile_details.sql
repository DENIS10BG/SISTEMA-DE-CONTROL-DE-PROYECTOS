-- Normalizacion de datos de usuario:
-- 1) auth.users = correo + password (gestionado por Supabase Auth)
-- 2) public.profiles = acceso, rol y estado de cuenta
-- 3) public.profile_details = datos personales/administrativos

create table if not exists public.profile_details (
  user_id uuid primary key references public.profiles(id) on delete cascade,
  first_name text not null,
  last_name text,
  birth_date date,
  address text,
  phone text,
  national_id text,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint profile_details_phone_chk
    check (phone is null or phone ~ '^[0-9+() -]{6,20}$'),
  constraint profile_details_national_id_chk
    check (national_id is null or length(trim(national_id)) between 4 and 32)
);

create unique index if not exists profile_details_national_id_uidx
  on public.profile_details (national_id)
  where national_id is not null;

-- Reusar helper de updated_at existente
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists profile_details_set_updated_at on public.profile_details;
create trigger profile_details_set_updated_at
before update on public.profile_details
for each row
execute procedure public.set_updated_at();

-- Backfill para usuarios ya existentes
insert into public.profile_details (user_id, first_name, last_name)
select
  p.id,
  coalesce(nullif(split_part(p.full_name, ' ', 1), ''), 'Usuario'),
  nullif(trim(regexp_replace(p.full_name, '^\\S+\\s*', '')), '')
from public.profiles p
left join public.profile_details d on d.user_id = p.id
where d.user_id is null;

-- Al registrar un usuario nuevo, crear tambien su fila de detalles
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  metadata_name text;
  first_name_value text;
  last_name_value text;
begin
  metadata_name := coalesce(new.raw_user_meta_data ->> 'full_name', split_part(new.email, '@', 1));
  first_name_value := coalesce(nullif(split_part(metadata_name, ' ', 1), ''), 'Usuario');
  last_name_value := nullif(trim(regexp_replace(metadata_name, '^\\S+\\s*', '')), '');

  insert into public.profiles (id, email, full_name, role)
  values (new.id, new.email, metadata_name, 'archivero')
  on conflict (id) do update
  set email = excluded.email,
      full_name = excluded.full_name;

  insert into public.profile_details (user_id, first_name, last_name)
  values (new.id, first_name_value, last_name_value)
  on conflict (user_id) do nothing;

  return new;
end;
$$;

-- Permisos Data API
grant select, insert, update, delete on table public.profile_details to authenticated;

alter table public.profile_details enable row level security;

-- Usuario autenticado: ver/editar solo su detalle
-- Director: administrar todos los detalles

drop policy if exists "profile_details_select_own" on public.profile_details;
create policy "profile_details_select_own"
on public.profile_details
for select
to authenticated
using ((select auth.uid()) = user_id);

drop policy if exists "profile_details_update_own" on public.profile_details;
create policy "profile_details_update_own"
on public.profile_details
for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

drop policy if exists "profile_details_director_select_all" on public.profile_details;
create policy "profile_details_director_select_all"
on public.profile_details
for select
to authenticated
using (public.is_director());

drop policy if exists "profile_details_director_insert_all" on public.profile_details;
create policy "profile_details_director_insert_all"
on public.profile_details
for insert
to authenticated
with check (public.is_director());

drop policy if exists "profile_details_director_update_all" on public.profile_details;
create policy "profile_details_director_update_all"
on public.profile_details
for update
to authenticated
using (public.is_director())
with check (public.is_director());

drop policy if exists "profile_details_director_delete_all" on public.profile_details;
create policy "profile_details_director_delete_all"
on public.profile_details
for delete
to authenticated
using (public.is_director());

-- Vista util para paneles de frontend
create or replace view public.users_full
with (security_invoker = true)
as
select
  p.id,
  p.email,
  p.full_name,
  p.role,
  p.is_active,
  d.first_name,
  d.last_name,
  d.birth_date,
  d.address,
  d.phone,
  d.national_id,
  d.avatar_url,
  p.created_at,
  p.updated_at
from public.profiles p
left join public.profile_details d on d.user_id = p.id;

grant select on public.users_full to authenticated;
