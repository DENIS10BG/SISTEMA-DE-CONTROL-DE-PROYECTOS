<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import projectPreview from '../../assets/images/IngenieroProyetos.png'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconCertificados from '@/components/icons/IconsProyect/Certificados.svg'
import ArchivosFijos from '@/components/icons/IconsProyect/ArchivosFijos.svg'
import ArchivosDestacados from '@/components/icons/IconsProyect/ArchivosDestacados.svg'
import IconDescarga from '@/components/icons/IconsProyect/Descarga.svg'
import IconPreguntas from '@/components/icons/IconsProyect/Preguntas.svg'
import IconFiltro from '@/components/icons/IconsUser/FiltroUsuario.svg'
import IconFlechaIzquierda from '@/components/icons/IconsUser/FlechaIzquierda.svg'
import { supabase } from '../../../utils/supabase'

const lugares = [
  'La Paz',
  'Oruro',
  'Potosi',
  'Cochabamba',
  'Tarija',
  'Beni',
  'Santa Cruz',
  'Pando',
  'Chuquisaca',
]

const anios = Array.from({ length: 17 }, (_, index) => String(2026 - index))

const selectedLugar = ref('')
const selectedAnio = ref('')

const route = useRoute()
const router = useRouter()

const caoRecord = ref(null)
const parentProject = ref(null)
const siblingCaos = ref([])
const loading = ref(false)
const loadError = ref('')
const actionError = ref('')
const isDownloading = ref(false)

const DIRECTORY_DB_NAME = 'sicepi-local-directory'
const DIRECTORY_STORE_NAME = 'handles'
const DIRECTORY_HANDLE_KEY = 'infra-root'
const INFRASTRUCTURE_ROOT_NAME = 'Proyectos de Infraestructura'
const runtimeRootHandle = ref(null)

const certificatesOpen = ref(true)

const selectedCaoId = computed(() => {
  return String(route.params.id || '')
})

const caoTitle = computed(() => caoRecord.value?.title || 'CAO')
const caoCode = computed(() => caoRecord.value?.cao_code || 'Sin codigo')
const caoPlace = computed(() => caoRecord.value?.place || parentProject.value?.place || '-')
const caoYear = computed(() => caoRecord.value?.year || parentProject.value?.year || '-')
const caoFileName = computed(() => caoRecord.value?.local_file_name || 'Sin archivo')
const projectSummary = computed(() => parentProject.value?.title || 'Proyecto relacionado')
const certificateSummary = computed(() => {
  if (siblingCaos.value.length === 0) return 'Sin CAO registrados'
  return siblingCaos.value.map((item) => item.cao_code || item.title).join(', ')
})
const descriptionText = computed(() => {
  const lines = [
    `Proyecto: ${projectSummary.value}`,
    `CAO: ${caoCode.value}`,
    `Titulo: ${caoTitle.value}`,
    `Lugar: ${caoPlace.value}`,
    `Año: ${caoYear.value}`,
    `Ruta local: ${caoRecord.value?.local_directory || '-'}\\${caoFileName.value}`,
  ]

  return lines.join('\n')
})

