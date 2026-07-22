<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import * as pdfjsLib from 'pdfjs-dist'
import pdfWorkerSrc from 'pdfjs-dist/build/pdf.worker.min.mjs?url'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import IconSubirArchivo from '@/components/icons/IconsProyect/subirArchivo.svg'
import { getCurrentUserIdFromSession } from '@/composables/useAppSession'
import { supabase } from '../../../utils/supabase'

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorkerSrc

const route = useRoute()
const mode = computed(() => {
  if (route.path.endsWith('/subir')) return 'subir'
  if (route.path.endsWith('/subarchivos')) return 'subarchivos'
  if (route.path.endsWith('/procesar')) return 'procesar'
  if (route.path.endsWith('/buscar')) return 'buscar'
  return 'principal'
})

const searchProjects = ref([])
const caoRecords = ref([])

const selectedAnio = ref('')
const selectedLugar = ref('')
const selectedEstado = ref('')
const searchText = ref('')

const yearsOptions = computed(() => [
  ...new Set(searchProjects.value.map((project) => project.year)),
])
const lugarOptions = computed(() => [
  ...new Set(searchProjects.value.map((project) => project.place)),
])

const filteredProjects = computed(() => {
  return searchProjects.value.filter((project) => {
    const matchesAnio = !selectedAnio.value || project.year === selectedAnio.value
    const matchesLugar = !selectedLugar.value || project.place === selectedLugar.value
    const projectEstado = project.is_processed ? 'procesado' : 'no-procesado'
    const matchesEstado = !selectedEstado.value || projectEstado === selectedEstado.value
    const query = searchText.value.trim().toLowerCase()
    const matchesSearch =
      !query ||
      project.title.toLowerCase().includes(query) ||
      project.file_type.toLowerCase().includes(query) ||
      project.local_directory.toLowerCase().includes(query)

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

const loadProjectFiles = async () => {
  try {
    const { data, error } = await supabase
      .from('project_files')
      .select(
        'id, title, place, year, file_type, is_processed, local_directory, local_file_name, file_url, preview_image_url, cao_directory, featured_directory, fixed_directory, created_at',
      )
      .order('created_at', { ascending: false })

    if (error) throw error

    const { data: caoData, error: caoError } = await supabase
      .from('cao_files')
      .select(
        'id, project_id, title, cao_code, place, year, local_directory, local_file_name, is_processed, created_at',
      )
      .order('created_at', { ascending: false })

    if (caoError) throw caoError
    caoRecords.value = caoData || []

    const mappedCaoRows = (caoData || []).map((item) => ({
      id: item.id,
      title: item.title,
      place: item.place,
      year: item.year,
      file_type: 'CAO',
      is_processed: item.is_processed,
      local_directory: item.local_directory,
      local_file_name: item.local_file_name,
      parent_project_id: item.project_id,
      cao_code: item.cao_code,
      created_at: item.created_at,
    }))

    searchProjects.value = [...(data || []), ...mappedCaoRows].sort(
      (left, right) => new Date(right.created_at) - new Date(left.created_at),
    )
    resetPage()
  } catch (error) {
    uploadError.value =
      error?.message || 'No se pudieron cargar los proyectos desde la base de datos.'
  }
}

const fileInputRef = ref(null)
const selectedPdfFile = ref(null)
const selectedUploadFiles = ref([])
const selectedPdfName = ref('')
const previewImageUrl = ref('')
const uploadMessage = ref('')
const uploadError = ref('')
const uploading = ref(false)
const isDragOver = ref(false)

const DIRECTORY_DB_NAME = 'sicepi-local-directory'
const DIRECTORY_STORE_NAME = 'handles'
const DIRECTORY_HANDLE_KEY = 'infra-root'
const INFRASTRUCTURE_ROOT_NAME = 'Proyectos de Infraestructura'
const CAO_FOLDER_NAME = 'CAO'
const FEATURED_FOLDER_NAME = 'Archivos Destacados'
const FIXED_FOLDER_NAME = 'Archivos Fijos'
const runtimeRootHandle = ref(null)

const uploadForm = reactive({
  title: '',
  place: '',
  year: '',
  fileType: 'Proyecto',
  cao: '',
  parentFile: '',
  parentProjectId: '',
})

const subUploadForm = reactive({
  projectId: '',
  titleQuery: '',
  title: '',
  subType: 'Archivos Fijos',
})

const showTitleSuggestions = ref(false)
const showParentProjectSuggestions = ref(false)

const baseProjectRows = computed(() =>
  searchProjects.value.filter((project) => project.file_type === 'Proyecto'),
)

const caoProjectSuggestions = computed(() => {
  const query = uploadForm.parentFile.trim().toLowerCase()
  const projects = baseProjectRows.value.map((project) => ({
    ...project,
    caoCount: caoRecords.value.filter((item) => item.project_id === project.id).length,
  }))

  if (!query) return projects.slice(0, 10)
  return projects.filter((project) => project.title.toLowerCase().includes(query)).slice(0, 10)
})

const uniqueProjectsByTitle = computed(() => {
  const seen = new Set()
  const results = []

  for (const project of baseProjectRows.value) {
    const key = project.title?.toLowerCase() || ''
    if (!key || seen.has(key)) continue
    seen.add(key)
    results.push(project)
  }

  return results
})

const subTitleSuggestions = computed(() => {
  const query = subUploadForm.titleQuery.trim().toLowerCase()
  if (!query) return uniqueProjectsByTitle.value.slice(0, 10)

  return uniqueProjectsByTitle.value
    .filter((project) => project.title.toLowerCase().includes(query))
    .slice(0, 10)
})

const dropZoneTitle = computed(() =>
  mode.value === 'subarchivos' ? 'SUBIR SUBARCHIVO' : 'SUBIR ARCHIVO',
)
const dropZoneHint = computed(() =>
  mode.value === 'subarchivos'
    ? 'Click o arrastra uno o varios archivos aqui'
    : 'Click o arrastra un PDF aqui',
)
const fileInputAccept = computed(() => (mode.value === 'subarchivos' ? '' : 'application/pdf,.pdf'))

const isCaoSelected = computed(() => uploadForm.fileType === 'CAO')
const isCaoCodeEnabled = computed(() => isCaoSelected.value && !!uploadForm.parentProjectId)
const selectedPdfDisplayName = computed(() => {
  if (mode.value === 'subarchivos') {
    if (selectedUploadFiles.value.length === 0) return ''
    if (selectedUploadFiles.value.length === 1) return selectedUploadFiles.value[0].name
    return `${selectedUploadFiles.value.length} archivos seleccionados`
  }

  if (!selectedPdfFile.value) return ''
  const titleName = sanitizeFolderName(uploadForm.title)
  return titleName ? `${titleName}.pdf` : selectedPdfName.value
})

const resetConditionalFields = () => {
  if (!isCaoSelected.value) {
    uploadForm.cao = ''
    uploadForm.parentFile = ''
    uploadForm.parentProjectId = ''
    showParentProjectSuggestions.value = false
  }
}

const selectParentProject = (project) => {
  uploadForm.parentProjectId = project.id
  uploadForm.parentFile = project.title
  uploadForm.place = project.place || ''
  uploadForm.year = project.year || ''
  showParentProjectSuggestions.value = false
}

const onParentProjectInput = () => {
  uploadForm.parentProjectId = ''
  uploadForm.cao = ''
  showParentProjectSuggestions.value = true

  const exactMatch = baseProjectRows.value.find(
    (project) => project.title.toLowerCase() === uploadForm.parentFile.trim().toLowerCase(),
  )

  if (exactMatch) {
    selectParentProject(exactMatch)
  }
}

const onParentProjectBlur = () => {
  setTimeout(() => {
    showParentProjectSuggestions.value = false
  }, 120)
}

const applySelectedProjectToForm = (project) => {
  if (!project) return

  subUploadForm.projectId = project.id
  subUploadForm.title = project.title
  subUploadForm.titleQuery = project.title
  uploadForm.title = project.title
  uploadForm.place = project.place || ''
  uploadForm.year = project.year || ''
  uploadForm.fileType = project.file_type === 'CAO' ? 'CAO' : 'Proyecto'
  uploadForm.parentFile = subUploadForm.subType
}

const selectSubTitle = (project) => {
  applySelectedProjectToForm(project)
  showTitleSuggestions.value = false
}

const onSubTitleInput = () => {
  showTitleSuggestions.value = true
  subUploadForm.projectId = ''
  const exactMatch = uniqueProjectsByTitle.value.find(
    (project) => project.title.toLowerCase() === subUploadForm.titleQuery.trim().toLowerCase(),
  )

  if (exactMatch) {
    applySelectedProjectToForm(exactMatch)
  }
}

const onSubTitleBlur = () => {
  setTimeout(() => {
    showTitleSuggestions.value = false
  }, 120)
}

watch(
  () => subUploadForm.subType,
  (newValue) => {
    if (mode.value === 'subarchivos') {
      uploadForm.parentFile = newValue
    }
  },
)

const getDirectoryPath = (projectFolderName, subFolderName) => {
  const base = `E:\\Proyectos de Infraestructura\\${projectFolderName}`
  return subFolderName ? `${base}\\${subFolderName}` : base
}

const ensureProjectSubDirectories = async (projectDirectory, projectFolderName) => {
  await projectDirectory.getDirectoryHandle(CAO_FOLDER_NAME, { create: true })
  await projectDirectory.getDirectoryHandle(FEATURED_FOLDER_NAME, { create: true })
  await projectDirectory.getDirectoryHandle(FIXED_FOLDER_NAME, { create: true })

  return {
    localDirectory: getDirectoryPath(projectFolderName),
    caoDirectory: getDirectoryPath(projectFolderName, CAO_FOLDER_NAME),
    featuredDirectory: getDirectoryPath(projectFolderName, FEATURED_FOLDER_NAME),
    fixedDirectory: getDirectoryPath(projectFolderName, FIXED_FOLDER_NAME),
  }
}

const getSelectedProjectForSubUpload = () => {
  if (subUploadForm.projectId) {
    const byId = baseProjectRows.value.find(
      (project) => String(project.id) === subUploadForm.projectId,
    )
    if (byId) return byId
  }

  const query = subUploadForm.titleQuery.trim().toLowerCase()
  if (!query) return null
  return baseProjectRows.value.find((project) => project.title.toLowerCase() === query) || null
}

const getSelectedParentProject = () => {
  if (!uploadForm.parentProjectId) return null

  return (
    baseProjectRows.value.find(
      (project) => String(project.id) === String(uploadForm.parentProjectId),
    ) || null
  )
}

const resolveProjectFolderName = (project) => {
  const fromLocalDirectory = project?.local_directory?.split('\\').filter(Boolean).at(-1)

  return fromLocalDirectory || sanitizeFolderName(project?.title || uploadForm.title)
}

const resolveStoredSubDirectoryPath = (project, subFolderName, projectFolderName) => {
  if (subFolderName === FEATURED_FOLDER_NAME) {
    return project?.featured_directory || getDirectoryPath(projectFolderName, FEATURED_FOLDER_NAME)
  }

  if (subFolderName === FIXED_FOLDER_NAME) {
    return project?.fixed_directory || getDirectoryPath(projectFolderName, FIXED_FOLDER_NAME)
  }

  if (subFolderName === CAO_FOLDER_NAME) {
    return project?.cao_directory || getDirectoryPath(projectFolderName, CAO_FOLDER_NAME)
  }

  return getDirectoryPath(projectFolderName, subFolderName)
}

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

const clearSavedDirectoryHandle = async () => {
  const db = await openDirectoryDb()
  await new Promise((resolve, reject) => {
    const tx = db.transaction(DIRECTORY_STORE_NAME, 'readwrite')
    tx.objectStore(DIRECTORY_STORE_NAME).delete(DIRECTORY_HANDLE_KEY)
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

  try {
    return await pickedHandle.getDirectoryHandle(INFRASTRUCTURE_ROOT_NAME, { create: false })
  } catch {
    throw new Error(
      'Selecciona la carpeta E:\\Proyectos de Infraestructura o una carpeta que la contenga.',
    )
  }
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

  if (!(await hasReadWritePermission(rootHandle))) {
    throw new Error('No se otorgo permiso de escritura para E:\\Proyectos de Infraestructura.')
  }

  runtimeRootHandle.value = rootHandle
  await saveDirectoryHandle(rootHandle)
  return rootHandle
}

const isMissingPathError = (error) => {
  const message = String(error?.message || '').toLowerCase()
  return error?.name === 'NotFoundError' || message.includes('could not be found')
}

const resetDirectoryAccess = async () => {
  runtimeRootHandle.value = null
  await clearSavedDirectoryHandle()
}

const openPdfPicker = () => {
  fileInputRef.value?.click()
}

const setSelectedFiles = async (files) => {
  selectedPdfFile.value = null
  selectedUploadFiles.value = []
  selectedPdfName.value = ''
  previewImageUrl.value = ''
  uploadError.value = ''
  uploadMessage.value = ''

  const validFiles = Array.isArray(files) ? files.filter(Boolean) : []
  if (validFiles.length === 0) return

  if (mode.value === 'subarchivos') {
    selectedUploadFiles.value = validFiles
    selectedPdfFile.value = validFiles[0]
    selectedPdfName.value =
      validFiles.length === 1 ? validFiles[0].name : `${validFiles.length} archivos seleccionados`
    return
  }

  const [file] = validFiles

  const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
  if (!isPdf) {
    uploadError.value = 'Solo se permite archivo PDF.'
    return
  }

  selectedPdfFile.value = file
  selectedUploadFiles.value = [file]
  selectedPdfName.value = file.name

  try {
    previewImageUrl.value = await renderFirstPdfPage(file)
  } catch (error) {
    previewImageUrl.value = ''
    uploadError.value = 'No se pudo generar la previsualizacion del PDF.'
  }
}

const onPdfChange = async (event) => {
  const files = Array.from(event.target?.files || [])
  await setSelectedFiles(files)
}

const onDropZoneDragOver = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

const onDropZoneDragLeave = (event) => {
  event.preventDefault()
  isDragOver.value = false
}

const onDropZoneDrop = async (event) => {
  event.preventDefault()
  isDragOver.value = false
  const files = Array.from(event.dataTransfer?.files || [])
  await setSelectedFiles(files)
}

const renderFirstPdfPage = async (file) => {
  const buffer = await file.arrayBuffer()
  const loadingTask = pdfjsLib.getDocument({ data: buffer })
  const pdf = await loadingTask.promise
  const page = await pdf.getPage(1)
  const viewport = page.getViewport({ scale: 1.3 })

  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  canvas.width = viewport.width
  canvas.height = viewport.height

  await page.render({ canvasContext: context, viewport }).promise
  return canvas.toDataURL('image/png')
}

const uploadProjectFile = async () => {
  uploadError.value = ''
  uploadMessage.value = ''

  if (!uploadForm.title.trim()) {
    uploadError.value = 'Titulo requerido.'
    return
  }

  if (!uploadForm.place.trim()) {
    uploadError.value = 'Lugar requerido.'
    return
  }

  if (!uploadForm.year.trim()) {
    uploadError.value = 'Año requerido.'
    return
  }

  if (isCaoSelected.value && (!uploadForm.cao.trim() || !uploadForm.parentFile.trim())) {
    uploadError.value = 'Si eliges CAO, completa CAO y Archivo perteneciente.'
    return
  }

  if (selectedUploadFiles.value.length === 0) {
    uploadError.value =
      mode.value === 'subarchivos'
        ? 'Selecciona al menos un archivo antes de subir.'
        : 'Selecciona un PDF antes de subir.'
    return
  }

  if (typeof window.showDirectoryPicker !== 'function') {
    uploadError.value =
      'Tu navegador no permite guardar automaticamente en carpeta local. Usa Chrome/Edge.'
    return
  }

  uploading.value = true

  try {
    const saveFileIntoInfrastructureFolder = async () => {
      const baseDirectory = await getInfrastructureRootHandle()
      const selectedProject = mode.value === 'subarchivos' ? getSelectedProjectForSubUpload() : null
      const selectedParentProject = isCaoSelected.value ? getSelectedParentProject() : null

      if (mode.value === 'subarchivos' && !selectedProject) {
        throw new Error('Selecciona un titulo valido para subir el subarchivo.')
      }

      if (isCaoSelected.value && !selectedParentProject) {
        throw new Error('Selecciona un proyecto valido en Archivo perteneciente.')
      }

      const projectFolderName =
        mode.value === 'subarchivos'
          ? resolveProjectFolderName(selectedProject)
          : isCaoSelected.value
            ? resolveProjectFolderName(selectedParentProject)
            : sanitizeFolderName(uploadForm.title)

      const projectDirectory = await baseDirectory.getDirectoryHandle(projectFolderName, {
        create: true,
      })

      const directoryPaths = await ensureProjectSubDirectories(projectDirectory, projectFolderName)
      const caoBaseDirectoryPath = isCaoSelected.value
        ? resolveStoredSubDirectoryPath(selectedParentProject, CAO_FOLDER_NAME, projectFolderName)
        : directoryPaths.caoDirectory

      const targetSubFolderName = mode.value === 'subarchivos' ? subUploadForm.subType : null
      const caoFolderName = isCaoSelected.value ? sanitizeFolderName(uploadForm.title) : null
      const targetDirectory = targetSubFolderName
        ? await projectDirectory.getDirectoryHandle(targetSubFolderName, { create: true })
        : isCaoSelected.value
          ? await (
              await projectDirectory.getDirectoryHandle(CAO_FOLDER_NAME, { create: true })
            ).getDirectoryHandle(caoFolderName, { create: true })
          : projectDirectory

      const filesToSave =
        mode.value === 'subarchivos' ? selectedUploadFiles.value : [selectedUploadFiles.value[0]]

      const uploadedRows = []
      const uploadedCaoRows = []

      for (const file of filesToSave) {
        const fileNameByTitle =
          mode.value === 'subarchivos' ? file.name : `${sanitizeFolderName(uploadForm.title)}.pdf`
        const fileHandle = await targetDirectory.getFileHandle(fileNameByTitle, {
          create: true,
        })
        const writable = await fileHandle.createWritable()
        await writable.write(file)
        await writable.close()

        const previewForDb =
          mode.value === 'subarchivos'
            ? null
            : previewImageUrl.value || (await renderFirstPdfPage(file))

        if (mode.value === 'subarchivos') {
          continue
        }

        const localDirectory = isCaoSelected.value
          ? `${caoBaseDirectoryPath}\${caoFolderName}`
          : directoryPaths.localDirectory
        const currentUserId = getCurrentUserIdFromSession()

        if (isCaoSelected.value) {
          const { data, error } = await supabase
            .from('cao_files')
            .insert({
              project_id: uploadForm.parentProjectId,
              title: uploadForm.title.trim(),
              cao_code: uploadForm.cao.trim(),
              place: uploadForm.place.trim(),
              year: uploadForm.year.trim(),
              local_directory: localDirectory,
              local_file_name: fileNameByTitle,
              is_processed: false,
              uploaded_by: currentUserId,
            })
            .select(
              'id, project_id, title, cao_code, place, year, local_directory, local_file_name, is_processed, created_at',
            )
            .single()

          if (error) throw error
          if (data) uploadedCaoRows.push(data)
          continue
        }

        const { data, error } = await supabase
          .from('project_files')
          .insert({
            title: uploadForm.title.trim(),
            place: uploadForm.place.trim(),
            year: uploadForm.year.trim(),
            file_type: uploadForm.fileType,
            local_directory: localDirectory,
            local_file_name: fileNameByTitle,
            cao_directory: caoBaseDirectoryPath,
            featured_directory: directoryPaths.featuredDirectory,
            fixed_directory: directoryPaths.fixedDirectory,
            storage_path: null,
            file_url: null,
            preview_image_url: previewForDb,
            uploaded_by: currentUserId,
          })
          .select(
            'id, title, place, year, file_type, is_processed, local_directory, local_file_name, file_url, preview_image_url, cao_directory, featured_directory, fixed_directory, parent_file, created_at',
          )
          .single()

        if (error) throw error
        if (data) uploadedRows.push(data)
      }

      for (const row of uploadedRows.reverse()) {
        searchProjects.value.unshift(row)
      }

      for (const row of uploadedCaoRows.reverse()) {
        caoRecords.value.unshift(row)
        searchProjects.value.unshift({
          id: row.id,
          title: row.title,
          place: row.place,
          year: row.year,
          file_type: 'CAO',
          is_processed: row.is_processed,
          local_directory: row.local_directory,
          local_file_name: row.local_file_name,
          parent_project_id: row.project_id,
          cao_code: row.cao_code,
          created_at: row.created_at,
        })
      }
    }

    try {
      await saveFileIntoInfrastructureFolder()
    } catch (firstError) {
      if (!isMissingPathError(firstError)) throw firstError
      await resetDirectoryAccess()
      await saveFileIntoInfrastructureFolder()
    }

    uploadMessage.value =
      mode.value === 'subarchivos'
        ? `${selectedUploadFiles.value.length} archivo(s) subidos correctamente en la carpeta local ${subUploadForm.subType} del proyecto seleccionado.`
        : 'PDF subido correctamente. Se guardo en Proyectos de Infraestructura/<Proyecto> y se crearon CAO, Archivos Destacados y Archivos Fijos.'
  } catch (error) {
    uploadError.value = error?.message || 'No se pudo subir el PDF.'
  } finally {
    uploading.value = false
  }
}

onMounted(loadProjectFiles)
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
        :class="{ active: mode === 'subarchivos' }"
        to="/panel/procesamiento/subarchivos"
      >
        Subir SubArchivos
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
        <button
          class="more-btn"
          :class="project.is_processed ? 'is-processed' : 'is-not-processed'"
        >
          {{ project.is_processed ? 'Procesado' : 'No procesado' }}
        </button>
      </article>

      <div class="pagination-controls">
        <button class="page-arrow" :disabled="!canGoPrev" @click="goPrevPage">←</button>
        <span class="page-indicator">{{ currentPage }} / {{ totalPages }}</span>
        <button class="page-arrow" :disabled="!canGoNext" @click="goNextPage">→</button>
      </div>
    </div>

    <div v-else class="content-grid">
      <div
        class="drop-zone"
        :class="{ 'is-drag-over': isDragOver }"
        @click="openPdfPicker"
        @dragover="onDropZoneDragOver"
        @dragleave="onDropZoneDragLeave"
        @drop="onDropZoneDrop"
      >
        <img
          v-if="previewImageUrl"
          :src="previewImageUrl"
          alt="Previsualizacion PDF"
          class="pdf-preview"
        />
        <template v-else>
          <img :src="IconSubirArchivo" alt="Subir archivo" class="drop-icon" />
          <span>{{ dropZoneTitle }}</span>
          <small v-if="selectedPdfName" class="picked-name">{{ selectedPdfDisplayName }}</small>
          <small v-else class="picked-name">{{ dropZoneHint }}</small>
        </template>
        <input
          ref="fileInputRef"
          class="native-file-input"
          type="file"
          :accept="fileInputAccept"
          :multiple="mode === 'subarchivos'"
          @change="onPdfChange"
        />
      </div>
      <div v-if="mode === 'subarchivos'" class="form-grid">
        <label class="autocomplete-box">
          <span>BUSCAR TITULO</span>
          <input
            v-model="subUploadForm.titleQuery"
            placeholder="Escribe el inicio del titulo"
            @focus="showTitleSuggestions = true"
            @blur="onSubTitleBlur"
            @input="onSubTitleInput"
          />
          <div v-if="showTitleSuggestions" class="autocomplete-list">
            <button
              v-for="project in subTitleSuggestions"
              :key="project.id"
              type="button"
              class="autocomplete-item"
              @mousedown.prevent="selectSubTitle(project)"
            >
              {{ project.title }}
            </button>
            <p v-if="subTitleSuggestions.length === 0" class="autocomplete-empty">
              No se encontraron titulos
            </p>
          </div>
        </label>

        <label>
          <span>TITULO</span>
          <input v-model="uploadForm.title" placeholder="Selecciona un titulo" readonly />
        </label>

        <label>
          <span>TIPO DE SUBARCHIVO</span>
          <select v-model="subUploadForm.subType">
            <option value="Archivos Fijos">Archivos Fijos</option>
            <option value="Archivos Destacados">Archivos Destacados</option>
          </select>
        </label>

        <div class="two-cols">
          <label><span>LUGAR</span><input v-model="uploadForm.place" readonly /></label>
          <label><span>AÑO</span><input v-model="uploadForm.year" readonly /></label>
        </div>

        <button class="download" :disabled="uploading" @click="uploadProjectFile">
          {{ uploading ? 'Subiendo...' : 'Subir SubArchivo' }}
        </button>

        <p v-if="uploadMessage" class="upload-message success">{{ uploadMessage }}</p>
        <p v-if="uploadError" class="upload-message error">{{ uploadError }}</p>
      </div>

      <div v-else class="form-grid">
        <label>
          <span>TITULO</span>
          <input v-model="uploadForm.title" placeholder="proyecto de infraestructura" />
        </label>
        <div class="two-cols">
          <label><span>LUGAR</span><input v-model="uploadForm.place" placeholder="La paz" /></label>
          <label><span>AÑO</span><input v-model="uploadForm.year" placeholder="2019" /></label>
        </div>
        <div class="two-cols">
          <label>
            <span>ARCHIVO</span>
            <select v-model="uploadForm.fileType" @change="resetConditionalFields">
              <option value="Proyecto">Proyecto</option>
              <option value="CAO">CAO</option>
            </select>
          </label>
          <label>
            <span>CAO</span>
            <input
              v-model="uploadForm.cao"
              :disabled="!isCaoCodeEnabled"
              :class="{ 'is-disabled': !isCaoCodeEnabled }"
              placeholder="Codigo CAO"
            />
          </label>
        </div>
        <div class="bottom-row">
          <label class="autocomplete-box">
            <span>ARCHIVO PERTENECIENTE</span>
            <input
              v-model="uploadForm.parentFile"
              :disabled="!isCaoSelected"
              :class="{ 'is-disabled': !isCaoSelected }"
              placeholder="Escribe el titulo del proyecto"
              @focus="showParentProjectSuggestions = isCaoSelected"
              @blur="onParentProjectBlur"
              @input="onParentProjectInput"
            />
            <div v-if="isCaoSelected && showParentProjectSuggestions" class="autocomplete-list">
              <button
                v-for="project in caoProjectSuggestions"
                :key="project.id"
                type="button"
                class="autocomplete-item"
                @mousedown.prevent="selectParentProject(project)"
              >
                {{ project.title }}
                <span class="autocomplete-meta">
                  {{ project.caoCount > 0 ? `${project.caoCount} CAO` : 'Sin CAO' }}
                </span>
              </button>
              <p v-if="caoProjectSuggestions.length === 0" class="autocomplete-empty">
                No se encontraron proyectos
              </p>
            </div>
          </label>
          <button class="download" :disabled="uploading" @click="uploadProjectFile">
            {{ uploading ? 'Subiendo...' : 'Subir Archivos' }}
          </button>
        </div>

        <p v-if="uploadMessage" class="upload-message success">{{ uploadMessage }}</p>
        <p v-if="uploadError" class="upload-message error">{{ uploadError }}</p>
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
  grid-template-columns: repeat(4, 1fr);
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
  cursor: pointer;

  span {
    color: #7c6b5f;
    font-weight: 700;
    font-size: 3rem;
  }
}

.drop-zone.is-drag-over {
  border-color: #5468ff;
  box-shadow: inset 0 0 0 2px rgba(84, 104, 255, 0.2);
}

.picked-name {
  margin-top: 0.25rem;
  font-size: 0.88rem;
  color: #6f5e54;
}

.pdf-preview {
  width: min(100%, 420px);
  max-height: 340px;
  object-fit: contain;
  border-radius: 12px;
  border: 1px solid #d8cab6;
  background: #fff;
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

.autocomplete-box {
  position: relative;
}

.autocomplete-list {
  position: absolute;
  top: calc(100% + 0.25rem);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #cbd3eb;
  border-radius: 10px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.12);
  z-index: 20;
  max-height: 220px;
  overflow-y: auto;
}

.autocomplete-item {
  width: 100%;
  border: 0;
  background: transparent;
  text-align: left;
  padding: 0.65rem 0.75rem;
  font-size: 0.9rem;
  color: #384062;
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;

  &:hover {
    background: #f4f7ff;
  }
}

.autocomplete-meta {
  color: #7e87a8;
  font-size: 0.8rem;
  white-space: nowrap;
}

.autocomplete-empty {
  margin: 0;
  padding: 0.65rem 0.75rem;
  color: #8a91a8;
  font-size: 0.88rem;
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

  select {
    border: 1px solid #b9a4ff;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    background: white;
  }
}

.is-disabled {
  background: #f0f2f7 !important;
  color: #9da4b9;
  cursor: not-allowed;
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

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.native-file-input {
  display: none;
}

.upload-message {
  margin: 0;
  font-size: 0.9rem;
}

.upload-message.success {
  color: #1e7b37;
}

.upload-message.error {
  color: #b42323;
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
