<script setup>
import { computed, ref } from 'vue'
import alertPreview from '../../assets/images/IngenieroProyetos.png'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'
import AlertaDoc from '@/components/icons/IconsAlert/AlertaPrincipal.svg'
import AnalisarAlerta from '@/components/icons/IconsAlert/AnalisarAlertas.svg'
import VerArchivo from '@/components/icons/IconsAlert/VerArchivoAlerta.svg'

const showAnalyzeModal = ref(false)
const selectedAlertId = ref(null)
const selectedAction = ref(null)

const modalAlerts = [
  { id: 1, code: '01.', text: 'Falta certificado de calificacion' },
  { id: 2, code: '01.', text: 'Falta certificado de calificacion' },
  { id: 3, code: '01.', text: 'Falta certificado de calificacion' },
]

const canChooseAction = computed(() => selectedAlertId.value !== null)

const openAnalyzeModal = () => {
  showAnalyzeModal.value = true
  selectedAlertId.value = null
  selectedAction.value = null
}

const closeAnalyzeModal = () => {
  showAnalyzeModal.value = false
}

const selectAlert = (alertId) => {
  selectedAlertId.value = alertId
}

const chooseAction = (action) => {
  if (!canChooseAction.value) return
  selectedAction.value = action
}
</script>

<template>
  <section class="detail-page">
    <div class="detail-head">
      <h1>ALERTAS</h1>
    </div>

    <article class="project-hero">
      <div class="folder">
        <img :src="IconCarpeta" alt="Carpeta" />
      </div>
      <div>
        <p class="label">Proyecto</p>
        <strong>Construccion Tinglado RSAT-1 BUCH-ORURO</strong>
      </div>
      <div>
        <p class="label blue">Lugar</p>
        <strong>Oruro</strong>
      </div>
      <div>
        <p class="label blue">Archivo</p>
        <strong>Proyecto</strong>
      </div>
      <div>
        <p class="label blue">Año</p>
        <strong>2019</strong>
      </div>
      <button class="details-btn">Mas detalles</button>
    </article>

    <h2>Construcción Tinglado RSAT-1 BUCH-ORURO</h2>

    <div class="detail-grid">
      <div class="preview-card">
        <span class="tag">Proyecto</span>
        <img class="mock-image" :src="alertPreview" alt="Documento del proyecto" />
        <small>3 CAO</small>
      </div>

      <div class="description-card">
        <div class="alert-section">
          <div class="alert-badge">
            <span>ALERTA</span>
            <span class="alert-icon">
              <img :src="AlertaDoc" alt="Alerta" />
            </span>
          </div>
          <div class="alert-table">
            <div class="alert-table-head">
              <span>SL No</span>
              <span>Alerta</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion de goledo sangines</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion</span>
            </div>
            <div class="alert-row">
              <span>01.</span>
              <span>Falta certificado de calificacion de coche rudimentario</span>
            </div>
          </div>
        </div>
      </div>

      <div class="side-stack">
        <button class="side-card active">
          <span class="side-title">Ver</span>
          <span class="side-icon pink">
            <img :src="VerArchivo" alt="Ver Archivo" />
          </span>
          <small>Ve el proyecto Completo</small>
        </button>
        <button class="side-card" @click="openAnalyzeModal">
          <span class="side-title">Analisar Alerta</span>
          <span class="side-icon orange">
            <img :src="AnalisarAlerta" alt="Analizar Alerta" />
          </span>
          <small>Analisar las Alertas</small>
        </button>
      </div>
    </div>

    <div v-if="showAnalyzeModal" class="modal-overlay" @click.self="closeAnalyzeModal">
      <article class="analyze-modal">
        <h3>ANALISAR ALERTAS</h3>

        <div class="modal-grid">
          <div class="modal-left">
            <button
              class="issue-btn"
              :class="{ active: selectedAction === 'titulos' }"
              :disabled="!canChooseAction"
              @click="chooseAction('titulos')"
            >
              Titulos Indenticos
            </button>
            <button
              class="issue-btn"
              :class="{ active: selectedAction === 'archivo' }"
              :disabled="!canChooseAction"
              @click="chooseAction('archivo')"
            >
              Archivo Inilegible
            </button>
            <button
              class="issue-btn"
              :class="{ active: selectedAction === 'sin-documento' }"
              :disabled="!canChooseAction"
              @click="chooseAction('sin-documento')"
            >
              Sin Documento
            </button>

            <div class="modal-actions">
              <button class="save-btn ghost" @click="closeAnalyzeModal">Cancelar</button>
              <button class="save-btn">Guardar</button>
            </div>
          </div>

          <div class="modal-center">
            <div class="mini-head">
              <span>No</span>
              <span>Alerta</span>
            </div>

            <button
              v-for="alert in modalAlerts"
              :key="alert.id"
              class="mini-row"
              :class="{ selected: selectedAlertId === alert.id }"
              @click="selectAlert(alert.id)"
            >
              <span>{{ alert.code }}</span>
              <span>{{ alert.text }}</span>
            </button>
          </div>

          <div v-if="selectedAction === 'titulos'" class="modal-right">
            <label>
              <span>Titulo Antes</span>
              <textarea :disabled="!canChooseAction" />
            </label>

            <label>
              <span>Titulo Despues</span>
              <textarea :disabled="!canChooseAction" />
            </label>

            <div class="right-actions">
              <button class="save-btn">Cargar</button>
              <button class="save-btn">Reprocesar</button>
            </div>
          </div>

          <div v-else-if="selectedAction === 'archivo'" class="modal-right">
            <h4>Datos De La Pagina</h4>

            <label>
              <span>Tipo</span>
              <input :disabled="!canChooseAction" />
            </label>

            <label>
              <span>Objeto</span>
              <input :disabled="!canChooseAction" />
            </label>

            <label>
              <span>Pagina</span>
              <input :disabled="!canChooseAction" />
            </label>

            <div class="right-actions single">
              <button class="save-btn">Cargar</button>
            </div>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss">
