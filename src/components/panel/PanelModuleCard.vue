<script setup>
import { RouterLink } from 'vue-router'
import IconUsuarios from '@/components/icons/Iconsnavbar/Usuarios.svg'
import IconProyectos from '@/components/icons/Iconsnavbar/Proyectos.svg'
import IconProcesamiento from '@/components/icons/Iconsnavbar/Procesamiento.svg'
import IconReportes from '@/components/icons/Iconsnavbar/Reportes.svg'
import IconAlertas from '@/components/icons/Iconsnavbar/Alertas.svg'
import IconAsistente from '@/components/icons/Iconsnavbar/Asistente.svg'

const iconByTitle = {
  Usuarios: IconUsuarios,
  Proyectos: IconProyectos,
  Procesamiento: IconProcesamiento,
  Reportes: IconReportes,
  Alertas: IconAlertas,
  Asistente: IconAsistente,
}

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  accent: {
    type: String,
    required: true,
  },
  iconColor: {
    type: String,
    required: true,
  },
  to: {
    type: String,
    required: false,
    default: '',
  },
})

const getIcon = () => iconByTitle[props.title] ?? IconUsuarios
</script>

<template>
  <RouterLink v-if="to" class="module-card" :class="title.toLowerCase()" :to="to">
    <h3>{{ title }}</h3>
    <div class="module-icon" :style="{ background: accent, color: iconColor }">
      <img :src="getIcon()" :alt="title" />
    </div>
    <p>{{ description }}</p>
  </RouterLink>

  <article v-else class="module-card" :class="title.toLowerCase()">
    <h3>{{ title }}</h3>
    <div class="module-icon" :style="{ background: accent, color: iconColor }">
      <img :src="getIcon()" :alt="title" />
    </div>
    <p>{{ description }}</p>
  </article>
</template>

<style scoped lang="scss">
.module-card {
  text-decoration: none;
  min-height: 130px;
  background: #ffffff;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 0.8rem 0.7rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  text-align: center;
  border: 0;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(35, 53, 87, 0.12);
  }

  h3 {
    margin: 0;
    font-size: 1.08rem;
    color: #343434;
  }

  p {
    margin: 0;
    color: #8d9bcc;
    font-size: 0.85rem;
    line-height: 1.15;
  }
}

.module-icon {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  margin: 0.55rem 0 0.7rem;

  img {
    width: 31px;
    height: 31px;
    object-fit: contain;
    filter: grayscale(1) brightness(0.78);
  }
}

.module-card.usuarios .module-icon img {
  filter: brightness(0) saturate(100%) invert(27%) sepia(93%) saturate(3428%) hue-rotate(228deg)
    brightness(103%) contrast(101%);
}

.module-card.proyectos .module-icon img {
  filter: brightness(0) saturate(100%) invert(76%) sepia(52%) saturate(602%) hue-rotate(14deg)
    brightness(94%) contrast(84%);
}

.module-card.procesamiento .module-icon img {
  filter: brightness(0) saturate(100%) invert(47%) sepia(81%) saturate(454%) hue-rotate(112deg)
    brightness(92%) contrast(96%);
}

.module-card.reportes .module-icon img {
  filter: brightness(0) saturate(100%) invert(42%) sepia(73%) saturate(572%) hue-rotate(160deg)
    brightness(95%) contrast(90%);
}

.module-card.alertas .module-icon img {
  filter: brightness(0) saturate(100%) invert(45%) sepia(49%) saturate(944%) hue-rotate(321deg)
    brightness(90%) contrast(91%);
}

.module-card.asistente .module-icon img {
  filter: brightness(0) saturate(100%) invert(63%) sepia(72%) saturate(676%) hue-rotate(1deg)
    brightness(97%) contrast(92%);
}
</style>
