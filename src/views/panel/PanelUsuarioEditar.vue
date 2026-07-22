<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useRoute } from 'vue-router'
import {
  ROLE_VALUES,
  getUserById,
  updateUserById,
  uploadUserAvatar,
} from '../../composables/useUsersData'

const route = useRoute()
const loading = ref(false)
const message = ref('')
const errorMessage = ref('')
const userId = ref('')
const currentAvatarUrl = ref('')
const selectedAvatarFile = ref(null)
const fileInputRef = ref(null)
const temporaryPreviewUrl = ref('')

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  birthDate: '',
  address: '',
  phone: '',
  nationalId: '',
  role: 'archivero',
  isActive: true,
})

const loadUser = async () => {
  userId.value = String(route.query.uid || '')
  if (!userId.value) {
    errorMessage.value = 'No se recibio el usuario a editar.'
    return
  }

  try {
    const user = await getUserById(userId.value)
    form.firstName = user.firstName || ''
    form.lastName = user.lastName || ''
    form.email = user.email || ''
    form.birthDate = user.birthDate || ''
    form.address = user.address || ''
    form.phone = user.phone || ''
    form.nationalId = user.nationalId || ''
    form.role = ROLE_VALUES.includes(user.role) ? user.role : 'archivero'
    form.isActive = !!user.isActive
    currentAvatarUrl.value = user.avatarUrl || ''
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo cargar el usuario.'
  }
}

const pickAvatar = () => {
  fileInputRef.value?.click()
}

const onAvatarChange = (event) => {
  const file = event.target?.files?.[0]
  selectedAvatarFile.value = file || null

  if (temporaryPreviewUrl.value) {
    URL.revokeObjectURL(temporaryPreviewUrl.value)
    temporaryPreviewUrl.value = ''
  }

  if (file) {
    temporaryPreviewUrl.value = URL.createObjectURL(file)
  }
}

const saveUser = async () => {
  if (!userId.value) return

  loading.value = true
  message.value = ''
  errorMessage.value = ''

  try {
    let avatarUrl = currentAvatarUrl.value || ''

    if (selectedAvatarFile.value) {
      avatarUrl = await uploadUserAvatar(
        userId.value,
        selectedAvatarFile.value,
        currentAvatarUrl.value,
      )
      currentAvatarUrl.value = avatarUrl
      selectedAvatarFile.value = null
      if (temporaryPreviewUrl.value) {
        URL.revokeObjectURL(temporaryPreviewUrl.value)
        temporaryPreviewUrl.value = ''
      }
      if (fileInputRef.value) {
        fileInputRef.value.value = ''
      }
    }

    await updateUserById(userId.value, {
      firstName: form.firstName,
      lastName: form.lastName,
      birthDate: form.birthDate,
      address: form.address,
      phone: form.phone,
      nationalId: form.nationalId,
      avatarUrl,
      role: form.role,
      isActive: form.isActive,
    })

    message.value = 'Usuario actualizado correctamente.'
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo actualizar el usuario.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUser()
})

onBeforeUnmount(() => {
  if (temporaryPreviewUrl.value) {
    URL.revokeObjectURL(temporaryPreviewUrl.value)
    temporaryPreviewUrl.value = ''
  }
})
</script>

