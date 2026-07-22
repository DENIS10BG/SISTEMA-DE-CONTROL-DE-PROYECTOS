-- Estado de procesado para registros CAO
-- false al subir, luego puede cambiarse a true cuando corresponda

alter table if exists public.cao_files
  add column if not exists is_processed boolean not null default false;

update public.cao_files
set is_processed = false
where is_processed is null;
