<template>
  <el-main class="bg edit_wrap comtabel_e releasing_notices">
    <el-form label-position="right" class="form p_4" label-width="70px" v-model="form">
      <el-row class="row_e">
        <el-col :xs="24" :sm="24" :lg="8" class="el_form_item_warp">
          <el-form-item label="通知标题">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="8" class="el_form_item_warp">
          <el-form-item label="通知方式">
            <el-checkbox-group v-model="checkList">
              <el-checkbox label="站内通知"></el-checkbox>
              <!-- <el-checkbox label="邮箱提醒"></el-checkbox> -->
            </el-checkbox-group>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="8" class="el_form_item_warp">
          <el-form-item label="接收人">
            <el-cascader
            style="width: 80%;"
            v-model="recipients"
            :options="options"
            :props="{multiple: true, emitPath: false}"
            collapse-tags
            clearable></el-cascader>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="8" class="el_form_item_warp">
          <el-form-item label="通知内容">
            <el-input type="textarea" v-model="form.content"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-col :xs="24" :sm="12" :lg="8" class="el_form_btn_warp">
        <el-form-item>
          <el-button type="primary" @click="submit">提交</el-button>
          <el-button @click="cancel()">取消</el-button>
        </el-form-item>
      </el-col>
    </el-form>
  </el-main>
</template>

<script>
import mixin from "@/mixins/page";

export default {
  mixins: [mixin],
  name: "releasing_notices_view",
  data() {
    return {
      form: {
        "title": '', // 通知标题
        "content": '', // 通知内容
      },
      checkList: [],
      options: [],
      recipients: []
    }
  },
  methods: {
    async getUser() {
      let res = await this.$get('~/api/user/get_list')
      if (res && res.result && res.result.list) {
        this.convertUsersToOptions(res.result.list);
      }
    },
    convertUsersToOptions(users) {
      // 按用户组分类
      const groupedUsers = {};
      
      users.forEach(user => {
        const groupName = user.user_group;
        if (!groupedUsers[groupName]) {
          groupedUsers[groupName] = [];
        }
        groupedUsers[groupName].push({
          value: user.user_id,
          label: user.nickname || user.username
        });
      });
      
      // 转换为options格式
      this.options = Object.keys(groupedUsers).map((groupName, index) => {
        return {
          value: index + 1,
          label: groupName,
          children: groupedUsers[groupName]
        };
      });
    },
    async submit() {
      if (!this.form.title) {
        this.$message.error('请输入通知标题');
        return;
      }
      if (!this.form.content) {
        this.$message.error('请输入通知内容');
        return;
      }
      if (this.checkList.length === 0) {
        this.$message.error('请选择通知方式');
        return;
      }
      if (this.recipients.length === 0) {
        this.$message.error('请选择接收人');
        return;
      }
      console.log(this.form);
      console.log(this.checkList);
      console.log(this.recipients);
      await this.$post('~/api/releasing_notices/add', {
        title: this.form.title,
        content: this.form.content,
        type: this.checkList.join(','),
      })
      this.recipients.forEach(async item => {
        let message_inform = {
          title: this.form.title,
          type: '系统',
          content: this.form.content,
          state: 1,
          user_id: item
        }
        await this.$post("~/api/message_inform/add",message_inform)
      })
      this.$router.push({
        path: '/releasing_notices/table'
      })
    }
  },
  created() {
    this.getUser()
  }
}
</script>

<style scoped>

</style>

