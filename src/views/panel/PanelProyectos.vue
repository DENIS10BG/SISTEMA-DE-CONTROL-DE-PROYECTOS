<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconFiltro from '@/components/icons/IconsUser/FiltroUsuario.svg'
import IconFlechaIzquierda from '@/components/icons/IconsUser/FlechaIzquierda.svg'
import IconFlechaDerecha from '@/components/icons/IconsUser/FlechaDerecha.svg'
import { supabase } from '../../../utils/supabase'

const projects = ref([])

const selectedLugar = ref('')
const selectedAnio = ref('')
const searchText = ref('')
const loadError = ref('')

const lugares = computed(() => [...new Set(projects.value.map((project) => project.place))])
const anios = computed(() => [...new Set(projects.value.map((project) => project.year))])

const filteredProjects = computed(() => {
  const query = searchText.value.trim().toLowerCase()
  return projects.value.filter((project) => {
    const byLugar = !selectedLugar.value || project.place === selectedLugar.value
    const byAnio = !selectedAnio.value || project.year === selectedAnio.value
    const byQuery =
      !query ||
      project.title.toLowerCase().includes(query) ||
      project.file_type.toLowerCase().includes(query) ||
      project.local_directory.toLowerCase().includes(query)

    return byLugar && byAnio && byQuery
  })
})

const rowsPerPage = 6
const currentPage = ref(1)

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

watch([selectedLugar, selectedAnio, searchText], () => {
  currentPage.value = 1
})

const loadProjects = async () => {
  loadError.value = ''
  try {
    const { data, error } = await supabase
      .from('project_files')
      .select('id, title, place, year, file_type, local_directory, created_at')
      .order('created_at', { ascending: false })

    if (error) throw error
    projects.value = data || []
  } catch (error) {
    loadError.value = error?.message || 'No se pudieron cargar los proyectos de la base de datos.'
  }
}

onMounted(loadProjects)
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>PROYECTOS</h1>
      <div class="search-shell">
        <span class="search-icon" aria-hidden="true"></span>
        <input v-model="searchText" class="search" placeholder="Search for anything..." />
      </div>
      <div class="filters">
        <div class="action-btn select-btn">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <select v-model="selectedLugar" class="filter-select" aria-label="Filtrar por lugar">
            <option value="">Lugar</option>
            <option v-for="lugar in lugares" :key="lugar" :value="lugar">{{ lugar }}</option>
          </select>
          <span class="chevron" aria-hidden="true"></span>
        </div>
        <div class="action-btn select-btn">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <select v-model="selectedAnio" class="filter-select" aria-label="Filtrar por año">
            <option value="">Año</option>
            <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
          </select>
          <span class="chevron" aria-hidden="true"></span>
        </div>
      </div>
    </div>

    <div class="list-card">
      <article v-for="project in paginatedProjects" :key="project.id" class="project-row">
        <div class="folder">
          <img :src="IconCarpeta" alt="Carpeta" />
        </div>
        <div class="project-text">
          <p class="label">Proyecto</p>
          <strong>{{ project.title }}</strong>
        </div>
        <div>
          <p class="label">Lugar</p>
          <strong>{{ project.place }}</strong>
        </div>
        <div>
          <p class="label">Archivo</p>
          <strong>{{ project.file_type }}</strong>
        </div>
        <div>
          <p class="label">Año</p>
          <strong>{{ project.year }}</strong>
        </div>
        <RouterLink
          class="more-btn"
          :to="{
            path: '/panel/proyectos/detalle',
            query: {
              id: project.id,
              title: project.title,
              place: project.place,
              year: project.year,
              fileType: project.file_type,
            },
          }"
          >Mas detalles</RouterLink
        >
      </article>

      <p v-if="loadError" class="load-error">{{ loadError }}</p>
    </div>

    <div class="pagination-controls">
      <button class="page-arrow" :disabled="!canGoPrev" @click="goPrevPage">
        <img :src="IconFlechaIzquierda" alt="Página anterior" />
      </button>
      <button class="page-arrow" :disabled="!canGoNext" @click="goNextPage">
        <img :src="IconFlechaDerecha" alt="Página siguiente" />
      </button>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1.5rem 1.4rem 1.1rem;
}

.section-head {
  display: grid;
  grid-template-columns: auto minmax(320px, 1fr) auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #35457f;
  font-size: clamp(2rem, 2.8vw, 2.8rem);
  font-weight: 800;
  line-height: 1;
}

.search-shell,
.action-btn,
.more-btn {
  border: 1px solid #c8ccda;
  border-radius: 12px;
  background: white;
}

.search-shell {
  min-height: 48px;
  display: flex;
  align-items: center;
  gap: 0.95rem;
  padding: 0 0.9rem 0 1rem;
  border-color: transparent;
  box-shadow: 0 6px 18px rgba(35, 53, 87, 0.05);
}

.search-icon {
  width: 18px;
  height: 18px;
  border: 2px solid #96a0b9;
  border-radius: 50%;
  flex: 0 0 auto;
  position: relative;
}

.search-icon::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 2px;
  background: #96a0b9;
  border-radius: 999px;
  right: -7px;
  bottom: -3px;
  transform: rotate(45deg);
  transform-origin: center;
}

.search {
  border: 0;
  outline: 0;
  width: 100%;
  min-width: 0;
  color: #4c5163;
  font-size: 0.95rem;
}

.filters {
  display: flex;
  gap: 0.85rem;
}

.action-btn {
  min-width: 176px;
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  padding: 0 0.9rem;
  color: #7a7f91;
  font-size: 0.95rem;
  box-shadow: 0 6px 18px rgba(35, 53, 87, 0.05);
}

.select-btn {
  position: relative;
}

.filter-select {
  appearance: none;
  border: 0;
  background: transparent;
  color: #7a7f91;
  font-size: 0.95rem;
  width: 100%;
  min-width: 0;
  outline: none;
  padding-right: 0.9rem;
}

.action-btn img {
  width: 16px;
  height: 16px;
  object-fit: contain;
  opacity: 0.8;
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

.list-card {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.load-error {
  margin: 0.2rem 0 0;
  color: #b42323;
  font-size: 0.9rem;
}

.pagination-controls {
  margin-top: 0.55rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.45rem;
}

.page-arrow {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid #c8ccda;
  background: white;
  display: grid;
  place-items: center;

  img {
    width: 14px;
    height: 14px;
    object-fit: contain;
  }

  &:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
}

.project-row {
  display: grid;
  grid-template-columns: 56px minmax(0, 1.2fr) 0.52fr 0.68fr 0.38fr 138px;
  gap: 0.85rem;
  align-items: center;
  background: white;
  border-radius: 20px;
  padding: 0.7rem 1rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

.label {
  margin: 0 0 0.18rem;
  color: #f1a0bb;
  font-size: 0.8rem;
  line-height: 1;
}

.project-text strong {
  display: block;
  max-width: 265px;
  font-size: 0.92rem;
  line-height: 1.1;
  font-weight: 600;
  color: #222;
}

.folder {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: #ffd97a;
  display: grid;
  place-items: center;

  img {
    width: 22px;
    height: 22px;
    object-fit: contain;
  }
}

.more-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  border-radius: 999px;
  padding-inline: 1.2rem;
  font-size: 0.95rem;
  font-weight: 700;
}

@media (max-width: 900px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .project-row {
    grid-template-columns: 1fr;
  }

  .project-text strong {
    max-width: none;
  }
}
</style>
