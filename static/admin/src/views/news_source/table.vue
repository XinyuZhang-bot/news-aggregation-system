<template>
  <el-main class="bg table_wrap">
    <el-form label-position="right" :model="query" class="form p_4" label-width="110">
      <el-row class="rows row1">
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="来源名称">
            <el-input v-model="query.name" placeholder="请输入来源名称" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="来源编码">
            <el-input v-model="query.code" placeholder="请输入来源编码" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="解析器">
            <el-input v-model="query.parser_name" placeholder="如 tencent / people" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row class="rows row2">
        <el-col :span="24" class="search_btn_wrap">
          <el-button type="primary" @click="search()">查询</el-button>
          <el-button @click="reset()">重置</el-button>
          <el-button type="success" class="float-right" @click="$router.push('./view?')">新增来源</el-button>
          <el-button type="danger" class="float-right mr8" @click="delInfo()">删除</el-button>
        </el-col>
      </el-row>
    </el-form>

    <el-table border stripe :data="list" @selection-change="selectionChange" style="width: 100%">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="code" label="编码" min-width="120" />
      <el-table-column prop="name" label="名称" min-width="140" />
      <el-table-column prop="source_type" label="来源类型" min-width="110" />
      <el-table-column prop="parser_name" label="解析器" min-width="110" />
      <el-table-column prop="base_url" label="基础地址" min-width="220" />
      <el-table-column prop="interval_minutes" label="频率(分钟)" min-width="110" />
      <el-table-column prop="priority" label="优先级" min-width="90" />
      <el-table-column label="状态" min-width="90">
        <template slot-scope="scope">
          <el-tag :type="Number(scope.row.enabled) ? 'success' : 'info'">
            {{ Number(scope.row.enabled) ? "启用" : "停用" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_run_at" label="最近抓取" min-width="170">
        <template slot-scope="scope">
          {{ scope.row.last_run_at ? $toTime(scope.row.last_run_at, "yyyy-MM-dd hh:mm:ss") : "-" }}
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" min-width="180">
        <template slot-scope="scope">
          <el-button size="small" type="primary" plain @click="goEdit(scope.row)">详情</el-button>
          <el-button
            size="small"
            :type="Number(scope.row.enabled) ? 'warning' : 'success'"
            plain
            @click="toggleEnabled(scope.row)"
          >
            {{ Number(scope.row.enabled) ? "停用" : "启用" }}
          </el-button>
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
      />
    </div>
  </el-main>
</template>

<script>
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
  data() {
    return {
      url_get_list: "~/api/news_source/get_list",
      url_del: "~/api/news_source/del?",
      field: "news_source_id",
      query: {
        size: 15,
        page: 1,
        orderby: "priority desc, news_source_id asc",
        name: "",
        code: "",
        parser_name: "",
      },
      list: [],
    };
  },
  methods: {
    reset() {
      this.query = {
        size: 15,
        page: 1,
        orderby: "priority desc, news_source_id asc",
        name: "",
        code: "",
        parser_name: "",
      };
      this.get_list();
    },
    goEdit(row) {
      this.$router.push(`./view?${this.field}=${row[this.field]}`);
    },
    async toggleEnabled(row) {
      const enabled = Number(row.enabled) ? 0 : 1;
      const res = await this.$post("~/api/news_source/set?", {
        news_source_id: row.news_source_id,
        enabled,
      });
      if (res && res.result) {
        this.$message.success(enabled ? "已启用" : "已停用");
        this.get_list();
      }
    },
  },
};
</script>

<style scoped>
.mr8 {
  margin-right: 8px;
}
</style>
