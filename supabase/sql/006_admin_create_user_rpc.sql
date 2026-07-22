-- Crear usuarios desde frontend sin rate limit de correo
-- Ejecutar en Supabase SQL Editor

create extension if not exists pgcrypto with schema extensions;

create or replace function public.admin_create_user_with_profile(
  p_email text,
  p_password text,
  p_first_name text,
  p_last_name text,
  p_birth_date date default null,
  p_address text default null,
  p_phone text default null,
  p_national_id text default null,
  p_role public.user_role default 'archivero',
  p_is_active boolean default true
)
returns uuid
language plpgsql
security definer
set search_path = public, auth, extensions
as $$
declare
  v_uid uuid;
  v_email text;
  v_first_name text;
  v_last_name text;
  v_full_name text;
begin
  if not public.is_director() then
    raise exception 'Solo director puede crear usuarios';
  end if;

  v_email := lower(trim(p_email));
  v_first_name := trim(coalesce(p_first_name, ''));
  v_last_name := trim(coalesce(p_last_name, ''));
  v_full_name := trim(concat_ws(' ', v_first_name, v_last_name));

  if v_email = '' or position('@' in v_email) = 0 then
    raise exception 'Correo invalido';
  end if;

  if length(coalesce(p_password, '')) < 6 then
    raise exception 'La contrasena debe tener al menos 6 caracteres';
  end if;

  if v_first_name = '' then
    raise exception 'Nombre requerido';
  end if;

  if exists (select 1 from auth.users where email = v_email) then
    raise exception 'El correo ya esta registrado';
  end if;

  v_uid := extensions.gen_random_uuid();

  insert into auth.users (
    id,
    instance_id,
    aud,
    role,
    email,
    encrypted_password,
    email_confirmed_at,
    invited_at,
    confirmation_token,
    recovery_token,
    email_change_token_new,
    email_change,
    raw_app_meta_data,
    raw_user_meta_data,
    created_at,
    updated_at
  )
  values (
    v_uid,
    '00000000-0000-0000-0000-000000000000',
    'authenticated',
    'authenticated',
    v_email,
    extensions.crypt(p_password, extensions.gen_salt('bf')),
    now(),
    now(),
    '',
    '',
    '',
    '',
    jsonb_build_object('provider', 'email', 'providers', array['email']),
    jsonb_build_object('full_name', v_full_name),
    now(),
    now()
  );

  insert into auth.identities (
    id,
    user_id,
    identity_data,
    provider,
    provider_id,
    created_at,
    updated_at,
    last_sign_in_at
  )
  values (
    extensions.gen_random_uuid(),
    v_uid,
    jsonb_build_object('sub', v_uid::text, 'email', v_email),
    'email',
    v_uid::text,
    now(),
    now(),
    now()
  );

  update public.profiles
  set
    full_name = case when v_full_name = '' then 'Usuario' else v_full_name end,
    role = p_role,
    is_active = p_is_active
  where id = v_uid;

  update public.profile_details
  set
    first_name = case when v_first_name = '' then 'Usuario' else v_first_name end,
    last_name = nullif(v_last_name, ''),
    birth_date = p_birth_date,
    address = nullif(trim(coalesce(p_address, '')), ''),
    phone = nullif(trim(coalesce(p_phone, '')), ''),
    national_id = nullif(trim(coalesce(p_national_id, '')), '')
  where user_id = v_uid;

  return v_uid;
end;
$$;

revoke all on function public.admin_create_user_with_profile(text, text, text, text, date, text, text, text, public.user_role, boolean) from public;
grant execute on function public.admin_create_user_with_profile(text, text, text, text, date, text, text, text, public.user_role, boolean) to authenticated;
