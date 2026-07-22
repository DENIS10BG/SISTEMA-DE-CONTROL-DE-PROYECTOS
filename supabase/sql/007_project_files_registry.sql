-- Registro de archivos de proyectos subidos por usuarios
-- Guarda metadatos en Supabase y la direccion local donde se almacena el PDF

create extension if not exists pgcrypto with schema extensions;

create table if not exists public.project_files (
  id uuid primary key default extensions.gen_random_uuid(),
  title text not null,
  place text not null,
  year text not null,
  file_type text not null,
  cao_code text,
  parent_file text,
  local_directory text not null,
  local_file_name text not null,
  uploaded_by uuid references public.profiles(id) on delete set null,
  is_processed boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint project_files_year_chk check (year ~ '^[0-9]{4}$'),
  constraint project_files_file_type_chk check (file_type in ('Proyecto', 'CAO'))
);

create index if not exists project_files_created_at_idx
  on public.project_files (created_at desc);

create index if not exists project_files_title_idx
  on public.project_files (title);

create index if not exists project_files_place_idx
  on public.project_files (place);

create index if not exists project_files_year_idx
  on public.project_files (year);

-- Reusar helper de updated_at
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists project_files_set_updated_at on public.project_files;
create trigger project_files_set_updated_at
before update on public.project_files
for each row
execute procedure public.set_updated_at();

-- Data API: permitir lectura/escritura para app con clave publishable
grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on table public.project_files to anon, authenticated;

alter table public.project_files enable row level security;

drop policy if exists "project_files_select_all" on public.project_files;
create policy "project_files_select_all"
on public.project_files
for select
to anon, authenticated
using (true);

drop policy if exists "project_files_insert_all" on public.project_files;
create policy "project_files_insert_all"
on public.project_files
for insert
to anon, authenticated
with check (true);

drop policy if exists "project_files_update_all" on public.project_files;
create policy "project_files_update_all"
on public.project_files
for update
to anon, authenticated
using (true)
with check (true);

drop policy if exists "project_files_delete_all" on public.project_files;
create policy "project_files_delete_all"
on public.project_files
for delete
to anon, authenticated
using (true);
