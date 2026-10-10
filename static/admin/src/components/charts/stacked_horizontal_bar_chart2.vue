<template>
  <div class="bar_chart" :id="idName">条形图</div>
</template>
<script>
import * as echarts from "@/assets/js/echarts.min.js";

export default {
  props: {
    idName: {
      type: String,
      default: "barChart"
    },
    title: {
      type: String,
      default: "XXX条形图"
    },
    vm: {
      type: Object,
      default: function() {
        return {
          yAxis: "yAxis",
          names: "names",
          values: "values"
        };
      }
    }
  },
  data() {
    return {
      option: {
        title: {
          text: "XXX条形图",
          left: "center"
        },
        grid: {
          left: "3%",
          right: "4%",
          top: "14%",
          bottom: "8%",
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: [],
          type: 'scroll',
          orient: 'horizontal',
          y: 'bottom'
        },
        xAxis: [{
          type: 'value',
          splitLine: { show: true, lineStyle: { opacity: 0.15 } }
        }],
        yAxis: [{
          type: 'category',
          data: [],
          axisTick: { show: false },
          axisLine: { show: false }
        }],
        series: [
          {
            name: 'Forest',
            type: 'bar',
            barGap: 0,
            barCategoryGap: "42%",
            barMaxWidth: 22,
            emphasis: {
              focus: 'series'
            },
            data: [320, 332, 301, 334, 390]
          }
        ]
      }
    };
  },
  computed: {
    series() {
      // 保留原计算属性逻辑，直接访问this.vm
      let values = this.vm.values;
      return values;
    }
  },
  mounted() {
    // Vue3 onMounted 转换为 Vue2 mounted 生命周期
    setTimeout(() => {
      this.init_chart();
    }, 200);
  },
  methods: {
    init_chart() {
      let optionObj = this.option;
      let titleObj = this.title;
      
      // 设置标题
      if (titleObj) {
        optionObj.title.text = titleObj;
      }

      // 更新系列数据和名称
      optionObj.series[0].data = this.series;
      optionObj.series[0].name = this.vm.names[0];

      // 设置 y 轴类目（须挂在 yAxis.axisLabel，不能写在 option 根上）
      let yAxis = optionObj.yAxis[0];
      yAxis.data = this.vm.xAxis;
      const maxChars = 16;
      yAxis.axisLabel = {
        interval: 0,
        fontSize: 12,
        formatter: function (val) {
          const s = String(val == null ? "" : val);
          if (s.length <= maxChars) {
            return s;
          }
          return s.slice(0, maxChars) + "…";
        }
      };

      const el = document.getElementById(this.idName);
      if (!el) {
        return;
      }
      let myChart = echarts.getInstanceByDom(el);
      if (myChart) {
        myChart.setOption(optionObj, true);
      } else {
        myChart = echarts.init(el);
        myChart.setOption(optionObj);
      }
    }
  }
};
</script>
