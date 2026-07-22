const APP_SESSION_KEY = 'sicepi_app_session'

const readRawSession = () => {
  const value = localStorage.getItem(APP_SESSION_KEY)
  if (!value) return null

  try {
    return JSON.parse(value)
  } catch {
    localStorage.removeItem(APP_SESSION_KEY)
    return null
  }
}

const getAppSession = () => {
  const session = readRawSession()
  if (!session?.userId || !session?.email) return null
  return session
}

const setAppSession = (payload) => {
  const safePayload = {
    userId: payload.userId,
    email: payload.email,
    fullName: payload.fullName ?? 'Usuario',
    role: payload.role ?? 'archivero',
    isActive: !!payload.isActive,
  }

  localStorage.setItem(APP_SESSION_KEY, JSON.stringify(safePayload))
}

const clearAppSession = () => {
  localStorage.removeItem(APP_SESSION_KEY)
}

const getCurrentUserIdFromSession = () => {
  const session = getAppSession()
  return session?.userId ?? null
}

const hasDirectorSession = () => {
  const session = getAppSession()
  return !!session && session.role === 'director' && session.isActive
}

export {
  APP_SESSION_KEY,
  clearAppSession,
  getAppSession,
  getCurrentUserIdFromSession,
  hasDirectorSession,
  setAppSession,
}
