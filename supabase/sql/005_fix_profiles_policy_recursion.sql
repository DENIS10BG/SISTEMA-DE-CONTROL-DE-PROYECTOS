-- Fix definitivo para recursion RLS en profiles
-- Ejecutar en Supabase SQL Editor

-- 1) Helper de rol sin recursion
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
    where p.id = (select auth.uid())
      and p.role = 'director'
      and p.is_active = true
  );
$$;

revoke all on function public.is_director() from public;
grant execute on function public.is_director() to authenticated;

-- 2) Politicas de profiles sin subconsultas a la misma tabla (evita recursion)
drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
on public.profiles
for select
to authenticated
using ((select auth.uid()) = id);

drop policy if exists "profiles_update_own_without_role_change" on public.profiles;
create policy "profiles_update_own_without_role_change"
on public.profiles
for update
to authenticated
using ((select auth.uid()) = id)
with check ((select auth.uid()) = id);

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

-- 3) Trigger para impedir que un usuario no-director se cambie su propio rol
create or replace function public.prevent_self_role_change()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if (new.id = (select auth.uid())) and not public.is_director() and (new.role is distinct from old.role) then
    raise exception 'No puedes cambiar tu propio rol';
  end if;

  return new;
end;
$$;

drop trigger if exists profiles_prevent_self_role_change on public.profiles;
create trigger profiles_prevent_self_role_change
before update on public.profiles
for each row
execute procedure public.prevent_self_role_change();

-- 4) Asegurar acceso a vista
grant select on public.users_full to authenticated;
