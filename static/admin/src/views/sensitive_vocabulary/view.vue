<template>
  <el-main class="bg edit_wrap comtable_e">
    <el-form ref="form" :model="form" status-icon label-width="120px">
      <el-row class="row_ce">
        <el-col :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
          <el-form-item label="敏感词汇" prop="sensitive_vocabulary">
            <el-input id="sensitive_vocabulary" v-model="form['sensitive_vocabulary']" placeholder="请输入敏感词汇"></el-input>
          </el-form-item>
        </el-col>


      </el-row>
      <el-col :xs="24" :sm="12" :lg="8" class="el_form_btn_warp">
        <el-form-item>
          <el-button type="primary" @click="submit()">提交</el-button>
          <el-button @click="cancel()">取消</el-button>
        </el-form-item>
      </el-col>

    </el-form>
  </el-main>
</template>

<script>
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
  data() {
    return {
      field: "sensitive_vocabulary_id",
      url_add: "~/api/sensitive_vocabulary/add?",
      url_set: "~/api/sensitive_vocabulary/set?",
      url_get_obj: "~/api/sensitive_vocabulary/get_obj?",
      url_upload: "~/api/sensitive_vocabulary/upload?",
      query: {
        "sensitive_vocabulary_id": 0,
      },
      form: {
        "sensitive_vocabulary": '', // 敏感词汇
        "sensitive_vocabulary_id": 0, // ID

      }
    }
  },
  methods: {
  },
  created() {
  },
}
</script>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}


</style>
