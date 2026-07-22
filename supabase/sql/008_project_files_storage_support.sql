-- Soporte para vista previa y archivo PDF en Supabase Storage
-- Extiende public.project_files con rutas/urls de visualizacion

alter table if exists public.project_files
  add column if not exists storage_path text,
  add column if not exists file_url text,
  add column if not exists preview_image_url text;

-- Bucket para PDFs de proyectos
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'project-files',
  'project-files',
  true,
  52428800,
  array['application/pdf']
)
on conflict (id) do update
set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

-- Politicas de acceso al bucket
drop policy if exists "project_files_storage_select_anon" on storage.objects;
create policy "project_files_storage_select_anon"
on storage.objects
for select
to anon, authenticated
using (bucket_id = 'project-files');

drop policy if exists "project_files_storage_insert_anon" on storage.objects;
create policy "project_files_storage_insert_anon"
on storage.objects
for insert
to anon, authenticated
with check (bucket_id = 'project-files');

drop policy if exists "project_files_storage_update_anon" on storage.objects;
create policy "project_files_storage_update_anon"
on storage.objects
for update
to anon, authenticated
using (bucket_id = 'project-files')
with check (bucket_id = 'project-files');

drop policy if exists "project_files_storage_delete_anon" on storage.objects;
create policy "project_files_storage_delete_anon"
on storage.objects
for delete
to anon, authenticated
using (bucket_id = 'project-files');
