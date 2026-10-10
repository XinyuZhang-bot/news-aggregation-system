 <!-- // 测评优化开始 -->
<template>
  <div class="evaluationTable">
    <el-table :data="tableData" :empty-text="'没有数据'" size="mini" style="width: 100%;">
      <el-table-column prop="name" label="起始分数" width="20%">
        <template slot-scope="scope">
          <el-input v-model="scope.row.score_min" placeholder="请输入起始分数"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="startTime" label="终止分数" width="20%">
        <template slot-scope="scope">
          <el-input v-model="scope.row.score_max" placeholder="请输入终止分数"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="endTime" label="结果描述" width="46%">
        <template slot-scope="scope">
          <el-input v-model="scope.row.result" placeholder="请输入结果描述"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="12%">
        <template slot-scope="scope">
          <div style="display: flex;justify-content: center;">
            <el-button @click="deleteRow(scope.$index)" type="text" size="small">
            删除
            </el-button>
          </div>
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
<style>
.evaluationTable .el-table__body {
  width: 100% !important;
}
.evaluationTable .el-table__header {
  width: 100% !important;
}
.evaluationTable .el-table__empty-block {
  width: 100% !important;
}
</style>
 <!-- // 测评优化结束 -->