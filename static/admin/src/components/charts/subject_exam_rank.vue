<!-- // 考试优化开始 -->
<template>
<div>
    <div style="display: flex;justify-content: space-between;">
      <h3>{{title}}</h3>
      <el-select v-model="subject_name" @change="subjectChange" placeholder="请选择">
        <el-option
          v-for="item in vm"
          :key="item.exam_id"
          :label="item.name"
          :value="item.exam_id">
        </el-option>
      </el-select>
    </div>
    <el-table
        :data="tableData"
        stripe
        style="width: 100%;margin-top: 10px">
      <el-table-column
          prop="rank"
          label="排名"
          align="center">
      </el-table-column>
      <el-table-column
          prop="nickname"
          label="姓名"
          align="center">
      </el-table-column>
      <el-table-column
          prop="score"
          label="分数"
          align="center">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  props:{
    vm: {
      type: Array
    },
    title: {
      type: String,
      default: '考试分数排名'
    }
  },
  data() {
    return {
      tableData: [],
      subject_name: '',
    }
  },
  created() {
    this.subject_name = this.vm[0].exam_id;
    this.getRank(this.subject_name);
  },
  methods:{
    async getRank(exam_id){
      let json = await this.$get("~/api/subject_user_answer/get_list",{exam_id});
      // 筛选每个user_id最新的一条数据
      const userMap = new Map();
      json.result.list.forEach(item => {
        // 如果该user_id不存在于Map中，或者当前数据的create_time比Map中已有数据的更新
        if (!userMap.has(item.user_id) || 
            new Date(item.create_time) > new Date(userMap.get(item.user_id).create_time)) {
          userMap.set(item.user_id, item);
        }
      });
      
      // 将Map转换回数组
      const filteredList = Array.from(userMap.values());
      
      // 按score分数从高到低排序
      let sortedList = filteredList.sort((a, b) => b.score - a.score);
      
      // 为每个对象添加排名属性
      this.tableData = sortedList.map((item, index) => {
        return {
          ...item,
          rank: index + 1  // 排名从1开始
        }
      });
    },
    subjectChange(val) {
      this.getRank(val);
    }
  }
}
</script>

<style scoped>

</style>
<!-- // 考试优化结束 -->