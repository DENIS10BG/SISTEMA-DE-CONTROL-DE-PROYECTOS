<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Escudo from '../../assets/images/Escudo.png'
import Letras from '../../assets/images/Letras.png'

const router = useRouter()
const menuOpen = ref(false)
const menuRoot = ref(null)

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

const logout = () => {
  closeMenu()
  router.push('/login')
}

const handleDocumentClick = (event) => {
  if (menuRoot.value && !menuRoot.value.contains(event.target)) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
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
        ⚙
      </RouterLink>
      <button class="top-icon alert" type="button">!</button>
      <div class="profile-text">
        <strong>Maria Roquez</strong>
      </div>
      <div ref="menuRoot" class="avatar-wrap">
        <button class="avatar" type="button" @click.stop="toggleMenu">MR</button>

        <div v-if="menuOpen" class="profile-menu">
          <button type="button" class="menu-option" @click="goToAjustes">
            <span class="menu-icon profile">👤</span>
            <span>Ver Perfil</span>
          </button>

          <button type="button" class="menu-option" @click="logout">
            <span class="menu-icon logout">✕</span>
            <span>Cerrar Sesion</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.panel-header {
  width: 100%;
  min-height: 100px;
  background: #ffffff;
  border-bottom: 1px solid #e4e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
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

  &.alert {
    color: #f05f73;
    background: #fff1f4;
  }

  &.gear-link {
    cursor: pointer;
  }
}

.profile-text {
  color: #38416a;
  font-size: 1.1rem;
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
}

.avatar-wrap {
  position: relative;
}

.profile-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 0.5rem);
  width: 190px;
  background: #ffffff;
  border: 1px solid #cfd77d;
  border-radius: 16px;
  box-shadow: 0 14px 28px rgba(35, 53, 87, 0.12);
  padding: 0.5rem;
  z-index: 20;
}

.menu-option {
  width: 100%;
  border: 0;
  background: transparent;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 0.7rem;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #38416a;
  text-align: left;
  cursor: pointer;

  &:hover {
    background: #f6f8ff;
  }
}

.menu-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: #ffeab5;
  color: #f2a400;

  &.logout {
    background: #d9e1ff;
    color: #3b63ff;
  }
}

@media (max-width: 768px) {
  .panel-header {
    flex-direction: column;
    gap: 0.9rem;
    align-items: flex-start;
  }

  .brand-slot {
    min-width: 0;
    width: 100%;
    border-right: 0;
    border-bottom: 1px solid #e4e7eb;
    padding-bottom: 0.75rem;
  }
}
</style>
