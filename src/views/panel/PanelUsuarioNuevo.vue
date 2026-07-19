<script setup>
import { RouterLink } from 'vue-router'
import profileImage from '../../assets/images/IngenieroProyetos.png'
</script>

<template>
  <section class="new-user-page">
    <div class="page-title">Añadir Usuario</div>

    <div class="new-user-card">
      <div class="tabs">
        <span class="tab active">Nuevo Usuario</span>
      </div>

      <div class="profile-body">
        <div class="avatar-wrap">
          <img :src="profileImage" alt="Nuevo usuario" />
          <span class="edit-badge">+</span>
        </div>

        <div class="fields-grid">
          <label><span>Nombre</span><input placeholder="Ingrese nombre" /></label>
          <label><span>Apellido</span><input placeholder="Ingrese apellido" /></label>
          <label><span>Correo</span><input placeholder="correo@ejemplo.com" /></label>
          <label><span>Contraseña</span><input type="password" placeholder="**********" /></label>
          <label><span>Teléfono</span><input placeholder="Ingrese teléfono" /></label>
          <label><span>Carnet</span><input placeholder="Ingrese carnet" /></label>
          <label><span>Rol</span><input placeholder="Administrador" /></label>
          <label><span>Estado de cuenta</span><input placeholder="Activo" /></label>
        </div>
      </div>

      <div class="footer-actions">
        <RouterLink class="cancel-btn" to="/panel/usuarios">Cancelar</RouterLink>
        <button class="save-btn" type="button">Guardar</button>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.new-user-page {
  height: 100%;
  box-sizing: border-box;
  padding: 0.75rem 1.2rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  overflow: auto;
}

.page-title {
  margin: 0;
  color: #35457f;
  font-size: clamp(1.9rem, 2.4vw, 2.5rem);
  line-height: 1.05;
  font-weight: 800;
}

.new-user-card {
  width: min(100%, 980px);
  box-sizing: border-box;
  margin: 0 auto;
  background: white;
  border-radius: 22px;
  border: 1px solid #a9a09a;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.8rem 1.1rem 0.95rem;
}

.tabs {
  display: flex;
  gap: 2.6rem;
  border-bottom: 1px solid #eef1f6;
  padding: 0.08rem 0 0.62rem 0.45rem;
}

.tab {
  text-decoration: none;
  color: #9aabd7;
  font-weight: 600;
  font-size: 1.18rem;
  padding-bottom: 0.64rem;
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
  grid-template-columns: 130px 1fr;
  gap: 0.85rem;
  padding-top: 0.8rem;
  align-items: start;
}

.avatar-wrap {
  position: relative;
  width: 98px;
  height: 98px;
  margin-left: 0.4rem;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
}

.edit-badge {
  position: absolute;
  right: 4px;
  bottom: 8px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #2f3dff;
  color: white;
  display: grid;
  place-items: center;
  font-size: 0.75rem;
  border: 3px solid white;
}

.fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.7rem 1rem;

  label {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  span {
    color: #6c6f7a;
    font-size: 0.86rem;
  }

  input {
    width: 100%;
    border: 1px solid #7046ff;
    border-radius: 12px;
    padding: 0.66rem 0.86rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.9rem;
    outline: none;
  }
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.65rem;
  padding-top: 0.7rem;
}

.cancel-btn,
.save-btn {
  border: 0;
  border-radius: 12px;
  min-width: 120px;
  padding: 0.55rem 0.9rem;
  font-weight: 700;
  text-align: center;
  text-decoration: none;
}

.cancel-btn {
  background: #e6e9f5;
  color: #3e4a71;
}

.save-btn {
  background: #2f3dff;
  color: white;
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

  .footer-actions {
    justify-content: stretch;

    .cancel-btn,
    .save-btn {
      width: 100%;
    }
  }
}
</style>
