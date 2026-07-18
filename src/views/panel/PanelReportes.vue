<template>
  <section class="section-shell">
    <h1>REPORTES</h1>

    <div class="stats-row">
      <div class="stat-card"><span>Numero de Proyectos</span><strong>120</strong></div>
      <div class="stat-card"><span>Numero de CAO</span><strong>120</strong></div>
      <div class="stat-card"><span>Alertas Detectadas</span><strong>20</strong></div>
    </div>

    <div class="chart-card">
      <div class="chart-placeholder">Reporte gráfico</div>
      <button class="download">Descargar</button>
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

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-card,
.chart-card {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

.stat-card {
  padding: 1rem;
  text-align: center;

  span {
    display: block;
    color: #7f93c5;
    margin-bottom: 0.35rem;
  }

  strong {
    font-size: 2.4rem;
  }
}

.chart-card {
  padding: 1rem;
}

.chart-placeholder {
  min-height: 260px;
  border-radius: 14px;
  background: linear-gradient(135deg, #eef1ff, #fff3df);
  display: grid;
  place-items: center;
  color: #7f93c5;
  margin-bottom: 1rem;
}

.download {
  margin-left: auto;
  display: block;
  border: 0;
  border-radius: 10px;
  background: #2832ff;
  color: white;
  padding: 0.95rem 1.2rem;
}

@media (max-width: 900px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}
</style>