<template>
  <section class="settings-page">
    <div class="page-title">Editar Usuario</div>

    <div class="settings-card">
      <div class="tabs">
        <RouterLink
          class="tab"
          :to="{ path: '/panel/usuarios/ver', query: { uid: route.query.uid } }"
          >Ver Usuario</RouterLink
        >
        <RouterLink
          class="tab active"
          :to="{ path: '/panel/usuarios/editar', query: { uid: route.query.uid } }"
          >Editar Usuario</RouterLink
        >
      </div>

      <p v-if="message" class="success-banner">{{ message }}</p>
      <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

      <div class="profile-body">
        <div class="avatar-wrap">
          <img
            v-if="temporaryPreviewUrl || currentAvatarUrl"
            :src="temporaryPreviewUrl || currentAvatarUrl"
            alt="Editar usuario"
          />
          <div v-else class="avatar-fallback" aria-label="Usuario sin avatar">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path
                d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M4 21C4 17.6863 7.58172 15 12 15C16.4183 15 20 17.6863 20 21"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>
          <button class="edit-badge" type="button" @click="pickAvatar">✎</button>
          <input
            ref="fileInputRef"
            class="avatar-input"
            type="file"
            accept="image/png,image/jpeg,image/webp"
            @change="onAvatarChange"
          />
        </div>

        <div class="fields-grid">
          <label><span>Nombre</span><input v-model="form.firstName" /></label>
          <label><span>Apellido</span><input v-model="form.lastName" /></label>
          <label><span>Correo</span><input :value="form.email" readonly /></label>
          <label><span>Contraseña</span><input value="**********" readonly /></label>
          <label
            ><span>Fecha de nacimiento</span><input v-model="form.birthDate" type="date"
          /></label>
          <label><span>Direccion</span><input v-model="form.address" /></label>
          <label><span>Teléfono</span><input v-model="form.phone" /></label>
          <label><span>Carnet</span><input v-model="form.nationalId" /></label>
          <label>
            <span>Rol</span>
            <select v-model="form.role">
              <option value="director">Director</option>
              <option value="jefe_seccion">Jefe de Seccion</option>
              <option value="archivero">Archivero</option>
            </select>
          </label>
          <label>
            <span>Estado de cuenta</span>
            <select v-model="form.isActive">
              <option :value="true">Activo</option>
              <option :value="false">Desactivo</option>
            </select>
          </label>
        </div>
      </div>

      <div class="footer-actions">
        <button :disabled="loading" class="save-btn" type="button" @click="saveUser">
          {{ loading ? 'Guardando...' : 'Guardar' }}
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.settings-page {
  padding: 1.8rem 1.5rem 1.2rem;
}

.page-title {
  margin: 0 0 1rem;
  color: #35457f;
  font-size: clamp(2.2rem, 3vw, 3.2rem);
  font-weight: 800;
}

.settings-card {
  max-width: 920px;
  margin: 0 auto;
  background: white;
  border-radius: 22px;
  border: 1px solid #a9a09a;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 1rem 1.2rem 1.4rem;
}

.tabs {
  display: flex;
  gap: 2rem;
  border-bottom: 1px solid #eef1f6;
  padding: 0 0 0.8rem 0.8rem;
}

.tab {
  text-decoration: none;
  color: #9aabd7;
  font-weight: 600;
  padding-bottom: 0.55rem;
  position: relative;

  &.active {
    color: #3d3dff;

    &::after {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      bottom: -0.8rem;
      height: 3px;
      border-radius: 999px;
      background: #3d3dff;
    }
  }
}

.profile-body {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 1.2rem;
  padding-top: 1.5rem;
  align-items: start;
}

.avatar-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  margin-left: 0.4rem;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #edf2ff;
  color: #3b66d2;
  display: grid;
  place-items: center;

  svg {
    width: 52%;
    height: 52%;
  }
}

.edit-badge {
  position: absolute;
  right: 4px;
  bottom: 8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #2f3dff;
  color: white;
  border: 0;
  display: grid;
  place-items: center;
  font-size: 0.95rem;
  border: 3px solid white;
  cursor: pointer;
}

.avatar-input {
  display: none;
}

.fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;

  label {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }

  span {
    color: #6c6f7a;
    font-size: 0.95rem;
  }

  input {
    width: 100%;
    border: 1px solid #7046ff;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.95rem;
    outline: none;
  }

  select {
    width: 100%;
    border: 1px solid #7046ff;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.95rem;
    outline: none;
  }
}

.success-banner,
.error-banner {
  margin: 0.7rem 0 0;
  border-radius: 10px;
  padding: 0.65rem 0.8rem;
  font-size: 0.88rem;
}

.success-banner {
  background: #ebfff0;
  color: #1a783f;
}

.error-banner {
  background: #ffe8e8;
  color: #9b2121;
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 1.2rem;
}

.save-btn {
  border: 0;
  border-radius: 12px;
  background: #2f3dff;
  color: white;
  min-width: 140px;
  padding: 0.95rem 1.2rem;
  font-weight: 700;
}

@media (max-width: 900px) {
  .profile-body {
    grid-template-columns: 1fr;
  }

  .avatar-wrap {
    margin: 0 auto;
  }

  .fields-grid {
    grid-template-columns: 1fr;
  }
}
</style>
