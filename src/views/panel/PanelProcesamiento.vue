<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="section-shell">
    <h1>PROCESAMIENTO</h1>

    <div class="actions-row">
      <RouterLink class="mini-card active" to="/panel/procesamiento/subir"
        >SUBIR ARCHIVO</RouterLink
      >
      <RouterLink class="mini-card" to="/panel/procesamiento/procesar">Procesar Archivo</RouterLink>
      <RouterLink class="mini-card" to="/panel/procesamiento/buscar">Buscar Archivo</RouterLink>
    </div>

    <div class="content-grid">
      <div class="drop-zone">↥</div>

      <div class="form-grid">
        <label>
          <span>TITULO</span>
          <input value="charlenereed@gmail.com" />
        </label>
        <div class="two-cols">
          <label><span>LUGAR</span><input value="25 January 1990" /></label>
          <label><span>AÑO</span><input /></label>
        </div>
        <div class="two-cols">
          <label><span>ARCHIVO</span><input value="78860123" /></label>
          <label><span>CAO</span><input value="78860123" /></label>
        </div>
        <div class="bottom-row">
          <label><span>ARCHIVO PERTENIECIECIENTE</span><input value="Administrador" /></label>
          <button class="download">Descargar</button>
        </div>
      </div>
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

.actions-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.mini-card {
  background: white;
  border-radius: 18px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  text-decoration: none;
  color: #2f2f2f;
  border: 2px solid transparent;
  font-weight: 700;
}

.mini-card.active {
  border-color: #c3322c;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 1.5rem;
}

.drop-zone {
  min-height: 370px;
  border: 2px dashed #7c6b5f;
  border-radius: 18px;
  background: #f4e0b2;
  display: grid;
  place-items: center;
  font-size: 6rem;
  color: rgba(166, 140, 132, 0.8);
  font-weight: 700;
}

.form-grid {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;

  label {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  span {
    color: #7f93c5;
    font-size: 0.85rem;
  }

  input {
    border: 1px solid #b9a4ff;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    background: white;
  }
}

.two-cols,
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.bottom-row {
  align-items: end;
}

.download {
  border: 0;
  border-radius: 10px;
  background: #2832ff;
  color: white;
  padding: 0.95rem 1rem;
}

@media (max-width: 1100px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .actions-row,
  .two-cols,
  .bottom-row {
    grid-template-columns: 1fr;
  }
}
</style>
