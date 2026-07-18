<script setup>
import projectPreview from '../../assets/images/IngenieroProyetos.png'
</script>

<template>
  <section class="detail-page">
    <div class="detail-head">
      <h1>PROYECTOS</h1>
      <input class="search" placeholder="Search for anything..." />
      <div class="filters">
        <button class="chip">Lugar</button>
        <button class="chip">Año</button>
      </div>
    </div>

    <article class="project-summary">
      <div class="project-hero">
        <div class="folder">▣</div>
        <div>
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
        <button class="details-btn">Mas detalles</button>
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
              <span class="action-icon">◔</span>
              <small>Ve el proyecto Completo</small>
            </button>
            <button class="action-box yellow">
              <span class="action-title">Descargar</span>
              <span class="action-icon">↓</span>
              <small>Descarga el Proyecto</small>
            </button>
            <button class="action-box green">
              <span class="action-title">Agente</span>
              <span class="action-icon">▢</span>
              <small>Agente de Preguntas</small>
            </button>
          </div>
        </div>

        <div class="side-stack">
          <button class="side-card"><span class="side-icon">⊚</span>Certificados de Obras</button>
          <button class="side-card"><span class="side-icon">⊚</span>Archivos Destacados</button>
          <button class="side-card"><span class="side-icon">⊚</span>Archivos Fijos</button>
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
  padding: 1.5rem 1.5rem 1.2rem;
  background: #eef1f6;
}

.detail-head {
  display: grid;
  grid-template-columns: auto minmax(280px, 1fr) auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(2rem, 2.9vw, 3rem);
  font-weight: 800;
}

.search,
.chip,
.details-btn {
  border: 1px solid #c8ccda;
  border-radius: 10px;
  background: white;
  padding: 0.75rem 1rem;
}

.search {
  max-width: 360px;
  width: 100%;
  justify-self: center;
  border-radius: 8px;
}

.filters {
  display: flex;
  gap: 0.75rem;
}

.chip {
  min-width: 96px;
  color: #6d7285;
}

.project-summary {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.project-hero {
  display: grid;
  grid-template-columns: 56px 1.55fr 0.75fr 0.9fr 0.55fr auto;
  gap: 1rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.9rem 1rem;
  box-shadow: 0 12px 24px rgba(35, 53, 87, 0.08);
}

.label {
  margin: 0 0 0.2rem;
  color: #f1a0bb;
  font-size: 0.85rem;
}

.label.blue {
  color: #7894d6;
}

.folder {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #ffd98f;
  display: grid;
  place-items: center;
  color: #2b2b2b;
  font-size: 1rem;
}

.details-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  border-radius: 999px;
  padding-inline: 1.2rem;
  font-weight: 700;
}

h2 {
  margin: 0;
  font-size: clamp(2.4rem, 3.2vw, 3.4rem);
  color: #222;
  font-weight: 500;
}

.detail-grid {
  display: grid;
  grid-template-columns: 250px 1fr 250px;
  gap: 1rem;
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
  padding: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
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
  height: 280px;
  border-radius: 8px;
  object-fit: cover;
  background: linear-gradient(180deg, #d55a40 0%, #b23d2b 100%);
}

.description-card {
  padding: 1rem 1.1rem 1.1rem;
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
  gap: 0.75rem;
}

.action-box {
  min-height: 118px;
  font-weight: 700;
  border: 2px solid #3f3f4d;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0.8rem 0.85rem;
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
  font-size: 1.5rem;
  line-height: 1;
}

.action-icon {
  width: 50px;
  height: 50px;
  border-radius: 999px;
  background: #ff6f8d;
  color: white;
  display: grid;
  place-items: center;
  font-size: 1.45rem;
}

.yellow .action-icon {
  background: #ffba49;
}

.green .action-icon {
  background: #96e07d;
}

.action-box small {
  max-width: 8rem;
  color: #4d5166;
  font-weight: 600;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.side-card,
.year-box {
  min-height: 62px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: left;
  font-weight: 700;
  padding: 0.8rem 1rem;
  border: 0;
  color: #33345a;
}

.side-card {
  gap: 0.8rem;
  font-size: 1.02rem;
}

.side-icon {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: #ffd7e1;
  color: #f48bb1;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
}

.year-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  font-size: 1.1rem;
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
