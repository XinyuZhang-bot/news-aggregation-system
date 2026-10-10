<template>
  <div class="list_result_search">
    <!-- 热点专题（文章）：大图卡片 + 关键词高亮 -->
    <template v-if="source_table === 'article' && list && list.length">
      <div class="section-head">
        <span class="section-bar" aria-hidden="true"></span>
        <h2 class="section-title">{{ title }}</h2>
      </div>
      <div class="article-hot-wrap">
        <router-link
          v-for="(o, i) in list"
          :key="'art-' + i"
          class="hot-search-card"
          :to="'/article/details?article_id=' + o.article_id"
        >
          <div class="hot-search-card__media">
            <span class="tag-hot">热点</span>
            <img
              :src="fullArticleImg(o)"
              v-default-img="'../../../public/img/default.png'"
              alt=""
            />
          </div>
          <div class="hot-search-card__body">
            <h3 class="hot-search-card__title" v-html="highlightText(o.title || o.display_title || '')"></h3>
            <div class="hot-search-card__meta">
              <span><b-icon icon="clock" class="ico" />{{ formatDate(o.create_time) }}</span>
              <span><b-icon icon="eye" class="ico" />{{ formatHits(o.hits) }}</span>
            </div>
          </div>
        </router-link>
      </div>
    </template>

    <!-- 新闻资讯：无图列表 + 摘要高亮 -->
    <template v-else-if="source_table === 'news_information' && list && list.length">
      <div class="section-head">
        <span class="section-bar" aria-hidden="true"></span>
        <h2 class="section-title">{{ title }}</h2>
      </div>
      <div class="news-search-list">
        <router-link
          v-for="(o, i) in list"
          :key="'news-' + (o.news_information_id != null ? o.news_information_id : i)"
          class="news-search-row"
          :to="'/news_information/details?news_information_id=' + o.news_information_id"
        >
          <div class="news-search-row__main">
            <h3 class="news-search-row__title" v-html="highlightText(o.news_headlines || o.display_title || '')"></h3>
            <span v-if="o.news_categories" class="news-cat">{{ o.news_categories }}</span>
            <div class="news-search-row__meta">
              <span>{{ formatDate(o.publication_date || o.create_time) }}</span>
              <span class="dot">·</span>
              <span>{{ formatHits(o.hits) }}</span>
            </div>
            <p class="news-search-row__excerpt" v-html="highlightText(newsExcerpt(o))"></p>
            <span class="news-search-row__more">阅读全文 &gt;</span>
          </div>
        </router-link>
      </div>
    </template>

    <!-- 其它表：保留简洁列表（若仍被引用） -->
    <template v-else-if="list && list.length">
      <div class="section-head section-head--plain">
        <span class="section-bar" aria-hidden="true"></span>
        <h2 class="section-title">{{ title }}</h2>
      </div>
      <div class="list_result list_result--fallback">
        <router-link
          v-for="(o, i) in list"
          :key="'fb-' + i"
          :to="fallbackLink(o)"
          class="item item--simple"
        >
          <div class="title">{{ i + 1 }}. {{ o.display_title || o.title }}</div>
        </router-link>
      </div>
    </template>

    <div v-else-if="showEmpty" class="no_result">没有找到{{ title }}相关内容</div>
  </div>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      default() {
        return [];
      },
    },
    title: {
      type: String,
      default: "",
    },
    source_table: {
      type: String,
      default: "",
    },
    keyword: {
      type: String,
      default: "",
    },
    showEmpty: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    escapeRegExp(string) {
      return String(string).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    },
    highlightText(text) {
      const raw = text == null ? "" : String(text);
      const kw = (this.keyword || "").trim();
      if (!kw) {
        return this.escapeHtml(raw);
      }
      const plain = this.stripHtml(raw);
      const regex = new RegExp("(" + this.escapeRegExp(kw) + ")", "gi");
      const esc = this.escapeHtml(plain);
      return esc.replace(regex, '<mark class="kw-hit">$1</mark>');
    },
    escapeHtml(s) {
      return String(s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    },
    stripHtml(s) {
      if (s == null || s === "") {
        return "";
      }
      let t = String(s).replace(/<[^>]+>/g, " ");
      t = t.replace(/\[SOURCE_URL:\][\s\S]*?(\[SOURCE_URL:\]|$)/g, " ");
      return t.replace(/\s+/g, " ").trim();
    },
    formatHits(n) {
      const v = Number(n) || 0;
      if (v >= 10000) {
        const w = v / 10000;
        const t = w >= 10 ? w.toFixed(0) : w.toFixed(1).replace(/\.0$/, "");
        return t + "万";
      }
      return String(v);
    },
    formatDate(val) {
      if (!val) {
        return "";
      }
      try {
        return this.$toTime(val, "yyyy-MM-dd");
      } catch (e) {
        return String(val).slice(0, 10);
      }
    },
    fullArticleImg(o) {
      const u = o.img || o.picture || "";
      return u ? this.$fullUrl(u) : "";
    },
    newsExcerpt(o) {
      const max = 160;
      let t = this.stripHtml(o.news_description || "");
      if (!t) {
        t = this.stripHtml(o.news_body || "");
      }
      if (t.length > max) {
        return t.slice(0, max) + "…";
      }
      return t;
    },
    fallbackLink(o) {
      const idKey = this.source_table + "_id";
      const id = o[idKey];
      return "/" + this.source_table + "/details?" + idKey + "=" + id;
    },
  },
};
</script>

