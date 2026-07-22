<script setup>
import { onMounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'
import profileImage from '../../assets/images/IngenieroProyetos.png'
import { getCurrentUser, updateOwnProfile, uploadUserAvatar } from '../../composables/useUsersData'

const loading = ref(false)
const message = ref('')
const errorMessage = ref('')
const currentUserId = ref(null)
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
  roleLabel: '',
  isActive: true,
})

const loadUser = async () => {
  try {
    const user = await getCurrentUser()
    if (!user) return

    currentUserId.value = user.id
    form.firstName = user.firstName || ''
    form.lastName = user.lastName || ''
    form.email = user.email || ''
    form.birthDate = user.birthDate || ''
    form.address = user.address || ''
    form.phone = user.phone || ''
    form.nationalId = user.nationalId || ''
    form.roleLabel = user.roleLabel || ''
    form.isActive = !!user.isActive
    currentAvatarUrl.value = user.avatarUrl || ''
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo cargar el perfil.'
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

const saveProfile = async () => {
  if (!currentUserId.value) return

  loading.value = true
  errorMessage.value = ''
  message.value = ''

  try {
    let avatarUrl = currentAvatarUrl.value || ''

    if (selectedAvatarFile.value) {
      avatarUrl = await uploadUserAvatar(
        currentUserId.value,
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

    await updateOwnProfile(currentUserId.value, {
      firstName: form.firstName,
      lastName: form.lastName,
      birthDate: form.birthDate,
      address: form.address,
      phone: form.phone,
      nationalId: form.nationalId,
      avatarUrl,
    })

    message.value = 'Perfil actualizado correctamente.'
    window.dispatchEvent(new CustomEvent('user-profile-updated'))
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo actualizar el perfil.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUser()
})
</script>

<template>
  <section class="settings-page">
    <div class="page-title">Ajustes</div>

    <div class="settings-card">
      <div class="tabs">
        <RouterLink class="tab" to="/panel/perfil">Perfil</RouterLink>
        <RouterLink class="tab active" to="/panel/ajustes">Editar Perfil</RouterLink>
      </div>

      <p v-if="message" class="success-banner">{{ message }}</p>
      <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

      <div class="profile-body">
        <div class="avatar-wrap">
          <img :src="temporaryPreviewUrl || currentAvatarUrl || profileImage" alt="Editar perfil" />
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
          <label>
            <span>Nombre</span>
            <input v-model="form.firstName" />
          </label>
          <label>
            <span>Apellido</span>
            <input v-model="form.lastName" />
          </label>
          <label>
            <span>Correo</span>
            <input :value="form.email" readonly />
          </label>
          <label>
            <span>Contraseña</span>
            <input value="**********" readonly />
          </label>
          <label>
            <span>Fecha de nacimiento</span>
            <input v-model="form.birthDate" type="date" />
          </label>
          <label>
            <span>Direccion</span>
            <input v-model="form.address" />
          </label>
          <label>
            <span>Telefono</span>
            <input v-model="form.phone" />
          </label>
          <label>
            <span>Carnet</span>
            <input v-model="form.nationalId" />
          </label>
          <label>
            <span>Rol</span>
            <input :value="form.roleLabel" readonly />
          </label>
          <label>
            <span>Estado de cuenta</span>
            <input :value="form.isActive ? 'Activo' : 'Desactivo'" readonly />
          </label>
        </div>
      </div>

      <div class="footer-actions">
        <button :disabled="loading" class="save-btn" type="button" @click="saveProfile">
          {{ loading ? 'Guardando...' : 'Guardar' }}
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.settings-page {
  height: 100%;
  box-sizing: border-box;
  padding: 0.75rem 1.2rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  overflow: auto;
}

.page-title {
  margin: 0;
  text-align: left;
  color: #35457f;
  font-size: clamp(1.9rem, 2.4vw, 2.5rem);
  line-height: 1.05;
  font-weight: 800;
}

.settings-card {
  width: min(100%, 980px);
  box-sizing: border-box;
  margin: 0 auto;
  background: white;
  border-radius: 22px;
  border: 1px solid #a9a09a;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.8rem 1.1rem 0.95rem;
  overflow: visible;
}

.tabs {
  display: flex;
  gap: 2.6rem;
  border-bottom: 1px solid #eef1f6;
  padding: 0.08rem 0 0.62rem 0.45rem;
}

.tab {
  text-decoration: none;
  color: #9aabd7;
  font-weight: 600;
  font-size: 1.18rem;
  padding-bottom: 0.64rem;
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

.profile-body {
  display: grid;
  grid-template-columns: 130px 1fr;
  gap: 0.85rem;
  padding-top: 0.8rem;
  align-items: start;
}

.avatar-wrap {
  position: relative;
  width: 98px;
  height: 98px;
  margin-left: 0.4rem;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
}

.edit-badge {
  position: absolute;
  right: 4px;
  bottom: 8px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #2f3dff;
  color: white;
  border: 0;
  display: grid;
  place-items: center;
  font-size: 0.75rem;
  border: 3px solid white;
  cursor: pointer;
}

.avatar-input {
  display: none;
}

.fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.7rem 1rem;

  label {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  span {
    color: #6c6f7a;
    font-size: 0.86rem;
  }

  input {
    width: 100%;
    border: 1px solid #7046ff;
    border-radius: 12px;
    padding: 0.66rem 0.86rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.9rem;
    outline: none;
  }
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.7rem;
}

.save-btn {
  border: 0;
  border-radius: 12px;
  background: #2f3dff;
  color: white;
  min-width: 120px;
  padding: 0.55rem 0.9rem;
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
