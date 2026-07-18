<script setup>
import Header_Principal from '@/layouts/Header_Principal.vue'
import Footer_Principal from '@/layouts/Footer_Principal.vue'
import IngPro from '../assets/images/IngenieroProyetos.png'
</script>

<template>
  <div class="inicio-principal">
    <!-- Header Component -->
    <Header_Principal />

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>Sistema de Control de Expedientes de</h1>
        <h2>Proyectos de Infraestructura</h2>
        <p>
          Bienvenido. Este sistema está encargado de controlar y analizar la integridad documental
          de los proyectos de infraestructura finalizados.
        </p>
        <RouterLink class="btn-primary" to="/login">Inicia Sesión</RouterLink>
      </div>
      <div class="hero-image">
        <img :src="IngPro" alt="Ilustración del sistema" />
      </div>
    </section>

    <!-- Footer Component -->
    <Footer_Principal />
  </div>
</template>

<style lang="scss" scoped>
.inicio-principal {
  display: flex;
  flex-direction: column;
}

// Hero Section
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 150px;
  background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
  height: 65vh;

  .hero-content {
    h1 {
      font-size: 3.2rem;
      color: #333;
      font-weight: 800;
      padding: 0;
      margin: 0;
      letter-spacing: 2px;
      line-height: normal;
    }

    h2 {
      font-size: 3.2rem;
      font-weight: 800;
      margin-bottom: 1rem;
      color: #45a049;
      letter-spacing: 2px;
      line-height: normal;
    }

    p {
      color: #666;
      margin-bottom: 2rem;
      letter-spacing: 1px;
      line-height: 1.6;
    }

    .btn-primary {
      background-color: #4caf50;
      color: white;
      border: none;
      padding: 0.75rem 2rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;
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

  .hero-image {
    display: flex;
    justify-content: left;
    padding-right: 400px;

    img {
      max-width: 150%;
    }
  }
}

// Responsiv
</style>
