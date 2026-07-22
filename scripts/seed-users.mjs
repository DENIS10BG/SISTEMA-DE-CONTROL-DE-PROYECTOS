import fs from 'node:fs'
import path from 'node:path'
import { createClient } from '@supabase/supabase-js'

function loadEnvFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8')
  const entries = content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'))

  const env = {}
  for (const entry of entries) {
    const eqIndex = entry.indexOf('=')
    if (eqIndex === -1) continue
    const key = entry.slice(0, eqIndex).trim()
    const value = entry.slice(eqIndex + 1).trim()
    env[key] = value
  }

  return env
}

const rootDir = process.cwd()
const envPath = path.join(rootDir, '.env.local')

if (!fs.existsSync(envPath)) {
  console.error('No existe .env.local en la raiz del proyecto.')
  process.exit(1)
}

const env = loadEnvFile(envPath)
const supabaseUrl = env.VITE_SUPABASE_URL
const serviceRoleKey = env.SUPABASE_SERVICE_ROLE_KEY

if (!supabaseUrl || !serviceRoleKey) {
  console.error('Faltan variables VITE_SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env.local')
  process.exit(1)
}

if (
  serviceRoleKey.includes('pega_aqui_tu_service_role_key') ||
  serviceRoleKey.startsWith('sb_publishable_')
) {
  console.error(
    'SUPABASE_SERVICE_ROLE_KEY no es valida para admin. Debes usar la Service Role Key real desde Supabase Dashboard.',
  )
  process.exit(1)
}

const admin = createClient(supabaseUrl, serviceRoleKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false,
  },
})

const users = [
  {
    email: 'director@empresa.com',
    password: 'Director123!',
    fullName: 'Carlos Mendoza',
    role: 'director',
    firstName: 'Carlos',
    lastName: 'Mendoza',
    birthDate: '1980-03-10',
    address: 'La Paz, Bolivia',
    phone: '77710001',
    nationalId: '4587123',
  },
  {
    email: 'jefe.seccion1@empresa.com',
    password: 'JefeSeccion123!',
    fullName: 'Mariana Salvatierra',
    role: 'jefe_seccion',
    firstName: 'Mariana',
    lastName: 'Salvatierra',
    birthDate: '1988-07-21',
    address: 'Cochabamba, Bolivia',
    phone: '77710002',
    nationalId: '5512390',
  },
  {
    email: 'jefe.seccion2@empresa.com',
    password: 'JefeSeccion123!',
    fullName: 'Juan Quispe',
    role: 'jefe_seccion',
    firstName: 'Juan',
    lastName: 'Quispe',
    birthDate: '1986-11-02',
    address: 'Santa Cruz, Bolivia',
    phone: '77710003',
    nationalId: '6688301',
  },
  {
    email: 'archivero@empresa.com',
    password: 'Archivero123!',
    fullName: 'Lucia Torres',
    role: 'archivero',
    firstName: 'Lucia',
    lastName: 'Torres',
    birthDate: '1992-01-15',
    address: 'Oruro, Bolivia',
    phone: '77710004',
    nationalId: '7340199',
  },
]

function formatSupabaseError(error) {
  if (!error) return 'Error desconocido'

  const parts = [error.message, error.code, error.details, error.hint].filter(Boolean)
  if (parts.length > 0) {
    return parts.join(' | ')
  }

  return JSON.stringify(error)
}

async function ensureProfilesTableExists() {
  const { error } = await admin
    .from('profiles')
    .select('id', { head: true, count: 'exact' })
    .limit(1)

  if (!error) {
    return true
  }

  if (
    error.message.toLowerCase().includes('relation') &&
    error.message.toLowerCase().includes('profiles')
  ) {
    console.error(
      'La tabla public.profiles no existe. Ejecuta primero el SQL: supabase/sql/001_auth_roles_setup.sql',
    )
    return false
  }

  console.error(`No se pudo validar la tabla profiles: ${formatSupabaseError(error)}`)
  return false
}

async function ensureProfileDetailsTableExists() {
  const { error } = await admin
    .from('profile_details')
    .select('user_id', { head: true, count: 'exact' })
    .limit(1)

  if (!error) {
    return true
  }

  if (
    error.message.toLowerCase().includes('relation') &&
    error.message.toLowerCase().includes('profile_details')
  ) {
    console.error(
      'La tabla public.profile_details no existe. Ejecuta primero el SQL: supabase/sql/003_user_profile_details.sql',
    )
    return false
  }

  console.error(`No se pudo validar la tabla profile_details: ${formatSupabaseError(error)}`)
  return false
}

async function createOrUpdateUsers() {
  const hasProfilesTable = await ensureProfilesTableExists()
  const hasProfileDetailsTable = await ensureProfileDetailsTableExists()

  if (!hasProfilesTable || !hasProfileDetailsTable) {
    process.exitCode = 1
    return
  }

  let hasErrors = false

  for (const item of users) {
    const { data, error } = await admin.auth.admin.createUser({
      email: item.email,
      password: item.password,
      email_confirm: true,
      user_metadata: {
        full_name: item.fullName,
      },
    })

    if (error && !error.message.toLowerCase().includes('already been registered')) {
      console.error(`Error creando ${item.email}: ${formatSupabaseError(error)}`)
      hasErrors = true
      continue
    }

    let userId = data?.user?.id

    if (!userId) {
      const { data: listData, error: listError } = await admin.auth.admin.listUsers({
        page: 1,
        perPage: 1000,
      })

      if (listError) {
        console.error(
          `No se pudo listar usuarios para ${item.email}: ${formatSupabaseError(listError)}`,
        )
        hasErrors = true
        continue
      }

      const existing = listData.users.find(
        (u) => u.email?.toLowerCase() === item.email.toLowerCase(),
      )
      userId = existing?.id
    }

    if (!userId) {
      console.error(`No se encontro id de usuario para ${item.email}`)
      hasErrors = true
      continue
    }

    const { error: upsertError } = await admin.from('profiles').upsert(
      {
        id: userId,
        email: item.email,
        full_name: item.fullName,
        role: item.role,
        is_active: true,
      },
      { onConflict: 'id' },
    )

    if (upsertError) {
      console.error(`Error guardando perfil de ${item.email}: ${formatSupabaseError(upsertError)}`)
      hasErrors = true
      continue
    }

    const { error: detailsError } = await admin.from('profile_details').upsert(
      {
        user_id: userId,
        first_name: item.firstName,
        last_name: item.lastName,
        birth_date: item.birthDate,
        address: item.address,
        phone: item.phone,
        national_id: item.nationalId,
      },
      { onConflict: 'user_id' },
    )

    if (detailsError) {
      console.error(
        `Error guardando detalle de ${item.email}: ${formatSupabaseError(detailsError)}`,
      )
      hasErrors = true
      continue
    }

    console.log(`Usuario listo: ${item.email} (${item.role})`)
  }

  if (hasErrors) {
    process.exitCode = 1
  }
}

createOrUpdateUsers()
  .then(() => {
    if (process.exitCode === 1) {
      console.error('Seed de usuarios finalizado con errores.')
      return
    }

    console.log('Seed de usuarios finalizado correctamente.')
  })
  .catch((error) => {
    console.error('Fallo inesperado:', error)
    process.exit(1)
  })
