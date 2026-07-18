<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

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
    no: '02.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Desactivo',
  },
  {
    id: 3,
    no: '03.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 4,
    no: '04.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
  {
    id: 5,
    no: '05.',
    nombres: 'Denis Helmer',
    apellidos: 'Ramos Paco',
    telefono: '6826065',
    rol: 'Administrador',
    estado: 'Activo',
  },
]

const activeStateIds = ref(new Set([1, 3, 4, 5]))

const isActive = (id) => activeStateIds.value.has(id)

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
      <button class="action-btn add">Añadir Usuarios</button>
      <input class="search" placeholder="Search for anything..." />
      <button class="action-btn filter">Filter</button>
    </div>

    <div class="table-card">
      <table>
        <thead>
          <tr>
            <th>No</th>
            <th>Nombres</th>
            <th>Apellidos</th>
            <th>Teléfono</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td>{{ row.no }}</td>
            <td>{{ row.nombres }}</td>
            <td>{{ row.apellidos }}</td>
            <td>{{ row.telefono }}</td>
            <td>{{ row.rol }}</td>
            <td>{{ row.estado }}</td>
            <td>
              <div class="options">
                <RouterLink class="opt view" to="/panel/usuarios/ver" aria-label="Ver usuario"
                  >👁</RouterLink
                >
                <RouterLink class="opt edit" to="/panel/usuarios/editar" aria-label="Editar usuario"
                  >✎</RouterLink
                >
                <button
                  class="opt status"
                  :class="isActive(row.id) ? 'green' : 'red'"
                  type="button"
                  :aria-label="isActive(row.id) ? 'Desactivar usuario' : 'Activar usuario'"
                  @click="toggleState(row.id)"
                >
                  ○
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped lang="scss">
.section-shell {
  padding: 1.8rem 1.5rem 1.2rem;
}

.section-head {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;

  h1 {
    margin: 0;
    color: #35457f;
    font-size: clamp(2rem, 2.8vw, 2.8rem);
    font-weight: 800;
  }
}

.action-btn,
.search {
  border: 1px solid #c8ccda;
  border-radius: 8px;
  background: white;
  padding: 0.75rem 1rem;
}

.add {
  background: #79c65e;
  color: white;
  border-color: transparent;
}

.search {
  min-width: 280px;
}

.table-card {
  background: white;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.9rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eef1f6;
  font-size: 0.95rem;
}

th {
  color: #7f93c5;
  font-weight: 700;
}

.options {
  display: flex;
  gap: 0.5rem;
}

.opt {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  text-decoration: none;
  border: 0;
  cursor: pointer;
}

.view {
  background: #b8f2b4;
  color: #2e8c33;
}

.edit {
  background: #ffd85c;
  color: #a66a00;
}

.green {
  background: #b8f2b4;
  color: #2e8c33;
}

.yellow {
  background: #ffd85c;
}

.red {
  background: #ff7777;
  color: #b11f1f;
}

@media (max-width: 900px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .search {
    min-width: 0;
    width: 100%;
  }
}
</style>
