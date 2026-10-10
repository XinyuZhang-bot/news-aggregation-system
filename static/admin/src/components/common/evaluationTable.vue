 <!-- // 测评优化开始 -->
<template>
  <div>
    <el-table :data="tableData" :empty-text="'没有数据'" size="mini">
      <el-table-column prop="name" label="起始分数" width="260">
        <template slot-scope="scope">
          <el-input v-model="scope.row.score_min" placeholder="请输入起始分数"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="startTime" label="终止分数" width="260">
        <template slot-scope="scope">
          <el-input v-model="scope.row.score_max" placeholder="请输入终止分数"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="endTime" label="结果描述">
        <template slot-scope="scope">
          <el-input v-model="scope.row.result" placeholder="请输入结果描述" style="max-width: none;"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template slot-scope="scope">
          <el-button @click="deleteRow(scope.$index)" type="text" size="small">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-button type="text" @click="addRow">+新增一行</el-button>
  </div>
</template>

<script>
export default {
  props: {
    jsonStr: {
      type: String,
      default: "[]",
    },
    max: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      tableData: [{
        score_min: '',
        score_max: '',
        result: ''
      }],
      tableTimer: null,
    };
  },
  watch: {
    jsonStr: {
      immediate: true,
      handler(newVal) {
        try {
          this.tableData = JSON.parse(newVal);
        } catch (e) {
          this.tableData = [];
        }
      },
    },
    tableData: {
      deep: true,
      handler(newVal) {
        this.tableTimer && clearTimeout(this.tableTimer);
        this.tableTimer = setTimeout(() => {
          this.$emit('tableChange', JSON.stringify(newVal));
        }, 300);
      },
    },
  },
  methods: {
    addRow() {
      const newRow = {
        score_min: '',
        score_max: '',
        result: ''
      };
      this.tableData.push(newRow);
    },
    deleteRow(index) {
      this.tableData.splice(index, 1);
    },
  }
};
</script>
 <!-- // 测评优化结束 -->