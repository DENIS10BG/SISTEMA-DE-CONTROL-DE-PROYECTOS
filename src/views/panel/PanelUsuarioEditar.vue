<script setup>
import { RouterLink } from 'vue-router'
import profileImage from '../../assets/images/IngenieroProyetos.png'
</script>

<template>
  <section class="settings-page">
    <div class="page-title">Editar Usuario</div>

    <div class="settings-card">
      <div class="tabs">
        <RouterLink class="tab" to="/panel/usuarios/ver">Ver Usuario</RouterLink>
        <RouterLink class="tab active" to="/panel/usuarios/editar">Editar Usuario</RouterLink>
      </div>

      <div class="profile-body">
        <div class="avatar-wrap">
          <img :src="profileImage" alt="Editar usuario" />
          <span class="edit-badge">✎</span>
        </div>

        <div class="fields-grid">
          <label><span>Nombre</span><input value="Denis Helmer" /></label>
          <label><span>Apellido</span><input value="Ramos Paco" /></label>
          <label><span>Correo</span><input value="denis@gmail.com" /></label>
          <label><span>Contraseña</span><input value="**********" /></label>
          <label><span>Teléfono</span><input value="6826065" /></label>
          <label><span>Carnet</span><input value="9978045" /></label>
          <label><span>Rol</span><input value="Administrador" /></label>
          <label><span>Estado de cuenta</span><input value="Activo" /></label>
        </div>
      </div>

      <div class="footer-actions">
        <button class="save-btn" type="button">Guardar</button>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.settings-page {
  padding: 1.8rem 1.5rem 1.2rem;
}

.page-title {
  margin: 0 0 1rem;
  color: #35457f;
  font-size: clamp(2.2rem, 3vw, 3.2rem);
  font-weight: 800;
}

.settings-card {
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

.edit-badge {
  position: absolute;
  right: 4px;
  bottom: 8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #2f3dff;
  color: white;
  display: grid;
  place-items: center;
  font-size: 0.95rem;
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
    border: 1px solid #7046ff;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    background: #ffffff;
    color: #465b92;
    font-size: 0.95rem;
    outline: none;
  }
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 1.2rem;
}

.save-btn {
  border: 0;
  border-radius: 12px;
  background: #2f3dff;
  color: white;
  min-width: 140px;
  padding: 0.95rem 1.2rem;
  font-weight: 700;
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
