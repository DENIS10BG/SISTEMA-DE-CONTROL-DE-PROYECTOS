-- Aumentar limite de tamano para archivos del bucket project-files
-- Valor: 500 MB

update storage.buckets
set file_size_limit = 524288000
where id = 'project-files';
