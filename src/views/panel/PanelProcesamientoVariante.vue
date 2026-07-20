<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconSubirArchivo from '@/components/icons/IconsProyect/subirArchivo.svg'

const route = useRoute()
const mode = computed(() => {
  if (route.path.endsWith('/subir')) return 'subir'
  if (route.path.endsWith('/procesar')) return 'procesar'
  if (route.path.endsWith('/buscar')) return 'buscar'
  return 'principal'
})

const searchProjects = [
  {
    id: 1,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Oruro',
    Archivo: 'Proyecto',
    codigo: '789945661-0',
    anio: '2019',
    processed: true,
  },
  {
    id: 2,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Oruro',
    codigo: '789945661-0',
    Archivo: 'Proyecto',
    anio: '2019',
    processed: false,
  },
  {
    id: 3,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Oruro',
    codigo: '789945661-0',
    Archivo: 'Proyecto',
    anio: '2019',
    processed: true,
  },
  {
    id: 4,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Oruro',
    codigo: '789945661-0',
    Archivo: 'Proyecto',
    anio: '2019',
    processed: false,
  },
  {
    id: 5,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'La Paz',
    codigo: '789945661-1',
    Archivo: 'Proyecto',
    anio: '2020',
    processed: true,
  },
  {
    id: 6,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Cochabamba',
    codigo: '789945661-2',
    Archivo: 'Proyecto',
    anio: '2021',
    processed: false,
  },
  {
    id: 7,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Tarija',
    codigo: '789945661-3',
    Archivo: 'Proyecto',
    anio: '2022',
    processed: true,
  },
  {
    id: 8,
    proyecto: 'Construccion Tinglado RSAT-1 BUCH-ORURO',
    lugar: 'Santa Cruz',
    codigo: '789945661-4',
    Archivo: 'Proyecto',
    anio: '2023',
    processed: false,
  },
]

const selectedAnio = ref('')
const selectedLugar = ref('')
const selectedEstado = ref('')
const searchText = ref('')

const yearsOptions = computed(() => [...new Set(searchProjects.map((project) => project.anio))])
const lugarOptions = computed(() => [...new Set(searchProjects.map((project) => project.lugar))])

const filteredProjects = computed(() => {
  return searchProjects.filter((project) => {
    const matchesAnio = !selectedAnio.value || project.anio === selectedAnio.value
    const matchesLugar = !selectedLugar.value || project.lugar === selectedLugar.value
    const projectEstado = project.processed ? 'procesado' : 'no-procesado'
    const matchesEstado = !selectedEstado.value || projectEstado === selectedEstado.value
    const query = searchText.value.trim().toLowerCase()
    const matchesSearch =
      !query ||
      project.proyecto.toLowerCase().includes(query) ||
      project.codigo.toLowerCase().includes(query) ||
      project.Archivo.toLowerCase().includes(query)

    return matchesAnio && matchesLugar && matchesEstado && matchesSearch
  })
})

const currentPage = ref(1)
const rowsPerPage = 4

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredProjects.value.length / rowsPerPage)),
)

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage
  return filteredProjects.value.slice(start, start + rowsPerPage)
})

const canGoPrev = computed(() => currentPage.value > 1)
const canGoNext = computed(() => currentPage.value < totalPages.value)

const goPrevPage = () => {
  if (canGoPrev.value) currentPage.value -= 1
}

const goNextPage = () => {
  if (canGoNext.value) currentPage.value += 1
}

const resetPage = () => {
  currentPage.value = 1
}
</script>

