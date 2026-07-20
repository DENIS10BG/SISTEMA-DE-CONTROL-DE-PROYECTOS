<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'

const alerts = [
  {
    id: 1,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Oruro',
    archivo: 'Proyecto',
    anio: '2019',
  },
  {
    id: 2,
    proyecto: 'Mejoramiento Unidad Educativa San Andres',
    lugar: 'La Paz',
    archivo: 'CAO',
    anio: '2020',
  },
  {
    id: 3,
    proyecto: 'Pavimentacion Avenida Principal Distrito 4',
    lugar: 'Cochabamba',
    archivo: 'Proyecto',
    anio: '2021',
  },
  {
    id: 4,
    proyecto: 'Sistema de Riego Comunidad Huayllani',
    lugar: 'Tarija',
    archivo: 'CAO',
    anio: '2022',
  },
  {
    id: 5,
    proyecto: 'Construccion Centro de Salud Municipal',
    lugar: 'Santa Cruz',
    archivo: 'Proyecto',
    anio: '2023',
  },
]

const searchText = ref('')
const selectedArchivo = ref('')
const selectedLugar = ref('')
const selectedAnio = ref('')

const archivoOptions = ['Proyecto', 'CAO']
const lugarOptions = computed(() => [...new Set(alerts.map((alert) => alert.lugar))])
const anioOptions = computed(() => [...new Set(alerts.map((alert) => alert.anio))])

const filteredAlerts = computed(() => {
  const query = searchText.value.trim().toLowerCase()

  return alerts.filter((alert) => {
    const matchesArchivo = !selectedArchivo.value || alert.archivo === selectedArchivo.value
    const matchesLugar = !selectedLugar.value || alert.lugar === selectedLugar.value
    const matchesAnio = !selectedAnio.value || alert.anio === selectedAnio.value
    const matchesSearch =
      !query ||
      alert.proyecto.toLowerCase().includes(query) ||
      alert.lugar.toLowerCase().includes(query) ||
      alert.archivo.toLowerCase().includes(query) ||
      alert.anio.includes(query)

    return matchesArchivo && matchesLugar && matchesAnio && matchesSearch
  })
})
</script>

<template>
  <section class="section-shell">
    <h1>ALERTAS</h1>

    <div class="search-controls">
      <input v-model="searchText" class="search-input" placeholder="Buscar archivo..." />
      <div class="control-group">
        <select v-model="selectedArchivo" class="control-select">
          <option value="">Tipo de archivo</option>
          <option v-for="archivo in archivoOptions" :key="archivo" :value="archivo">
            {{ archivo }}
          </option>
        </select>
        <select v-model="selectedLugar" class="control-select">
          <option value="">Lugar</option>
          <option v-for="lugar in lugarOptions" :key="lugar" :value="lugar">{{ lugar }}</option>
        </select>
        <select v-model="selectedAnio" class="control-select">
          <option value="">Año</option>
          <option v-for="anio in anioOptions" :key="anio" :value="anio">{{ anio }}</option>
        </select>
      </div>
    </div>

    <div class="list-card">
      <article v-for="alert in filteredAlerts" :key="alert.id" class="alert-row">
        <div class="folder"><img :src="IconCarpeta" alt="Carpeta" /></div>
        <div>
          <p class="label">Proyecto</p>
          <strong>{{ alert.proyecto }}</strong>
        </div>
        <div>
          <p class="label">Lugar</p>
          <strong>{{ alert.lugar }}</strong>
        </div>
        <div>
          <p class="label">Archivo</p>
          <strong>{{ alert.archivo }}</strong>
        </div>
        <div>
          <p class="label">Año</p>
          <strong>{{ alert.anio }}</strong>
        </div>
        <RouterLink class="more-btn" to="/panel/alertas/detalle">Mas detalles</RouterLink>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1rem 1.5rem 1.2rem;
}

h1 {
  margin: 0 0 1.3rem;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
}

.search-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.control-group {
  display: grid;
  grid-template-columns: repeat(3, minmax(130px, 1fr));
  gap: 0.8rem;
  flex: 1;
}

.control-select,
.search-input {
  min-height: 44px;
  border: 1px solid #c8ccda;
  border-radius: 12px;
  background: white;
  padding: 0 0.9rem;
  color: #5f667c;
  font-size: 0.95rem;
}

.search-input {
  width: min(320px, 100%);
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
  .search-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .control-group {
    grid-template-columns: 1fr;
  }

  .search-input {
    width: 100%;
  }

  .alert-row {
    grid-template-columns: 1fr;
  }
}
</style>
