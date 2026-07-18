<script setup>
import alertPreview from '../../assets/images/IngenieroProyetos.png'
</script>

<template>
  <section class="detail-page">
    <div class="detail-head">
      <h1>ALERTAS</h1>
    </div>

    <article class="project-hero">
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
    </article>

    <h2>Construcción Tinglado RSAT-1 BUCH-ORURO</h2>

    <div class="detail-grid">
      <div class="preview-card">
        <span class="tag">Proyecto</span>
        <img class="mock-image" :src="alertPreview" alt="Documento del proyecto" />
        <small>3 CAO</small>
      </div>

      <div class="description-card">
        <h3>Descripción</h3>
        <p>
          Brainstorming brings team members' diverse experience into play. Brainstorming brings team
          members' diverse experience into play. Brainstorming brings team members' diverse
          experience into play. Brainstorming brings team members' diverse experience into play.
          Brainstorming brings team members' diverse experience into play.
        </p>
        <div class="alert-section">
          <div class="alert-badge">
            <span>ALERTA</span>
            <span class="alert-icon">📄</span>
          </div>
          <div class="alert-table">
            <div class="alert-table-head">
              <span>SL No</span>
              <span>Alerta</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion</span>
            </div>
          </div>
        </div>
      </div>

      <div class="side-stack">
        <button class="side-card active">
          <span class="side-title">Ver</span>
          <span class="side-icon pink">📄</span>
          <small>Ve el proyecto Completo</small>
        </button>
        <button class="side-card">
          <span class="side-title">SUBE</span>
          <span class="side-icon orange">↓</span>
          <small>Descarga el Proyecto</small>
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.detail-page {
  padding: 1.4rem 1.5rem 1.2rem;
  background: #eef1f6;
  min-height: 100%;
}

.detail-head {
  margin-bottom: 0.4rem;
}

h1,
h2 {
  margin: 0 0 1rem;
  color: #35457f;
}

h1 {
  font-size: clamp(2rem, 2.9vw, 3rem);
  font-weight: 800;
}

h2 {
  font-size: clamp(2.4rem, 3.2vw, 3.4rem);
  font-weight: 500;
  color: #222;
}

.project-hero {
  display: grid;
  grid-template-columns: 56px 1.5fr 0.75fr 0.9fr 0.5fr auto;
  gap: 1rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.9rem 1rem;
  box-shadow: 0 12px 24px rgba(35, 53, 87, 0.08);
  margin-bottom: 1rem;
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
}

.details-btn,
.side-card {
  border: 1px solid #c8ccda;
  border-radius: 10px;
  background: white;
  padding: 0.75rem 1rem;
}

.details-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  border-radius: 999px;
  padding-inline: 1.2rem;
  font-weight: 700;
}

.detail-grid {
  display: grid;
  grid-template-columns: 250px 1fr 220px;
  gap: 1rem;
  align-items: start;
}

.preview-card,
.description-card,
.side-card {
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

.alert-section {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 1rem;
  align-items: stretch;
}

.alert-badge {
  background: #f8a6b0;
  color: #2f3558;
  border-radius: 14px;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  font-size: 1.45rem;
  font-weight: 800;
}

.alert-icon {
  width: 58px;
  height: 58px;
  border-radius: 999px;
  background: #ff6487;
  color: white;
  display: grid;
  place-items: center;
  font-size: 1.6rem;
}

.alert-table {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.7rem 1rem 1rem;
}

.alert-table-head,
.alert-row {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 1rem;
  align-items: center;
}

.alert-table-head {
  color: #97b0e1;
  font-size: 0.85rem;
  padding: 0 0.2rem 0.3rem;
}

.alert-row {
  padding: 0.45rem 0.2rem;
  color: #383f60;
  font-size: 1rem;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.side-card {
  min-height: 138px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  text-align: left;
  font-weight: 700;
  border: 2px solid #3f3f4d;
  border-radius: 14px;
  padding: 0.8rem 0.9rem;
  color: #2f3558;
}

.side-card.active {
  background: #ffd8e4;
}

.side-title {
  font-size: 1.5rem;
  line-height: 1;
}

.side-icon {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  color: white;
  font-size: 1.45rem;
  align-self: center;
}

.pink {
  background: #ff6f8d;
}

.orange {
  background: #ffba49;
}

@media (max-width: 1100px) {
  .detail-grid,
  .project-hero,
  .alert-section,
  .detail-head {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .project-hero {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: 2rem;
  }
}
</style>
