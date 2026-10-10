<template>
  <el-main class="bg edit_wrap">
    <el-form ref="form" :model="form" label-width="110px">
      <el-row>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="来源编码">
            <el-input v-model="form.code" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="来源名称">
            <el-input v-model="form.name" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="启用状态">
            <el-switch v-model="form.enabled" :active-value="1" :inactive-value="0" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="来源类型">
            <el-select v-model="form.source_type">
              <el-option label="builtin" value="builtin" />
              <el-option label="rss" value="rss" />
              <el-option label="list" value="list" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="解析器类型">
            <el-select v-model="form.parser_type">
              <el-option label="builtin" value="builtin" />
              <el-option label="generic" value="generic" />
              <el-option label="rss" value="rss" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="解析器名称">
            <el-input v-model="form.parser_name" placeholder="如 tencent / people / xinhuanet" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="基础地址">
            <el-input v-model="form.base_url" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="频率(分钟)">
            <el-input-number v-model="form.interval_minutes" :min="1" :max="1440" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="12" :lg="8">
          <el-form-item label="优先级">
            <el-input-number v-model="form.priority" :min="0" :max="100" />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="列表地址">
            <el-input
              type="textarea"
              :rows="4"
              v-model="form.list_urls"
              placeholder="每行一个列表地址；RSS 来源可直接填 XML 地址"
            />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="扩展配置 JSON">
            <el-input
              type="textarea"
              :rows="6"
              v-model="form.extra_json"
              placeholder='例如 {"host_keywords":["news.cn"],"origin_name":"新华社"}'
            />
          </el-form-item>
        </el-col>
        <el-col :span="24" class="el_form_btn_warp">
          <el-form-item>
            <el-button type="primary" @click="submit()">提交</el-button>
            <el-button @click="cancel()">取消</el-button>
          </el-form-item>
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
      field: "news_source_id",
      url_add: "~/api/news_source/add?",
      url_set: "~/api/news_source/set?",
      url_get_obj: "~/api/news_source/get_obj?",
      query: {
        news_source_id: 0,
      },
      obj: {},
      form: {
        news_source_id: 0,
        code: "",
        name: "",
        enabled: 1,
        source_type: "builtin",
        parser_type: "builtin",
        parser_name: "",
        base_url: "",
        list_urls: "",
        interval_minutes: 30,
        priority: 50,
        extra_json: "",
        last_run_at: "",
        last_status: "",
      },
    };
  },
};
</script>
