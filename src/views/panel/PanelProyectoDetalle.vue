<script setup>
import { RouterLink } from 'vue-router'
import projectPreview from '../../assets/images/IngenieroProyetos.png'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconCertificados from '@/components/icons/IconsProyect/Certificados.svg'
import IconArchivosDestacados from '@/components/icons/IconsProyect/ArchivosDestacados.svg'
import IconArchivosFijos from '@/components/icons/IconsProyect/ArchivosFijos.svg'
import IconDescarga from '@/components/icons/IconsProyect/Descarga.svg'
import IconPreguntas from '@/components/icons/IconsProyect/Preguntas.svg'
import IconFiltro from '@/components/icons/IconsUser/FiltroUsuario.svg'
import IconFlechaIzquierda from '@/components/icons/IconsUser/FlechaIzquierda.svg'
</script>

<template>
  <section class="detail-page">
    <div class="detail-head">
      <h1>PROYECTOS</h1>
      <div class="search-shell">
        <span class="search-icon" aria-hidden="true"></span>
        <input class="search" placeholder="Search for anything..." />
      </div>
      <div class="filters">
        <button class="chip">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <span>Lugar</span>
          <span class="chevron" aria-hidden="true"></span>
        </button>
        <button class="chip">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <span>Año</span>
          <span class="chevron" aria-hidden="true"></span>
        </button>
      </div>
    </div>

    <article class="project-summary">
      <div class="project-hero">
        <div class="folder">
          <img :src="IconCarpeta" alt="Carpeta del proyecto" />
        </div>
        <div class="project-text">
          <p class="label">Proyecto</p>
          <strong>Construccion Tinglado RSAT-1 BUCH-ORURO</strong>
        </div>
        <div>
          <p class="label blue">Lugar</p>
          <strong>Oruro</strong>
        </div>
        <div>
          <p class="label blue">Archivo</p>
          <strong>Proyecto</strong>
        </div>
        <div>
          <p class="label blue">Año</p>
          <strong>2019</strong>
        </div>
        <RouterLink class="details-btn" to="/panel/proyectos" aria-label="Volver a proyectos">
          <img :src="IconFlechaIzquierda" alt="" aria-hidden="true" />
        </RouterLink>
      </div>

      <h2>Construcción Tinglado RSAT-1 BUCH-ORURO</h2>

      <div class="detail-grid">
        <div class="preview-card">
          <span class="tag">Proyecto</span>
          <img class="mock-image" :src="projectPreview" alt="Documento del proyecto" />
          <small>3 CAO</small>
        </div>

        <div class="center-stack">
          <div class="description-card">
            <h3>Descripción</h3>
            <p>
              Brainstorming brings team members' diverse experience into play. Brainstorming brings
              team members' diverse experience into play. Brainstorming brings team members' diverse
              experience into play. Brainstorming brings team members' diverse experience into play.
              Brainstorming brings team members' diverse experience into play.
            </p>
          </div>

          <div class="action-row">
            <button class="action-box pink">
              <span class="action-title">Ver</span>
              <span class="action-icon">
                <img :src="IconCarpeta" alt="Ver proyecto" />
              </span>
              <small>Ve el proyecto Completo</small>
            </button>
            <button class="action-box yellow">
              <span class="action-title">Descargar</span>
              <span class="action-icon">
                <img :src="IconDescarga" alt="Descargar proyecto" />
              </span>
              <small>Descarga el Proyecto</small>
            </button>
            <button class="action-box green">
              <span class="action-title">Agente</span>
              <span class="action-icon">
                <img :src="IconPreguntas" alt="Agente de preguntas" />
              </span>
              <small>Agente de Preguntas</small>
            </button>
          </div>
        </div>

        <div class="side-stack">
          <button class="side-card">
            <span class="side-icon">
              <img :src="IconCertificados" alt="Certificados de obras" />
            </span>
            Certificados de Obras
          </button>
          <button class="side-card">
            <span class="side-icon">
              <img :src="IconArchivosDestacados" alt="Archivos destacados" />
            </span>
            Archivos Destacados
          </button>
          <button class="side-card">
            <span class="side-icon">
              <img :src="IconArchivosFijos" alt="Archivos fijos" />
            </span>
            Archivos Fijos
          </button>
          <div class="year-box">
            <span>2019</span>
            <span>ORURO</span>
          </div>
        </div>
      </div>
    </article>
  </section>
</template>

<style scoped lang="scss">
.detail-page {
  min-height: 100%;
  padding: 1.25rem 1.25rem 1rem;
  background: #eef1f6;
}

