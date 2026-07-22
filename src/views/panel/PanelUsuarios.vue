<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { getCurrentUserId, listUsers, setUserState } from '../../composables/useUsersData'
import IconAnadirUsuario from '@/components/icons/IconsUser/AñadirUsuario.svg'
import IconBusqueda from '@/components/icons/IconsUser/Busqueda.svg'
import IconFiltroUsuario from '@/components/icons/IconsUser/FiltroUsuario.svg'
import IconFlechaAbajo from '@/components/icons/IconsUser/FlechaAbajo.svg'
import IconFlechaIzquierda from '@/components/icons/IconsUser/FlechaIzquierda.svg'
import IconFlechaDerecha from '@/components/icons/IconsUser/FlechaDerecha.svg'
import IconVerPerfilUsuario from '@/components/icons/IconsUser/VerPerfilUsuario.svg'
import IconEditarPerfilUsuario from '@/components/icons/IconsUser/EditarPerfilUsuario.svg'
import IconUsuarioActivo from '@/components/icons/IconsUser/UsuarioActivo.svg'
import IconUsuarioDesactivado from '@/components/icons/IconsUser/UsuarioDesactivado.svg'

const users = ref([])
const searchText = ref('')
const loading = ref(false)
const errorMessage = ref('')
const currentPage = ref(1)
const rowsPerPage = 7
const sortField = ref('nombres')
const sortDirection = ref('asc')

const loadUsers = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const currentUserId = await getCurrentUserId()
    users.value = await listUsers({ excludeUserId: currentUserId })
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo cargar la lista de usuarios.'
  } finally {
    loading.value = false
  }
}

const isActive = (row) => !!row.isActive

const getStateLabel = (row) => (isActive(row) ? 'Activo' : 'Desactivo')

const getStateIcon = (row) => (isActive(row) ? IconUsuarioActivo : IconUsuarioDesactivado)

const filteredRows = computed(() => {
  const term = searchText.value.trim().toLowerCase()
  if (!term) {
    return users.value
  }

  return users.value.filter((row) => {
    const bag =
      `${row.firstName} ${row.lastName} ${row.email} ${row.phone} ${row.roleLabel}`.toLowerCase()
    return bag.includes(term)
  })
})

const totalPages = computed(() => {
  const pages = Math.ceil(filteredRows.value.length / rowsPerPage)
  return Math.max(1, pages)
})

const sortedRows = computed(() => {
  const direction = sortDirection.value === 'asc' ? 1 : -1

  return [...filteredRows.value].sort((left, right) => {
    const leftValue =
      sortField.value === 'no'
        ? left.id
        : sortField.value === 'nombres'
          ? left.firstName
          : sortField.value === 'apellidos'
            ? left.lastName
            : sortField.value === 'telefono'
              ? left.phone
              : sortField.value === 'rol'
                ? left.roleLabel
                : getStateLabel(left)

    const rightValue =
      sortField.value === 'no'
        ? right.id
        : sortField.value === 'nombres'
          ? right.firstName
          : sortField.value === 'apellidos'
            ? right.lastName
            : sortField.value === 'telefono'
              ? right.phone
              : sortField.value === 'rol'
                ? right.roleLabel
                : getStateLabel(right)

    return String(leftValue).localeCompare(String(rightValue), 'es', { numeric: true }) * direction
  })
})

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage
  return sortedRows.value.slice(start, start + rowsPerPage)
})

const canGoPrevious = computed(() => currentPage.value > 1)
const canGoNext = computed(() => currentPage.value < totalPages.value)

const goPrevious = () => {
  if (!canGoPrevious.value) return
  currentPage.value -= 1
}

const goNext = () => {
  if (!canGoNext.value) return
  currentPage.value += 1
}

const setSort = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }

  currentPage.value = 1
}

const toRowNumber = (row) => {
  const fullIndex = sortedRows.value.findIndex((item) => item.id === row.id)
  return `${String(fullIndex + 1).padStart(2, '0')}.`
}

