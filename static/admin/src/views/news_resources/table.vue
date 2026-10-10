<template>
  <el-main class="bg table_wrap comtabel_t">
    <el-form
      label-position="right"
      :model="query"
      class="form p_4"
      label-width="120"
    >
      <el-row class="rows row1"> </el-row>
      <el-row class="rows row2">
        <el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap search_btns">
          <el-col
            :xs="24"
            :sm="10"
            :lg="8"
            class="search_btn_1 search_btn_wrap_1 btns"
          >
            <el-select
              v-model="selectedSource"
              size="small"
              placeholder="选择爬取来源"
              @change="handleSourceChange"
              style="width: 180px; margin-right: 10px;"
            >
              <el-option
                v-for="item in sourceOptions"
                :key="item.value === '' ? '__all__' : item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <!-- 该项已在后端强制执行（最近几天 + 清洗规则），隐藏前端展示 -->
            <div style="display: none;">
              <el-input-number
                v-model="maxAgeDays"
                size="small"
                :min="1"
                :max="30"
                :step="1"
                controls-position="right"
                style="width: 170px; margin-right: 10px;"
              />
              <span style="font-size: 12px; color: #606266; margin-right: 10px;">
                仅抓最近 N 天新闻
              </span>
            </div>

            <el-button
              v-if="
                $check_action('/news_resources/table', 'del') ||
                  $check_action('/news_resources/view', 'del')
              "
              class="search_btn_del"
              type="danger"
              @click="delInfo()"
              >删除</el-button
            >
            <el-button
              v-if="$check_action('/news_resources/table', 'set')"
              type="primary"
              @click="getSpider()"
              class="search_btn_find"
              :loading="spiderLoading"
              >爬取</el-button
            >
          </el-col>
        </el-col>
      </el-row>
      <el-row class="rows scheduler-row-wrap">
        <el-col :span="24">
          <div class="scheduler-panel">
            <div class="scheduler-title">自动爬取详细设置</div>
            <!-- 移除提示信息展示（按你的要求不再显示红框那段说明） -->
            <div class="scheduler-hint" style="display: none;"></div>
            <div
              v-for="item in schedulerSourceOptions"
              :key="item.value"
              class="scheduler-line"
            >
              <span class="scheduler-label">{{ item.label }}</span>
              <el-switch
                v-model="schedulerDraft[item.value].enabled"
                active-text="开启"
                inactive-text="关闭"
              />
              <span class="scheduler-every">每</span>
              <el-input-number
                v-model="schedulerDraft[item.value].interval_minutes"
                :min="1"
                :max="1440"
                :step="1"
                size="small"
                controls-position="right"
                style="width: 120px;"
              />
              <span class="scheduler-unit">分钟</span>
            </div>
            <div class="scheduler-actions">
              <el-button
                type="primary"
                size="small"
                :loading="schedulerSaving"
                @click="saveSchedulerConfig"
              >
                保存定时设置
              </el-button>
              <el-button size="small" @click="loadSchedulerConfig"
                >重新加载</el-button
              >
            </div>
          </div>
        </el-col>
      </el-row>
      <div class="statistics-info" v-if="statisticsData.total > 0"></div>
    </el-form>
    <el-table
      :data="list"
      @selection-change="selectionChange"
      @sort-change="$sortChange"
      style="width: 100%"
      id="dataTable"
      row-key="news_resources_id"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      :default-expand-all="isExpandAll"
      ref="tableRef"
    >
      <el-table-column fixed type="selection" tooltip-effect="dark" width="55">
      </el-table-column>
      <el-table-column
        prop="title"
        @sort-change="$sortChange"
        label="标题"
        v-if="$check_field('get', 'title')"
        min-width="300"
      >
        <template slot-scope="scope">
          {{ scope.row["title"] }}
        </template>
      </el-table-column>
      <el-table-column
        prop="url"
        @sort-change="$sortChange"
        label="详情链接"
        v-if="$check_field('get', 'url')"
        min-width="300"
      >
        <template slot-scope="scope">
          <a :href="scope.row['url']" target="_blank">{{ scope.row["url"] }}</a>
        </template>
      </el-table-column>
      <el-table-column
        prop="origin"
        @sort-change="$sortChange"
        label="发布来源"
        v-if="$check_field('get', 'origin')"
        min-width="300"
      >
        <template slot-scope="scope">
          {{ scope.row["origin"] }}
        </template>
      </el-table-column>
      <el-table-column
        prop="release_time"
        @sort-change="$sortChange"
        label="发布时间"
        v-if="$check_field('get', 'release_time')"
        min-width="300"
      >
        <template slot-scope="scope">
          {{ scope.row["release_time"] }}
        </template>
      </el-table-column>
      <el-table-column
        prop="content"
        @sort-change="$sortChange"
        label="正文内容"
        v-if="$check_field('get', 'content')"
        min-width="300"
      >
        <template slot-scope="scope">
          {{ scope.row["content"] }}
        </template>
      </el-table-column>

      <el-table-column
        prop="extra"
        @sort-change="$sortChange"
        label="信息"
        min-width="300"
        v-if="hasExtraData"
      >
        <template slot-scope="scope">
          <div
            v-for="(value, key) in JSON.parse(scope.row.extra || '{}')"
            :key="key"
          >
            {{ key }}：{{ value }}
          </div>
        </template>
      </el-table-column>
      <el-table-column
        sortable
        prop="create_time"
        label="创建时间"
        min-width="200"
      >
        <template slot-scope="scope">
          {{ $toTime(scope.row["create_time"], "yyyy-MM-dd hh:mm:ss") }}
        </template>
      </el-table-column>

      <el-table-column
        sortable
        prop="update_time"
        label="更新时间"
        min-width="200"
      >
        <template slot-scope="scope">
          {{ $toTime(scope.row["update_time"], "yyyy-MM-dd hh:mm:ss") }}
        </template>
      </el-table-column>

      <el-table-column
        fixed="right"
        label="操作"
        min-width="200"
        v-if="
          $check_action('/news_resources/table', 'set') ||
            $check_action('/news_resources/view', 'set') ||
            $check_action('/news_resources/view', 'get')
        "
      >
        <template slot-scope="scope">
          <div class="view_a">
            <el-button
              class="e-button el-button--small is-plain el-button--success"
              style="margin: 5px !important;"
              v-if="
                $check_action('/news_resources/table', 'set') ||
                  $check_action('/news_resources/view', 'set') ||
                  $check_action('/news_resources/view', 'get')
              "
              type="success"
              size="small"
              @click="goToNewsInfoAdd(scope.row)"
            >
              <span>详情</span>
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页器 -->
    <div class="mt text_center">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="query.page"
        :page-sizes="[10, 15, 30, 50]"
        :page-size="query.size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="count"
      >
      </el-pagination>
    </div>
    <!-- /分页器 -->
    <el-dialog
      title="重要提醒"
      :visible.sync="showModal"
      width="400px"
      :before-close="closeModal"
    >
      <div style="text-align: center">
        <p style="margin-bottom: 16px; font-size: 16px; color: #333;">
          当前有数据达到预警值！
        </p>
        <p style="color: #666;">{{ message }}</p>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeModal">取消</el-button>
        <el-button type="primary" @click="closeModal">确定</el-button>
      </div>
    </el-dialog>
  </el-main>