<style scoped>
.section-head {
  display: flex;
  align-items: center;
  margin: 8px 0 18px;
  padding: 0 2px;
}

.section-bar {
  display: inline-block;
  width: 4px;
  height: 18px;
  background: #e4393c;
  border-radius: 2px;
  margin-right: 10px;
  flex-shrink: 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #222;
  margin: 0;
  letter-spacing: 0.02em;
}

.article-hot-wrap {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px 20px;
  margin-bottom: 28px;
}

@media (max-width: 767px) {
  .article-hot-wrap {
    grid-template-columns: 1fr;
  }
}

.hot-search-card {
  display: block;
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #eee;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hot-search-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
}

.hot-search-card__media {
  position: relative;
  height: 160px;
  background: #f5f5f5;
}

.hot-search-card__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tag-hot {
  position: absolute;
  left: 10px;
  top: 10px;
  z-index: 1;
  background: #e4393c;
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 3px;
  font-weight: 600;
}

.hot-search-card__body {
  padding: 12px 14px 14px;
}

.hot-search-card__title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.45;
  margin: 0 0 10px;
  color: #222;
}

.hot-search-card__title >>> .kw-hit,
.news-search-row__title >>> .kw-hit,
.news-search-row__excerpt >>> .kw-hit {
  background: transparent;
  color: #ff6600;
  font-weight: 700;
  padding: 0 1px;
}

.hot-search-card__meta {
  font-size: 13px;
  color: #999;
  display: flex;
  gap: 16px;
}

.hot-search-card__meta .ico {
  margin-right: 4px;
  vertical-align: -0.1em;
}

.news-search-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.news-search-row {
  display: block;
  padding: 14px 16px;
  background: #fafafa;
  border: none;
  border-radius: 8px;
  border-left: 3px solid #e8e8e8;
  text-decoration: none;
  color: inherit;
  transition: background 0.2s, border-left-color 0.2s;
}

.news-search-row:hover {
  background: #fff5f5;
  border-left-color: #e4393c;
  text-decoration: none;
  color: inherit;
}

.news-search-row__main {
  width: 100%;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.news-search-row__title {
  font-size: 17px;
  font-weight: 600;
  margin: 0 0 8px;
  line-height: 1.45;
  color: #222;
}

.news-cat {
  display: inline-block;
  font-size: 12px;
  color: #409eff;
  background: rgba(64, 158, 255, 0.1);
  padding: 2px 8px;
  border-radius: 3px;
  margin-bottom: 8px;
}

.news-search-row__meta {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.news-search-row__meta .dot {
  margin: 0 4px;
}

.news-search-row__excerpt {
  font-size: 14px;
  color: #555;
  line-height: 1.65;
  margin: 0 0 10px;
  width: 100%;
}

.news-search-row__more {
  font-size: 14px;
  color: #e4393c;
  font-weight: 500;
}

.list_result--fallback .item--simple {
  display: block;
  padding: 10px 12px;
  margin-bottom: 8px;
  border: 1px solid #eee;
  border-radius: 6px;
  color: #333;
  text-decoration: none;
}

.list_result--fallback .item--simple:hover {
  background: #fafafa;
  text-decoration: none;
  color: #e4393c;
}

.no_result {
  margin: 10px 0;
  color: #909399;
  font-size: 14px;
}
</style>
