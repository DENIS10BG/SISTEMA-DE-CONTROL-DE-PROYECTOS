<script setup>
import { RouterLink } from 'vue-router'
import profileImage from '../../assets/images/IngenieroProyetos.png'
</script>

<template>
  <section class="profile-page">
    <div class="page-title">Ver Perfil</div>

    <div class="profile-card">
      <div class="tabs">
        <RouterLink class="tab active" to="/panel/perfil">Perfil</RouterLink>
        <RouterLink class="tab" to="/panel/ajustes">Editar Perfil</RouterLink>
      </div>

      <div class="profile-body">
        <div class="avatar-wrap">
          <img :src="profileImage" alt="Perfil" />
          <span class="status-dot"></span>
        </div>

        <div class="fields-grid">
          <label>
            <span>Nombre</span>
            <input value="Charlene Reed" readonly />
          </label>
          <label>
            <span>Apellido</span>
            <input value="Charlene Reed" readonly />
          </label>
          <label>
            <span>Correo</span>
            <input value="charlenereed@gmail.com" readonly />
          </label>
          <label>
            <span>Contraseña</span>
            <input value="**********" readonly />
          </label>
          <label>
            <span>Fecha de nacimiento</span>
            <input value="25 January 1990" readonly />
          </label>
          <label>
            <span>Direccion</span>
            <input value="San Jose, California, USA" readonly />
          </label>
          <label>
            <span>Telefono</span>
            <input value="78860123" readonly />
          </label>
          <label>
            <span>Carnet</span>
            <input value="9978045" readonly />
          </label>
          <label>
            <span>Rol</span>
            <input value="Administrador" readonly />
          </label>
          <label>
            <span>Estado de cuenta</span>
            <input value="Activo" readonly />
          </label>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.profile-page {
  padding: 1.8rem 1.5rem 1.2rem;
}

.page-title {
  margin: 0 0 1rem;
  color: #35457f;
  font-size: clamp(2.2rem, 3vw, 3.2rem);
  font-weight: 800;
}

.profile-card {
  max-width: 920px;
  margin: 0 auto;
  background: white;
  border-radius: 22px;
  border: 1px solid #a9a09a;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 1rem 1.2rem 1.4rem;
}

.tabs {
  display: flex;
  gap: 2rem;
  border-bottom: 1px solid #eef1f6;
  padding: 0 0 0.8rem 0.8rem;
}

.tab {
  text-decoration: none;
  color: #9aabd7;
  font-weight: 600;
  padding-bottom: 0.55rem;
  position: relative;

  &.active {
    color: #3d3dff;

    &::after {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      bottom: -0.8rem;
      height: 3px;
      border-radius: 999px;
      background: #3d3dff;
    }
  }
}

.profile-body {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 1.2rem;
  padding-top: 1.5rem;
  align-items: start;
}

.avatar-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  margin-left: 0.4rem;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
}

.status-dot {
  position: absolute;
  right: 8px;
  bottom: 10px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #28d962;
  border: 3px solid white;
}

.fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.2rem;

  label {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }

  span {
    color: #6c6f7a;
    font-size: 0.95rem;
  }

  input {
    width: 100%;
    border: 1px solid #dfe6f7;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.95rem;
  }
}

@media (max-width: 900px) {
  .profile-body {
    grid-template-columns: 1fr;
  }

  .avatar-wrap {
    margin: 0 auto;
  }

  .fields-grid {
    grid-template-columns: 1fr;
  }
}
</style>
