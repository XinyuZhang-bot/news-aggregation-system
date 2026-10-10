<template>
  <div class="page_search search_index">
    <div class="warp search-page-warp">
      <div class="container">
        <div class="row">
          <div class="col-12 col-lg-8 main-search-col">
            <div class="card_result_search card_result_search--jd">
              <div class="search-result-heading" role="heading" aria-level="1">
                <div class="search-result-heading__row">
                  <span class="search-result-heading__label">搜索结果</span>
                  <span class="search-result-heading__dot" aria-hidden="true">·</span>
                  <span class="search-result-heading__meta">关键词 <mark class="search-result-heading__kw">{{ query.word || "—" }}</mark></span>
                </div>
              </div>

              <list_result_search
                v-if="$check_action('/article/list', 'get') && result_article && result_article.length"
                :list="result_article"
                title="热点专题"
                source_table="article"
                :keyword="query.word"
              />

              <list_result_search
                v-if="$check_action('/news_information/list', 'get') && result_news_information_news_headlines && result_news_information_news_headlines.length"
                :list="result_news_information_news_headlines"
                title="新闻资讯"
                source_table="news_information"
                :keyword="query.word"
              />

              <div
                v-if="result_news_information_news_headlines && result_news_information_news_headlines.length && newsCount > newsSize"
                class="search-pager-wrap"
              >
                <b-pagination
                  v-model="newsPage"
                  :total-rows="newsCount"
                  :per-page="newsSize"
                  align="center"
                  @change="onNewsPageChange"
                />
              </div>

              <div v-if="!hasAnyResult" class="no_search_result">
                没有找到与「{{ query.word }}」相关的内容
              </div>
            </div>
          </div>

          <div class="col-12 col-lg-4 sidebar-search-col">
            <div class="search-hot-card">
              <h3 class="search-hot-card__title">新闻推荐</h3>
              <router-link
                v-for="(h, i) in hotRecommend"
                :key="'hot-' + (h.news_information_id != null ? h.news_information_id : i)"
                class="search-hot-item"
                :to="'/news_information/details?news_information_id=' + h.news_information_id"
              >
                <div class="search-hot-item__text">
                  <div class="search-hot-item__t">{{ h.news_headlines || "无标题" }}</div>
                  <div class="search-hot-item__m">
                    发布日期：{{ formatHotRelative(h) }}<span class="meta-gap"></span>浏览量：{{ formatHotViews(h.hits) }}
                  </div>
                </div>
              </router-link>
              <div v-if="!hotRecommend.length" class="search-hot-empty">暂无推荐</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import mixin from "../../mixins/page.js";
import list_result_search from "../../components/diy/list_result_search.vue";

