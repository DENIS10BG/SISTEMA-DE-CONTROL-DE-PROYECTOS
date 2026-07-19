<script setup>
import { computed, ref } from 'vue'
import IconFiltro from '@/components/icons/IconsUser/FiltroUsuario.svg'

const yearlyReportData = {
  2026: {
    stats: { proyectos: 120, cao: 120, alertas: 20 },
    chart: [
      { year: '2026', cao: 52, proyectos: 96 },
      { year: '2025', cao: 40, proyectos: 76 },
      { year: '2024', cao: 38, proyectos: 54 },
      { year: '2023', cao: 86, proyectos: 46 },
      { year: '2022', cao: 58, proyectos: 87 },
      { year: '2021', cao: 61, proyectos: 40 },
      { year: '2020', cao: 73, proyectos: 88 },
    ],
  },
  2025: {
    stats: { proyectos: 108, cao: 101, alertas: 16 },
    chart: [
      { year: '2025', cao: 48, proyectos: 82 },
      { year: '2024', cao: 44, proyectos: 61 },
      { year: '2023', cao: 79, proyectos: 52 },
      { year: '2022', cao: 55, proyectos: 80 },
      { year: '2021', cao: 58, proyectos: 43 },
      { year: '2020', cao: 68, proyectos: 83 },
      { year: '2019', cao: 49, proyectos: 58 },
    ],
  },
  2024: {
    stats: { proyectos: 94, cao: 88, alertas: 12 },
    chart: [
      { year: '2024', cao: 43, proyectos: 68 },
      { year: '2023', cao: 72, proyectos: 49 },
      { year: '2022', cao: 50, proyectos: 73 },
      { year: '2021', cao: 54, proyectos: 39 },
      { year: '2020', cao: 65, proyectos: 77 },
      { year: '2019', cao: 44, proyectos: 55 },
      { year: '2018', cao: 38, proyectos: 46 },
    ],
  },
}

const availableYears = Object.keys(yearlyReportData)
const selectedYear = ref('2026')

const currentReport = computed(
  () => yearlyReportData[selectedYear.value] ?? yearlyReportData['2026'],
)
</script>

<template>
  <section class="section-shell">
    <div class="header-row">
      <h1>REPORTES</h1>

      <div class="filter-chip">
        <img :src="IconFiltro" alt="" aria-hidden="true" />
        <select v-model="selectedYear" class="year-select" aria-label="Filtrar por año">
          <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
        </select>
        <span class="chevron" aria-hidden="true"></span>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <span>Numero de Proyectos</span>
        <strong>{{ currentReport.stats.proyectos }}</strong>
      </div>
      <div class="stat-card">
        <span>Numero de CAO</span>
        <strong>{{ currentReport.stats.cao }}</strong>
      </div>
      <div class="stat-card">
        <span>Alertas Detectadas</span>
        <strong>{{ currentReport.stats.alertas }}</strong>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-head">
        <div class="legend">
          <span class="legend-item">
            <i class="legend-dot cao"></i>
            CAO
          </span>
          <span class="legend-item">
            <i class="legend-dot proyectos"></i>
            Proyectos
          </span>
        </div>
      </div>

      <div class="chart-area">
        <div v-for="item in currentReport.chart" :key="item.year" class="chart-group">
          <div class="bars">
            <span class="bar cao" :style="{ height: `${item.cao}px` }"></span>
            <span class="bar proyectos" :style="{ height: `${item.proyectos}px` }"></span>
          </div>
          <span class="year-label">{{ item.year }}</span>
        </div>
      </div>

      <button class="download">Descargar</button>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1.4rem 1.5rem 1.2rem;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
}

.filter-chip {
  min-width: 130px;
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0 0.9rem;
  border: 1px solid #b7bfd4;
  border-radius: 10px;
  background: #f6f8fc;

  img {
    width: 14px;
    height: 14px;
    object-fit: contain;
    opacity: 0.8;
  }
}

.year-select {
  appearance: none;
  border: 0;
  background: transparent;
  color: #7a7f91;
  font-size: 0.95rem;
  width: 100%;
  min-width: 0;
  outline: none;
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
    font-weight: 700;
    font-size: 1.1rem;
  }

  strong {
    font-size: 2.4rem;
    font-weight: 500;
  }
}

.chart-card {
  padding: 1rem 1rem 0.8rem;
}

.chart-head {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.35rem;
}

.legend {
  display: flex;
  align-items: center;
  gap: 2.2rem;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.7rem;
  color: #7f93c5;
  font-weight: 600;
}

.legend-dot {
  width: 18px;
  height: 12px;
  border-radius: 5px;
  display: inline-block;
}

.legend-dot.cao {
  background: linear-gradient(180deg, #4565ff 0%, #2a24e8 100%);
}

.legend-dot.proyectos {
  background: linear-gradient(180deg, #f06aa7 0%, #ea4f8e 100%);
}

.chart-area {
  min-height: 260px;
  border-radius: 14px;
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 1.2rem;
  align-items: end;
  padding: 0.7rem 1rem 0.2rem;
  margin-bottom: 1rem;
}

.chart-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.45rem;
}

.bars {
  min-height: 188px;
  width: 100%;
  display: flex;
  align-items: end;
  justify-content: center;
  gap: 0.8rem;
}

.bar {
  width: min(36px, 100%);
  border-radius: 10px;
  display: block;
}

.bar.cao {
  background: linear-gradient(180deg, #4565ff 0%, #2a24e8 100%);
}

.bar.proyectos {
  background: linear-gradient(180deg, #ffb218 0%, #f8a400 100%);
}

.year-label {
  color: #7f93c5;
  font-size: 0.92rem;
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
  .header-row,
  .stats-row {
    grid-template-columns: 1fr;
  }

  .header-row {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-chip {
    width: 100%;
  }

  .chart-area {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>
