-- Tabla dedicada para CAO relacionados a project_files
-- project_files queda reservado para proyectos principales

create extension if not exists pgcrypto with schema extensions;

create table if not exists public.cao_files (
  id uuid primary key default extensions.gen_random_uuid(),
  project_id uuid not null references public.project_files(id) on delete cascade,
  title text not null,
  cao_code text not null,
  place text not null,
  year text not null,
  local_directory text not null,
  local_file_name text not null,
  uploaded_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint cao_files_year_chk check (year ~ '^[0-9]{4}$')
);

create index if not exists cao_files_project_id_idx
  on public.cao_files (project_id);

create index if not exists cao_files_created_at_idx
  on public.cao_files (created_at desc);

create index if not exists cao_files_code_idx
  on public.cao_files (cao_code);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists cao_files_set_updated_at on public.cao_files;
create trigger cao_files_set_updated_at
before update on public.cao_files
for each row
execute procedure public.set_updated_at();

grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on table public.cao_files to anon, authenticated;

alter table public.cao_files enable row level security;

drop policy if exists "cao_files_select_all" on public.cao_files;
create policy "cao_files_select_all"
on public.cao_files
for select
to anon, authenticated
using (true);

drop policy if exists "cao_files_insert_all" on public.cao_files;
create policy "cao_files_insert_all"
on public.cao_files
for insert
to anon, authenticated
with check (true);

drop policy if exists "cao_files_update_all" on public.cao_files;
create policy "cao_files_update_all"
on public.cao_files
for update
to anon, authenticated
using (true)
with check (true);

drop policy if exists "cao_files_delete_all" on public.cao_files;
create policy "cao_files_delete_all"
on public.cao_files
for delete
to anon, authenticated
using (true);

-- Migracion basica de CAO existentes que antes estaban en project_files
insert into public.cao_files (
  project_id,
  title,
  cao_code,
  place,
  year,
  local_directory,
  local_file_name,
  uploaded_by,
  created_at,
  updated_at
)
select
  parent_project_id,
  title,
  coalesce(cao_code, title),
  place,
  year,
  local_directory,
  local_file_name,
  uploaded_by,
  created_at,
  updated_at
from public.project_files
where file_type = 'CAO'
  and parent_project_id is not null
  and not exists (
    select 1
    from public.cao_files c
    where c.project_id = public.project_files.parent_project_id
      and c.title = public.project_files.title
      and c.local_file_name = public.project_files.local_file_name
  );
