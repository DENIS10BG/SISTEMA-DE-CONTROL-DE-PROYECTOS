-- OBSOLETO para el enfoque actual.
-- Antes: relacionaba filas CAO dentro de project_files.
-- Ahora: los CAO viven en public.cao_files y se relacionan con project_files mediante project_id.
-- Usa 012_cao_files_registry.sql como modelo vigente.

-- Relacionar filas CAO con su proyecto principal
-- parent_project_id apunta a public.project_files(id)

alter table if exists public.project_files
  add column if not exists parent_project_id uuid references public.project_files(id) on delete set null;

create index if not exists project_files_parent_project_id_idx
  on public.project_files (parent_project_id);

-- Backfill basico para CAO existentes usando el titulo guardado en parent_file
update public.project_files cao
set parent_project_id = parent.id
from public.project_files parent
where cao.file_type = 'CAO'
  and cao.parent_project_id is null
  and parent.file_type = 'Proyecto'
  and cao.parent_file = parent.title;
