<script setup>
import { onMounted, ref } from 'vue'
import PanelModuleCard from '@/components/panel/PanelModuleCard.vue'
import { getCurrentUser } from '../composables/useUsersData'

const modules = [
  {
    title: 'Usuarios',
    description: 'Gestiona los usuarios',
    accent: 'rgba(77, 109, 255, 0.18)',
    iconColor: '#3857f6',
    to: '/panel/usuarios',
  },
  {
    title: 'Proyectos',
    description: 'Baúl de proyectos',
    accent: 'rgba(255, 230, 130, 0.34)',
    iconColor: '#bfb63c',
    to: '/panel/proyectos',
  },
  {
    title: 'Procesamiento',
    description: 'Control de proyectos de infraestructura',
    accent: 'rgba(101, 229, 166, 0.34)',
    iconColor: '#1caa68',
    to: '/panel/procesamiento',
  },
  {
    title: 'Reportes',
    description: 'Reportes de actividad',
    accent: 'rgba(120, 202, 236, 0.34)',
    iconColor: '#2a87b5',
    to: '/panel/reportes',
  },
  {
    title: 'Alertas',
    description: 'Gestiona las alertas',
    accent: 'rgba(238, 154, 154, 0.34)',
    iconColor: '#c54c4c',
    to: '/panel/alertas',
  },
  {
    title: 'Asistente',
    description: 'Asistente de proyectos directos',
    accent: 'rgba(255, 215, 102, 0.34)',
    iconColor: '#c58a16',
    to: '/panel/asistente',
  },
]

const user = ref(null)

const loadUser = async () => {
  try {
    user.value = await getCurrentUser()
  } catch {
    user.value = null
  }
}

onMounted(() => {
  loadUser()
})
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>BIENVENIDO AL SISTEMA SICEPI</h1>
    </div>

    <section class="profile-card">
      <div class="profile-info">
        <div class="avatar-photo">
          <img v-if="user?.avatarUrl" :src="user.avatarUrl" alt="Perfil" />
          <span v-else>{{ user?.initials || 'US' }}</span>
        </div>
        <div>
          <strong>{{ user?.fullName || 'Usuario' }}</strong>
          <span>{{ user?.roleLabel || 'Sin rol' }}</span>
        </div>
      </div>

      <div class="info-group">
        <span>Ciudad</span>
        <strong>{{ user?.address || 'Sin dato' }}</strong>
      </div>

      <div class="info-group">
        <span>Estado</span>
        <strong class="state">{{ user?.isActive ? 'Activado' : 'Desactivado' }}</strong>
      </div>
    </section>

    <div class="panel-title-row">
      <h2>PANEL GENERAL</h2>
    </div>

    <section class="module-grid">
      <PanelModuleCard
        v-for="module in modules"
        :key="module.title"
        :title="module.title"
        :description="module.description"
        :accent="module.accent"
        :iconColor="module.iconColor"
        :to="module.to"
      />
    </section>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  height: 100%;
  box-sizing: border-box;
  overflow: auto;
  padding: 1rem 1.25rem 0.9rem;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.7rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(1.8rem, 2.5vw, 2.7rem);
  font-weight: 800;
  text-align: center;
}

.profile-card {
  width: min(100%, 940px);
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1rem;
  align-items: center;
  background: #ffffff;
  border-radius: 24px;
  padding: 0.45rem 1.15rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  margin: 0 auto 0.75rem;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 0.7rem;

  strong,
  span {
    display: block;
  }

  strong {
    font-size: clamp(1.15rem, 1.4vw, 1.55rem);
    font-weight: 600;
    color: #2b3241;
    line-height: 1.1;
  }

  span {
    color: #8e9ac1;
    font-size: 0.58rem;
    font-weight: 600;
  }
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;

  span {
    color: #7e95cc;
    font-size: 0.65rem;
    font-weight: 500;
  }

  strong {
    color: #1f2937;
    font-weight: 700;
    font-size: clamp(0.95rem, 1.2vw, 1.35rem);
    line-height: 1.1;
  }

  .state {
    color: #26cfb7;
  }
}

.panel-title-row {
  width: min(100%, 1080px);
  margin: 0 auto 0.7rem;

  h2 {
    margin: 0;
    color: #3a4779;
    font-size: clamp(1.6rem, 2vw, 2.2rem);
    font-weight: 800;
  }
}

.module-grid {
  width: min(100%, 1080px);
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
  padding-bottom: 0.8rem;
  margin: 0 auto;
}

.avatar-photo {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 28%, #f5dacd 0%, #d6b7a4 40%, #85aeb8 100%);
  color: #ffffff;
  display: grid;
  place-items: center;
  overflow: hidden;
  font-weight: 700;
  font-size: 0.86rem;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

@media (max-width: 1200px) {
  .module-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .profile-card {
    grid-template-columns: 1fr;
    text-align: center;
    width: min(100%, 560px);
    gap: 0.7rem;
    padding: 0.9rem 1rem;
  }

  .profile-info {
    justify-content: center;

    strong {
      font-size: 1.1rem;
    }

    span {
      font-size: 0.68rem;
    }
  }

  .info-group strong {
    font-size: 1rem;
  }

  .info-group span {
    font-size: 0.72rem;
  }
}

@media (max-width: 640px) {
  .module-grid {
    grid-template-columns: 1fr;
  }

  .section-shell {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
