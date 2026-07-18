<script setup>
import PanelModuleCard from '@/components/panel/PanelModuleCard.vue'

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
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>BIENVENIDO AL SISTEMA SICEPI</h1>
    </div>

    <section class="profile-card">
      <div class="profile-info">
        <div class="avatar large">MR</div>
        <div>
          <strong>Maria Rocke Castillo</strong>
          <span>Administrador</span>
        </div>
      </div>

      <div class="info-group">
        <span>Ciudad</span>
        <strong>La paz - Bolivia</strong>
      </div>

      <div class="info-group">
        <span>Estado</span>
        <strong class="state">Activado</strong>
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
  padding: 1.8rem 1.5rem 1.2rem;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 3rem);
  font-weight: 800;
  text-align: center;
}

.profile-card {
  width: min(100%, 540px);
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 1rem;
  align-items: center;
  background: #ffffff;
  border-radius: 18px;
  padding: 0.8rem 1.1rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  margin: 0 auto 1rem;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;

  strong,
  span {
    display: block;
  }

  span {
    color: #8e9ac1;
    font-size: 0.92rem;
  }
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;

  span {
    color: #8e9ac1;
    font-size: 0.92rem;
  }

  strong {
    color: #1f2937;
    font-weight: 700;
  }

  .state {
    color: #26cfb7;
  }
}

.panel-title-row {
  width: min(100%, 1080px);
  margin: 0 auto 1rem;

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
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.1rem;
  padding-bottom: 1.4rem;
  margin: 0 auto;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #cfd6e7, #9ca9ca);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 0.95rem;

  &.large {
    width: 48px;
    height: 48px;
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
    width: min(100%, 420px);
  }

  .profile-info {
    justify-content: center;
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
