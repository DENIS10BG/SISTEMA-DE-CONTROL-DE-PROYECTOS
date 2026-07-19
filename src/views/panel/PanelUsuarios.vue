<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
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

const rows = [
  {
    id: 1,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 2,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Desactivo',
  },
  {
    id: 3,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 4,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 5,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 6,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 7,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 8,
    no: '01.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
]

const activeStateIds = ref(new Set([1, 3, 4, 5]))
const currentPage = ref(1)
const rowsPerPage = 7
const sortField = ref('nombres')
const sortDirection = ref('asc')

const isActive = (id) => activeStateIds.value.has(id)

const getStateLabel = (id) => (isActive(id) ? 'Activo' : 'Desactivo')

const getStateIcon = (id) => (isActive(id) ? IconUsuarioActivo : IconUsuarioDesactivado)

const totalPages = computed(() => Math.ceil(rows.length / rowsPerPage))

const sortedRows = computed(() => {
  const direction = sortDirection.value === 'asc' ? 1 : -1

  return [...rows].sort((left, right) => {
    const leftValue = sortField.value === 'estado' ? getStateLabel(left.id) : left[sortField.value]
    const rightValue =
      sortField.value === 'estado' ? getStateLabel(right.id) : right[sortField.value]

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

const toggleState = (id) => {
  const next = new Set(activeStateIds.value)

  if (next.has(id)) {
    next.delete(id)
  } else {
    next.add(id)
  }

  activeStateIds.value = next
}
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
        <input class="search" placeholder="Search for anything..." />
      </div>

      <button class="action-btn filter" type="button">
        <img :src="IconFiltroUsuario" alt="Filtro" />
        <span>Filter</span>
        <img class="arrow-icon" :src="IconFlechaAbajo" alt="Expandir" />
      </button>
    </div>

    <div class="table-card">
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
            <td>{{ row.no }}</td>
            <td>{{ row.nombres }}</td>
            <td>{{ row.apellidos }}</td>
            <td>{{ row.telefono }}</td>
            <td>{{ row.rol }}</td>
            <td>{{ getStateLabel(row.id) }}</td>
            <td>
              <div class="options">
                <RouterLink class="opt view" to="/panel/usuarios/ver" aria-label="Ver usuario">
                  <img :src="IconVerPerfilUsuario" alt="Ver usuario" />
                </RouterLink>
                <RouterLink
                  class="opt edit"
                  to="/panel/usuarios/editar"
                  aria-label="Editar usuario"
                >
                  <img :src="IconEditarPerfilUsuario" alt="Editar usuario" />
                </RouterLink>
                <button
                  class="opt status"
                  :class="isActive(row.id) ? 'active' : 'inactive'"
                  type="button"
                  :aria-label="isActive(row.id) ? 'Desactivar usuario' : 'Activar usuario'"
                  @click="toggleState(row.id)"
                >
                  <img :src="getStateIcon(row.id)" :alt="getStateLabel(row.id)" />
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
