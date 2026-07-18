<script setup>
import { RouterLink, useRoute } from 'vue-router'

const menuItems = [
  { label: 'Panel General', to: '/panel/general' },
  { label: 'Usuarios', to: '/panel/usuarios' },
  { label: 'Proyectos', to: '/panel/proyectos' },
  { label: 'Procesamiento', to: '/panel/procesamiento' },
  { label: 'Reportes', to: '/panel/reportes' },
  { label: 'Alertas', to: '/panel/alertas' },
  { label: 'Asistente', to: '/panel/asistente' },
]

const route = useRoute()

const isActive = (to) => route.path === to
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
        {{ item.label }}
      </RouterLink>
    </nav>

    <RouterLink class="logout-btn" to="/">Cerrar Sesion</RouterLink>
  </aside>
</template>

<style scoped lang="scss">
.sidebar {
  background: #ffffff;
  border-right: 1px solid #e4e7eb;
  padding: 1.2rem 0.9rem 1.3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
}

.menu-item {
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
  }

  &:hover {
    color: #2756ff;
    background: #f6f8ff;
  }
}

.logout-btn {
  text-decoration: none;
  text-align: center;
  background: #70cf77;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-weight: 700;
}
</style>
