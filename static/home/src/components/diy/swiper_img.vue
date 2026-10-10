<template>
  <div class="carousel-hero">
    <b-carousel
      id="carousel"
      v-model="slide"
      class="carousel-hero__bv"
      :interval="4000"
      :controls="false"
      indicators
      background="transparent"
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      <b-carousel-slide v-for="(o, i) in list" :key="i">
        <template #img>
          <div class="carousel-hero__slide">
            <a
              v-if="o[vm.url]"
              class="carousel-hero__media-link"
              target="_blank"
              rel="noopener"
              :href="o[vm.url]"
            >
              <div
                class="swiper-imgs"
                :style="{ backgroundImage: 'url(' + $fullUrl(o[vm.img]) + ')' }"
              ></div>
            </a>
            <div
              v-else
              class="swiper-imgs"
              :style="{ backgroundImage: 'url(' + $fullUrl(o[vm.img]) + ')' }"
            ></div>
            <div class="carousel-hero__shade"></div>
            <div class="carousel-hero__overlay">
              <div class="carousel-hero__content">
                <p class="carousel-hero__kicker">NEWS</p>
                <h2 class="carousel-hero__title">新闻中心</h2>
                <p class="carousel-hero__desc">
                  汇聚全球热点资讯，为您提供及时、准确、全面的新闻报道
                </p>
                <router-link to="/news_information/list" class="carousel-hero__cta">
                  <span class="carousel-hero__cta-label">{{ heroCtaText }}</span>
                  <b-icon icon="arrow-right" class="carousel-hero__cta-arrow" />
                </router-link>
              </div>
            </div>
          </div>
        </template>
      </b-carousel-slide>
    </b-carousel>
  </div>
</template>

<script>
import mixin from "@/mixins/component.js";
export default {
  mixins: [mixin],
  props: {
    list: {
      type: Array,
      default: function () {
        return [];
      },
    },
    vm: {
      type: Object,
      default: function () {
        return {
          img: "img",
          title: "title",
          url: "url",
        };
      },
    },
  },
  data() {
    return {
      slide: 0,
      sliding: null,
      heroCtaText: "浏览最新资讯",
    };
  },
  methods: {
    onSlideStart() {
      this.sliding = true;
    },
    onSlideEnd() {
      this.sliding = false;
    },
  },
};
</script>

<style scoped>
.carousel-hero {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.carousel-hero__bv {
  text-shadow: none;
}

/* 高度随屏幕宽度变化：小屏有下限、大屏有上限，中间段平滑过渡 */
.carousel-hero__slide {
  position: relative;
  min-height: clamp(10rem, 14vw + 8rem, 30rem);
}

.swiper-imgs {
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  height: clamp(10rem, 14vw + 8rem, 30rem);
  display: block;
}

.carousel-hero__media-link {
  display: block;
  height: 100%;
}

.carousel-hero__shade {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.55) 0%,
    rgba(0, 0, 0, 0.25) 45%,
    rgba(0, 0, 0, 0.1) 100%
  );
  pointer-events: none;
}

.carousel-hero__overlay {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  display: flex;
  align-items: center;
  padding: 1.5rem 2rem 2.5rem;
  pointer-events: none;
}

.carousel-hero__content {
  max-width: 26rem;
  pointer-events: auto;
}

.carousel-hero__kicker {
  margin: 0 0 0.35rem;
  font-size: 2rem;
  font-weight: 800;
  font-style: normal;
  letter-spacing: 0.12em;
  color: #fff;
  line-height: 1;
}

.carousel-hero__title {
  margin: 0 0 0.65rem;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}

.carousel-hero__desc {
  margin: 0 0 1.15rem;
  font-size: 14px;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.92);
}

.carousel-hero__cta {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  background: #e4393c;
  color: #fff !important;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 4px 14px rgba(228, 57, 60, 0.45);
  transition: background 0.2s, transform 0.2s;
}

.carousel-hero__cta-label {
  line-height: 1.2;
}

.carousel-hero__cta-arrow {
  font-size: 1rem;
  color: #fff;
}

.carousel-hero__cta:hover {
  background: #c81623;
  color: #fff !important;
  transform: translateY(-1px);
}

/* 轮播指示器靠右、圆点样式 */
.carousel-hero >>> .carousel-indicators {
  justify-content: flex-end;
  margin: 0 1.25rem 0.75rem 0;
}

.carousel-hero >>> .carousel-indicators li {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.45);
  border: none;
}

.carousel-hero >>> .carousel-indicators .active {
  background-color: #fff;
}

.carousel-hero >>> .carousel-control-prev,
.carousel-hero >>> .carousel-control-next {
  display: none !important;
}

@media (max-width: 996px) {
  /* 窄屏略提高 vw 占比，仍用 clamp 避免过高或过低 */
  .swiper-imgs {
    height: clamp(9rem, 36vw + 2rem, 20rem);
  }
  .carousel-hero__slide {
    min-height: clamp(9rem, 36vw + 2rem, 20rem);
  }
  .carousel-hero__overlay {
    padding: 1rem 1.25rem 2rem;
  }
  .carousel-hero__kicker {
    font-size: 1.5rem;
  }
}
</style>
