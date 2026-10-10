<template>
  <footer class="page_footer mall-footer">
    <div class="mall-footer__main">
      <div class="container mall-footer__inner">
        <div class="row mall-footer__row">
          <div class="col-12">
            <div class="mall-footer__grid">
              <div class="mall-footer__col mall-footer__brand">
                <div class="mall-footer__brand-row">
                  <span class="mall-footer__logo-mark" aria-hidden="true">N</span>
                  <span class="mall-footer__site-name">新闻聚合系统</span>
                </div>
                <p class="mall-footer__desc">
                  汇聚全球热点资讯，为您提供及时、准确、全面的新闻报道
                </p>
              </div>

              <div class="mall-footer__col">
                <h3 class="mall-footer__h">快速链接</h3>
                <ul class="mall-footer__list">
                  <li>
                    <router-link to="/">首页</router-link>
                  </li>
                  <li>
                    <router-link to="/news_information/list">新闻资讯</router-link>
                  </li>
                  <li>
                    <router-link to="/news_information/recommend">猜你喜欢</router-link>
                  </li>
                  <li>
                    <router-link to="/article/list">热点专题</router-link>
                  </li>
                  <li>
                    <router-link to="/notice/list">最新公告</router-link>
                  </li>
                </ul>
              </div>

              <div class="mall-footer__col">
                <h3 class="mall-footer__h">关于我们</h3>
                <ul class="mall-footer__list mall-footer__list--plain">
                  <li>公司简介</li>
                  <li>联系方式</li>
                  <li>加入我们</li>
                  <li>隐私政策</li>
                </ul>
              </div>

              <div class="mall-footer__col">
                <h3 class="mall-footer__h">联系我们</h3>
                <ul class="mall-footer__contact">
                  <li>
                    <b-icon icon="geo-alt" class="mall-footer__ico" />
                    <span>陕西省汉中市陕西理工大学</span>
                  </li>
                  <li>
                    <b-icon icon="telephone" class="mall-footer__ico" />
                    <span>400-123-4567</span>
                  </li>
                  <li>
                    <b-icon icon="envelope" class="mall-footer__ico" />
                    <span>contact@news.com</span>
                  </li>
                </ul>
              </div>
            </div>

            <div class="mall-footer__legal">
              <p class="mall-footer__copy">
                © 2026 新闻聚合系统 版权所有 | 京ICP备12345678号
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import mixin from "@/mixins/component.js";

export default {
  mixins: [mixin],
  components: {},
  data() {
    return {};
  },
  methods: {},
  created() {},
};
</script>

<style scoped>
.page_footer.mall-footer {
  position: relative;
  overflow: visible;
  height: auto !important;
  min-height: 0;
  margin-top: 0;
  background: #1a1a1a !important;
  font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial,
    sans-serif;
}

.page_footer.mall-footer::before {
  display: none !important;
  content: none !important;
}

.mall-footer__main {
  background: #1a1a1a;
  color: #999;
  padding: 3rem 0 1.25rem;
}

.mall-footer__inner {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
}

.mall-footer__row {
  margin: 0 !important;
}

.mall-footer__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 2rem 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.mall-footer__h {
  margin: 0 0 1rem;
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  line-height: 1.3;
}

.mall-footer__brand-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.mall-footer__logo-mark {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(145deg, #e4393c, #ff6b6b);
  color: #fff;
  font-weight: 800;
  font-size: 1.15rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.mall-footer__site-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}

.mall-footer__desc {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.65;
  color: #a3a3a3;
  max-width: 22rem;
}

.mall-footer__list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.mall-footer__list li {
  margin-bottom: 0.65rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.mall-footer__list a {
  color: #a3a3a3 !important;
  text-decoration: none !important;
  transition: color 0.2s;
}

.mall-footer__list a:hover {
  color: #e4393c !important;
}

.mall-footer__list--plain li {
  color: #a3a3a3;
  cursor: default;
}

.mall-footer__contact {
  list-style: none;
  margin: 0;
  padding: 0;
}

.mall-footer__contact li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  line-height: 1.55;
  color: #a3a3a3;
}

.mall-footer__ico {
  flex-shrink: 0;
  margin-top: 2px;
  color: #888;
  font-size: 1rem;
}

.mall-footer__legal {
  padding-top: 1.25rem;
  text-align: center;
}

.mall-footer__copy {
  margin: 0;
  font-size: 0.8rem;
  color: #777;
  line-height: 1.6;
}

@media (max-width: 992px) {
  .mall-footer__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 576px) {
  .mall-footer__grid {
    grid-template-columns: 1fr;
  }

  .mall-footer__main {
    padding: 2rem 0 1rem;
  }
}
</style>
