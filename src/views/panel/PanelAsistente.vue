<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'

const assistants = [
  {
    id: 1,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Oruro',
    archivo: 'Proyecto',
    anio: '2019',
  },
  {
    id: 2,
    proyecto: 'Refaccion Hospital Municipal Norte',
    lugar: 'La Paz',
    archivo: 'CAO',
    anio: '2020',
  },
  {
    id: 3,
    proyecto: 'Mejoramiento Camino Vecinal Tramo B',
    lugar: 'Cochabamba',
    archivo: 'Proyecto',
    anio: '2021',
  },
  {
    id: 4,
    proyecto: 'Ampliacion Red de Alcantarillado Zona Sur',
    lugar: 'Tarija',
    archivo: 'CAO',
    anio: '2022',
  },
]

const searchText = ref('')
const selectedArchivo = ref('')
const selectedLugar = ref('')
const selectedAnio = ref('')

const archivoOptions = ['Proyecto', 'CAO']
const lugarOptions = computed(() => [...new Set(assistants.map((item) => item.lugar))])
const anioOptions = computed(() => [...new Set(assistants.map((item) => item.anio))])

const filteredAssistants = computed(() => {
  const query = searchText.value.trim().toLowerCase()

  return assistants.filter((item) => {
    const matchesArchivo = !selectedArchivo.value || item.archivo === selectedArchivo.value
    const matchesLugar = !selectedLugar.value || item.lugar === selectedLugar.value
    const matchesAnio = !selectedAnio.value || item.anio === selectedAnio.value
    const matchesSearch =
      !query ||
      item.proyecto.toLowerCase().includes(query) ||
      item.lugar.toLowerCase().includes(query) ||
      item.archivo.toLowerCase().includes(query) ||
      item.anio.includes(query)

    return matchesArchivo && matchesLugar && matchesAnio && matchesSearch
  })
})
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>ASISTENTE</h1>
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
      <article v-for="assistant in filteredAssistants" :key="assistant.id" class="project-row">
        <div class="folder"><img :src="IconCarpeta" alt="Carpeta" /></div>
        <div>
          <p class="label">Proyecto</p>
          <strong>{{ assistant.proyecto }}</strong>
        </div>
        <div>
          <p class="label">Lugar</p>
          <strong>{{ assistant.lugar }}</strong>
        </div>
        <div>
          <p class="label">Archivo</p>
          <strong>{{ assistant.archivo }}</strong>
        </div>
        <div>
          <p class="label">Año</p>
          <strong>{{ assistant.anio }}</strong>
        </div>
        <RouterLink class="more-btn" to="/panel/asistente/detalle">Mas detalles</RouterLink>
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

.search-input,
.control-select,
.more-btn {
  border: 1px solid #c8ccda;
  border-radius: 8px;
  background: white;
  padding: 0.75rem 1rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.search-input {
  width: 100%;
}

.control-group {
  display: grid;
  grid-template-columns: repeat(3, minmax(130px, 1fr));
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
}

@media (max-width: 900px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .control-group {
    grid-template-columns: 1fr;
  }

  .project-row {
    grid-template-columns: 1fr;
  }
}
</style>
