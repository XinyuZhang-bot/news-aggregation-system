<template>
  <el-main class="bg edit_wrap">
    <el-form label-width="110px" v-if="obj && obj.crawl_run_id">
      <el-row>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="运行ID">{{ obj.run_id || "-" }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="状态">{{ obj.status || "-" }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="来源名称">{{ obj.source_name || "-" }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="来源编码">{{ obj.source_code || "-" }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="抓取数">{{ obj.fetched_count || 0 }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="写入数">{{ obj.written_count || 0 }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="过滤数">{{ obj.dropped_count || 0 }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="开始时间">
            {{ obj.started_at ? $toTime(obj.started_at, "yyyy-MM-dd hh:mm:ss") : "-" }}
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="12">
          <el-form-item label="结束时间">
            {{ obj.finished_at ? $toTime(obj.finished_at, "yyyy-MM-dd hh:mm:ss") : "-" }}
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="24">
          <el-form-item label="错误信息">{{ obj.error_message || "-" }}</el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="24">
          <el-form-item label="摘要">{{ obj.summary || "-" }}</el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </el-main>
</template>

<script>
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
  data() {
    return {
      field: "crawl_run_id",
      url_get_obj: "~/api/crawl_run/get_obj?",
      query: {
        crawl_run_id: 0,
      },
      obj: {},
    };
  },
};
</script>
