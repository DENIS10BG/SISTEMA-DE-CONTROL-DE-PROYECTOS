<script setup>
import { ref } from 'vue'
import IconCarpeta from '@/components/icons/IconsProyect/Carpeta.svg'

const quickQuestions = ['Ver Indice', 'Ver Inventario Doc']

const answerItems = ref([
  {
    id: 1,
    numero: '1',
    texto: 'Formulario 3',
    pagina: 'Pag 3',
  },
])

const questionInput = ref('')
const detailInput = ref('')

const applyQuickQuestion = (question) => {
  questionInput.value = question
}

const submitQuestion = () => {
  if (!questionInput.value.trim()) return

  answerItems.value.unshift({
    id: Date.now(),
    numero: String(answerItems.value.length + 1),
    texto: questionInput.value.trim(),
    pagina: 'Pag 1',
  })

  questionInput.value = ''
  detailInput.value = ''
}
</script>

<template>
  <section class="assistant-detail-page">
    <h1>Asistente</h1>

    <article class="project-hero">
      <div class="folder">
        <img :src="IconCarpeta" alt="Carpeta" />
      </div>
      <div>
        <p class="label pink">Proyecto</p>
        <strong>Construccion Tinglado RSAT-1 BUCH-ORURO</strong>
      </div>
      <div>
        <p class="label blue">Lugar</p>
        <strong>Oruro</strong>
      </div>
      <div>
        <p class="label blue">Codigo identificador</p>
        <strong>789945661-0</strong>
      </div>
      <div>
        <p class="label blue">Año</p>
        <strong>2019</strong>
      </div>
      <span class="status">Disponible</span>
    </article>

    <div class="qa-grid">
      <section class="qa-card question-card">
        <h2>PREGUNTAS</h2>

        <button
          v-for="question in quickQuestions"
          :key="question"
          class="quick-question"
          type="button"
          @click="applyQuickQuestion(question)"
        >
          <span class="dot"></span>
          <span>{{ question }}</span>
        </button>

        <input
          v-model="questionInput"
          class="input-box"
          type="text"
          placeholder="Buscar Invetario o Indice"
        />

        <textarea v-model="detailInput" class="input-box multiline" placeholder=""></textarea>

        <div class="actions-row">
          <button class="send-btn" type="button" @click="submitQuestion">Enviar</button>
        </div>
      </section>

      <section class="qa-card answer-card">
        <h2>Respuestas</h2>

        <article v-for="item in answerItems" :key="item.id" class="answer-item">
          <div class="number-pill">{{ item.numero }}</div>
          <p>{{ item.texto }}</p>
          <div class="page-pill">{{ item.pagina }}</div>
        </article>

        <div v-if="answerItems.length === 0" class="empty-state">
          Sin respuestas por el momento.
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped lang="scss">
.assistant-detail-page {
  padding: 0.6rem 1rem 1rem;
  min-height: 100%;
  background: #d7dae1;
}

h1 {
  margin: 0 0 0.8rem;
  color: #293564;
  font-size: clamp(2rem, 3vw, 2.9rem);
  font-weight: 800;
}

.project-hero {
  display: grid;
  grid-template-columns: 56px 1.6fr 0.8fr 1fr 0.5fr auto;
  gap: 1rem;
  align-items: center;
  background: #f2f2f3;
  border-radius: 18px;
  padding: 0.9rem 0.85rem;
  margin-bottom: 0.85rem;
}

.label {
  margin: 0;
  font-size: 0.75rem;
}

.label.pink {
  color: #d78caf;
}

.label.blue {
  color: #7f9ad0;
}

.project-hero strong {
  color: #22242d;
  font-size: 1rem;
  line-height: 1.2;
}

.folder {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  background: #f1deaa;
  display: grid;
  place-items: center;
}

.folder img {
  width: 26px;
}

.status {
  justify-self: end;
  min-width: 136px;
  min-height: 40px;
  border-radius: 999px;
  background: #51cb3d;
  color: #e7ffe4;
  display: grid;
  place-items: center;
  font-weight: 700;
}

.qa-grid {
  display: grid;
  grid-template-columns: minmax(320px, 390px) minmax(420px, 1fr);
  gap: 1rem;
  align-items: stretch;
}

.qa-card {
  border: 3px solid #1e1f25;
  border-radius: 18px;
  background: #ececef;
  padding: 1rem;
  min-height: clamp(380px, 56vh, 400px);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.qa-card h2 {
  margin: 0;
  color: #1a173e;
  font-size: clamp(1.7rem, 2.7vw, 2.6rem);
  font-weight: 800;
}

.quick-question {
  width: 100%;
  min-height: 52px;
  border: 0;
  border-radius: 12px;
  background: #d6d4e3;
  color: #1a173e;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0 1rem;
  font-size: 1.15rem;
  font-weight: 700;
  text-align: left;
}

.dot {
  width: 13px;
  height: 13px;
  border-radius: 999px;
  background: #71c255;
  flex-shrink: 0;
}

.input-box {
  border: 0;
  border-radius: 12px;
  background: #d6d4e3;
  min-height: 52px;
  padding: 0 1rem;
  color: #1a173e;
  font-size: 1.1rem;
  font-weight: 700;
}

.input-box::placeholder {
  color: #1a173e;
  opacity: 1;
}

.multiline {
  padding-top: 0.5rem;
  resize: none;
}

.actions-row {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
}

.send-btn {
  border: 0;
  border-radius: 999px;
  background: #51cb3d;
  color: white;
  min-width: 140px;
  min-height: 46px;
  padding: 0.65rem 1.4rem;
  font-size: 1.15rem;
  font-weight: 700;
}

.answer-card {
  padding-bottom: 1rem;
  overflow-y: auto;
}

.answer-item {
  background: #f5f5f5;
  border-radius: 14px;
  min-height: 56px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 0.8rem;
  padding: 0 0.8rem;
}

.number-pill {
  min-width: 35px;
  height: 35px;
  border-radius: 8px;
  background: #f1e6c9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1e1f25;
  font-size: 1.1rem;
  font-weight: 800;
}

.answer-item p {
  margin: 0;
  color: #323238;
  font-size: 1.05rem;
  font-weight: 700;
}

.page-pill {
  min-width: 72px;
  height: 35px;
  border-radius: 999px;
  background: #f1e6c9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #34353a;
  font-size: 0.84rem;
  font-weight: 800;
}

.empty-state {
  margin-top: 0.5rem;
  color: #666678;
  font-size: 1rem;
}

@media (max-width: 1100px) {
  .qa-grid {
    grid-template-columns: 1fr;
  }

  .project-hero {
    grid-template-columns: 1fr;
    gap: 0.65rem;
  }

  .status {
    justify-self: start;
  }

  .qa-card {
    min-height: 360px;
  }
}
</style>
