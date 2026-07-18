<script setup>
import Escudo from '../assets/images/Escudo.png'
import Letras from '../assets/images/LetrasFooter.png'
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-section">
        <div class="logo-footer">
          <img :src="Escudo" alt="Escudo de la unidad" />
          <img :src="Letras" alt="Letras de la unidad" />
        </div>
        <p class="copyright">Copyright © 2026 SICEPI</p>
        <p class="derechos">Todos los Derechos reservados</p>
      </div>

      <div class="footer-section">
        <h4>Navegación</h4>
        <ul>
          <li><a href="#inicio">Inicio</a></li>
          <li><a href="#sobre">Sobre nosotros</a></li>
          <li><a href="#contacto">Contactanos</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>Contactos</h4>
        <p>Telefono: 68266526</p>
        <p>WhatsApp: 68266526</p>
        <p>Email: contacto@gmail.com</p>
      </div>

      <div class="footer-section">
        <h4>Datos Generales</h4>
        <p>Horarios de Atención: Lunes - Viernes, 8:00 - 18:00</p>
        <p>Dirección: Zn. de Miraflores Av. Saavedra No. 2303</p>
      </div>
    </div>
  </footer>
</template>

<style lang="scss" scoped>
.footer {
  background-color: #263238;
  color: white;
  padding: 1rem 2.2rem 0.7rem;
  margin-top: auto;
  overflow: auto;
  height: 20vh;
  box-sizing: border-box;

  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    height: 100%;
    display: grid;
    grid-template-columns: 1.1fr 0.85fr 0.85fr 1.2fr;
    gap: 0.9rem;

    .footer-section {
      h4 {
        margin: 0 0 0.55rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: #eef3f6;
      }

      p {
        margin: 0.22rem 0;
        font-size: 0.78rem;
        line-height: 1.25;
        color: #d8e0e5;
      }

      ul {
        list-style: none;
        padding: 0;
        margin: 0;

        li {
          margin: 0.25rem 0;

          a {
            color: #d8e0e5;
            font-size: 0.78rem;
            text-decoration: none;
            transition: color 0.3s;

            &:hover {
              color: #ffffff;
            }
          }
        }
      }

      .logo-footer {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
        font-size: 1.2rem;

        img {
          width: auto;
        }

        img:first-child {
          height: 30px;
        }

        img:last-child {
          height: 40px;
        }
      }

      .copyright {
        font-size: 0.8rem;
        margin-top: 0.35rem;
      }

      .derechos {
        font-size: 0.8rem;
      }
    }
  }
}

@media (max-width: 768px) {
  .footer {
    padding: 0.7rem 1rem 0.45rem;

    .footer-container {
      min-width: 900px;
      grid-template-columns: 1.1fr 0.85fr 0.85fr 1.2fr;
      gap: 0.7rem;
    }
  }
}
</style>
