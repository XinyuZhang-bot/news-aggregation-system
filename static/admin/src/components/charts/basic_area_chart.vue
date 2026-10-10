<template>
  <div class="line_chart" :id="idName">折线图</div>
</template>

<script>
import echarts from "@/assets/js/echarts.min.js";

export default {
  props: {
    idName: {
      type: String,
      default: "lineChart"
    },
    title: {
      type: String,
      default: "XXX折线图"
    },
    vm: {
      type: Object,
      default: function() {
        return {
          xAxis: "xAxis",
          names: "names",
          values: "values"
        };
      }
    },
    timeout: {
      type: Number,
      default: 2000
    },
    color: {
      type: Array,
      default: function() {
        return [];
      }
    }
  },
  data() {
    return {
      option: {
        title: {
          text: "XXX折线图",
          left: "center"
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: [], // 动态从props获取，初始化留空
          y: 'bottom'
        },
        grid: {
          left: "3%",
          right: "10%",
          bottom: "14%",
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: [{
          type: 'category',
          boundaryGap: false,
          data: [] // 动态从props获取，初始化留空
        }],
        yAxis: [{
          type: 'value'
        }],
        series: [
          {
            name: '点赞数',
            data: [], // 动态从props获取，初始化留空
            type: 'line',
            areaStyle: {}
          }
        ]
      }
    };
  },
  computed: {
    series() {
      // 重构series计算逻辑，匹配Vue2语法
      let list = this.vm.names;
      let values = this.vm.values;
      let seriesobj = [];
      
      // 修复原Vue3代码中未return的问题
      if (list && values) {
        seriesobj.push({
          areaStyle: {},
          type: 'line',
          data: values,
          name: list[0] || '默认系列' // 使用names第一个元素作为系列名称
        });
      }
      return seriesobj;
    }
  },
  watch: {
    series(newValue) {
      if (newValue) {
        this.init_chart();
      }
    }
  },
  mounted() {
    // 处理颜色配置
    if (this.color.length > 0) {
      this.option.color = this.color;
    }
    
    // 延迟初始化图表，确保DOM加载完成
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
      
      // 动态绑定数据（原Vue3中直接在ref初始化时绑定，Vue2需在方法中设置）
      optionObj.legend.data = this.vm.names || [];
      optionObj.xAxis[0].data = this.vm.xAxis || [];
      optionObj.series = this.series; // 使用计算属性的series数据
      
      // 初始化图表
      let myChart = echarts.init(document.getElementById(this.idName));
      myChart.setOption(optionObj);
    }
  }
};
</script>
