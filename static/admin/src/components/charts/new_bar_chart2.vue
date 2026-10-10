<template>
  <div class="bar_chart" :id="idName">条形图</div>
</template>

<script>
import echarts from "@/assets/js/echarts.min.js";

export default {
  props: {
    idName: {
      type: String,
      default: "barChart",
    },
    title: {
      type: String,
      default: "XXX条形图",
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
    avg: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      option: {
        title: {
          text: "7日个类商品销售额",
          left: "center",
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          type: 'scroll',
          orient: 'horizontal',
          y: 'bottom'
        },
        xAxis: [{
          type: 'category',
          axisTick: {
            show: false
          },
          data: []
        }],
        yAxis: [{
          type: 'value'
        }],
        series: [
          {
            data: [],
            type: 'bar'
          }
        ]
      }
    };
  },
  computed: {
    series() {
      let values = this.vm.values;
      return values;
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
    setTimeout(() => {
      this.init_chart();
    }, 200);
  },
  methods: {
    init_chart() {
      let optionObj = this.option;

      let titleObj = this.title;
      if (titleObj) {
        optionObj.title.text = titleObj;
      }
      optionObj.series[0].data = this.series;

      let xAxis = optionObj.xAxis[0];
      xAxis.data = this.vm.xAxis;

      if (xAxis.data.length > 4) {
        optionObj.axisLabel = {
          interval: 0, //使x轴文字显示全
          formatter: function(params) {
            let newParamsName = '';
            const paramsNameNumber = params.length; // 文字总长度
            const provideNumber = 4; //一行显示几个字
            const rowNumber = Math.ceil(paramsNameNumber / provideNumber);
            if (paramsNameNumber > provideNumber) {
              for (let p = 0; p < rowNumber; p++) {
                const start = p * provideNumber;
                const end = start + provideNumber;
                const tempStr = p === rowNumber - 1 ? params.substring(start, paramsNameNumber) : params.substring(start, end) + '\n';
                newParamsName += tempStr;
              }
            } else {
              newParamsName = params;
            }
            return newParamsName;
          },
        };
      }
      let myChart = echarts.init(document.getElementById(this.idName));
      myChart.setOption(optionObj);
    }
  }
};
</script>
