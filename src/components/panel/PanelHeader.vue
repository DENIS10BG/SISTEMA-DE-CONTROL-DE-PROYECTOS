<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { getCurrentUser } from '../../composables/useUsersData'
import { clearAppSession } from '../../composables/useAppSession'
import Escudo from '../../assets/images/Escudo.png'
import Letras from '../../assets/images/Letras.png'
import IconEngranaje from '@/components/icons/Iconsnavbar/Engranaje.svg'
import IconVerPerfil from '@/components/icons/Iconsnavbar/Verperfil.svg'
import IconCerrarSesion from '@/components/icons/Iconsnavbar/CerrarSesion.svg'

const router = useRouter()
const menuOpen = ref(false)
const menuRoot = ref(null)
const currentUser = ref(null)

const loadCurrentUser = async () => {
  try {
    currentUser.value = await getCurrentUser()
  } catch {
    currentUser.value = null
  }
}

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

const goToAjustes = () => {
  closeMenu()
  router.push('/panel/perfil')
}

const logout = async () => {
  closeMenu()
  clearAppSession()
  router.push('/login')
}

const handleDocumentClick = (event) => {
  if (menuRoot.value && !menuRoot.value.contains(event.target)) {
    closeMenu()
  }
}

const handleProfileUpdated = () => {
  loadCurrentUser()
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
  window.addEventListener('user-profile-updated', handleProfileUpdated)
  loadCurrentUser()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
  window.removeEventListener('user-profile-updated', handleProfileUpdated)
})
</script>

<template>
  <header class="panel-header">
    <div class="brand-slot">
      <div class="brand-mark">
        <img :src="Escudo" alt="Escudo SICEPI" />
        <img :src="Letras" alt="SICEPI" />
      </div>
    </div>

    <div class="profile-area">
      <RouterLink class="top-icon gear-link" to="/panel/ajustes" aria-label="Editar perfil">
        <img :src="IconEngranaje" alt="Configuración" />
      </RouterLink>
      <div class="profile-text">
        <strong>{{ currentUser?.fullName || 'Usuario' }}</strong>
      </div>
      <div ref="menuRoot" class="avatar-wrap">
        <button class="avatar" type="button" @click.stop="toggleMenu">
          <img
            v-if="currentUser?.avatarUrl"
            class="avatar-image"
            :src="currentUser.avatarUrl"
            alt="Avatar"
          />
          <span v-else>{{ currentUser?.initials || 'US' }}</span>
        </button>

        <div v-if="menuOpen" class="profile-menu">
          <button type="button" class="menu-option" @click="goToAjustes">
            <span class="menu-icon profile">
              <img :src="IconVerPerfil" alt="Ver perfil" />
            </span>
            <span class="menu-label">Ver Perfil</span>
          </button>

          <button type="button" class="menu-option" @click="logout">
            <span class="menu-icon logout">
              <img :src="IconCerrarSesion" alt="Cerrar sesión" />
            </span>
            <span class="menu-label">Cerrar Sesion</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.panel-header {
  width: 100%;
  height: 10vh;
  min-height: 10vh;
  position: relative;
  z-index: 40;
  background: #ffffff;
  border-bottom: 1px solid #e4e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  box-sizing: border-box;
  overflow: visible;
}

.brand-slot {
  display: flex;
  align-items: center;
  min-width: 230px;
  height: 100%;
  padding-right: 1rem;
  border-right: 1px solid #e4e7eb;
}

.brand-mark {
  display: flex;
  align-items: center;
  gap: 0.4rem;

  img:first-child {
    width: 42px;
    height: 42px;
    object-fit: contain;
  }

  img:last-child {
    width: 150px;
    object-fit: contain;
  }
}

.profile-area {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  min-width: 0;
}

.top-icon {
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 50%;
  background: #eef2fb;
  color: #7d87a8;
  font-size: 1.2rem;
  display: grid;
  place-items: center;
  text-decoration: none;

  img {
    width: 18px;
    height: 18px;
    object-fit: contain;
    filter: grayscale(1) brightness(0.72);
  }

  &.gear-link {
    cursor: pointer;
  }
}

.profile-text {
  color: #38416a;
  font-size: 1.1rem;
  white-space: nowrap;
}

.avatar {
  width: 52px;
  height: 52px;
  border: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, #cfd6e7, #9ca9ca);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-wrap {
  position: relative;
  z-index: 60;
}

.profile-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 0.5rem);
  width: 165px;
  background: #ffffff;
  border: 1px solid #b8c86b;
  border-radius: 14px;
  box-shadow: 0 10px 20px rgba(35, 53, 87, 0.1);
  padding: 0.35rem;
  z-index: 120;
}

.menu-option {
  width: 100%;
  border: 0;
  background: transparent;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.35rem 0.4rem;
  border-radius: 10px;
  color: #2e3650;
  text-align: left;
  cursor: pointer;

  &:hover {
    background: #f6f8ff;
  }
}

.menu-label {
  font-size: 0.58rem;
  font-weight: 600;
  line-height: 1.1;
  white-space: nowrap;
}

.menu-icon {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: #fbeabc;

  img {
    width: 20px;
    height: 20px;
    object-fit: contain;
    filter: brightness(0) saturate(100%) invert(75%) sepia(57%) saturate(1560%) hue-rotate(1deg)
      brightness(102%) contrast(93%);
  }

  &.logout {
    background: #dce3ff;

    img {
      filter: brightness(0) saturate(100%) invert(28%) sepia(97%) saturate(2867%) hue-rotate(222deg)
        brightness(103%) contrast(103%);
    }
  }
}

@media (max-width: 768px) {
  .panel-header {
    padding: 0.4rem 0.8rem;
    gap: 0.5rem;
  }

  .brand-slot {
    min-width: 155px;
    border-right: 1px solid #e4e7eb;
    border-bottom: 0;
    padding-right: 0.5rem;
    padding-bottom: 0;
  }

  .brand-mark img:first-child {
    width: 32px;
    height: 32px;
  }

  .brand-mark img:last-child {
    width: 108px;
  }

  .top-icon {
    width: 33px;
    height: 33px;
    font-size: 1rem;
  }

  .avatar {
    width: 38px;
    height: 38px;
    font-size: 0.8rem;
  }

  .profile-text {
    font-size: 0.85rem;
  }
}
</style>
