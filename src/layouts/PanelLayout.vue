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
  height: 100vh;
  display: grid;
  grid-template-rows: 10vh 80vh 10vh;
  background: #eceff3;
  overflow: hidden;
}

.panel-body {
  display: grid;
  grid-template-columns: 252px 1fr;
  height: 80vh;
  min-height: 80vh;
  overflow: hidden;
}

.panel-content {
  min-width: 0;
  min-height: 0;
  overflow: auto;
}

@media (max-width: 900px) {
  .panel-body {
    grid-template-columns: 1fr;
  }
}
</style>
