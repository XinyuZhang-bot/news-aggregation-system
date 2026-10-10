<template>
  <div class="pie_chart" :id="id">环形图</div>
</template>

<script>
import * as echarts from "@/assets/js/echarts.min.js";

export default {
  name: "Home",
  components: {},
  props: {
    id: {
      type: String,
      default: "pieChart"
    },
    title: {
      type: String,
      default: "XXX饼状图"
    },
    list: {
      type: Array,
      required: true
    },
    type: {
      type: String,
      default: "参数"
    },
    /** 图例在左、环形图偏右，关闭扇区文字，避免与图例重复或重叠 */
    compactLayout: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      option: {},
    }
  },
  created() {},
  mounted() {
    let that=this;
    setTimeout(function(){
      that.init_chart();
    },200)
  },
  methods: {
    init_chart() {
      const title = this.title;
      const type = this.type;
      const compact = this.compactLayout;

      const legend = compact
        ? {
            orient: "vertical",
            left: 6,
            top: "middle",
            itemWidth: 10,
            itemHeight: 10,
            itemGap: 10,
            icon: "circle",
            textStyle: { fontSize: 12, color: "#595959" },
            formatter: (name) =>
              name && name.length > 7 ? name.slice(0, 7) + "…" : name,
          }
        : {
            orient: "vertical",
            left: "left",
          };

      const series = {
        name: type || "",
        type: "pie",
        radius: compact ? ["30%", "52%"] : ["40%", "70%"],
        center: compact ? ["68%", "50%"] : ["50%", "50%"],
        data: this.list || [],
        label: { show: !compact },
        labelLine: { show: !compact },
        emphasis: {
          label: {
            show: true,
            fontSize: 12,
          },
        },
      };

      this.option = {
        title: {
          text: title || "",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend,
        series: [series],
      };

      const el = document.getElementById(this.id);
      if (!el) return;
      let myChart = echarts.getInstanceByDom(el);
      if (!myChart) {
        myChart = echarts.init(el);
      }
      myChart.setOption(this.option, true);
    },
  },
  watch: {
    list() {
      this.init_chart();
    },
    compactLayout() {
      this.init_chart();
    },
  },
};
</script>
