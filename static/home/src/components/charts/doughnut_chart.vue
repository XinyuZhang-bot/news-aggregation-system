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
  },
  data() {
    return {
      option: {
        title: {
          text:"",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: '',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            data: [],
          }
        ]
      },
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
      // 外部参数
      var title = this.title;
      var type = this.type;

      // 标题
      if (title) {
        this.option.title.text = title;
      }

      // 分类名
      if (type) {
        this.option.series[0].name = type;
      }

      // 参数
      console.log(this.list)
      this.option.series[0].data = this.list;

      let myChart = echarts.init(document.getElementById(this.id));
      myChart.setOption(this.option);
    },
  },
  watch: {
    list() {
      this.init_chart();
    },
  },
};
</script>
