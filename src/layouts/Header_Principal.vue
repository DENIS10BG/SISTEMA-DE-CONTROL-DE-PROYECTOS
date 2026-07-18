<script setup>
import Escudo from '../assets/images/Escudo.png'
import Letras from '../assets/images/Letras.png'
</script>

<template>
  <header class="navbar">
    <div class="navbar-container">
      <RouterLink class="logo" to="/">
        <img :src="Escudo" alt="Escudo de la unidad" />
        <img :src="Letras" alt="Letras de la unidad" />
      </RouterLink>
      <nav class="nav-links">
        <a href="#inicio">Inicio</a>
        <a href="#sobre">Sobre Nosotros</a>
        <a href="#contacto">Contactanos</a>
      </nav>
      <RouterLink class="btn-login" to="/login">Inicia Sesión</RouterLink>
    </div>
  </header>
</template>

<style lang="scss" scoped>
.navbar {
  background-color: #f8f9fa;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 10vh;
  box-sizing: border-box;
  overflow: hidden;

  .navbar-container {
    max-width: 100%;
    height: 100%;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .logo {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: bold;
      font-size: 1.5rem;
      text-decoration: none;
      color: inherit;

      img {
        height: 40px;
      }
    }

    .nav-links {
      display: flex;
      gap: 2rem;

      a {
        text-decoration: none;
        color: #333;
        transition: color 0.3s;

        &:hover {
          color: #4caf50;
        }
      }
    }

    .btn-login {
      background-color: #4caf50;
      color: white;
      border: none;
      padding: 0.75rem 1.5rem;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;

      &:hover {
        background-color: #45a049;
      }
    }
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 0.5rem 0.8rem;

    .navbar-container {
      gap: 0.6rem;
    }

    .logo img {
      height: 28px;
    }

    .nav-links {
      gap: 0.8rem;

      a {
        font-size: 0.82rem;
      }
    }

    .btn-login {
      padding: 0.45rem 0.7rem;
      font-size: 0.82rem;
    }
  }
}
</style>