const toggleState = async (row) => {
  try {
    await setUserState(row.id, !row.isActive)
    row.isActive = !row.isActive
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo actualizar el estado del usuario.'
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <section class="section-shell">
    <div class="section-head">
      <h1>USUARIOS</h1>
      <RouterLink class="action-btn add" to="/panel/usuarios/nuevo">
        <img :src="IconAnadirUsuario" alt="Añadir usuario" />
        <span>Añadir Usuarios</span>
      </RouterLink>

      <div class="search-wrap">
        <img class="search-icon" :src="IconBusqueda" alt="Buscar" />
        <input v-model="searchText" class="search" placeholder="Buscar por nombre, correo o rol" />
      </div>

      <button class="action-btn filter" type="button">
        <img :src="IconFiltroUsuario" alt="Filtro" />
        <span>Filter</span>
        <img class="arrow-icon" :src="IconFlechaAbajo" alt="Expandir" />
      </button>
    </div>

    <div class="table-card">
      <p v-if="loading" class="table-message">Cargando usuarios...</p>
      <p v-if="errorMessage" class="table-error">{{ errorMessage }}</p>

      <table>
        <thead>
          <tr>
            <th>
              <button class="head-sort" type="button" @click="setSort('no')">
                <span>No</span>
                <img
                  :class="[
                    'sort-arrow',
                    {
                      active: sortField === 'no',
                      desc: sortField === 'no' && sortDirection === 'desc',
                    },
                  ]"
                  :src="IconFlechaAbajo"
                  alt="Ordenar No"
                />
              </button>
            </th>
            <th>
              <button class="head-sort" type="button" @click="setSort('nombres')">
                <span>Nombres</span>
                <img
                  :class="[
                    'sort-arrow',
                    {
                      active: sortField === 'nombres',
                      desc: sortField === 'nombres' && sortDirection === 'desc',
                    },
                  ]"
                  :src="IconFlechaAbajo"
                  alt="Ordenar nombres"
                />
              </button>
            </th>
            <th>
              <button class="head-sort" type="button" @click="setSort('apellidos')">
                <span>Apellidos</span>
                <img
                  :class="[
                    'sort-arrow',
                    {
                      active: sortField === 'apellidos',
                      desc: sortField === 'apellidos' && sortDirection === 'desc',
                    },
                  ]"
                  :src="IconFlechaAbajo"
                  alt="Ordenar apellidos"
                />
              </button>
            </th>
            <th>
              <button class="head-sort" type="button" @click="setSort('telefono')">
                <span>Teléfono</span>
                <img
                  :class="[
                    'sort-arrow',
                    {
                      active: sortField === 'telefono',
                      desc: sortField === 'telefono' && sortDirection === 'desc',
                    },
                  ]"
                  :src="IconFlechaAbajo"
                  alt="Ordenar teléfono"
                />
              </button>
            </th>
            <th>
              <button class="head-sort" type="button" @click="setSort('rol')">
                <span>Rol</span>
                <img
                  :class="[
                    'sort-arrow',
                    {
                      active: sortField === 'rol',
                      desc: sortField === 'rol' && sortDirection === 'desc',
                    },
                  ]"
                  :src="IconFlechaAbajo"
                  alt="Ordenar rol"
                />
              </button>
            </th>
            <th>
              <button class="head-sort" type="button" @click="setSort('estado')">
                <span>Estado</span>
                <img
                  :class="[
                    'sort-arrow',
                    {
                      active: sortField === 'estado',
                      desc: sortField === 'estado' && sortDirection === 'desc',
                    },
                  ]"
                  :src="IconFlechaAbajo"
                  alt="Ordenar estado"
                />
              </button>
            </th>
            <th>Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in paginatedRows" :key="row.id">
            <td>{{ toRowNumber(row) }}</td>
            <td>
              <div class="user-cell">
                <span class="user-name">{{ row.firstName }}</span>
              </div>
            </td>
            <td>{{ row.lastName }}</td>
            <td>{{ row.phone }}</td>
            <td>{{ row.roleLabel }}</td>
            <td>{{ getStateLabel(row) }}</td>
            <td>
              <div class="options">
                <RouterLink
                  class="opt view"
                  :to="{ path: '/panel/usuarios/ver', query: { uid: row.id } }"
                  aria-label="Ver usuario"
                >
                  <img :src="IconVerPerfilUsuario" alt="Ver usuario" />
                </RouterLink>
                <RouterLink
                  class="opt edit"
                  :to="{ path: '/panel/usuarios/editar', query: { uid: row.id } }"
                  aria-label="Editar usuario"
                >
                  <img :src="IconEditarPerfilUsuario" alt="Editar usuario" />
                </RouterLink>
                <button
                  class="opt status"
                  :class="isActive(row) ? 'active' : 'inactive'"
                  type="button"
                  :aria-label="isActive(row) ? 'Desactivar usuario' : 'Activar usuario'"
                  @click="toggleState(row)"
                >
                  <img :src="getStateIcon(row)" :alt="getStateLabel(row)" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pager-row">
        <button
          class="pager"
          :class="{ disabled: !canGoPrevious }"
          type="button"
          aria-label="Anterior"
          :disabled="!canGoPrevious"
          @click="goPrevious"
        >
          <img :src="IconFlechaIzquierda" alt="Anterior" />
        </button>
        <button
          class="pager"
          :class="{ disabled: !canGoNext }"
          type="button"
          aria-label="Siguiente"
          :disabled="!canGoNext"
          @click="goNext"
        >
          <img :src="IconFlechaDerecha" alt="Siguiente" />
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  height: 100%;
  box-sizing: border-box;
  padding: 1.05rem 1rem 0.85rem;
  display: flex;
  flex-direction: column;
}