.detail-head {
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
.chip,
.details-btn {
  border: 1px solid #c8ccda;
  border-radius: 12px;
  background: white;
}

.search-shell {
  min-height: 48px;
  width: 100%;
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

.chip {
  min-width: 132px;
  min-height: 48px;
  color: #6d7285;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  padding: 0 0.9rem;
  box-shadow: 0 6px 18px rgba(35, 53, 87, 0.05);
}

.chip img {
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

.project-summary {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.project-hero {
  display: grid;
  grid-template-columns: 48px minmax(0, 1.28fr) 0.56fr 0.68fr 0.38fr 54px;
  gap: 0.75rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.64rem 0.9rem;
  box-shadow: 0 12px 24px rgba(35, 53, 87, 0.08);
}

.label {
  margin: 0 0 0.18rem;
  color: #f1a0bb;
  font-size: 0.8rem;
  line-height: 1;
}

.label.blue {
  color: #7894d6;
}

.project-text strong {
  display: block;
  max-width: 250px;
  font-size: 0.89rem;
  line-height: 1.08;
  font-weight: 600;
  color: #222;
}

.folder {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #ffd98f;
  display: grid;
  place-items: center;

  img {
    width: 20px;
    height: 20px;
    object-fit: contain;
  }
}

.details-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  border-radius: 999px;
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  padding: 0;
  justify-self: end;

  img {
    width: 18px;
    height: 18px;
    object-fit: contain;
    filter: brightness(0) invert(1);
  }
}

h2 {
  margin: 0;
  font-size: clamp(2rem, 2.8vw, 3rem);
  color: #222;
  font-weight: 500;
  line-height: 1.05;
}

.detail-grid {
  display: grid;
  grid-template-columns: 230px minmax(0, 1fr) 230px;
  gap: 0.9rem;
  align-items: start;
}

.center-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preview-card,
.description-card,
.side-card,
.year-box {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

.preview-card {
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  align-items: center;
}

.tag {
  align-self: flex-start;
  background: #d7f1d9;
  color: #80bd7a;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
}

.mock-image {
  width: 100%;
  height: 198px;
  border-radius: 8px;
  object-fit: cover;
  background: linear-gradient(180deg, #d55a40 0%, #b23d2b 100%);
}

.description-card {
  padding: 0.9rem 1rem 1rem;
}

.description-card h3 {
  margin: 0 0 0.45rem;
  color: #33345a;
  font-size: 1.05rem;
}

.description-card p {
  margin: 0;
  color: #6d7487;
  line-height: 1.45;
  font-size: 0.92rem;
}

.action-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.7rem;
}

.action-box {
  min-height: 104px;

  img {
    width: 24px;
    height: 24px;
    object-fit: contain;
    filter: brightness(0) invert(1);
  }
  font-weight: 700;
  border: 1.5px solid #3f3f4d;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0.72rem 0.8rem;
  text-align: left;
  color: #31365f;
}

.pink {
  background: #ffd9e0;
}
.yellow {
  background: #fde8bf;
}
.green {
  background: #d8ffd9;
}

.action-title {
  font-size: 1.18rem;
  line-height: 1;
}

.action-icon {
  width: 44px;
  height: 44px;
  border-radius: 999px;
  background: #ff6f8d;
  color: white;
  display: grid;
  place-items: center;
}

.yellow .action-icon {
  background: #ffba49;
}

.green .action-icon {
  background: #96e07d;
}

.action-box small {
  max-width: 7rem;
  color: #4d5166;
  font-weight: 600;
  font-size: 0.8rem;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.side-card,
.year-box {
  min-height: 54px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: left;
  font-weight: 700;
  padding: 0.65rem 0.85rem;
  border: 0;
  color: #33345a;
}

.side-card {
  gap: 0.8rem;
  font-size: 0.94rem;
}

.side-icon {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  background: #ffd7e1;
  color: #f48bb1;
  display: grid;
  place-items: center;
  flex: 0 0 auto;

  img {
    width: 16px;
    height: 16px;
    object-fit: contain;
  }
}

.year-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  font-size: 0.95rem;
  gap: 0;
}

@media (max-width: 1100px) {
  .detail-grid,
  .project-hero,
  .detail-head {
    grid-template-columns: 1fr;
  }

  .search {
    max-width: none;
    justify-self: stretch;
  }

  .project-text strong {
    max-width: none;
  }
}

@media (max-width: 900px) {
  .action-row {
    grid-template-columns: 1fr;
  }

  .side-stack {
    order: 3;
  }

  .filters {
    flex-direction: column;
  }

  h2 {
    font-size: 2rem;
  }
}
</style>
