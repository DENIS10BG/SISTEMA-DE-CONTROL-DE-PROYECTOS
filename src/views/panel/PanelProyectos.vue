<script setup>
import { RouterLink } from 'vue-router'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconFiltro from '@/components/icons/IconsUser/FiltroUsuario.svg'

const projects = [1, 2, 3, 4, 5]
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>PROYECTOS</h1>
      <div class="search-shell">
        <span class="search-icon" aria-hidden="true"></span>
        <input class="search" placeholder="Search for anything..." />
      </div>
      <div class="filters">
        <button class="action-btn">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <span>Lugar</span>
          <span class="chevron" aria-hidden="true"></span>
        </button>
        <button class="action-btn">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <span>Año</span>
          <span class="chevron" aria-hidden="true"></span>
        </button>
      </div>
    </div>

    <div class="list-card">
      <article v-for="index in projects" :key="index" class="project-row">
        <div class="folder">
          <img :src="IconCarpeta" alt="Carpeta" />
        </div>
        <div>
          <p class="label">Proyecto</p>
          <strong>Construccion Tinglado RSAT-1 BUCH-ORURO</strong>
        </div>
        <div>
          <p class="label">Lugar</p>
          <strong>Oruro</strong>
        </div>
        <div>
          <p class="label">Archivo</p>
          <strong>Proyecto</strong>
        </div>
        <div>
          <p class="label">Año</p>
          <strong>2019</strong>
        </div>
        <RouterLink class="more-btn" to="/panel/proyectos/detalle">Mas detalles</RouterLink>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1.5rem 1.4rem 1.1rem;
}

.section-head {
  display: grid;
  grid-template-columns: auto minmax(320px, 1fr) auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
  line-height: 1;
}

.search-shell,
.action-btn,
.more-btn {
  border: 1px solid #c8ccda;
  border-radius: 12px;
  background: white;
}

.search-shell {
  min-height: 48px;
  display: flex;
  align-items: center;
  gap: 0.95rem;
  padding: 0 0.9rem 0 1rem;
  border-color: transparent;
  box-shadow: 0 6px 18px rgba(35, 53, 87, 0.05);
}

.search-icon {
  width: 18px;
  height: 18px;
  border: 2px solid #96a0b9;
  border-radius: 50%;
  flex: 0 0 auto;
  position: relative;
}

.search-icon::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 2px;
  background: #96a0b9;
  border-radius: 999px;
  right: -7px;
  bottom: -3px;
  transform: rotate(45deg);
  transform-origin: center;
}

.search {
  border: 0;
  outline: 0;
  width: 100%;
  min-width: 0;
  color: #4c5163;
  font-size: 0.95rem;
}

.filters {
  display: flex;
  gap: 0.85rem;
}

.action-btn {
  min-width: 132px;
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  padding: 0 0.9rem;
  color: #7a7f91;
  font-size: 0.95rem;
  box-shadow: 0 6px 18px rgba(35, 53, 87, 0.05);
}

.action-btn img {
  width: 16px;
  height: 16px;
  object-fit: contain;
  opacity: 0.8;
}

.chevron {
  width: 7px;
  height: 7px;
  border-right: 2px solid #8d93a8;
  border-bottom: 2px solid #8d93a8;
  transform: rotate(45deg);
  margin-top: -2px;
  flex: 0 0 auto;
}

.list-card {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.project-row {
  display: grid;
  grid-template-columns: 56px minmax(0, 1.2fr) 0.52fr 0.68fr 0.38fr 138px;
  gap: 0.85rem;
  align-items: center;
  background: white;
  border-radius: 20px;
  padding: 0.7rem 1rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

.label {
  margin: 0 0 0.18rem;
  color: #f1a0bb;
  font-size: 0.8rem;
  line-height: 1;
}

.project-text strong {
  display: block;
  max-width: 265px;
  font-size: 0.92rem;
  line-height: 1.1;
  font-weight: 600;
  color: #222;
}

.folder {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: #ffd97a;
  display: grid;
  place-items: center;

  img {
    width: 22px;
    height: 22px;
    object-fit: contain;
  }
}

.more-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  border-radius: 999px;
  padding-inline: 1.2rem;
  font-size: 0.95rem;
  font-weight: 700;
}

@media (max-width: 900px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .project-row {
    grid-template-columns: 1fr;
  }

  .project-text strong {
    max-width: none;
  }
}
</style>
