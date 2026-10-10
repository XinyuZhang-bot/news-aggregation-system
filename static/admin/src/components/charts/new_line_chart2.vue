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
          values: "values",
        };
      },
    },
    timeout: {
      type: Number,
      default: 2000
    },
    color: {
      type: Array,
      default: []
    }
  },
  data() {
    return {
      option: {
        title: {
          text: "XXX折线图",
          left: "center",
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          type: 'scroll',
          orient: 'horizontal',
          y: 'bottom'
        },
        grid: {
          left: "3%",
          right: "10%",
          bottom: "14%",
          containLabel: true,
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        xAxis: [{
          type: 'category',
          boundaryGap: false,
          data: []
        }],
        yAxis: [{
          type: 'value'
        }],
        series: []
      }
    };
  },
  computed: {
    series() {
      let list = this.vm.names;
      let values = this.vm.values;
      let seriesobj = [];
      
      for (let i = 0; i < list.length; i++) {
        let data = [];
        for (let j = 0; j < values.length; j++) {
          if (Array.isArray(values[j])) {
            data.push(values[j][i]);
          } else {
            data.push(values[j]);
          }
        }
        seriesobj.push({
          name: list[i],
          type: 'line',
          data: data
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
    if (this.color.length > 0) {
      this.option.color = this.color;
    }
    
    setTimeout(() => {
      this.init_chart();
    }, 200);
  },
  methods: {
    init_chart() {
      let optionObj = this.option;
      
      // 设置标题
      if (this.title) {
        optionObj.title.text = this.title;
      }
      
      // 设置系列数据
      optionObj.series = this.series;
      
      // 设置x轴数据
      let xAxis = optionObj.xAxis[0];
      xAxis.data = this.vm.xAxis;
      
      // x轴标签换行处理
      if (xAxis.data.length > 4) {
        optionObj.axisLabel = {
          interval: 0,
          formatter: function(params) {
            let newParamsName = '';
            const paramsNameNumber = params.length;
            const provideNumber = 4;
            const rowNumber = Math.ceil(paramsNameNumber / provideNumber);
            
            if (paramsNameNumber > provideNumber) {
              for (let p = 0; p < rowNumber; p++) {
                const start = p * provideNumber;
                const end = start + provideNumber;
                const tempStr = p === rowNumber - 1 
                  ? params.substring(start, paramsNameNumber) 
                  : params.substring(start, end) + '\n';
                newParamsName += tempStr;
              }
            } else {
              newParamsName = params;
            }
            return newParamsName;
          }
        };
      }
      
      // 初始化图表
      let myChart = echarts.init(document.getElementById(this.idName));
      myChart.setOption(optionObj);
    }
  }
};
</script>
