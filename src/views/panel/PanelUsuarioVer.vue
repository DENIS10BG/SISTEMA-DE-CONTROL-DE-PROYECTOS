<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useRoute } from 'vue-router'
import { getUserById } from '../../composables/useUsersData'

const route = useRoute()
const user = ref(null)
const errorMessage = ref('')

const birthDateText = computed(() => {
  if (!user.value?.birthDate) return ''
  return new Date(`${user.value.birthDate}T00:00:00`).toLocaleDateString('es-BO')
})

const loadUser = async () => {
  const userId = route.query.uid
  if (!userId) {
    errorMessage.value = 'No se recibio el usuario a visualizar.'
    return
  }

  try {
    user.value = await getUserById(userId)
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo cargar el usuario.'
  }
}

onMounted(() => {
  loadUser()
})
</script>

<template>
  <section class="profile-page">
    <div class="page-title">Ver Usuario</div>

    <div class="profile-card">
      <div class="tabs">
        <RouterLink
          class="tab active"
          :to="{ path: '/panel/usuarios/ver', query: { uid: route.query.uid } }"
          >Ver Usuario</RouterLink
        >
        <RouterLink
          class="tab"
          :to="{ path: '/panel/usuarios/editar', query: { uid: route.query.uid } }"
          >Editar Usuario</RouterLink
        >
      </div>

      <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

      <div class="profile-body">
        <div class="avatar-wrap">
          <img v-if="user?.avatarUrl" :src="user.avatarUrl" alt="Usuario" />
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
          <span class="status-dot"></span>
        </div>

        <div class="fields-grid">
          <label><span>Nombre</span><input :value="user?.firstName || ''" readonly /></label>
          <label><span>Apellido</span><input :value="user?.lastName || ''" readonly /></label>
          <label><span>Correo</span><input :value="user?.email || ''" readonly /></label>
          <label><span>Contraseña</span><input value="**********" readonly /></label>
          <label><span>Fecha de nacimiento</span><input :value="birthDateText" readonly /></label>
          <label><span>Direccion</span><input :value="user?.address || ''" readonly /></label>
          <label><span>Teléfono</span><input :value="user?.phone || ''" readonly /></label>
          <label><span>Carnet</span><input :value="user?.nationalId || ''" readonly /></label>
          <label><span>Rol</span><input :value="user?.roleLabel || ''" readonly /></label>
          <label
            ><span>Estado de cuenta</span
            ><input :value="user?.isActive ? 'Activo' : 'Desactivo'" readonly
          /></label>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.profile-page {
  padding: 1.8rem 1.5rem 1.2rem;
}

.page-title {
  margin: 0 0 1rem;
  color: #35457f;
  font-size: clamp(2.2rem, 3vw, 3.2rem);
  font-weight: 800;
}

.profile-card {
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

.error-banner {
  margin: 0.7rem 0 0;
  border-radius: 10px;
  padding: 0.65rem 0.8rem;
  font-size: 0.88rem;
  background: #ffe8e8;
  color: #9b2121;
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

.status-dot {
  position: absolute;
  right: 8px;
  bottom: 10px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #28d962;
  border: 3px solid white;
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
    border: 1px solid #dfe6f7;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.95rem;
  }
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
