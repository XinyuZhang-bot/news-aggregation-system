<template>
  <el-card>
    <div slot="header">
      <span>知识图谱</span>
    </div>
    <div id="knowledgeGraphChat" style="width: 100%; height: 800px;"></div>
  </el-card>
</template>

<script>
import echarts from "@/assets/js/echarts.min.js";
import { data as graph } from "./data.js";

export default {
  name: "knowledgeGraphChat",
  data() {
    return {
      myChart: null
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.init_chart();
      window.addEventListener('resize', this.handleResize);
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    if (this.myChart) {
      this.myChart.dispose(); // 清理图表实例
    }
  },
  methods: {
    handleResize() {
      if (this.myChart) {
        this.myChart.resize(); // 调整图表大小
      }
    },
    init_chart() {
      this.myChart = echarts.init(document.getElementById("knowledgeGraphChat"), null, {
        renderer: 'canvas',
        useDirtyRect: false
      });
      console.log('graph====', graph);

      const option = {
        tooltip: {
          formatter: function (params) {
            if (params.dataType === "node") {
              // 显示节点名称和值
              return params.data.name;
            } else if (params.dataType === "edge") {
              // 获取源节点和目标节点的名称
              const sourceId = params.data.source;
              const targetId = params.data.target;
              // 从节点数据中查找对应的名称
              const sourceNode = graph.nodes.find(
                (node) => node.id === sourceId
              );
              const targetNode = graph.nodes.find(
                (node) => node.id === targetId
              );
              if (sourceNode && targetNode) {
                return sourceNode.name + " -> " + targetNode.name;
              } else {
                return sourceId + " -> " + targetId; // 备用，如果找不到节点
              }
            }
          },
        },
        legend: [
          {
            data: graph.categories.map(function (a) {
              return a.name;
            })
          }
        ],
        series: [
          {
            type: 'graph',
            layout: 'force',
            symbolSize: 60,
            data: graph.nodes,
            links: graph.links,
            categories: graph.categories,
            roam: true, // 禁止拖拽
            edgeSymbol: ['circle', 'arrow'], // 两端样式，箭头朝向
            edgeSymbolSize: [4, 6], // 两端大小
            label: {
              show: true,
            },
            links: graph.links.map(function (item) {
              return {
                ...item,
                label: {
                  show: !!item.link, // 控制是否显示标签
                  formatter: item.link || '' // 设置要显示的文本
                }
              };
            }),
            force: {
              // 使用 repulsion 来增加节点之间的间隔
              repulsion: 800, // 这是一个示例值，您可以根据需要调整
              // 使用 gravity 来控制节点向中心的引力
              gravity: 0.1, // 这是一个示例值，您可以根据需要调整
              // 使用 edgeLength 来控制边的长度
              edgeLength: [50, 200], // 这是一个示例值，您可以根据需要调整
              layoutAnimation: false,  // 关闭布局动画
            },
            scaleLimit: {
              min: 0.4,
              max: 2
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3
            }
          }]
      };

      this.myChart.setOption(option);
    }
  },
};
</script>
