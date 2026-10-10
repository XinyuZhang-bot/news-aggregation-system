<template>
  <div class="basic_area_chart" :id="idName"></div>
</template>
<script>
import echarts from "@/assets/js/echarts.min.js";

export default {
  name: "RadarChart",
  props: {
    idName: {
      type: String,
      default: "barChart",
    },
    title: {
      type: String,
      default: "XXX饼状图"
    },
    vm: {
      type: Object,
      default: function () {
        return {
          xAxis: "xAxis",
          names: "names",
          values: "values",
        };
      },
    },
  },
  data() {
    return {
      option: {
        title: {
          left: "center",
          text: '访问数统计'
        },
        legend: {
          data: [],
          type: 'scroll',
          orient: 'horizontal',
          y: 'bottom'
        },
        radar: {
          indicator: [],
          radius: '65%'
        },
        series: [{
          name: '访问数',
          type: 'radar',
          data: [
            {
              value: [],
              name: '访问数'
            }
          ]
        }]
      },
      user_id: this.$store.state.user.user_id
    };
  },
  computed: {
    series() {
      return this.vm.values;
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
      
      optionObj.series[0].data[0].value = this.series;
      optionObj.series[0].data[0].name = this.vm.names[0];
      optionObj.series[0].name = this.vm.names[0];
      optionObj.legend.data = this.vm.names;
      optionObj.radar.indicator = this.vm.indicator;

      let myChart = echarts.init(document.getElementById(this.idName));
      myChart.setOption(optionObj);
    }
  }
};
</script>
