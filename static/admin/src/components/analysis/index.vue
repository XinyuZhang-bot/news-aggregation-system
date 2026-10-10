<template>
  <div>
    <el-button type="primary" @click="aiHandle" :loading="loading" v-if="showBtn">
      {{ btnText }}
    </el-button>
    <div
      class="analysis-content"
      v-if="mode === 'anlHtml'"
      v-loading="loading"
      element-loading-text="分析中..."
    >
      <div v-html="renderMD(answerMD)"></div>
    </div>
    <div v-if="mode === 'anlDialog'">
      <el-dialog title="数据分析" :visible.sync="dialogVisible" width="70%" :modal="false">
        <div
          v-html="renderMD(answerMD)"
          v-loading="loading"
          element-loading-text="分析中..."
        ></div>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false"
            >确 定</el-button
          >
        </span>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import MarkdownIt from "markdown-it";
import { $aiPost } from "@/api/aiApi";
const md = new MarkdownIt();

export default {
  props: {
    content: {
      type: Object | Array | String,
      default: null,
    },
    prompt: {
      type: String,
      default:
        "根据我提供的数据进行分析，请分析数据并总结关键信息，要求：只返回分析结果，不要解释分析过程，用简洁的语言描述。数据如下：",
    },
    /**
     * @type {string}
     * @default "anlHtml"
     * - "anlHtml": 以 HTML 形式展示分析结果
     * - "anlDialog": 以弹框形式展示分析结果
     */
    mode: {
      type: String,
      default: "anlHtml",
    },

    btnText: {
      type: String,
      default: "数据分析",
    },
  },
  data() {
    return {
      answerMD: "",
      md: new MarkdownIt(),
      dialogVisible: false,
      loading: false,
      showBtn: true,
    };
  },
  methods: {
    async aiHandle() {
      if (this.mode === "anlDialog") {
        this.dialogVisible = true;
      } else if (this.mode === "anlHtml") {
        this.showBtn = false;
      }
      this.loading = true;
      let res = await $aiPost({
        messages: [
          {
            role: "user",
            content: this.prompt + JSON.stringify(this.content) || this.content,
          },
        ],
      });
      this.answerMD = res.choices[0].message.content;
      this.loading = false;
      this.$emit("analysisEvent", this.answerMD);
    },
    renderMD(data) {
      return this.md.render(data);
    },
  },
};
</script>
<style scoped>
.analysis-content {
  min-height: 80px;
}
</style>
