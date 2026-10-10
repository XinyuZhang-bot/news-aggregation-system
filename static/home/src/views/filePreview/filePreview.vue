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
import VueOfficePPTX from "@vue-office/pptx/lib/v2/index.js"
import VueOfficeDocx from '@vue-office/docx/lib/v2/index.js'
// vue-office/docx 在不同版本中 CSS 入口可能变化，这里按当前包结构引入
import '@vue-office/docx/lib/v2/index.css'
import VueOfficeXLSX from '@vue-office/excel/lib/v2/index.js'
import '@vue-office/excel/lib/v2/index.css'

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
    console.log(this.fileUrl,'文件URL');
    this.type = this.$route.query.type;
    console.log(this.type,'文件类型');
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
