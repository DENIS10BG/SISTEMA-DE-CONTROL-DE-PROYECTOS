-- Guardar rutas de subcarpetas base del proyecto
-- CAO, Archivos Destacados y Archivos Fijos

alter table if exists public.project_files
  add column if not exists cao_directory text,
  add column if not exists featured_directory text,
  add column if not exists fixed_directory text;

update public.project_files
set
  cao_directory = coalesce(cao_directory, local_directory || '\\CAO'),
  featured_directory = coalesce(featured_directory, local_directory || '\\Archivos Destacados'),
  fixed_directory = coalesce(fixed_directory, local_directory || '\\Archivos Fijos')
where local_directory is not null;
