<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="detail-page">
    <h1>ASISTENTE</h1>

    <article class="project-hero">
      <div class="folder">▣</div>
      <div>
        <p class="label">Proyecto</p>
        <strong>Construccion Tinglado RSAT-1 BUCH-ORURO</strong>
      </div>
      <div>
        <p class="label">Lugar</p>
        <strong>Oruro</strong>
      </div>
      <div>
        <p class="label">Codigo identificador</p>
        <strong>789945661-0</strong>
      </div>
      <div>
        <p class="label">Año</p>
        <strong>2019</strong>
      </div>
      <span class="status">Disponible</span>
    </article>

    <div class="qa-grid">
      <section class="qa-card">
        <h2>PREGUNTAS</h2>
        <div class="bubble">
          <strong>Wireframes</strong>
          <p>..........................................................</p>
          <p>fasfafadfadsfdsfdsfdfsdfsdfsdfsdfs</p>
        </div>
        <button class="send-btn">Enviar</button>
      </section>

      <section class="qa-card">
        <h2>Respuestas</h2>
        <div class="bubble">
          <strong>Wireframes</strong>
          <p>..........................................................dfsfas</p>
          <p>fasfadfadsfsdfsdfsdfdsfsdfsdf</p>
        </div>
      </section>
    </div>

    <div class="footer-links">
      <RouterLink class="back-btn" to="/panel/asistente">Volver</RouterLink>
    </div>
  </section>
</template>

<style scoped lang="scss">
.detail-page {
  padding: 1.8rem 1.5rem 1.2rem;
}

h1 {
  margin: 0 0 1rem;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
}

.project-hero {
  display: grid;
  grid-template-columns: 56px 1.5fr 0.7fr 1fr 0.4fr auto;
  gap: 1rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.9rem 1rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  margin-bottom: 1rem;
}

.label {
  margin: 0 0 0.2rem;
  color: #f1a0bb;
  font-size: 0.85rem;
}

.folder {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #ffd97a;
  display: grid;
  place-items: center;
}

.status {
  justify-self: end;
  background: #63d24d;
  color: white;
  border-radius: 16px;
  padding: 0.55rem 1rem;
  font-weight: 700;
}

.qa-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.qa-card {
  border: 2px solid #373737;
  border-radius: 12px;
  background: #f7f7f7;
  padding: 1rem;
  min-height: 330px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.qa-card h2 {
  margin: 0;
  color: #35457f;
}

.bubble {
  background: white;
  border-radius: 12px;
  min-height: 160px;
  padding: 1rem;
}

.send-btn {
  align-self: center;
  border: 0;
  border-radius: 14px;
  background: #63d24d;
  color: white;
  padding: 0.7rem 2rem;
}

.footer-links {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.back-btn {
  text-decoration: none;
  color: #35457f;
}

@media (max-width: 1100px) {
  .project-hero,
  .qa-grid {
    grid-template-columns: 1fr;
  }
}
</style>
