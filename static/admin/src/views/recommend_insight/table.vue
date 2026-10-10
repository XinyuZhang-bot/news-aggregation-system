<template>
  <el-main class="table_wrap recommend-insight-page">
    <el-form :model="query" class="form p_4 recommend-filter" label-width="88px">
      <div class="filter-row">
        <el-form-item label="选择用户" class="compact-item">
          <el-select v-model="query.user_id" filterable clearable placeholder="请选择普通用户" style="width: 280px">
            <el-option
              v-for="u in userOptions"
              :key="u.user_id"
              :label="`${u.nickname || u.username}（ID:${u.user_id}）`"
              :value="u.user_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="推荐条数" class="compact-item">
          <el-input-number v-model="query.top_k" :min="5" :max="30" />
        </el-form-item>
        <el-form-item class="compact-item">
          <el-button type="primary" :loading="loading" @click="runAnalysis">分析</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </div>
    </el-form>
    
    <div class="kpi-strip">
      <div class="kpi-card kpi-card--1">
        <div class="kpi-title">已选用户</div>
        <div class="kpi-value">{{ selectedUserLabel || "未选择" }}</div>
      </div>
      <div class="kpi-card kpi-card--2">
        <div class="kpi-title">行为总量</div>
        <div class="kpi-value">{{ summary.behaviorTotal }}</div>
      </div>
      <div class="kpi-card kpi-card--3">
        <div class="kpi-title">推荐样本数</div>
        <div class="kpi-value">{{ recommendationList.length }}</div>
      </div>
      <div class="kpi-card kpi-card--4">
        <div class="kpi-title">分析覆盖率</div>
        <div class="kpi-value">{{ summary.coverage }}%</div>
      </div>
    </div>

    <el-row :gutter="12" class="content-row">
      <el-col :xs="24" :lg="8">
        <div class="panel">
          <div class="panel-title">用户行为构成</div>
          <div class="metric-line"><span>点击（hits）</span><b>{{ summary.hitsCount }}</b></div>
          <div class="metric-line"><span>历史（history）</span><b>{{ summary.historyCount }}</b></div>
          <div class="metric-line"><span>收藏（collect）</span><b>{{ summary.collectCount }}</b></div>
          <div class="metric-line"><span>点赞（praise）</span><b>{{ summary.praiseCount }}</b></div>
        </div>

        <div class="panel" style="margin-top: 12px">
          <div class="panel-title">推荐分类分布</div>
          <div v-if="!query.user_id" class="empty-text">请先选择用户</div>
          <div v-else-if="!analysisDone" class="empty-text">请点击「分析」查看该用户浏览过的新闻分类</div>
          <div v-else-if="viewedCategoryPie.length === 0" class="empty-text">暂无浏览分类数据（该用户尚无资讯点击记录）</div>
          <div v-else class="pie-wrap">
            <doughnutChart
              id="recommend_insight_category_pie"
              :list="viewedCategoryPie"
              title=""
              type="分类"
              :compact-layout="true"
            />
          </div>
          <div v-if="analysisDone && recommendAdviceMessage" class="recommend-advice-box">
            {{ recommendAdviceMessage }}
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :lg="16">
        <div class="panel">
          <div class="panel-title">推荐Top样本</div>
          <el-table :data="recommendationList" border stripe height="460">
            <el-table-column type="index" width="56" label="#" />
            <el-table-column prop="news_information_id" label="ID" width="76" />
            <el-table-column prop="news_headlines" label="新闻标题" min-width="260" show-overflow-tooltip />
            <el-table-column prop="news_categories" label="分类" width="100" />
            <el-table-column prop="hits" label="点击" width="80" />
            <el-table-column label="推荐值" width="100">
              <template slot-scope="scope">
                {{ recommendDisplay(scope.row) }}
              </template>
            </el-table-column>
            <el-table-column label="排序分" width="96">
              <template slot-scope="scope">
                {{ scoreRow(scope.row) }}
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="发布时间" min-width="160">
              <template slot-scope="scope">
                {{ scope.row.create_time ? $toTime(scope.row.create_time, "yyyy-MM-dd hh:mm:ss") : "-" }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </el-main>
</template>

<script>
import mixin from "@/mixins/page.js";
import doughnutChart from "@/components/charts/doughnut_chart";

export default {
  mixins: [mixin],
  components: {
    doughnutChart,
  },
  data() {
    return {
      loading: false,
      query: {
        user_id: "",
        top_k: 15,
      },
      userOptions: [],
      recommendationList: [],
      summary: {
        behaviorTotal: 0,
        hitsCount: 0,
        historyCount: 0,
        collectCount: 0,
        praiseCount: 0,
        coverage: 0,
      },
      categoryStats: [],
      /** 基于 hits 汇总的「浏览过的新闻分类」环形图数据；仅在选择用户并点击分析后加载 */
      viewedCategoryPie: [],
      recommendAdviceMessage: "",
      analysisDone: false,
    };
  },
  computed: {
    selectedUserLabel() {
      if (!this.query.user_id) return "";
      const row = this.userOptions.find((u) => Number(u.user_id) === Number(this.query.user_id));
      return row ? (row.nickname || row.username || `用户${row.user_id}`) : `用户${this.query.user_id}`;
    },
  },
  watch: {
    "query.user_id"() {
      this.analysisDone = false;
      this.viewedCategoryPie = [];
      this.recommendAdviceMessage = "";
      this.recommendationList = [];
      this.categoryStats = [];
      this.summary = {
        behaviorTotal: 0,
        hitsCount: 0,
        historyCount: 0,
        collectCount: 0,
        praiseCount: 0,
        coverage: 0,
      };
    },
  },
  created() {
    this.loadUsers();
  },
  methods: {
    async loadUsers() {
      const res = await this.$get("~/api/user/get_list", {
        page: 1,
        size: 500,
        like: 0,
        user_group: "普通用户",
      });
      const list = (res && res.result && res.result.list) ? res.result.list : [];
      this.userOptions = list.filter(
        (u) =>
          Number(u.user_id) > 0 &&
          String(u.user_group || "").trim() === "普通用户"
      );
      if (
        this.query.user_id &&
        !this.userOptions.some((u) => Number(u.user_id) === Number(this.query.user_id))
      ) {
        this.query.user_id = "";
      }
    },
    async loadViewedCategoryPie(uid) {
      try {
        const res = await this.$get("~/api/user/viewed_news_categories", { user_id: uid }, null);
        const pie = res && res.result;
        this.viewedCategoryPie = Array.isArray(pie) ? pie : [];
      } catch (e) {
        this.viewedCategoryPie = [];
      }
    },
    async runAnalysis() {
      if (!this.query.user_id) {
        this.$message.warning("请先选择普通用户");
        return;
      }
      this.analysisDone = false;
      this.viewedCategoryPie = [];
      this.recommendAdviceMessage = "";
      this.loading = true;
      try {
        const uid = this.query.user_id;
        const topK = Number(this.query.top_k) || 15;

        const [hitsRes, historyRes, collectRes, praiseRes, recommendRes, adviceRes] = await Promise.all([
          this.$get("~/api/hits/count", { source_table: "news_information", user_id: uid, like: 0 }),
          this.$get("~/api/history/count", { source_table: "news_information", user_id: uid, like: 0 }),
          this.$get("~/api/collect/count", { source_table: "news_information", user_id: uid, like: 0 }),
          this.$get("~/api/praise/count", { source_table: "news_information", user_id: uid, status: 1, like: 0 }),
          this.$get("~/api/news_information/get_hits_list", { user_id: uid, top_k: topK, page: 1, size: topK }),
          this.$get("~/api/news_information/recommend_advice", { user_id: uid }),
        ]);

        const toNum = (v) => Number(v || 0);
        const hitsCount = toNum(hitsRes && hitsRes.result);
        const historyCount = toNum(historyRes && historyRes.result);
        const collectCount = toNum(collectRes && collectRes.result);
        const praiseCount = toNum(praiseRes && praiseRes.result);
        const behaviorTotal = hitsCount + historyCount + collectCount + praiseCount;

        this.recommendationList = (recommendRes && recommendRes.result && recommendRes.result.list) ? recommendRes.result.list : [];
        this.summary = {
          behaviorTotal,
          hitsCount,
          historyCount,
          collectCount,
          praiseCount,
          coverage: topK > 0 ? Math.round((this.recommendationList.length / topK) * 100) : 0,
        };

        this.buildCategoryStats();
        await this.loadViewedCategoryPie(uid);
        const advice = adviceRes && adviceRes.result;
        this.recommendAdviceMessage = advice && advice.message ? advice.message : "";
        this.analysisDone = true;
      } finally {
        this.loading = false;
      }
    },
    buildCategoryStats() {
      const catMap = {};
      this.recommendationList.forEach((row) => {
        const key = (row.news_categories || "未分类").trim() || "未分类";
        catMap[key] = (catMap[key] || 0) + 1;
      });
      const total = this.recommendationList.length || 1;
      this.categoryStats = Object.keys(catMap)
        .map((k) => ({
          name: k,
          count: catMap[k],
          percent: Math.round((catMap[k] / total) * 100),
        }))
        .sort((a, b) => b.count - a.count);
    },
    /**
     * 排序分（内部）：推荐列表内同分类条数×8 + 点击量×0.8 + recommend×1.2 + 收藏人数×1.5 + 点赞人数×1
     * （分类条数来自当前 Top-K 推荐样本，用于排序权重）
     */
    scoreRow(row) {
      const toNum = (v) => Number(v || 0);
      const hits = toNum(row.hits);
      const recommend = toNum(row.recommend);
      const collectLen = toNum(row.collect_len);
      const praiseLen = toNum(row.praise_len);
      const cat = (row.news_categories || "未分类").trim() || "未分类";
      const catItem = this.categoryStats.find((x) => x.name === cat);
      const catWeight = catItem ? catItem.count : 0;
      const score = catWeight * 8 + hits * 0.8 + recommend * 1.2 + collectLen * 1.5 + praiseLen;
      return Math.round(score * 100) / 100;
    },
    /**
     * 推荐值（展示列）：按优先级取值
     * ① 若接口字段 recommend_display 为正数 → 用它；
     * ② 否则若 recommend 为正数 → 用它；
     * ③ 否则用排序分 scoreRow（见下式）；
     * ④ 否则兜底 0.08×点击量 + 0.06。
     */
    recommendDisplay(row) {
      const raw = row.recommend_display;
      if (raw !== undefined && raw !== null && raw !== "") {
        const n = Number(raw);
        if (!Number.isNaN(n) && n > 0) return n;
      }
      const r = Number(row.recommend || 0);
      if (r > 0) return Math.round(r * 100) / 100;
      const s = this.scoreRow(row);
      if (s > 0) return s;
      return Math.round((Number(row.hits || 0) * 0.08 + 0.06) * 100) / 100;
    },
    reset() {
      this.query = {
        user_id: "",
        top_k: 15,
      };
      this.recommendationList = [];
      this.categoryStats = [];
      this.viewedCategoryPie = [];
      this.recommendAdviceMessage = "";
      this.analysisDone = false;
      this.summary = {
        behaviorTotal: 0,
        hitsCount: 0,
        historyCount: 0,
        collectCount: 0,
        praiseCount: 0,
        coverage: 0,
      };
    },
  },
};
</script>

<style scoped>
.recommend-insight-page {
  padding: 12px 12px 16px;
  background: #f0f2f5 !important;
  min-height: calc(100vh - 120px);
  box-sizing: border-box;
}
.recommend-filter {
  margin-bottom: 12px;
  padding: 14px 16px 8px !important;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8e8e8;
}
.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
  align-items: center;
}
.compact-item {
  margin-bottom: 8px !important;
}
/* 四块 KPI 单行铺满，中间留白间距 */
.kpi-strip {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  width: 100%;
  box-sizing: border-box;
  gap: 16px;
  margin-bottom: 12px;
}
.kpi-card {
  flex: 1 1 0;
  min-width: 0;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 12px 14px;
  min-height: 88px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.kpi-card--1 {
  border-top: 3px solid #1890ff;
}
.kpi-card--2 {
  border-top: 3px solid #13c2c2;
}
.kpi-card--3 {
  border-top: 3px solid #52c41a;
}
.kpi-card--4 {
  border-top: 3px solid #fa8c16;
}
@media (max-width: 992px) {
  .kpi-strip {
    flex-wrap: wrap;
  }
  .kpi-card {
    flex: 1 1 calc(50% - 8px);
    min-width: 140px;
  }
}
.kpi-title {
  color: #666;
  font-size: 13px;
}
.kpi-value {
  margin-top: 10px;
  color: #1a1a1a;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.35;
  word-break: break-all;
  white-space: normal;
  overflow: visible;
}
.panel {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 14px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.panel-title {
  font-size: 15px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 12px;
}
.pie-wrap {
  height: 280px;
  padding-left: 4px;
  overflow: hidden;
}
.recommend-insight-page ::v-deep .pie_chart {
  width: 100%;
  height: 280px;
}
.recommend-insight-page ::v-deep .el-table th {
  background: #1890ff !important;
  color: #fff !important;
}
.recommend-insight-page ::v-deep .el-table th > .cell {
  color: #fff;
}
.recommend-insight-page ::v-deep .el-table td {
  padding: 8px 0;
  color: #303133;
}
.recommend-insight-page ::v-deep .el-table {
  background: #fff;
}
.metric-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #606266;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.metric-line:last-child {
  border-bottom: 0;
}
.metric-line b {
  color: #1890ff;
  font-weight: 600;
}
.empty-text {
  min-height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
}
.recommend-advice-box {
  margin-top: 12px;
  padding: 12px 14px;
  border: 1px solid #ffc9c9;
  border-radius: 6px;
  background: #fff5f5;
  color: #c45656;
  font-size: 14px;
  line-height: 1.6;
  font-weight: 600;
}
</style>
