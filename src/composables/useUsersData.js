import { supabase } from '../../utils/supabase'
import { getCurrentUserIdFromSession } from './useAppSession'

const AVATARS_BUCKET = 'Avatras'
const MAX_AVATAR_SIZE_BYTES = 2 * 1024 * 1024
const ALLOWED_AVATAR_TYPES = ['image/jpeg', 'image/png', 'image/webp']

const ROLE_LABELS = {
  director: 'Director',
  jefe_seccion: 'Jefe de Seccion',
  archivero: 'Archivero',
}

const ROLE_VALUES = ['director', 'jefe_seccion', 'archivero']

const toRoleLabel = (role) => ROLE_LABELS[role] ?? role ?? 'Sin rol'

const toRoleValue = (value) => {
  if (ROLE_VALUES.includes(value)) return value
  return 'archivero'
}

const normalizeText = (value) => (value ?? '').replace(/\s+/g, ' ').trim()

const normalizeEmail = (value) => normalizeText(value).toLowerCase()

const extractStoragePathFromUrl = (url) => {
  const cleanUrl = normalizeText(url)
  if (!cleanUrl) return null

  const marker = `/storage/v1/object/public/${AVATARS_BUCKET}/`
  const markerIndex = cleanUrl.indexOf(marker)
  if (markerIndex === -1) return null

  const encodedPath = cleanUrl.slice(markerIndex + marker.length)
  const pathWithoutQuery = encodedPath.split('?')[0]
  return decodeURIComponent(pathWithoutQuery)
}

const toSafeFileName = (name) => {
  const normalized = normalizeText(name).replace(/[^a-zA-Z0-9._-]/g, '_')
  return normalized || 'avatar.jpg'
}

const validateAvatarFile = (file) => {
  if (!file) {
    throw new Error('Debes seleccionar una imagen.')
  }

  if (!ALLOWED_AVATAR_TYPES.includes(file.type)) {
    throw new Error('Formato no valido. Usa JPG, PNG o WEBP.')
  }

  if (file.size > MAX_AVATAR_SIZE_BYTES) {
    throw new Error('La imagen excede 2MB.')
  }
}

const uploadUserAvatar = async (userId, file, previousAvatarUrl = '') => {
  validateAvatarFile(file)

  const previousPath = extractStoragePathFromUrl(previousAvatarUrl)
  if (previousPath) {
    const { error: deleteError } = await supabase.storage
      .from(AVATARS_BUCKET)
      .remove([previousPath])

    // Ignorar archivo no encontrado para permitir reemplazo robusto
    if (deleteError && !String(deleteError.message).toLowerCase().includes('not found')) {
      throw deleteError
    }
  }

  const fileName = toSafeFileName(file.name)
  const path = `${userId}/${Date.now()}-${fileName}`

  const { error: uploadError } = await supabase.storage.from(AVATARS_BUCKET).upload(path, file, {
    cacheControl: '3600',
    upsert: false,
    contentType: file.type,
  })

  if (uploadError) {
    throw uploadError
  }

  const { data } = supabase.storage.from(AVATARS_BUCKET).getPublicUrl(path)
  return data.publicUrl
}

const toInitials = (firstName, lastName, fullName) => {
  const raw = `${firstName ?? ''} ${lastName ?? ''}`.trim() || fullName || ''
  const parts = raw.split(/\s+/).filter(Boolean)
  if (parts.length === 0) return 'US'

  if (parts.length === 1) {
    return parts[0].slice(0, 2).toUpperCase()
  }

  return `${parts[0][0] ?? ''}${parts[1][0] ?? ''}`.toUpperCase()
}

const normalizeUser = (row) => {
  if (!row) return null

  return {
    id: row.id,
    email: row.email,
    fullName: row.full_name ?? '',
    role: toRoleValue(row.role),
    roleLabel: toRoleLabel(row.role),
    isActive: !!row.is_active,
    firstName: row.first_name ?? '',
    lastName: row.last_name ?? '',
    birthDate: row.birth_date ?? '',
    address: row.address ?? '',
    phone: row.phone ?? '',
    nationalId: row.national_id ?? '',
    avatarUrl: row.avatar_url ?? '',
    initials: toInitials(row.first_name, row.last_name, row.full_name),
  }
}

const selectUserColumns =
  'id, email, full_name, role, is_active, first_name, last_name, birth_date, address, phone, national_id, avatar_url'

const getCurrentUserId = async () => {
  return getCurrentUserIdFromSession()
}

const getCurrentUser = async () => {
  const userId = await getCurrentUserId()
  if (!userId) return null

  const { data, error } = await supabase
    .from('users_full')
    .select(selectUserColumns)
    .eq('id', userId)
    .single()

  if (error) {
    throw error
  }

  return normalizeUser(data)
}

const getUserById = async (userId) => {
  const { data, error } = await supabase
    .from('users_full')
    .select(selectUserColumns)
    .eq('id', userId)
    .single()

  if (error) {
    throw error
  }

  return normalizeUser(data)
}

