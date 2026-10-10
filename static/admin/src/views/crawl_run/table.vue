<template>
  <el-main class="bg table_wrap">
    <el-form label-position="right" :model="query" class="form p_4" label-width="110">
      <el-row class="rows row1">
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="来源编码">
            <el-input v-model="query.source_code" placeholder="请输入来源编码" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="状态">
            <el-select v-model="query.status" clearable placeholder="全部">
              <el-option label="success" value="success" />
              <el-option label="failed" value="failed" />
              <el-option label="running" value="running" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row class="rows row2">
        <el-col :span="24" class="search_btn_wrap">
          <el-button type="primary" @click="search()">查询</el-button>
          <el-button @click="reset()">重置</el-button>
        </el-col>
      </el-row>
    </el-form>

    <el-table border stripe :data="list" style="width: 100%">
      <el-table-column prop="run_id" label="运行ID" min-width="180">
      </el-table-column>
      <el-table-column prop="source_name" label="来源名称" min-width="120">
      </el-table-column>
      <el-table-column prop="source_code" label="来源编码" min-width="120">
      </el-table-column>
      <el-table-column prop="status" label="状态" min-width="90">
        <template slot-scope="scope">
          <el-tag :type="statusTag(scope.row.status)">{{ scope.row.status || "-" }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="fetched_count" label="抓取数" min-width="90">
      </el-table-column>
      <el-table-column prop="written_count" label="写入数" min-width="90">
      </el-table-column>
      <el-table-column prop="dropped_count" label="过滤数" min-width="90">
      </el-table-column>
      <el-table-column prop="started_at" label="开始时间" min-width="170">
        <template slot-scope="scope">
          {{ scope.row.started_at ? $toTime(scope.row.started_at, "yyyy-MM-dd hh:mm:ss") : "-" }}
        </template>
      </el-table-column>
      <el-table-column prop="finished_at" label="结束时间" min-width="170">
        <template slot-scope="scope">
          {{ scope.row.finished_at ? $toTime(scope.row.finished_at, "yyyy-MM-dd hh:mm:ss") : "-" }}
        </template>
      </el-table-column>
      <el-table-column prop="error_message" label="失败原因" min-width="260">
      </el-table-column>
      <el-table-column fixed="right" label="操作" min-width="100">
        <template slot-scope="scope">
          <el-button size="small" type="primary" plain @click="goView(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

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
  </el-main>
</template>

<script>
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
  data() {
    return {
      url_get_list: "~/api/crawl_run/get_list",
      field: "crawl_run_id",
      query: {
        size: 15,
        page: 1,
        orderby: "crawl_run_id desc",
        source_code: "",
        status: "",
      },
      list: [],
    };
  },
  methods: {
    reset() {
      this.query = {
        size: 15,
        page: 1,
        orderby: "crawl_run_id desc",
        source_code: "",
        status: "",
      };
      this.get_list();
    },
    goView(row) {
      this.$router.push(`./view?${this.field}=${row[this.field]}`);
    },
    statusTag(status) {
      if (status === "success") return "success";
      if (status === "failed") return "danger";
      if (status === "running") return "warning";
      return "info";
    },
  },
};
</script>
