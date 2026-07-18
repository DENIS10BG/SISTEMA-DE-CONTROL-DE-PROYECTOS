<script setup>
import Escudo from '../../assets/images/Escudo.png'
import Letras from '../../assets/images/LetrasFooter.png'
</script>

<template>
  <footer class="dashboard-footer">
    <div class="footer-brand">
      <div class="brand-row">
        <img :src="Escudo" alt="Escudo SICEPI" />
        <img :src="Letras" alt="SICEPI" />
      </div>
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
  height: 10vh;
  background: #2b3740;
  color: #d4d8de;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 0.6rem;
  padding: 0.35rem 0.9rem;
  box-sizing: border-box;
  overflow: hidden;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.1rem;

  .brand-row {
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }

  .brand-row img:first-child {
    width: 34px;
    height: 34px;
    object-fit: contain;
  }

  .brand-row img:last-child {
    width: 118px;
    object-fit: contain;
  }

  p {
    margin: 0;
    font-size: 0.62rem;
    line-height: 1.1;
  }
}

.footer-copy {
  text-align: center;
  justify-self: center;

  p,
  strong {
    display: block;
  }

  p {
    margin: 0 0 0.15rem;
    font-size: 0.82rem;
    line-height: 1.1;
  }

  strong {
    font-size: 0.92rem;
    font-weight: 600;
  }
}

.footer-badge {
  display: flex;
  justify-content: flex-end;
  justify-self: end;

  img {
    width: 58px;
    height: 58px;
    object-fit: contain;
  }
}

@media (max-width: 900px) {
  .dashboard-footer {
    grid-template-columns: 1fr auto 1fr;
    gap: 0.45rem;
    padding: 0.3rem 0.55rem;
  }

  .footer-brand .brand-row img:first-child {
    width: 28px;
    height: 28px;
  }

  .footer-brand .brand-row img:last-child {
    width: 96px;
  }

  .footer-brand p,
  .footer-copy p,
  .footer-copy strong {
    font-size: 0.66rem;
  }

  .footer-badge img {
    width: 46px;
    height: 46px;
  }

  .footer-badge {
    justify-content: flex-end;
  }
}
</style>
