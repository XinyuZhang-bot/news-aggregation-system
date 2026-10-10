<template>
    <div id="app" :style="{paddingTop: isStandaloneAuthPage ? '0px' : '113px'}">
        <page_header v-if="!isStandaloneAuthPage"/>
        <div class="space" v-if="!isStandaloneAuthPage"/>
        <transition name="fade-transform" mode="out-in">
            <router-view :key="$route.fullPath"/>
        </transition>
        <page_footer v-if="!isStandaloneAuthPage"/>
		<div class="back_top" v-if="showBackTop" @click="scrollToTop"><i class="el-icon-upload2"></i></div>
    </div>
</template>

<style lang='less'>
    @import "../public/css/base.css";
    @import "../public/css/theme.css";
    html,
    body {
      height: 100%;
      width: 100%;
    }

    #app {
      width: 100%;
      height: 100%;
    }

    .page-item.active .page-link {
        background-color: var(--color_primary) !important;
        border-color: var(--color_primary) !important;
    }

    .btn-outline-primary {
        color: var(--color_primary) !important;
        border-color: var(--color_primary) !important;
    }

    //放大镜
    .mouse-cover-canvas {
        position: absolute;
        left: calc(50% - 6rem) !important;
        top: 8rem !important;
    }

    body {
        background-color: #F4F7F9 !important;
        font-family: auto !important;
    }

    [class="col-"] {
        padding: 0;
    }

    .space {
        // height: 5rem;
    }

    .page_header {
        position: fixed;
        top: 0;
        z-index: 1000;
        width: 100%;
    }

    a {
        color: inherit !important;
        text-decoration: none;
        -webkit-transition: all 0.3s ease 0s;
        -o-transition: all 0.3s ease 0s;
        transition: all 0.3s ease 0s;
    }

    a:hover {
        text-decoration: none !important;
        /*color: var(--color_primary) !important;*/
        color: #909399 !important;
    }

    .toast {
        opacity: 1 !important;
        min-width: 200px;
    }

    .b-toaster-top-right {
        position: absolute;
        top: 10rem;
        left: 50%;
        transform: translate(-50%);
    }

    figure,
    p,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    ul,
    li {
        margin: 0;
        padding: 0;
    }

    .fade-transform-leave-active,
    .fade-transform-enter-active {
        transition: all 0.5s;
    }

    .fade-transform-enter {
        opacity: 0;
        transform: translateX(-30px);
    }

    .fade-transform-leave-to {
        opacity: 0;
        transform: translateX(30px);
    }
	.back_top {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 30px;
		height: 30px;
		font-size: 20px;
		font-weight: 700;
		position: fixed;
		bottom: 100px;
		right: 50px;
		border-radius: 30px;
		background-color: #fff;
		cursor: pointer;
		z-index: 8;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
	}
	
	@import "../public/css/diy.css";
</style>
<script>
export default {
  data() {
      return {
        showBackTop: false
      }
  },
  computed: {
  	isQrcode() {
      return this.$route.path.includes('/qrcodeDetails')
    },
    isStandaloneAuthPage() {
      const p = this.$route.path || ''
      return (
        p.includes('/qrcodeDetails') ||
        p === '/account/login' ||
        p === '/account/forgot' ||
        p === '/account/register'
      )
    }
  },
  mounted() {
      window.addEventListener('scroll', this.handleScroll)
  },
  methods: {
      handleScroll() {
        this.showBackTop = window.scrollY > 400
      },
      scrollToTop() {
        window.scrollTo({
          top: 0,
          behavior:'smooth'
        })
      }
  },
  beforeDestroy() {
      window.removeEventListener('scroll', this.handleScroll)
  },
  watch: {
    $route(to, from) {
      let currentPath = window.location.hash.slice(1)
      if (this.$route.path !== currentPath) {
        this.$router.push(currentPath)
      }
    }
  }
}
</script>