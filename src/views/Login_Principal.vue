<script setup>
import Header_Principal from '@/layouts/Header_Principal.vue'
import Footer_Principal from '@/layouts/Footer_Principal.vue'
import { useRouter } from 'vue-router'
import Escudo from '../assets/images/Escudo.png'

const router = useRouter()

const iniciarSesion = () => {
  router.push('/panel/general')
}
</script>

<template>
  <div class="login-page">
    <Header_Principal />

    <main class="login-main">
      <section class="login-card">
        <div class="login-brand">
          <img :src="Escudo" alt="Escudo SICEPI" />
          <h1>BIENVENIDO A SICEPI</h1>
          <p>
            Estás iniciando sesión para acceder a tu cuenta y gestionar tus datos en el sistema.
          </p>
        </div>

        <div class="login-form-panel">
          <h2>INICIA SESIÓN</h2>

          <form class="login-form" @submit.prevent="iniciarSesion">
            <label class="field">
              <span>Usuario</span>
              <input type="text" placeholder="Username" autocomplete="username" />
            </label>

            <label class="field">
              <span>Contraseña</span>
              <input type="password" placeholder="Password" autocomplete="current-password" />
            </label>

            <button type="submit" class="btn-submit">Inicia Sesion</button>
            <a href="#" class="forgot-link">Olvidaste tu Contraseña?</a>
          </form>
        </div>
      </section>
    </main>

    <Footer_Principal />
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.login-main {
  flex: 1;
  display: grid;
  place-items: center;
  background: linear-gradient(180deg, #ddd8d6 0%, #ece8e6 100%);
  padding: 2rem;
}

.login-card {
  width: min(100%, 980px);
  min-height: 560px;
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  background: #ffffff;
  border-radius: 40px;
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(34, 49, 63, 0.16);
}

.login-brand {
  background: linear-gradient(180deg, #54c425 0%, #49ba21 100%);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem;
  text-align: center;

  img {
    width: 110px;
    height: 110px;
    object-fit: contain;
    margin-bottom: 1rem;
  }

  h1 {
    margin: 0;
    font-size: clamp(2rem, 3vw, 2.4rem);
    font-weight: 800;
    line-height: 1.1;
  }

  p {
    max-width: 320px;
    margin: 1rem 0 0;
    color: rgba(255, 255, 255, 0.82);
    line-height: 1.5;
  }
}

.login-form-panel {
  padding: 3.5rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;

  h2 {
    margin: 0 0 1.75rem;
    font-size: clamp(2rem, 3vw, 2.4rem);
    font-weight: 800;
    color: #111827;
  }
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;

  span {
    font-size: 0.95rem;
    font-weight: 600;
    color: #4b5563;
  }

  input {
    border: none;
    border-radius: 12px;
    background: #f4f0ff;
    padding: 0.95rem 1rem;
    font-size: 1rem;
    outline: none;
    box-shadow: inset 0 0 0 1px rgba(17, 24, 39, 0.04);
  }
}

.btn-submit {
  margin-top: 0.5rem;
  border: none;
  border-radius: 12px;
  background: #4caf50;
  color: white;
  font-size: 1rem;
  font-weight: 700;
  padding: 0.95rem 1rem;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    background-color 0.18s ease;

  &:hover {
    background: #409944;
    transform: translateY(-1px);
  }
}

.forgot-link {
  margin-top: 0.15rem;
  text-align: center;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.92rem;
}

@media (max-width: 900px) {
  .login-card {
    grid-template-columns: 1fr;
    border-radius: 28px;
  }

  .login-brand,
  .login-form-panel {
    padding: 2rem;
  }
}
</style>
