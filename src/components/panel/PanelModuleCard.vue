<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  accent: {
    type: String,
    required: true,
  },
  iconColor: {
    type: String,
    required: true,
  },
  to: {
    type: String,
    required: false,
    default: '',
  },
})
</script>

<template>
  <RouterLink v-if="to" class="module-card" :to="to">
    <h3>{{ title }}</h3>
    <div class="module-icon" :style="{ background: accent, color: iconColor }">
      {{ title.charAt(0) }}
    </div>
    <p>{{ description }}</p>
  </RouterLink>

  <article v-else class="module-card">
    <h3>{{ title }}</h3>
    <div class="module-icon" :style="{ background: accent, color: iconColor }">
      {{ title.charAt(0) }}
    </div>
    <p>{{ description }}</p>
  </article>
</template>

<style scoped lang="scss">
.module-card {
  text-decoration: none;
  min-height: 158px;
  background: #ffffff;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 1rem 0.9rem;
  box-shadow: 0 10px 24px rgba(35, 53, 87, 0.08);
  text-align: center;
  border: 0;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(35, 53, 87, 0.12);
  }

  h3 {
    margin: 0;
    font-size: 1.2rem;
    color: #343434;
  }

  p {
    margin: 0;
    color: #8d9bcc;
    font-size: 0.92rem;
    line-height: 1.15;
  }
}

.module-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 1.55rem;
  font-weight: 800;
  margin: 0.8rem 0 1rem;
}
</style>
