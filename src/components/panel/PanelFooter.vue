<script setup>
import Escudo from '../../assets/images/Escudo.png'
import Letras from '../../assets/images/LetrasFooter.png'
</script>

<template>
  <footer class="dashboard-footer">
    <div class="footer-brand">
      <img :src="Escudo" alt="Escudo SICEPI" />
      <img :src="Letras" alt="SICEPI" />
      <p>Copyright © 2026 SICEPI</p>
      <p>Todos los Derechos reservados</p>
    </div>

    <div class="footer-copy">
      <p>Sistema de control de proyectos de infraestructura</p>
      <strong>SICEPI 2026</strong>
    </div>

    <div class="footer-badge">
      <img :src="Escudo" alt="Escudo SICEPI" />
    </div>
  </footer>
</template>

<style scoped lang="scss">
.dashboard-footer {
  width: 100%;
  background: #2b3740;
  color: #d4d8de;
  display: grid;
  grid-template-columns: 1fr 1.4fr 0.8fr;
  align-items: center;
  gap: 1rem;
  padding: 0.95rem 1.5rem;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;

  img:first-child {
    width: 34px;
    height: 34px;
    object-fit: contain;
  }

  img:nth-child(2) {
    width: 110px;
    object-fit: contain;
    margin-bottom: 0.35rem;
  }

  p {
    margin: 0;
    font-size: 0.75rem;
  }
}

.footer-copy {
  text-align: center;

  p,
  strong {
    display: block;
  }

  p {
    margin: 0 0 0.4rem;
    font-size: 1rem;
  }

  strong {
    font-size: 1.2rem;
    font-weight: 500;
  }
}

.footer-badge {
  display: flex;
  justify-content: flex-end;

  img {
    width: 72px;
    height: 72px;
    object-fit: contain;
  }
}

@media (max-width: 900px) {
  .dashboard-footer {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .footer-badge {
    justify-content: center;
  }
}
</style>