.detail-page {
  padding: 1.4rem 1.5rem 1.2rem;
  background: #eef1f6;
  min-height: 100%;
}

.detail-head {
  margin-bottom: 0.4rem;
}

h1,
h2 {
  margin: 0 0 1rem;
  color: #35457f;
}

h1 {
  font-size: clamp(2rem, 2.9vw, 3rem);
  font-weight: 800;
}

h2 {
  font-size: clamp(2.4rem, 3.2vw, 3.4rem);
  font-weight: 500;
  color: #222;
}

.project-hero {
  display: grid;
  grid-template-columns: 56px 1.5fr 0.75fr 0.9fr 0.5fr auto;
  gap: 1rem;
  align-items: center;
  background: white;
  border-radius: 18px;
  padding: 0.9rem 1rem;
  box-shadow: 0 12px 24px rgba(35, 53, 87, 0.08);
  margin-bottom: 1rem;
}

.label {
  margin: 0 0 0.2rem;
  color: #f1a0bb;
  font-size: 0.85rem;
}

.label.blue {
  color: #7894d6;
}

.folder {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #ffd98f;
  display: grid;
  place-items: center;
}

.details-btn,
.side-card {
  border: 1px solid #c8ccda;
  border-radius: 10px;
  background: white;
  padding: 0.75rem 1rem;
}

.details-btn {
  background: #63d24d;
  color: white;
  border-color: transparent;
  border-radius: 999px;
  padding-inline: 1.2rem;
  font-weight: 700;
}

.detail-grid {
  display: grid;
  grid-template-columns: 250px 1fr 220px;
  gap: 1rem;
  align-items: start;
}

.preview-card,
.description-card,
.side-card {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
}

.preview-card {
  padding: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: center;
}

.tag {
  align-self: flex-start;
  background: #d7f1d9;
  color: #80bd7a;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
}

.mock-image {
  width: 100%;
  height: 210px;
  border-radius: 8px;
  object-fit: cover;
}

.description-card {
  padding: 1rem 1.1rem 1.1rem;
}

.description-card h3 {
  margin: 0 0 0.45rem;
  color: #33345a;
  font-size: 1.05rem;
}

.description-card p {
  margin: 0;
  color: #6d7487;
  line-height: 1.45;
  font-size: 0.92rem;
}

.alert-section {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 1rem;
  align-items: stretch;
}

.alert-badge {
  background: #f8a6b0;
  color: #2f3558;
  border-radius: 14px;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  font-size: 1.45rem;
  font-weight: 800;
}

