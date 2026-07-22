-- Hotfix para error 500 en users_full por recursion RLS
-- Ejecutar en Supabase SQL Editor

-- 1) Reemplazar helper de autorizacion para evitar recursion de politicas
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

-- Limitar ejecucion explicita de la funcion
revoke all on function public.is_director() from public;
grant execute on function public.is_director() to authenticated;

-- 2) Re-crear politicas de profiles para limpiar estados anteriores
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
with check (
  (select auth.uid()) = id
  and role = (
    select p.role
    from public.profiles p
    where p.id = (select auth.uid())
  )
);

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

-- 3) Re-aplicar grants sobre vista (seguridad por si faltan)
grant select on public.users_full to authenticated;
