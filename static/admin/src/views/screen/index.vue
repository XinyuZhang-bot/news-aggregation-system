<template>
  <div class="screen-container">
    <iframe
      v-if="screenAvailable"
      :src="screenUrl"
      frameborder="0"
      style="width: 100%; height: 100vh;"
    ></iframe>
    <div v-else class="screen-fallback">
      <div class="screen-fallback-title">大屏页面暂不可用</div>
      <div class="screen-fallback-desc">
        未检测到 <code>{{ screenUrl }}</code>，请确认已部署大屏静态文件。
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      screenUrl: '/screen/screen.html',
      screenAvailable: true,
    }
  },
  async created() {
    try {
      const res = await fetch(this.screenUrl, { method: 'HEAD' });
      this.screenAvailable = !!(res && res.ok);
    } catch (e) {
      this.screenAvailable = false;
    }
  }
}
</script>

<style scoped>
.screen-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
.screen-fallback {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  background: #f5f7fa;
  color: #606266;
}
.screen-fallback-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 10px;
}
.screen-fallback-desc {
  font-size: 14px;
}
</style>