.alert-icon {
  width: 58px;
  height: 58px;
  border-radius: 999px;
  background: #ff6487;
  color: white;
  display: grid;
  place-items: center;
  font-size: 1.6rem;
}

.alert-table {
  background: white;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  padding: 0.7rem 1rem 1rem;
}

.alert-table-head,
.alert-row {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 1rem;
  align-items: center;
}

.alert-table-head {
  color: #97b0e1;
  font-size: 0.85rem;
  padding: 0 0.2rem 0.3rem;
}

.alert-row {
  padding: 0.45rem 0.2rem;
  color: #383f60;
  font-size: 1rem;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.side-card {
  min-height: 138px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  text-align: left;
  font-weight: 700;
  border: 2px solid #3f3f4d;
  border-radius: 14px;
  padding: 0.8rem 0.9rem;
  color: #2f3558;
}

.side-card.active {
  background: #ffd8e4;
}

.side-title {
  font-size: 1.5rem;
  line-height: 1;
}

.side-icon {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  color: white;
  font-size: 1.45rem;
  align-self: center;
}

.pink {
  background: #ff6f8d;
}

.orange {
  background: #ffba49;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 40;
  background: rgba(40, 35, 40, 0.65);
  display: grid;
  place-items: center;
  padding: 1rem;
}

.analyze-modal {
  width: min(980px, 96vw);
  min-height: min(620px, 92vh);
  background: #ececef;
  border-radius: 28px;
  padding: 1.1rem 1.4rem 1.35rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: auto;
}

.analyze-modal h3 {
  margin: 0;
  font-size: clamp(1.7rem, 3vw, 3rem);
  color: #16133a;
  text-align: center;
  letter-spacing: 0.02em;
}

.modal-grid {
  display: grid;
  grid-template-columns: 200px 1fr minmax(280px, 350px);
  gap: 1rem;
  min-height: 500px;
}

.modal-left {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.issue-btn {
  min-height: 46px;
  border: 2px solid #9793a9;
  border-radius: 12px;
  background: #f8f8fb;
  color: #6f6e81;
  font-size: 1.05rem;
  font-weight: 700;
}

.issue-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.issue-btn.active {
  background: #d7c2e1;
}

.modal-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.save-btn {
  min-height: 40px;
  border: 0;
  border-radius: 8px;
  background: #69c370;
  color: #f3fff2;
  font-weight: 700;
}

.save-btn.ghost {
  background: #69c370;
}

.modal-center {
  border: 1px solid #62616d;
  border-radius: 16px;
  padding: 0.35rem 0.5rem 0.7rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.mini-head,
.mini-row {
  display: grid;
  grid-template-columns: 56px 1fr;
  gap: 0.4rem;
  align-items: center;
}

.mini-head {
  color: #95abd5;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0 0.3rem;
}

.mini-row {
  min-height: 40px;
  border: 2px solid #2f2f35;
  border-radius: 4px;
  background: #f7f7f8;
  color: #444;
  text-align: left;
  padding: 0 0.35rem;
  font-size: 1.05rem;
}

.mini-row.selected {
  background: #b0ee7d;
}

.modal-right {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.modal-right h4 {
  margin: 0;
  color: #767087;
  font-size: 2rem;
  font-weight: 500;
}

.modal-right label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.modal-right span {
  color: #585865;
  font-size: 1.03rem;
}

.modal-right input,
.modal-right textarea {
  border: 1.6px solid #54545f;
  border-radius: 18px;
  background: #f5f5f5;
  min-height: 38px;
  padding: 0.5rem 0.75rem;
  resize: vertical;
}

.modal-right textarea {
  min-height: 88px;
}

.modal-right input:disabled,
.modal-right textarea:disabled {
  opacity: 0.6;
}

.right-actions {
  margin-top: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.9rem;
}

.right-actions.single {
  grid-template-columns: 1fr;
  width: 55%;
  margin-inline: auto;
}

@media (max-width: 1100px) {
  .detail-grid,
  .project-hero,
  .alert-section,
  .detail-head {
    grid-template-columns: 1fr;
  }

  .modal-grid {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .modal-actions {
    margin-top: 0.75rem;
  }

  .right-actions.single {
    width: 100%;
  }
}

@media (max-width: 900px) {
  .project-hero {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: 2rem;
  }
}
</style>
