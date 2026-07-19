<script setup>
import { RouterLink } from 'vue-router'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
const alerts = [1, 2, 3, 4, 5]
</script>

<template>
  <section class="section-shell">
    <h1>ALERTAS</h1>

    <div class="list-card">
      <article v-for="index in alerts" :key="index" class="alert-row">
        <div class="folder"><img :src="IconCarpeta" alt="Carpeta" /></div>
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
        <RouterLink class="more-btn" to="/panel/alertas/detalle">Mas detalles</RouterLink>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1.8rem 1.5rem 1.2rem;
}

h1 {
  margin: 0 0 1.3rem;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
}

.list-card {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.alert-row {
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
  border: 0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 900px) {
  .alert-row {
    grid-template-columns: 1fr;
  }
}
</style>
