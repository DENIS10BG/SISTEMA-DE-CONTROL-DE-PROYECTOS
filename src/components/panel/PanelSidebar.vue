<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router'
import IconPanelGeneral from '@/components/icons/Iconsnavbar/PanelGeneral.svg'
import IconUsuarios from '@/components/icons/Iconsnavbar/Usuarios.svg'
import IconProyectos from '@/components/icons/Iconsnavbar/Proyectos.svg'
import IconProcesamiento from '@/components/icons/Iconsnavbar/Procesamiento.svg'
import IconReportes from '@/components/icons/Iconsnavbar/Reportes.svg'
import IconAlertas from '@/components/icons/Iconsnavbar/Alertas.svg'
import IconAsistente from '@/components/icons/Iconsnavbar/Asistente.svg'
import { clearAppSession } from '../../composables/useAppSession'

const menuItems = [
  { label: 'Panel General', to: '/panel/general', icon: IconPanelGeneral },
  { label: 'Usuarios', to: '/panel/usuarios', icon: IconUsuarios },
  { label: 'Proyectos', to: '/panel/proyectos', icon: IconProyectos },
  { label: 'Procesamiento', to: '/panel/procesamiento', icon: IconProcesamiento },
  { label: 'Reportes', to: '/panel/reportes', icon: IconReportes },
  { label: 'Alertas', to: '/panel/alertas', icon: IconAlertas },
  { label: 'Asistente', to: '/panel/asistente', icon: IconAsistente },
]

const route = useRoute()
const router = useRouter()

const isActive = (to) => {
  if (route.path === to) return true
  return route.path.startsWith(`${to}/`)
}

const logout = async () => {
  clearAppSession()
  router.push('/login')
}
</script>

<template>
  <aside class="sidebar">
    <nav class="menu">
      <RouterLink
        v-for="item in menuItems"
        :key="item.label"
        class="menu-item"
        :class="{ active: isActive(item.to) }"
        :to="item.to"
      >
        <span class="menu-icon" aria-hidden="true">
          <img :src="item.icon" :alt="item.label" />
        </span>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <button class="logout-btn" type="button" @click="logout">Cerrar Sesion</button>
  </aside>
</template>

<style scoped lang="scss">
.sidebar {
  height: 100%;
  background: #ffffff;
  border-right: 1px solid #e4e7eb;
  padding: 1.2rem 1rem 1.3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow: auto;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
}

.menu-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  text-decoration: none;
  color: #b3b3b8;
  padding: 0.9rem 0.8rem;
  border-radius: 16px;
  font-weight: 600;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;

  &.active {
    color: #2756ff;
    background: #eef3ff;

    &::before {
      content: '';
      position: absolute;
      left: -0.9rem;
      top: 50%;
      transform: translateY(-50%);
      width: 6px;
      height: 32px;
      border-radius: 0 8px 8px 0;
      background: #3f62ff;
      box-shadow: 0 0 12px rgba(63, 98, 255, 0.55);
    }
  }

  &:hover {
    color: #2756ff;
    background: #f6f8ff;
  }
}

.menu-icon {
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    filter: grayscale(1) brightness(0.82);
  }
}

.menu-item.active .menu-icon img,
.menu-item:hover .menu-icon img {
  filter: brightness(0) saturate(100%) invert(28%) sepia(83%) saturate(3667%) hue-rotate(224deg)
    brightness(102%) contrast(101%);
}

.logout-btn {
  border: 0;
  cursor: pointer;
  text-align: center;
  background: #70cf77;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 700;
}
</style>
