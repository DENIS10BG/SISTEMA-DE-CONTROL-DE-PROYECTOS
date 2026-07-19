<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import projectPreview from '../../assets/images/IngenieroProyetos.png'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconCertificados from '@/components/icons/IconsProyect/Certificados.svg'
import ArchivosFijos from '@/components/icons/IconsProyect/ArchivosFijos.svg'
import ArchivosDestacados from '@/components/icons/IconsProyect/ArchivosDestacados.svg'
import IconDescarga from '@/components/icons/IconsProyect/Descarga.svg'
import IconPreguntas from '@/components/icons/IconsProyect/Preguntas.svg'
import IconFiltro from '@/components/icons/IconsUser/FiltroUsuario.svg'
import IconFlechaIzquierda from '@/components/icons/IconsUser/FlechaIzquierda.svg'

const lugares = [
  'La Paz',
  'Oruro',
  'Potosi',
  'Cochabamba',
  'Tarija',
  'Beni',
  'Santa Cruz',
  'Pando',
  'Chuquisaca',
]

const anios = Array.from({ length: 17 }, (_, index) => String(2026 - index))

const selectedLugar = ref('')
const selectedAnio = ref('')

const certificatesOpen = ref(true)
const certificateItems = Array.from({ length: 7 }, (_, index) => index + 1)
const route = useRoute()

const selectedCaoId = computed(() => {
  const parsed = Number(route.params.id)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 1
})

const toggleCertificates = () => {}
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
        <div class="chip select-chip">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <select v-model="selectedLugar" class="chip-select" aria-label="Filtrar por lugar">
            <option value="">Lugar</option>
            <option v-for="lugar in lugares" :key="lugar" :value="lugar">{{ lugar }}</option>
          </select>
          <span class="chevron" aria-hidden="true"></span>
        </div>
        <div class="chip select-chip">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <select v-model="selectedAnio" class="chip-select" aria-label="Filtrar por año">
            <option value="">Año</option>
            <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
          </select>
          <span class="chevron" aria-hidden="true"></span>
        </div>
      </div>
    </div>

    <article class="project-summary">
      <div class="project-hero">
        <div class="folder">
          <img :src="IconCarpeta" alt="Carpeta del proyecto" />
        </div>
        <div class="project-text">
          <p class="label">CAO</p>
          <strong>Certificado de Avance de Obras {{ selectedCaoId }}</strong>
        </div>
        <div>
          <p class="label blue">Lugar</p>
          <strong>Oruro</strong>
        </div>
        <div>
          <p class="label blue">CAO</p>
          <strong>Certificado {{ selectedCaoId }}</strong>
        </div>
        <div>
          <p class="label blue">Año</p>
          <strong>2019</strong>
        </div>
        <RouterLink class="details-btn" to="/panel/proyectos" aria-label="Volver a proyectos">
          <img :src="IconFlechaIzquierda" alt="" aria-hidden="true" />
        </RouterLink>
      </div>

      <h2>Certificado de Avance de Obras {{ selectedCaoId }}</h2>

      <div class="detail-grid">
        <div class="preview-card">
          <span class="tag">CAO</span>
          <img class="mock-image" :src="projectPreview" alt="Documento del proyecto" />
          <small>CAO {{ selectedCaoId }}</small>
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
          <div class="certificate-panel">
            <div class="certificate-root">
              <button class="side-card side-card-expand">
                <span class="side-icon">
                  <img :src="IconCertificados" alt="Certificados de obras" />
                </span>
                <span class="side-card-content">
                  <span class="side-card-title">Certificados de Avance de Obras</span>
                  <span class="side-card-sub">1, 2, 3, 4, 5, 6, 7</span>
                </span>
                <span class="side-card-arrow open" aria-hidden="true"></span>
              </button>

              <button class="side-card side-card-plain">
                <span class="side-icon">
                  <img :src="ArchivosDestacados" alt="Archivos Destacados" />
                </span>
                <span class="side-card-content">
                  <span class="side-card-title">Archivos Destacados</span>
                </span>
              </button>

              <button class="side-card side-card-plain">
                <span class="side-icon">
                  <img :src="ArchivosFijos" alt="Archivos Fijos" />
                </span>
                <span class="side-card-content">
                  <span class="side-card-title">Archivos Fijos</span>
                </span>
              </button>
            </div>

            <div v-if="certificatesOpen" class="certificate-overlay">
              <div class="certificate-back certificate-back-root">
                <span>Certificados de Avances de Obras</span>
              </div>

              <div class="certificate-scroll certificate-list">
                <RouterLink
                  v-for="item in certificateItems"
                  :key="item"
                  :to="`/panel/proyectos/cao/${item}`"
                  class="certificate-line certificate-link"
                  :class="{ active: item === selectedCaoId }"
                >
                  <span class="certificate-folder">
                    <img :src="IconCarpeta" alt="Carpeta" />
                  </span>
                  <span class="certificate-text">Certificado de Avance de Obras {{ item }}</span>
                </RouterLink>
              </div>
            </div>
          </div>
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
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
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
  min-width: 176px;
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

.select-chip {
  position: relative;
}

