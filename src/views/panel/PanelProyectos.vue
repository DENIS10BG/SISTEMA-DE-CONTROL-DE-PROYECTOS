<script setup>
import { RouterLink } from 'vue-router'

const projects = [1, 2, 3, 4, 5]
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>PROYECTOS</h1>
      <input class="search" placeholder="Search for anything..." />
      <div class="filters">
        <button class="action-btn">Lugar</button>
        <button class="action-btn">Año</button>
      </div>
    </div>

    <div class="list-card">
      <article v-for="index in projects" :key="index" class="project-row">
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
        <RouterLink class="more-btn" to="/panel/proyectos/detalle">Mas detalles</RouterLink>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1.8rem 1.5rem 1.2rem;
}

.section-head {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
}

.search,
.action-btn,
.more-btn {
  border: 1px solid #c8ccda;
  border-radius: 8px;
  background: white;
  padding: 0.75rem 1rem;
}

.filters {
  display: flex;
  gap: 0.75rem;
}

.list-card {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.project-row {
  display: grid;
  grid-template-columns: 56px 1.5fr 0.7fr 1fr 0.4fr auto;
  gap: 1rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.9rem 1rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
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

.more-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 900px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .project-row {
    grid-template-columns: 1fr;
  }
}
</style>
