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
  padding: 2rem 2rem 1rem;
  margin-top: auto;
  overflow: hidden;

  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 250px 250px 1fr;
    gap: 1rem;

    .footer-section {
      h4 {
        margin-bottom: 1rem;
        color: #4caf50;
      }

      p {
        margin: 0.3rem 0;
        font-size: 0.8rem;
      }

      ul {
        list-style: none;
        padding: 0;

        li {
          margin: 0.5rem 0;

          a {
            color: #bbb;
            text-decoration: none;
            transition: color 0.3s;

            &:hover {
              color: #4caf50;
            }
          }
        }
      }

      .logo-footer {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
        font-size: 1.2rem;

        img {
          height: 30px;
        }
      }

      .copyright {
        font-size: 0.9rem;
        margin-top: 1rem;
      }

      .derechos {
        font-size: 0.9rem;
      }
    }
  }
}

@media (max-width: 768px) {
  .footer {
    .footer-container {
      grid-template-columns: 1fr;
    }
  }
}
</style>