<template>
  <section class="section-shell">
    <h1>PROCESAMIENTO</h1>

    <div class="actions-row">
      <RouterLink
        class="mini-card"
        :class="{ active: mode === 'subir' }"
        to="/panel/procesamiento/subir"
      >
        SUBIR ARCHIVO
      </RouterLink>
      <RouterLink
        class="mini-card"
        :class="{ active: mode === 'procesar' }"
        to="/panel/procesamiento/procesar"
      >
        Procesar Archivo
      </RouterLink>
      <RouterLink
        class="mini-card"
        :class="{ active: mode === 'buscar' }"
        to="/panel/procesamiento/buscar"
      >
        Buscar Archivo
      </RouterLink>
    </div>

    <div v-if="mode === 'buscar'" class="search-controls">
      <div class="control-group">
        <select v-model="selectedAnio" class="control-select" @change="resetPage">
          <option value="">Año</option>
          <option v-for="anio in yearsOptions" :key="anio" :value="anio">{{ anio }}</option>
        </select>
        <select v-model="selectedLugar" class="control-select" @change="resetPage">
          <option value="">Lugar</option>
          <option v-for="lugar in lugarOptions" :key="lugar" :value="lugar">{{ lugar }}</option>
        </select>
        <select v-model="selectedEstado" class="control-select" @change="resetPage">
          <option value="">Estado</option>
          <option value="procesado">Procesado</option>
          <option value="no-procesado">No procesado</option>
        </select>
      </div>

      <input
        v-model="searchText"
        class="search-input"
        placeholder="Buscar archivo..."
        @input="resetPage"
      />
    </div>

    <div v-if="mode === 'buscar'" class="list-card">
      <article v-for="project in paginatedProjects" :key="project.id" class="project-row">
        <div class="folder">
          <img :src="IconCarpeta" alt="Carpeta" />
        </div>
        <div>
          <p class="label">Proyecto</p>
          <strong>{{ project.proyecto }}</strong>
        </div>
        <div>
          <p class="label">Lugar</p>
          <strong>{{ project.lugar }}</strong>
        </div>
        <div>
          <p class="label">Archivo</p>
          <strong>{{ project.Archivo }}</strong>
        </div>
        <div>
          <p class="label">Año</p>
          <strong>{{ project.anio }}</strong>
        </div>
        <button class="more-btn" :class="project.processed ? 'is-processed' : 'is-not-processed'">
          {{ project.processed ? 'Procesado' : 'No procesado' }}
        </button>
      </article>

      <div class="pagination-controls">
        <button class="page-arrow" :disabled="!canGoPrev" @click="goPrevPage">←</button>
        <span class="page-indicator">{{ currentPage }} / {{ totalPages }}</span>
        <button class="page-arrow" :disabled="!canGoNext" @click="goNextPage">→</button>
      </div>
    </div>

    <div v-else class="content-grid">
      <div class="drop-zone">
        <img :src="IconSubirArchivo" alt="Subir archivo" class="drop-icon" />
        <span>SUBIR ARCHIVO</span>
      </div>
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
  padding: 0.5rem 1.5rem 1rem;
}

h1 {
  margin: 0 0 0.4rem;
  color: #35457f;
  font-size: clamp(1rem, 2.5vw, 2.8rem);
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
  border-color: #b71c1c;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 1.5rem;
}

.search-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.9rem;
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

.pagination-controls {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.3rem;
}

.page-arrow {
  width: 34px;
  height: 34px;
  border: 1px solid #c8ccda;
  border-radius: 8px;
  background: white;
  font-size: 1rem;
  font-weight: 700;
  color: #566088;

  &:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
}

.page-indicator {
  color: #69739d;
  font-weight: 700;
  min-width: 58px;
  text-align: center;
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
  color: white;
  border-color: transparent;
  border: 0;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-weight: 700;
}

.more-btn.is-processed {
  background: #63d24d;
  width: 120px;
}

.more-btn.is-not-processed {
  background: #d33a3a;
}

.drop-zone {
  min-height: 370px;
  border: 2px dashed #7c6b5f;
  border-radius: 18px;
  background: #f0dfb2;
  display: grid;
  place-items: center;
  gap: 0rem;
  span {
    color: #7c6b5f;
    font-weight: 700;
    font-size: 3rem;
  }
}

.drop-icon {
  width: min(160px, 52vw);
  height: auto;
}

.note-card,
.form-grid {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

.note-card {
  min-height: 370px;
  display: grid;
  place-items: center;
  color: #6d7487;
  font-weight: 600;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;

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

@media (max-width: 900px) {
  .actions-row,
  .content-grid,
  .two-cols,
  .bottom-row {
    grid-template-columns: 1fr;
  }

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

  .project-row {
    grid-template-columns: 1fr;
  }
}
</style>
