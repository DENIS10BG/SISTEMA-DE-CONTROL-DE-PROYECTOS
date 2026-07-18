<script setup>
import PanelHeader from '@/components/panel/PanelHeader.vue'
import PanelSidebar from '@/components/panel/PanelSidebar.vue'
import PanelFooter from '@/components/panel/PanelFooter.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="panel-layout">
    <PanelHeader />

    <div class="panel-body">
      <PanelSidebar />

      <main class="panel-content">
        <RouterView />
      </main>
    </div>

    <PanelFooter />
  </div>
</template>

<style scoped lang="scss">
.panel-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #eceff3;
}

.panel-body {
  flex: 1;
  display: grid;
  grid-template-columns: 230px 1fr;
  min-height: 0;
}

.panel-content {
  min-width: 0;
  min-height: 0;
}

@media (max-width: 900px) {
  .panel-body {
    grid-template-columns: 1fr;
  }
}
</style>