</template>
<script>
import mixin from "@/mixins/page.js";
import { resolveSpiderServiceBase } from "@/utils/spiderServiceBase.js";

export default {
  mixins: [mixin],
  components: {},
  data() {
    return {
      statisticsData: {
        total: 0,
      },
      // 弹框
      showModal: false,
      // 获取数据地址
      url_get_list: "~/api/news_resources/get_list",
      url_del: "~/api/news_resources/del?",

      // 字段ID
      field: "news_resources_id",
      // 查询
      query: {
        size: 15,
        page: 1,
        login_time: "",
        create_time: "",
        orderby: `news_resources_id desc`,
      },

      // 数据
      list: [],
      spiderLoading: false,
      maxAgeDays: 3,
      // 来源筛选：空字符串表示“全部来源”
      selectedSource: "",
      sourceOptions: [
        { label: "全部来源", value: "" },
        { label: "腾讯新闻", value: "tencent" },
        { label: "人民网", value: "people" },
        { label: "新华社", value: "xinhuanet" },
        { label: "中国新闻网", value: "chinanews" },
      ],
      spiderServiceBase: "http://127.0.0.1:5001",
      schedulerDraft: {
        tencent: { enabled: false, interval_minutes: 5 },
        people: { enabled: false, interval_minutes: 5 },
        xinhuanet: { enabled: false, interval_minutes: 5 },
        chinanews: { enabled: false, interval_minutes: 5 },
      },
      schedulerSaving: false,
      message: "",
      // 控制展开状态
      isExpandAll: true,
      // 存储展开的行
      expandKeys: [],
      prevSelection: [],
    };
  },
  methods: {
    // 来源切换时同步过滤当前列表
    handleSourceChange() {
      this.query.page = 1;
      const origin = this.getOriginBySource(this.selectedSource);
      if (origin) {
        this.query.origin = origin;
      } else {
        delete this.query.origin;
      }
      this.get_list();
    },
    getOriginBySource(sourceValue) {
      if (sourceValue === "" || sourceValue == null) {
        return "";
      }
      const map = {
        tencent: "腾讯新闻",
        people: "人民网",
        xinhuanet: "新华社",
        chinanews: "中国新闻网",
      };
      return map[sourceValue] || "";
    },
    previewFile(fileName) {
      if (!fileName) {
        return;
      }
      const fileExtension = fileName
        .split(".")
        .pop()
        .toLowerCase();
      if (
        fileExtension == "docx" ||
        fileExtension == "xlsx" ||
        fileExtension == "pptx"
      ) {
        this.$router.push(
          "/filePreview?url=" + fileName + "&type=" + fileExtension,
        );
        return;
      }
      window.open(this.$fullUrl(fileName), "_blank");
    },
    showPreview(file) {
      if (!file) {
        return false;
      }
      let fileType = file
        .split(".")
        .pop()
        .toLowerCase();
      if (fileType == "docx" || fileType == "xlsx" || fileType == "pptx") {
        return true;
      } else {
        return false;
      }
    },
    // 关闭弹框
    closeModal() {
      this.showModal = false;
    },
    /**
     * @description 获取到列表事件
     * @param {Object} res 响应结果
     */
    get_list_after: function get_list_after(res, func, url) {
      let _this = this;
    },

    async delInfo() {
      var list = this.selection;
      if (list.length === 0) {
        this.$message({
          type: "info",
          message: "选择对象不能为空!",
        });
        return;
      }
      for (let i = 0; i < list.length; i++) {
        let type = list[i];
        let res;
      }
      this.$confirm("删除后数据将无法恢复，请确认是否删除？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async () => {
          await this.delAll(list);
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    getSpider() {
      if (!this.selectedSource) {
        this.$message.warning("请先选择具体爬取来源（不能为全部来源）");
        return;
      }
      this.spiderLoading = true;
      const sourceLabel = this.getSourceLabel(this.selectedSource);
      // 后端已强制最近几天+图文清洗；前端隐藏该控制项后，这里固定传参
      const agePart = `&max_age_days=3&ignore_disabled=1&fmt=json`;
      this.$axios
        .get(
          `${this.spiderServiceBase}/spider?search_word=1&source=${encodeURIComponent(
            this.selectedSource,
          )}${agePart}`,
          {},
        )
        .then((res) => {
          this.spiderLoading = false;
          const d = res && res.data;
          let message = "";
          let ntype = "success";
          if (d && typeof d === "object" && !Array.isArray(d) && "fetched" in d) {
            message = `爬取${d.fetched}条数据，本次保留${d.kept}条数据，入库${d.inserted}条数据`;
            if (d.error) {
              message += `（${String(d.error).slice(0, 120)}）`;
            }
            if (d.ok === false) {
              ntype = "warning";
            }
          } else {
            const raw = (res && res.data) != null ? String(res.data) : "";
            message = raw
              ? raw.slice(0, 220)
              : `${sourceLabel} 爬取已完成（未返回统计 JSON，请升级爬虫服务）`;
          }
          this.$notify({
            title: d && d.ok === false ? "爬取异常" : "爬取完毕",
            message: `${sourceLabel}：${message}`,
            type: ntype,
            duration: 7500,
          });
          // 爬取后保持当前来源筛选并刷新列表
          this.handleSourceChange();
        })
        .catch((res) => {
          this.spiderLoading = false;
          console.error(res);
          const body = res && res.response && res.response.data;
          if (body && typeof body === "object" && "fetched" in body) {
            const line = `爬取${body.fetched}条数据，本次保留${body.kept}条数据，入库${body.inserted}条数据`;
            this.$notify({
              title: "爬取失败",
              message: `${sourceLabel}：${line}${body.error ? `（${body.error}）` : ""}`,
              type: "error",
              duration: 8000,
            });
            return;
          }
          const msg = (res && res.message) ? `：${res.message}` : "";
          this.$message.error(`爬取失败，请检查爬虫服务是否启动${msg}`);
        });
    },
    getSourceLabel(sourceValue) {
      const target = this.sourceOptions.find(
        (item) => item.value === sourceValue,
      );
      return target ? target.label : sourceValue;
    },

    goToNewsInfoAdd(row) {
      if (!row) return;
      // Prefill data from `news_resources` -> `news_information` add form.
      const publicationDate = row.release_time
        ? String(row.release_time).slice(0, 10)
        : "";
      const parsedExtra = this.parseExtra(row.extra);
      const inferredCategory = this.getPreferredCategory(row, parsedExtra);
      // 原文链接（用于发布页的“阅读原文”按钮，以及拉取原文含图正文）
      const sourceUrl = (row.url || "").trim();
      const videoUrl = (parsedExtra && parsedExtra.video_url) || "";
      let newsDescription = (row.origin || "").trim();
      if (videoUrl) {
        newsDescription = newsDescription
          ? `${newsDescription} | 视频：${videoUrl}`
          : `视频：${videoUrl}`;
      }
      let initialNewsBody = row.content || "";

      const form = {
        news_information_id: 0,
        news_headlines: row.title || "",
        publication_date: publicationDate,
        news_pictures: "",
        news_categories: inferredCategory,
        news_description: newsDescription,
        news_body: initialNewsBody,
      };
      // Do not rely on relative URL; push with query object to avoid
      // old query params leaking into the target page.
      $.db.set("form", form);
      $.db.set("news_resource_meta", {
        source_url: sourceUrl,
        crawl_time: row.create_time
          ? this.$toTime(row.create_time, "yyyy-MM-dd hh:mm:ss")
          : "",
      });
      this.$router.push({
        path: "/news_information/view",
        query: { news_information_id: 0, like: 0 },
      });
    },
    parseExtra(extra) {
      if (!extra) return {};
      try {
        return typeof extra === "string" ? JSON.parse(extra) : extra;
      } catch (e) {
        return {};
      }
    },
    getPreferredCategory(row, parsedExtra) {
      const fromExtra = (parsedExtra && parsedExtra.category)
        ? String(parsedExtra.category).trim()
        : "";
      if (fromExtra) return this.normalizeCategoryForCurrentSchema(fromExtra);
      return this.normalizeCategoryForCurrentSchema(this.inferNewsCategory(row));
    },
    normalizeCategoryForCurrentSchema(category) {
      const c = String(category || "").trim();
      if (!c) return "";
      return c;
    },
    inferNewsCategory(row) {
      // 回退分类（主路径优先使用 extra.category）
      const title = row.title || "";
      const content = row.content || "";
      const url = String(row.url || "").toLowerCase();
      const raw = `${title} ${content}`;
      const text = raw.toLowerCase();

      const politicsTitle =
        /人民网观点|人民时评|人民网评|新华视点|评论员文章|光明日报|经济日报|求是|学习强国/.test(
          title,
        );
      const politicsUrl =
        url.includes("opinion.people.com.cn") ||
        (url.includes("people.com.cn") && /观点|opinion/.test(url));
      if (politicsTitle || politicsUrl) return "时政";

      if (/军事|国防|军演|演习|战机|导弹|海军|空军|陆军|武器|航母|舰艇|军舰|护卫舰|驱逐舰|潜艇|军售/.test(text))
        return "军事";

      const techStrong =
        /芯片|半导体|大模型|人工智能|算法|量子|专利|航天|卫星|火箭|回旋加速器|同位素|原子能|\bai\b|5g/.test(
          raw,
        );
      const techSoft =
        /科技|科学|技术|科研|研发|研制|实验室|院士|数码|计算机|软件|智能制造/.test(raw);
      const techNoiseOnly =
        /互联网|网络|数字化/.test(raw) &&
        !techStrong &&
        !/科技|科学|技术|科研|芯片|半导体|大模型|人工智能/.test(title);
      if ((techStrong || (techSoft && !techNoiseOnly)) && !politicsTitle) return "科技";

      if (
        /财经|金融|股市|A股|港股|证券|期货|银行|保险|理财|央行|降准|降息|汇率|通胀|上市公司|财报|营收|涨停|收盘|开盘|股指/.test(
          raw,
        )
      ) {
        return "财经";
      }

      const healthStrong =
        /医院|诊疗|疾控|公共卫生|医保|疫苗|临床|诊断|药物|医疗器械|生物医药|核医学|康复|体检|流行病|心理健康/.test(
          raw,
        );
      if (healthStrong) return "健康";

      if (/教育|高考|考研|高校|中小学|招生|课堂|教师/.test(text)) return "教育";

      if (/文学|非遗|博物馆|文物|出版|传统文化|考古|民俗|展览|书法|戏剧|典籍/.test(text))
        return "文化";

      if (/娱乐|电影|电视剧|综艺|明星|票房|艺人|动漫|体育|足球|篮球|奥运|联赛|世界杯|运动员|cba|nba/.test(text))
        return "娱乐";

      if (/外交|联合国|安理会|联大|国际关系|国际局势|外事/.test(text)) return "国际";
      if (/全球|海外|欧洲|中东|社会|民生|交通|治安|事故|救援|公益|社区/.test(text))
        return "社会";
      if (/时政|国务院|政务|党建|政策解读|监管|舆情/.test(text)) return "时政";
      return "综合";
    },
    // 查询方法
    search() {
      this.query.page = 1;
      this.get_list();
    },

    // 重置方法
    reset() {
      // 原有的重置逻辑
      Object.keys(this.query).forEach((key) => {
        if (key !== "size" && key !== "page" && key !== "orderby") {
          if (key.includes("_min") || key.includes("_max")) {
            this.query[key] = "";
          } else {
            this.query[key] = "";
          }
        }
      });

      this.query.orderby = "create_time desc";
      this.selectedSource = "";
      delete this.query.origin;
      this.get_list();
    },
    buildSchedulerDraftFromApi(cfg) {
      const src = (cfg && cfg.sources) || {};
      const draft = {};
      this.schedulerSourceOptions.forEach((item) => {
        const cur = src[item.value] || {};
        draft[item.value] = {
          enabled: !!cur.enabled,
          interval_minutes: Number(cur.interval_minutes) > 0
            ? Number(cur.interval_minutes)
            : 5,
        };
      });
      this.schedulerDraft = draft;
    },
    async loadSchedulerConfig() {
      try {
        const res = await this.$axios.get(
          `${this.spiderServiceBase}/scheduler/config`,
        );
        this.buildSchedulerDraftFromApi(res.data || {});
      } catch (e) {
        console.error(e);
        this.$message.warning(
          "无法加载定时爬取配置（请确认本机已启动爬虫服务：python spider/app.py，端口 5001）",
        );
      }
    },
    async saveSchedulerConfig() {
      const sources = {};
      this.schedulerSourceOptions.forEach((item) => {
        const row = this.schedulerDraft[item.value] || {};
        sources[item.value] = {
          enabled: !!row.enabled,
          interval_minutes: Math.max(1, Number(row.interval_minutes) || 5),
        };
      });
      this.schedulerSaving = true;
      try {
        await this.$axios.post(`${this.spiderServiceBase}/scheduler/config`, {
          sources,
        });
        this.$message.success("定时爬取设置已保存");
        await this.loadSchedulerConfig();
      } catch (e) {
        console.error(e);
        this.$message.error("保存失败，请确认爬虫服务（5001）已启动并可访问");
      } finally {
        this.schedulerSaving = false;
      }
    },
  },
  created() {
    this.spiderServiceBase = resolveSpiderServiceBase();
    // 默认显示全部来源
    delete this.query.origin;
    this.buildSchedulerDraftFromApi({});
    this.loadSchedulerConfig();
  },
  computed: {
    schedulerSourceOptions() {
      return this.sourceOptions.filter((i) => i.value);
    },
    hasExtraData() {
      return this.list.some((item) => item.extra && item.extra.trim() !== "");
    },
  },
};
</script>

<style type="text/css">
.bg {
  background: white;
}

.form.p_4 {
  padding: 1rem;
}

.form .el-input {
  width: initial;
}

.mt {
  margin-top: 1rem;
}

.text_center {
  text-align: center;
}

.float-right {
  float: right;
}

.modal_wrap {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9999999999;
}
.el-date-editor .el-range-separator {
  width: 10% !important;
}
.num_range {
  display: flex;
  align-items: center;
}

.num_range_span {
  font-size: 28px;
}
td > .cell > a,
td > .cell > span,
td > .cell {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
}
.expand-all {
  margin-top: 10px;
}
.el-table__indent,
.el-table__placeholder {
  display: inline-block !important;
}
.route-map-dialog {
  display: flex;
  height: 500px;
}

.route-map-left {
  flex: 1;
  position: relative;
  height: 100%;
  background: #f5f5f5;
}

.route-map-container {
  width: 100%;
  height: 100%;
}

.route-map-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  color: #409eff;
  font-size: 14px;
}

.route-map-right {
  width: 320px;
  padding-left: 20px;
  overflow-y: auto;
  border-left: 1px solid #eee;
}

.route-map-info-row {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.route-map-info-label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.route-map-info-value {
  color: #666;
  line-height: 1.5;
  font-size: 14px;
}

.scheduler-row-wrap {
  margin-top: 8px;
}
.scheduler-panel {
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  padding: 12px 14px;
  background: #fafafa;
}
.scheduler-title {
  font-weight: 600;
  margin-bottom: 6px;
  color: #303133;
}
.scheduler-hint {
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
  line-height: 1.5;
}
.scheduler-line {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}
.scheduler-label {
  min-width: 100px;
  color: #606266;
  font-size: 13px;
}
.scheduler-every,
.scheduler-unit {
  font-size: 13px;
  color: #606266;
}
.scheduler-actions {
  margin-top: 10px;
}
</style>