const listUsers = async (options = {}) => {
  const excludeUserId = options.excludeUserId ? String(options.excludeUserId) : null

  const { data, error } = await supabase
    .from('users_full')
    .select(selectUserColumns)
    .order('created_at', { ascending: true })

  if (error) {
    throw error
  }

  let normalized = (data ?? []).map(normalizeUser)

  if (excludeUserId) {
    normalized = normalized.filter((item) => item.id !== excludeUserId)
  }

  return normalized
}

const buildFullName = (firstName, lastName) =>
  `${normalizeText(firstName)} ${normalizeText(lastName)}`.replace(/\s+/g, ' ').trim()

const updateOwnProfile = async (userId, payload) => {
  const fullName = buildFullName(payload.firstName, payload.lastName)

  const { error: profileError } = await supabase
    .from('profiles')
    .update({
      full_name: fullName || payload.fullName || 'Usuario',
    })
    .eq('id', userId)

  if (profileError) {
    throw profileError
  }

  const { error: detailError } = await supabase
    .from('profile_details')
    .update({
      first_name: normalizeText(payload.firstName) || 'Usuario',
      last_name: normalizeText(payload.lastName) || null,
      birth_date: payload.birthDate || null,
      address: normalizeText(payload.address) || null,
      phone: normalizeText(payload.phone) || null,
      national_id: normalizeText(payload.nationalId) || null,
      avatar_url: normalizeText(payload.avatarUrl) || null,
    })
    .eq('user_id', userId)

  if (detailError) {
    throw detailError
  }
}

const updateUserById = async (userId, payload) => {
  const fullName = buildFullName(payload.firstName, payload.lastName)

  const { error: profileError } = await supabase
    .from('profiles')
    .update({
      full_name: fullName || payload.fullName || 'Usuario',
      role: toRoleValue(payload.role),
      is_active: !!payload.isActive,
    })
    .eq('id', userId)

  if (profileError) {
    throw profileError
  }

  const { error: detailsError } = await supabase.from('profile_details').upsert(
    {
      user_id: userId,
      first_name: normalizeText(payload.firstName) || 'Usuario',
      last_name: normalizeText(payload.lastName) || null,
      birth_date: payload.birthDate || null,
      address: normalizeText(payload.address) || null,
      phone: normalizeText(payload.phone) || null,
      national_id: normalizeText(payload.nationalId) || null,
      avatar_url: normalizeText(payload.avatarUrl) || null,
    },
    { onConflict: 'user_id' },
  )

  if (detailsError) {
    throw detailsError
  }
}

const setUserState = async (userId, isActive) => {
  const { error } = await supabase
    .from('profiles')
    .update({ is_active: !!isActive })
    .eq('id', userId)

  if (error) {
    throw error
  }
}

const createUserWithProfile = async (payload) => {
  const actorUserId = getCurrentUserIdFromSession()

  if (!actorUserId) {
    throw new Error('Sesion no valida. Inicia sesion nuevamente.')
  }

  const cleanEmail = normalizeEmail(payload.email)
  const cleanPassword = String(payload.password ?? '')

  if (!cleanEmail || !cleanEmail.includes('@')) {
    throw new Error('Correo invalido. Ejemplo valido: admin@gmail.com')
  }

  if (cleanPassword.length < 6) {
    throw new Error('La contrasena debe tener al menos 6 caracteres.')
  }

  const { data, error } = await supabase.rpc('admin_create_user_with_profile', {
    p_actor_user_id: actorUserId,
    p_email: cleanEmail,
    p_password: cleanPassword,
    p_first_name: normalizeText(payload.firstName),
    p_last_name: normalizeText(payload.lastName),
    p_birth_date: payload.birthDate || null,
    p_address: normalizeText(payload.address) || null,
    p_phone: normalizeText(payload.phone) || null,
    p_national_id: normalizeText(payload.nationalId) || null,
    p_role: toRoleValue(payload.role),
    p_is_active: !!payload.isActive,
  })

  if (error) {
    throw error
  }

  const userId = data

  // Safety pass to ensure values remain normalized after trigger defaults
  await updateUserById(userId, {
    firstName: normalizeText(payload.firstName),
    lastName: normalizeText(payload.lastName),
    birthDate: payload.birthDate,
    address: normalizeText(payload.address),
    phone: normalizeText(payload.phone),
    nationalId: normalizeText(payload.nationalId),
    role: payload.role,
    isActive: payload.isActive,
  })

  return userId
}

export {
  AVATARS_BUCKET,
  ROLE_VALUES,
  getCurrentUser,
  getCurrentUserId,
  getUserById,
  listUsers,
  uploadUserAvatar,
  toRoleLabel,
  toInitials,
  updateOwnProfile,
  updateUserById,
  setUserState,
  createUserWithProfile,
}