.chip-select {
  appearance: none;
  border: 0;
  background: transparent;
  color: #6d7285;
  font-size: 0.95rem;
  width: 100%;
  min-width: 0;
  outline: none;
  padding-right: 0.9rem;
}

.chevron {
  width: 7px;
  height: 7px;
  border-right: 2px solid #8d93a8;
  border-bottom: 2px solid #8d93a8;
  transform: rotate(45deg);
  margin-top: -2px;
  flex: 0 0 auto;
  pointer-events: none;
}

.project-summary {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  flex: 1;
  min-height: 0;
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
  grid-template-columns: 1fr 2fr 1.6fr;
  gap: 0.9rem;
  align-items: start;
  flex: 1;
  min-height: 0;
  align-items: stretch;
}

.center-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  align-items: flex-start;
}

.preview-card,
.description-card,
.side-card,
.year-box {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  span {
    font-weight: 700;
  }
}

.preview-card {
  padding: 0.8rem;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 0.65rem;
  align-items: start;
  height: 100%;
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
  height: 100%;
  min-height: 198px;
  max-height: 320px;
  border-radius: 8px;
  object-fit: cover;
  background: linear-gradient(180deg, #d55a40 0%, #b23d2b 100%);
}

.description-card {
  padding: 0.9rem 1rem 1rem;
  flex: 1;
  width: 100%;
  align-self: flex-start;
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
  width: 100%;
  align-self: flex-start;
}

.action-box {
  min-height: 10px;

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
  width: 40px;
  height: 40px;
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
  gap: 0.85rem;
  height: 100%;
}

.certificate-panel {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  position: relative;
}

.certificate-root {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.side-card-content {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
  flex: 1;
}

.side-card-title {
  font-size: 1rem;
  line-height: 1.1;
}

.side-card-sub {
  font-size: 0.8rem;
  font-weight: 600;
  color: #8a91ad;
}

.side-card-expand {
  width: 100%;
}

.side-card-plain {
  width: 100%;
}

.side-card,
.year-box {
  min-height: 75px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  font-weight: 800;
  padding: 0.65rem 0.85rem;
  border: 0;
  color: #33345a;
}

.side-card {
  gap: 0.8rem;
  font-size: 1rem;
  justify-content: flex-start;
  text-align: left;
}

.side-card-expand {
  padding-right: 0.7rem;
}

.side-card-arrow {
  width: 8px;
  height: 8px;
  border-right: 2px solid #8d93a8;
  border-bottom: 2px solid #8d93a8;
  transform: rotate(45deg);
  flex: 0 0 auto;
  margin-left: auto;
}

.side-card-arrow.open {
  transform: rotate(225deg);
  margin-top: 4px;
}

.side-card-arrow.left {
  transform: rotate(225deg);
  margin-left: 0;
  margin-right: 0.2rem;
}

.side-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background: #ffd7e1;
  color: #f48bb1;
  display: grid;
  place-items: center;
  flex: 0 0 auto;

  img {
    width: 25px;
    height: 25px;
    object-fit: contain;
  }
}
.certificate-overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.6rem;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.certificate-back-root {
  margin-bottom: 0.8rem;
}

.certificate-back {
  width: 100%;
  min-height: 54px;
  border: 0;
  border-radius: 14px;
  background: #f6f8fc;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.65rem 0.75rem;
  text-align: left;
  color: #33345a;
  font-weight: 800;
  margin-bottom: 0.6rem;
}

.certificate-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.certificate-detail {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  min-height: 0;
  flex: 1;
}

.certificate-detail-title {
  font-size: 1rem;
  font-weight: 800;
  color: #33345a;
}

.certificate-detail-sub {
  font-size: 0.8rem;
  color: #8a91ad;
  font-weight: 600;
}

.certificate-scroll {
  margin-top: 0.35rem;
  max-height: 100%;
  overflow-y: auto;
  padding-right: 0.25rem;
}

.certificate-line {
  min-height: 42px;
  border-radius: 12px;
  background: #fff7fa;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.55rem 0.75rem;
  margin-bottom: 0;
  color: #33345a;
  font-weight: 600;
  border: 0;
  width: 100%;
  text-align: left;
}

.certificate-link {
  text-decoration: none;
}

.certificate-line.active {
  background: #ffeef5;
  outline: 1px solid #f4d9e5;
}

.certificate-line.detail-line {
  margin-bottom: 0.45rem;
}

.certificate-folder {
  width: 28px;
  height: 28px;
  border-radius: 9px;
  background: #ffd7e1;
  display: grid;
  place-items: center;
  flex: 0 0 auto;

  img {
    width: 16px;
    height: 16px;
    object-fit: contain;
  }
}

.certificate-text {
  flex: 1;
}

.side-icon.small {
  width: 44px;
  height: 44px;

  img {
    width: 18px;
    height: 18px;
    object-fit: contain;
  }
}

.year-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  font-size: 0.95rem;
  gap: 0;
  margin-top: auto;
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

  .detail-grid,
  .center-stack,
  .side-stack,
  .preview-card {
    height: auto;
    min-height: 0;
  }

  .mock-image {
    height: 198px;
    max-height: none;
  }

  .description-card {
    width: 100%;
  }

  .action-row {
    width: 100%;
  }

  .certificate-dropdown {
    max-height: none;
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
