-- Ejecuta este SQL en Supabase SQL Editor para asignar rol director
-- Reemplaza el correo por el usuario que ya existe en auth.users/profiles

update public.profiles
set role = 'director',
    is_active = true
where email = 'director@empresa.com';

-- Verificacion
select id, email, full_name, role, is_active
from public.profiles
where email = 'director@empresa.com';