.section-head {
  display: grid;
  grid-template-columns: auto auto minmax(260px, 1fr) auto;
  gap: 0.85rem;
  align-items: center;
  margin-bottom: 0.85rem;

  h1 {
    margin: 0;
    color: #35457f;
    font-size: clamp(2.1rem, 2.8vw, 2.75rem);
    font-weight: 800;
  }
}

.action-btn,
.search {
  border: 1px solid #c8ccda;
  border-radius: 9px;
  background: white;
  padding: 0.58rem 0.9rem;
  font-size: 0.95rem;
}

.add {
  background: #79c65e;
  color: white;
  border-color: transparent;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;

  img {
    width: 1rem;
    height: 1rem;
    object-fit: contain;
  }
}

.search-wrap {
  display: flex;
  align-items: center;
  min-width: 0;
  border: 1px solid #d5daea;
  border-radius: 9px;
  background: #ffffff;
  padding: 0 0.65rem;
}

.search-icon {
  width: 1rem;
  height: 1rem;
  object-fit: contain;
  margin-right: 0.4rem;
}

.search {
  min-width: 0;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 0.58rem 0;
  outline: none;
  color: #6f7a95;
}

.table-card {
  flex: 1;
  min-height: 0;
  background: white;
  border-radius: 20px;
  overflow-x: hidden;
  overflow-y: auto;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.35rem 0.7rem 0.45rem;
}

.table-message,
.table-error {
  margin: 0.45rem 0.4rem;
  font-size: 0.9rem;
}

.table-message {
  color: #395791;
}

.table-error {
  color: #a62b2b;
}

.user-cell {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
}

.user-avatar {
  width: 1.85rem;
  height: 1.85rem;
  border-radius: 50%;
  overflow: hidden;
  background: #edf1ff;
  color: #4a5d8f;
  display: grid;
  place-items: center;
  font-size: 0.68rem;
  font-weight: 700;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.user-name {
  white-space: nowrap;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th,
td {
  padding: 0.72rem 0.85rem;
  text-align: left;
  border-bottom: 1px solid #eef1f6;
  font-size: 0.91rem;
}

th {
  color: #7f93c5;
  font-weight: 600;
}

.head-sort {
  display: inline-flex;
  align-items: center;
  gap: 0.28rem;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
}

.sort-arrow {
  width: 0.72rem;
  height: 0.72rem;
  object-fit: contain;
  opacity: 0.42;
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.sort-arrow.active {
  opacity: 0.9;
}

.sort-arrow.desc {
  transform: rotate(180deg);
}

th:first-child,
td:first-child {
  width: 58px;
}

th:nth-child(2),
td:nth-child(2) {
  width: 150px;
}

th:nth-child(3),
td:nth-child(3) {
  width: 150px;
}

th:nth-child(4),
td:nth-child(4) {
  width: 108px;
}

th:nth-child(5),
td:nth-child(5) {
  width: 150px;
}

th:nth-child(6),
td:nth-child(6) {
  width: 94px;
}

th:last-child,
td:last-child {
  width: 136px;
  text-align: center;
}

.options {
  display: flex;
  gap: 0.55rem;
  justify-content: center;
}

.opt {
  width: 2.15rem;
  height: 2.15rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  text-decoration: none;
  border: 0;
  cursor: pointer;
  padding: 0;

  img {
    width: 1.12rem;
    height: 1.12rem;
    object-fit: contain;
  }
}

.view {
  background: #f9d192;
}

.edit {
  background: #ffd34d;
}

.status {
  background: #c6ee80;
}

.status.inactive {
  background: #ffb5b5;
}

.filter {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  color: #66708a;

  img {
    width: 0.95rem;
    height: 0.95rem;
    object-fit: contain;
  }

  .arrow-icon {
    width: 0.8rem;
    height: 0.8rem;
  }
}

.pager-row {
  display: flex;
  justify-content: flex-end;
  gap: 0.65rem;
  padding: 0.45rem 2.3rem 0.15rem 0;
  min-height: 2rem;
  box-sizing: border-box;
}

.pager {
  border: 0;
  background: transparent;
  display: grid;
  place-items: center;
  width: 1.9rem;
  height: 1.9rem;
  padding: 0;
  cursor: pointer;

  img {
    width: 1.45rem;
    height: 1.45rem;
    object-fit: contain;
  }
}

.pager.disabled {
  opacity: 0.35;
  cursor: default;
}

@media (max-width: 900px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .table-card {
    padding: 0.3rem 0.45rem 0.35rem;
  }
}
</style>