const sanitizeFolderName = (value) =>
  (value || 'Proyecto')
    .trim()
    .replace(/[\\/:*?"<>|]/g, '_')
    .replace(/\s+/g, ' ')

const openDirectoryDb = () =>
  new Promise((resolve, reject) => {
    const request = indexedDB.open(DIRECTORY_DB_NAME, 1)

    request.onupgradeneeded = () => {
      const db = request.result
      if (!db.objectStoreNames.contains(DIRECTORY_STORE_NAME)) {
        db.createObjectStore(DIRECTORY_STORE_NAME)
      }
    }

    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error)
  })

const getSavedDirectoryHandle = async () => {
  const db = await openDirectoryDb()
  const handle = await new Promise((resolve, reject) => {
    const tx = db.transaction(DIRECTORY_STORE_NAME, 'readonly')
    const request = tx.objectStore(DIRECTORY_STORE_NAME).get(DIRECTORY_HANDLE_KEY)
    request.onsuccess = () => resolve(request.result || null)
    request.onerror = () => reject(request.error)
  })
  db.close()
  return handle
}

const saveDirectoryHandle = async (handle) => {
  const db = await openDirectoryDb()
  await new Promise((resolve, reject) => {
    const tx = db.transaction(DIRECTORY_STORE_NAME, 'readwrite')
    tx.objectStore(DIRECTORY_STORE_NAME).put(handle, DIRECTORY_HANDLE_KEY)
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
  db.close()
}

const hasReadWritePermission = async (handle, allowPrompt = true) => {
  if (!handle) return false

  const options = { mode: 'readwrite' }
  if ((await handle.queryPermission(options)) === 'granted') return true
  if (allowPrompt && (await handle.requestPermission(options)) === 'granted') return true
  return false
}

const resolveInfrastructureDirectory = async (pickedHandle) => {
  const pickedName = (pickedHandle?.name || '').toLowerCase()
  const targetName = INFRASTRUCTURE_ROOT_NAME.toLowerCase()

  if (pickedName === targetName) {
    return pickedHandle
  }

  return pickedHandle.getDirectoryHandle(INFRASTRUCTURE_ROOT_NAME, { create: false })
}

const getInfrastructureRootHandle = async () => {
  if (runtimeRootHandle.value && (await hasReadWritePermission(runtimeRootHandle.value, false))) {
    return runtimeRootHandle.value
  }

  const savedHandle = await getSavedDirectoryHandle()
  if (savedHandle && (await hasReadWritePermission(savedHandle))) {
    runtimeRootHandle.value = savedHandle
    return savedHandle
  }

  const pickedHandle = await window.showDirectoryPicker({ mode: 'readwrite', id: 'infra-root' })
  const rootHandle = await resolveInfrastructureDirectory(pickedHandle)
  runtimeRootHandle.value = rootHandle
  await saveDirectoryHandle(rootHandle)
  return rootHandle
}

const getProjectFolderName = () => {
  const localDirectory = parentProject.value?.local_directory || ''
  const segments = localDirectory.split('\\').filter(Boolean)
  return segments.at(-1) || sanitizeFolderName(parentProject.value?.title)
}

const getCaoFolderName = () => sanitizeFolderName(caoTitle.value)

const getLocalCaoFile = async () => {
  if (typeof window.showDirectoryPicker !== 'function') {
    throw new Error('Tu navegador no permite abrir archivos locales. Usa Chrome o Edge.')
  }

  const rootDirectory = await getInfrastructureRootHandle()
  const projectFolderName = getProjectFolderName()
  const projectDirectory = await rootDirectory.getDirectoryHandle(projectFolderName, {
    create: false,
  })
  const caoDirectory = await projectDirectory.getDirectoryHandle('CAO', { create: false })
  const targetDirectory = await caoDirectory.getDirectoryHandle(getCaoFolderName(), {
    create: false,
  })
  const fileHandle = await targetDirectory.getFileHandle(caoFileName.value, { create: false })
  return fileHandle.getFile()
}

const toggleCertificates = () => {
  certificatesOpen.value = !certificatesOpen.value
}

const openCaoPdf = () => {
  actionError.value = ''

  getLocalCaoFile()
    .then((file) => {
      const objectUrl = URL.createObjectURL(file)
      window.open(objectUrl, '_blank', 'noopener,noreferrer')
      setTimeout(() => URL.revokeObjectURL(objectUrl), 15000)
    })
    .catch((error) => {
      actionError.value = error?.message || 'No se pudo abrir el archivo local del CAO.'
    })
}

const downloadCaoPdf = async () => {
  actionError.value = ''
  isDownloading.value = true

  try {
    const file = await getLocalCaoFile()
    const objectUrl = URL.createObjectURL(file)
    const anchor = document.createElement('a')
    anchor.href = objectUrl
    anchor.download = caoFileName.value
    document.body.appendChild(anchor)
    anchor.click()
    anchor.remove()
    URL.revokeObjectURL(objectUrl)
  } catch (error) {
    actionError.value = error?.message || 'No se pudo descargar el archivo local del CAO.'
  } finally {
    isDownloading.value = false
  }
}

const goToAssistant = () => {
  router.push('/panel/asistente')
}

const loadCaoDetail = async () => {
  loading.value = true
  loadError.value = ''
  actionError.value = ''
  caoRecord.value = null
  parentProject.value = null
  siblingCaos.value = []

  try {
    const { data: caoData, error: caoError } = await supabase
      .from('cao_files')
      .select('id, project_id, title, cao_code, place, year, local_directory, local_file_name')
      .eq('id', selectedCaoId.value)
      .single()

    if (caoError) throw caoError
    caoRecord.value = caoData

    const { data: projectData, error: projectError } = await supabase
      .from('project_files')
      .select(
        'id, title, place, year, local_directory, featured_directory, fixed_directory, cao_directory',
      )
      .eq('id', caoData.project_id)
      .single()

    if (projectError) throw projectError
    parentProject.value = projectData

    const { data: siblingsData, error: siblingsError } = await supabase
      .from('cao_files')
      .select('id, title, cao_code')
      .eq('project_id', caoData.project_id)
      .order('created_at', { ascending: true })

    if (siblingsError) throw siblingsError
    siblingCaos.value = siblingsData || []

    selectedLugar.value = caoData.place || projectData.place || ''
    selectedAnio.value = caoData.year || projectData.year || ''
  } catch (error) {
    loadError.value = error?.message || 'No se pudo cargar el detalle del CAO.'
  } finally {
    loading.value = false
  }
}

onMounted(loadCaoDetail)
watch(() => route.params.id, loadCaoDetail)
</script>

<template>
  <section class="detail-page">
    <div class="detail-head">
      <h1>PROYECTOS</h1>
      <div class="search-shell">
        <span class="search-icon" aria-hidden="true"></span>
        <input class="search" placeholder="Search for anything..." />
      </div>
      <div class="filters">
        <div class="chip select-chip">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <select v-model="selectedLugar" class="chip-select" aria-label="Filtrar por lugar">
            <option value="">Lugar</option>
            <option v-for="lugar in lugares" :key="lugar" :value="lugar">{{ lugar }}</option>
          </select>
          <span class="chevron" aria-hidden="true"></span>
        </div>
        <div class="chip select-chip">
          <img :src="IconFiltro" alt="" aria-hidden="true" />
          <select v-model="selectedAnio" class="chip-select" aria-label="Filtrar por año">
            <option value="">Año</option>
            <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
          </select>
          <span class="chevron" aria-hidden="true"></span>
        </div>
      </div>
    </div>

    <article class="project-summary">
      <div class="project-hero">
        <div class="folder">
          <img :src="IconCarpeta" alt="Carpeta del proyecto" />
        </div>
        <div class="project-text">
          <p class="label">CAO</p>
          <strong>{{ caoTitle }}</strong>
        </div>
        <div>
          <p class="label blue">Lugar</p>
          <strong>{{ caoPlace }}</strong>
        </div>
        <div>
          <p class="label blue">CAO</p>
          <strong>{{ caoCode }}</strong>
        </div>
        <div>
          <p class="label blue">Año</p>
          <strong>{{ caoYear }}</strong>
        </div>
        <RouterLink
          class="details-btn"
          :to="{ path: '/panel/proyectos/detalle', query: { id: parentProject?.id } }"
          aria-label="Volver al proyecto"
        >
          <img :src="IconFlechaIzquierda" alt="" aria-hidden="true" />
        </RouterLink>
      </div>

      <h2>{{ caoTitle }}</h2>

      <p v-if="loading" class="helper-text">Cargando detalle del CAO...</p>
      <p v-if="loadError" class="helper-text error">{{ loadError }}</p>

      <div class="detail-grid">
        <div class="preview-card">
          <span class="tag">CAO</span>
          <img class="mock-image" :src="projectPreview" alt="Documento del proyecto" />
        </div>

        <div class="center-stack">
          <div class="description-card">
            <h3>Descripción</h3>
            <p>{{ descriptionText }}</p>
          </div>

          <div class="action-row">
            <button class="action-box pink" @click="openCaoPdf">
              <span class="action-title">Ver</span>
              <span class="action-icon">
                <img :src="IconCarpeta" alt="Ver proyecto" />
              </span>
              <small>Ve el proyecto Completo</small>
            </button>
            <button class="action-box yellow" :disabled="isDownloading" @click="downloadCaoPdf">
              <span class="action-title">{{ isDownloading ? 'Descargando...' : 'Descargar' }}</span>
              <span class="action-icon">
                <img :src="IconDescarga" alt="Descargar proyecto" />
              </span>
              <small>Descarga el Proyecto</small>
            </button>
            <button class="action-box green" @click="goToAssistant">
              <span class="action-title">Agente</span>
              <span class="action-icon">
                <img :src="IconPreguntas" alt="Agente de preguntas" />
              </span>
              <small>Agente de Preguntas</small>
            </button>
          </div>

          <p v-if="actionError" class="helper-text error">{{ actionError }}</p>
        </div>

        <div class="side-stack">
          <div class="certificate-panel">
            <div class="certificate-root">
              <button class="side-card side-card-expand" @click="toggleCertificates">
                <span class="side-icon">
                  <img :src="IconCertificados" alt="Certificados de obras" />
                </span>
                <span class="side-card-content">
                  <span class="side-card-title">Certificados de Avance de Obras</span>
                  <span class="side-card-sub">{{ certificateSummary }}</span>
                </span>
                <span class="side-card-arrow open" aria-hidden="true"></span>
              </button>

              <button class="side-card side-card-plain">
                <span class="side-icon">
                  <img :src="ArchivosDestacados" alt="Archivos Destacados" />
                </span>
                <span class="side-card-content">
                  <span class="side-card-title">Archivos Destacados</span>
                </span>
              </button>

              <button class="side-card side-card-plain">
                <span class="side-icon">
                  <img :src="ArchivosFijos" alt="Archivos Fijos" />
                </span>
                <span class="side-card-content">
                  <span class="side-card-title">Archivos Fijos</span>
                </span>
              </button>
            </div>

            <div v-if="certificatesOpen" class="certificate-overlay">
              <div class="certificate-back certificate-back-root">
                <span>Certificados de Avances de Obras</span>
              </div>

              <div class="certificate-scroll certificate-list">
                <p v-if="siblingCaos.length === 0" class="helper-text">No hay CAO registrados.</p>
                <RouterLink
                  v-for="item in siblingCaos"
                  :key="item.id"
                  :to="`/panel/proyectos/cao/${item.id}`"
                  class="certificate-line certificate-link"
                  :class="{ active: item.id === selectedCaoId }"
                >
                  <span class="certificate-folder">
                    <img :src="IconCarpeta" alt="Carpeta" />
                  </span>
                  <span class="certificate-text">{{ item.cao_code || item.title }}</span>
                </RouterLink>
              </div>
            </div>
          </div>
          <div class="year-box">
            <span>{{ caoYear }}</span>
            <span>{{ String(caoPlace).toUpperCase() }}</span>
          </div>
        </div>
      </div>
    </article>
  </section>
</template>

<style scoped lang="scss">
.detail-page {
  min-height: 100%;
  padding: 1.25rem 1.25rem 1rem;
  background: #eef1f6;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.detail-head {
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
.chip,
.details-btn {
  border: 1px solid #c8ccda;
  border-radius: 12px;
  background: white;
}

.search-shell {
  min-height: 48px;
  width: 100%;
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

.chip {
  min-width: 176px;
  min-height: 48px;
  color: #6d7285;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.65rem;
  padding: 0 0.9rem;
  box-shadow: 0 6px 18px rgba(35, 53, 87, 0.05);
}

.chip img {
  width: 16px;
  height: 16px;
  object-fit: contain;
  opacity: 0.8;
}

.select-chip {
  position: relative;
}

.chip-select {
  appearance: none;
  border: 0;
  background: transparent;
  color: #6d7285;
  font-size: 0.95rem;
  width: 100%;
  min-width: 0;
  outline: none;
  padding-right: 0.9rem;
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

.project-summary {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  flex: 1;
  min-height: 0;
}

.project-hero {
  display: grid;
  grid-template-columns: 48px minmax(0, 1.28fr) 0.56fr 0.68fr 0.38fr 54px;
  gap: 0.75rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.64rem 0.9rem;
  box-shadow: 0 12px 24px rgba(35, 53, 87, 0.08);
}

.label {
  margin: 0 0 0.18rem;
  color: #f1a0bb;
  font-size: 0.8rem;
  line-height: 1;
}

.label.blue {
  color: #7894d6;
}

.project-text strong {
  display: block;
  max-width: 250px;
  font-size: 0.89rem;
  line-height: 1.08;
  font-weight: 600;
  color: #222;
}

.folder {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #ffd98f;
  display: grid;
  place-items: center;

  img {
    width: 20px;
    height: 20px;
    object-fit: contain;
  }
}

.details-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  border-radius: 999px;
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  padding: 0;
  justify-self: end;

  img {
    width: 18px;
    height: 18px;
    object-fit: contain;
    filter: brightness(0) invert(1);
  }
}

h2 {
  margin: 0;
  font-size: clamp(2rem, 2.8vw, 3rem);
  color: #222;
  font-weight: 500;
  line-height: 1.05;
}

.helper-text {
  margin: 0;
  font-size: 0.92rem;
  color: #4f5a7b;
}

.helper-text.error {
  color: #b42323;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1.6fr;
  gap: 0.9rem;
  align-items: start;
  flex: 1;
  min-height: 0;
  align-items: stretch;
}

.center-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  align-items: flex-start;
}

.preview-card,
.description-card,
.side-card,
.year-box {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  span {
    font-weight: 700;
  }
}

.preview-card {
  padding: 0.8rem;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 0.65rem;
  align-items: start;
  height: 100%;
}

.tag {
  align-self: flex-start;
  background: #d7f1d9;
  color: #80bd7a;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
}

.mock-image {
  width: 100%;
  height: 100%;
  min-height: 198px;
  max-height: 320px;
  border-radius: 8px;
  object-fit: cover;
  background: linear-gradient(180deg, #d55a40 0%, #b23d2b 100%);
}

.description-card {
  padding: 0.9rem 1rem 1rem;
  flex: 1;
  width: 100%;
  align-self: flex-start;
}

.description-card h3 {
  margin: 0 0 0.45rem;
  color: #33345a;
  font-size: 1.05rem;
}

.description-card p {
  margin: 0;
  color: #6d7487;
  line-height: 1.45;
  font-size: 0.92rem;
  white-space: pre-line;
}

.action-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.7rem;
  width: 100%;
  align-self: flex-start;
}

.action-box {
  min-height: 10px;

  img {
    width: 24px;
    height: 24px;
    object-fit: contain;
    filter: brightness(0) invert(1);
  }
  font-weight: 700;
  border: 1.5px solid #3f3f4d;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 0.72rem 0.8rem;
  text-align: left;
  color: #31365f;

  &:disabled {
    opacity: 0.72;
    cursor: not-allowed;
  }
}

.pink {
  background: #ffd9e0;
}
.yellow {
  background: #fde8bf;
}
.green {
  background: #d8ffd9;
}

.action-title {
  font-size: 1.18rem;
  line-height: 1;
}

.action-icon {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: #ff6f8d;
  color: white;
  display: grid;
  place-items: center;
}

.yellow .action-icon {
  background: #ffba49;
}

.green .action-icon {
  background: #96e07d;
}

.action-box small {
  max-width: 7rem;
  color: #4d5166;
  font-weight: 600;
  font-size: 0.8rem;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  height: 100%;
}

.certificate-panel {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  position: relative;
}

.certificate-root {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.side-card-content {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
  flex: 1;
}

.side-card-title {
  font-size: 1rem;
  line-height: 1.1;
}

.side-card-sub {
  font-size: 0.8rem;
  font-weight: 600;
  color: #8a91ad;
}

.side-card-expand {
  width: 100%;
}

.side-card-plain {
  width: 100%;
}

.side-card,
.year-box {
  min-height: 75px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  font-weight: 800;
  padding: 0.65rem 0.85rem;
  border: 0;
  color: #33345a;
}

.side-card {
  gap: 0.8rem;
  font-size: 1rem;
  justify-content: flex-start;
  text-align: left;
}

.side-card-expand {
  padding-right: 0.7rem;
}

.side-card-arrow {
  width: 8px;
  height: 8px;
  border-right: 2px solid #8d93a8;
  border-bottom: 2px solid #8d93a8;
  transform: rotate(45deg);
  flex: 0 0 auto;
  margin-left: auto;
}

.side-card-arrow.open {
  transform: rotate(225deg);
  margin-top: 4px;
}

.side-card-arrow.left {
  transform: rotate(225deg);
  margin-left: 0;
  margin-right: 0.2rem;
}

.side-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background: #ffd7e1;
  color: #f48bb1;
  display: grid;
  place-items: center;
  flex: 0 0 auto;

  img {
    width: 25px;
    height: 25px;
    object-fit: contain;
  }
}
.certificate-overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.6rem;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.certificate-back-root {
  margin-bottom: 0.8rem;
}

.certificate-back {
  width: 100%;
  min-height: 54px;
  border: 0;
  border-radius: 14px;
  background: #f6f8fc;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.65rem 0.75rem;
  text-align: left;
  color: #33345a;
  font-weight: 800;
  margin-bottom: 0.6rem;
}

.certificate-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.certificate-detail {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  min-height: 0;
  flex: 1;
}

.certificate-detail-title {
  font-size: 1rem;
  font-weight: 800;
  color: #33345a;
}

.certificate-detail-sub {
  font-size: 0.8rem;
  color: #8a91ad;
  font-weight: 600;
}

.certificate-scroll {
  margin-top: 0.35rem;
  max-height: 100%;
  overflow-y: auto;
  padding-right: 0.25rem;
}

.certificate-line {
  min-height: 42px;
  border-radius: 12px;
  background: #fff7fa;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.55rem 0.75rem;
  margin-bottom: 0;
  color: #33345a;
  font-weight: 600;
  border: 0;
  width: 100%;
  text-align: left;
}

.certificate-link {
  text-decoration: none;
}

.certificate-line.active {
  background: #ffeef5;
  outline: 1px solid #f4d9e5;
}

.certificate-line.detail-line {
  margin-bottom: 0.45rem;
}

.certificate-folder {
  width: 28px;
  height: 28px;
  border-radius: 9px;
  background: #ffd7e1;
  display: grid;
  place-items: center;
  flex: 0 0 auto;

  img {
    width: 16px;
    height: 16px;
    object-fit: contain;
  }
}

.certificate-text {
  flex: 1;
}

.side-icon.small {
  width: 44px;
  height: 44px;

  img {
    width: 18px;
    height: 18px;
    object-fit: contain;
  }
}

.year-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  font-size: 0.95rem;
  gap: 0;
  margin-top: auto;
}

@media (max-width: 1100px) {
  .detail-grid,
  .project-hero,
  .detail-head {
    grid-template-columns: 1fr;
  }

  .search {
    max-width: none;
    justify-self: stretch;
  }

  .project-text strong {
    max-width: none;
  }

  .detail-grid,
  .center-stack,
  .side-stack,
  .preview-card {
    height: auto;
    min-height: 0;
  }

  .mock-image {
    height: 198px;
    max-height: none;
  }

  .description-card {
    width: 100%;
  }

  .action-row {
    width: 100%;
  }

  .certificate-dropdown {
    max-height: none;
  }
}

@media (max-width: 900px) {
  .action-row {
    grid-template-columns: 1fr;
  }

  .side-stack {
    order: 3;
  }

  .filters {
    flex-direction: column;
  }

  h2 {
    font-size: 2rem;
  }
}
</style>
