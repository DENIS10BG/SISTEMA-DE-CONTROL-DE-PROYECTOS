<template>
  <header class="topbar">
    <div class="spacer"></div>
    <div class="profile-area">
      <button class="top-icon" type="button">⚙</button>
      <button class="top-icon alert" type="button">!</button>
      <div class="profile-text">
        <strong>Maria Roquez</strong>
      </div>
      <div class="avatar">MR</div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.topbar {
  min-height: 78px;
  background: #ffffff;
  border-bottom: 1px solid #e4e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
}

.profile-area {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.top-icon {
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 50%;
  background: #eef2fb;
  color: #7d87a8;
  font-size: 1.2rem;

  &.alert {
    color: #f05f73;
    background: #fff1f4;
  }
}

.profile-text {
  color: #38416a;
  font-size: 1.1rem;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #cfd6e7, #9ca9ca);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 0.95rem;
}
</style>
