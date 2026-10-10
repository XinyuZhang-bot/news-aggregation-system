<!-- // 文件下载与预览优化开始 -->
<template>
  <div id="filePreview">
    <VueOfficeDocx
      v-if="type === 'docx'"
      :src="fileUrl"
      style="min-height: 700px;max-height: 100%;"
    />
    <VueOfficeXLSX
      v-if="type=='xlsx' || type=='xls'"
      :src="fileUrl"
      style="min-height: 700px;max-height: 100%;"
    />
    <VueOfficePPTX
      v-if="type=='pptx' || type=='ppt'"
      :src="fileUrl"
      style="min-height: 700px;max-height: 100%;"
    />
  </div>
</template>
<script>
import mixin from "@/mixins/page.js";
import VueOfficePPTX from "@vue-office/pptx"
import VueOfficeDocx from '@vue-office/docx'
import '@vue-office/docx/lib/index.css'
import VueOfficeXLSX from '@vue-office/excel'
import '@vue-office/excel/lib/index.css'

export default {
  mixins: [mixin],
  data() {
    return {
      fileUrl: null,
      type: null,
    };
  },
  components: {
    VueOfficePPTX,
    VueOfficeDocx,
    VueOfficeXLSX,
  },
  mounted() {
    this.fileUrl = this.$fullUrl(this.$route.query.url)
    this.type = this.$route.query.type;
  },
  methods: {
    
  },
};
</script>

<style type="text/css">
#filePreview {
  margin: 37px auto 0;
  width: 50%;
  min-height: 700px;
  max-height: 100%;
  overflow: auto;
}
</style>
<!-- // 文件下载与预览优化结束 -->
