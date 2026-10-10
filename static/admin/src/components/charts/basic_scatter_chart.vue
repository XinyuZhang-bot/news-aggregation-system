<template>
  <div class="basic_area_chart" :id="idName">散点图</div>
</template>
<script>
import echarts from "@/assets/js/echarts.min.js";

export default {
  // 定义组件名称
  name: "BasicScatterChart",

  // props定义（替代defineProps）
  props: {
    idName: {
      type: String,
      default: "lineChart",
    },
    title: {
      type: String,
      default: "XXX散点图",
    },
    vm: {
      type: Object,
      default: function() {
        return {
          xAxis: "xAxis",
          names: "names",
          values: "values",
        };
      },
    },
  },

  // 数据定义（替代ref/reactive）
  data() {
    return {
      option: {
        title: {
          text: "XXX散点图",
          left: "center",
        },
        color: ["#dd4444", "#fec42c", "#80F1BE"],
        legend: {
          data: ["正常账户", "禁用账户"],
          textStyle: { fontSize: 16 },
          y: "bottom",
        },
        grid: {
          left: "3%",
          right: "10%",
          bottom: "14%",
          containLabel: true,
        },
        tooltip: {
          backgroundColor: "rgba(255,255,255,0.7)",
          formatter: function(param) {
            var value = param.value;
            return (
              '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' +
              param.seriesName +
              " " +
              value[1]
            );
          },
        },
        xAxis: [
          {
            type: "category",
            name: "月份",
            boundaryGap: false,
            data: [], // 将在init_chart中动态赋值
          },
        ],
        yAxis: {},
        series: [
          {
            name: "正常账户",
            type: "scatter",
            itemStyle: this.itemStyle,
            data: [],
          },
          {
            name: "禁用账户",
            type: "scatter",
            itemStyle: this.itemStyle,
            data: [],
          },
        ],
      },
      itemStyle: {
        opacity: 0.8,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: "rgba(0,0,0,0.3)",
      },
      user_id: this.$store.state.user.user_id, // 原user_id定义移至data
    };
  },

  // 计算属性（替代computed API）
  computed: {
    series() {
      let values = [];
      values[0] = this.vm.values.available;
      values[1] = this.vm.values.freeze;
      return values;
    },
  },

  // 监听器（替代watch API）
  watch: {
    series(newValue) {
      if (newValue) {
        this.init_chart();
      }
    },
  },

  // 生命周期钩子（替代onMounted）
  mounted() {
    setTimeout(() => {
      this.init_chart();
    }, 200);
  },

  // 方法定义（原init_chart移至methods）
  methods: {
    init_chart() {
      let optionObj = this.option;
      let titleObj = this.title;

      // 更新标题
      if (titleObj) {
        optionObj.title.text = titleObj;
      }

      // 更新数据
      optionObj.series[0].data = this.series[0];
      optionObj.series[1].data = this.series[1];
      optionObj.xAxis[0].data = this.vm.xAxis; // 绑定xAxis数据

      // 初始化图表
      let myChart = echarts.init(document.getElementById(this.idName));
      myChart.setOption(optionObj);
    },
  },
};
</script>