export default {
  mixins: [mixin],
  data() {
    return {
      query: {
        word: "",
      },
      result_article: [],
      result_news_information_news_headlines: [],
      newsPage: 1,
      newsSize: 10,
      newsCount: 0,
      hotRecommend: [],
    };
  },
  methods: {
    get_article() {
      if (!this.query.word) {
        this.result_article = [];
        return;
      }
      this.$get(
        "~/api/article/get_list",
        { page: 1, size: 10, title: this.query.word },
        (json) => {
          if (json.result) {
            this.result_article = json.result.list || [];
          }
        }
      );
    },
    get_news_information_news_headlines() {
      if (!this.query.word) {
        this.result_news_information_news_headlines = [];
        this.newsCount = 0;
        return;
      }
      const url = "~/api/news_information/get_list";
      const params = {
        page: this.newsPage,
        size: this.newsSize,
        news_headlines: this.query.word,
      };
      this.$get(url, params, (json) => {
        if (json.result) {
          const list = json.result.list || [];
          list.forEach((o) => {
            o.title = o.news_headlines;
          });
          this.result_news_information_news_headlines = list;
          this.newsCount = json.result.count != null ? json.result.count : list.length;
        }
      });
    },
    get_hot_recommend() {
      this.$get(
        "~/api/news_information/get_list",
        { page: 1, size: 8, orderby: "hits desc" },
        (json) => {
          if (json.result && json.result.list) {
            this.hotRecommend = json.result.list;
          } else {
            this.hotRecommend = [];
          }
        }
      );
    },
    /** 侧栏浏览量：小数字用整数，过万仍用「万」 */
    formatHotViews(n) {
      const v = Number(n) || 0;
      if (v >= 10000) {
        const w = v / 10000;
        const t = w >= 10 ? w.toFixed(0) : w.toFixed(1).replace(/\.0$/, "");
        return t + "万";
      }
      return String(Math.floor(v));
    },
    formatHotRelative(h) {
      const val = h.publication_date || h.create_time;
      if (!val) {
        return "—";
      }
      const t = new Date(val).getTime();
      if (Number.isNaN(t)) {
        return String(val).slice(0, 10);
      }
      const sec = Math.floor((Date.now() - t) / 1000);
      if (sec < 60) {
        return "刚刚";
      }
      if (sec < 3600) {
        const m = Math.max(1, Math.floor(sec / 60));
        return m === 1 ? "一分钟前" : m + "分钟前";
      }
      if (sec < 86400) {
        const h0 = Math.floor(sec / 3600);
        return h0 === 1 ? "一小时前" : h0 + "小时前";
      }
      if (sec < 172800) {
        return "昨天";
      }
      if (sec < 86400 * 7) {
        const d = Math.floor(sec / 86400);
        const cn = { 2: "两", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七" };
        if (cn[d]) {
          return cn[d] + "天前";
        }
        return d + "天前";
      }
      try {
        return this.$toTime(val, "yyyy-MM-dd");
      } catch (e) {
        return String(val).slice(0, 10);
      }
    },
    reloadSearch() {
      this.newsPage = 1;
      this.get_article();
      this.get_news_information_news_headlines();
      this.get_hot_recommend();
    },
    onNewsPageChange() {
      this.get_news_information_news_headlines();
    },
  },
  components: { list_result_search },
  computed: {
    hasAnyResult() {
      return (
        (this.result_article && this.result_article.length) ||
        (this.result_news_information_news_headlines &&
          this.result_news_information_news_headlines.length)
      );
    },
  },
  created() {
    this.query.word = this.$route.query.word || "";
  },
  mounted() {
    this.reloadSearch();
  },
  watch: {
    $route() {
      $.push(this.query, this.$route.query);
      this.reloadSearch();
    },
  },
};
</script>

<style scoped>
.search-page-warp {
  padding-top: 16px;
  padding-bottom: 32px;
}

.main-search-col {
  margin-bottom: 24px;
}

.card_result_search--jd {
  background: #fff;
  border-radius: 10px;
  padding: 18px 20px 22px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

/* 独立类名，避免 public/css/diy.css 中 .title:before/after 花边图 */
.search-result-heading {
  margin: 0 0 18px;
  padding: 12px 14px;
  background: linear-gradient(105deg, #fff6f6 0%, #fff 42%, #fafafa 100%);
  border: 1px solid #f0e6e6;
  border-radius: 10px;
  border-left: 4px solid #e4393c;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85);
}

.search-result-heading__row {
  display: flex;
  flex-wrap: nowrap;
  align-items: baseline;
  gap: 8px;
  min-width: 0;
  width: 100%;
  font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  white-space: nowrap;
  overflow: hidden;
}

.search-result-heading__label {
  flex-shrink: 0;
  font-size: 17px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: 0.04em;
}

.search-result-heading__dot {
  flex-shrink: 0;
  color: #d4d4d4;
  font-weight: 300;
  font-size: 18px;
  line-height: 1;
  user-select: none;
}

.search-result-heading__meta {
  flex: 1;
  min-width: 0;
  font-size: 14px;
  font-weight: 400;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-result-heading__kw {
  display: inline;
  margin: 0 0 0 4px;
  padding: 1px 8px;
  font-size: 14px;
  font-weight: 600;
  font-style: normal;
  color: #e4393c;
  background: rgba(228, 57, 60, 0.08);
  border-radius: 4px;
  vertical-align: baseline;
  border: none;
  -webkit-appearance: none;
  appearance: none;
}

@media (max-width: 575px) {
  .search-result-heading__row {
    font-size: 13px;
  }
  .search-result-heading__label {
    font-size: 15px;
  }
  .search-result-heading__meta {
    font-size: 12px;
  }
  .search-result-heading__kw {
    font-size: 12px;
  }
}

.search-pager-wrap {
  margin-top: 20px;
  padding-top: 8px;
}

.search-pager-wrap >>> .pagination {
  margin-bottom: 0;
}

.search-pager-wrap >>> .page-item.active .page-link {
  background-color: #e4393c;
  border-color: #e4393c;
}

.search-pager-wrap >>> .page-link {
  color: #e4393c;
}

.no_search_result {
  padding: 28px 16px;
  text-align: center;
  color: #909399;
  font-size: 15px;
  border: 1px dashed #dcdfe6;
  border-radius: 8px;
  margin-top: 16px;
}

.sidebar-search-col {
  margin-bottom: 24px;
}

.search-hot-card {
  background: #fff;
  border-radius: 10px;
  padding: 16px 14px 18px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 88px;
}

.search-hot-card__title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
  color: #222;
}

.search-hot-item {
  display: block;
  margin-bottom: 14px;
  text-decoration: none;
  color: inherit;
}

.search-hot-item:last-of-type {
  margin-bottom: 0;
}

.search-hot-item:hover {
  text-decoration: none;
  color: #e4393c;
}

.search-hot-item__text {
  min-width: 0;
}

.search-hot-item__t {
  font-size: 13px;
  line-height: 1.45;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.search-hot-item:hover .search-hot-item__t {
  color: #e4393c;
}

.search-hot-item__m {
  font-size: 12px;
  color: #999;
  margin-top: 6px;
  line-height: 1.5;
}

.search-hot-item__m .meta-gap {
  display: inline-block;
  width: 1em;
}

.search-hot-empty {
  font-size: 13px;
  color: #bbb;
  text-align: center;
  padding: 12px 0;
}
</style>
