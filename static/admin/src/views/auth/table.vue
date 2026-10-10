<template>
  <el-main class="bg table_wrap auth">

    <el-form label-position="right" :model="query" class="form p_4" label-width="120">
      <el-row class="rows row1">
        <el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
          <el-form-item label="权限名">
            <el-input v-model="query.mod_name"></el-input>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
          <el-form-item label="用户组">
            <el-select v-model="query.user_group">
              <el-option v-for="(o,i) in list_user_group" :label="o.name" :value="o.name" :key="i"></el-option>
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
          <el-form-item label="添加权限">
            <el-select v-model="query.add">
              <el-option value="" :key="-1" label=""></el-option>
              <el-option v-for="(o,i) in list_state" :value="o.value" :label="o.name" :key="i">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
          <el-form-item label="修改权限">
            <el-select v-model="query.set">
              <el-option value="" :key="-1" label=""></el-option>
              <el-option v-for="(o,i) in list_state" :value="o.value" :label="o.name" :key="i">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
          <el-form-item label="删除权限">
            <el-select v-model="query.del">
              <el-option value="" :key="-1" label=""></el-option>
              <el-option v-for="(o,i) in list_state" :value="o.value" :label="o.name" :key="i">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
          <el-form-item label="查询权限">
            <el-select v-model="query.get">
              <el-option value="" :key="-1" label=""></el-option>
              <el-option v-for="(o,i) in list_state" :value="o.value" :label="o.name" :key="i">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row class="rows row2">
        <el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap">
          <el-col :xs="24" :sm="12" :lg="12" class="search_btn_1 btns">
            <el-button type="primary" @click="search()" class="search_btn_find">查询</el-button>
              <el-button @click="reset()" class="search_btn_reset">重置</el-button>
          </el-col>
          <!--					<el-col :xs="24" :sm="12" :lg="12" class="search_btn_2">-->
          <!--						<el-form-item>-->
          <!--							<el-button v-if="user_group == '管理员' || $check_action('/auth/table','del')"-->
          <!--								class="float-right search_btn_del" type="danger" @click="delInfo()">删除</el-button>-->
          <!--							<router-link v-if="user_group == '管理员' || $check_action('/auth/view')"-->
          <!--								class="el-button float-right el-button&#45;&#45;default el-button&#45;&#45;primary search_btn_add" to="./view?"><span>添加</span>-->
          <!--							</router-link>-->
          <!--						</el-form-item>-->
          <!--					</el-col>-->
        </el-col>
      </el-row>
    </el-form>

    <el-table border :data="list" @selection-change="selectionChange" style="width: 100%">

      <!-- 多选按钮 -->
      <el-table-column fixed type="selection" tooltip-effect="dark" width="55">
      </el-table-column>
      <!-- /多选按钮 -->

      <el-table-column fixed prop="user_group" label="用户组">
      </el-table-column>

      <el-table-column prop="mod_name" label="权限名称" min-width="200">
        <template slot-scope="scope">
          <div class="view_a">
          <span v-if="scope.row.path.replace('/'+scope.row.table_name+'/','')=='table'">{{scope.row.mod_name+'后台列表'}}</span>
          <span v-if="scope.row.path.replace('/'+scope.row.table_name+'/','')=='view'">{{scope.row.mod_name+'后台详情'}}</span>
          <span v-if="scope.row.path.replace('/'+scope.row.table_name+'/','')=='list'">{{scope.row.mod_name+'前台列表'}}</span>
          <span v-if="scope.row.path.replace('/'+scope.row.table_name+'/','')=='details'">{{scope.row.mod_name+'前台详情'}}</span>
          <span v-if="scope.row.path.replace('/'+scope.row.table_name+'/','')=='edit'">{{scope.row.mod_name+'前台编辑'}}</span>
        </div>
        </template>
      </el-table-column>


<!--      <el-table-column prop="page_title" label="页面标题">-->
<!--      </el-table-column>-->

      <el-table-column prop="add" label="添加权限" min-width="80">
        <template slot-scope="scope">
          {{ scope.row.add==1 ? "有" : "无" }}
        </template>
      </el-table-column>

      <el-table-column prop="set" label="修改权限" min-width="80">
        <template slot-scope="scope">
          {{ scope.row.set==1 ? "有" : "无" }}
        </template>
      </el-table-column>

      <el-table-column prop="del" label="删除权限" min-width="80">
        <template slot-scope="scope">
          {{ scope.row.del==1 ? "有" : "无" }}
        </template>
      </el-table-column>

      <el-table-column prop="get" label="查询权限" min-width="80">
        <template slot-scope="scope">
          {{ scope.row.get==1 ? "有" : "无" }}
        </template>
      </el-table-column>

      <el-table-column sortable prop="create_time" label="创建时间" min-width="200">
        <template slot-scope="scope">
          {{ $toTime(scope.row["create_time"], "yyyy-MM-dd hh:mm:ss") }}
        </template>
      </el-table-column>

      <el-table-column sortable prop="update_time" label="更新时间" min-width="200">
        <template slot-scope="scope">
          {{ $toTime(scope.row["update_time"], "yyyy-MM-dd hh:mm:ss") }}
        </template>
      </el-table-column>

      <!-- 操作 -->
      <el-table-column fixed="right" label="操作" width="120">
        <template slot-scope="scope">
          <router-link v-if="scope.row.user_group != '管理员'"
                       class="e-button el-button--small is-plain el-button--primary"
                       :to="'./view?' + field + '=' + scope.row[field]" size="small">
            <span>修改</span>
          </router-link>
        </template>
      </el-table-column>
      <!-- /操作 -->

    </el-table>

    <!-- 分页器 -->
    <div class="mt text_center">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                     :current-page="query.page" :page-sizes="[10, 15, 30, 50]" :page-size="query.size"
                     layout="total, sizes, prev, pager, next, jumper" :total="count">
      </el-pagination>
    </div>
    <!-- /分页器 -->

  </el-main>
</template>

<script>
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
  data() {
    return {
      table: "auth",
      field: "auth_id",
      url_get_list: "~/api/auth/get_list",
      url_del: "~/api/auth/del?",

      query: {
        size: 15,
        page: 1,
        mod_name: "",
        user_group: "",
        add: "",
        set: "",
        del: "",
        get: "",
      },

      // 数据
      list: [],

      // 获取状态
      list_state: [{
        name: "无",
        value: "0"
      }, {
        name: "有",
        value: "1"
      }],

      list_user_group: []
    }
  },
  methods: {
    async get_list_user_group() {
      var json = await this.$get("~/api/user_group/get_list?");
      if (json.result) {
        this.list_user_group = json.result.list;
      } else if (json.error) {
        console.error(json.error);
      }
    },

    table_class({
                  row,
                  column,
                  rowIndex,
                  columnIndex
                }) {
      return "table_class";
    }
  },
  created() {
    this.get_list_user_group();
  }
}
</script>

<style>

</style>
