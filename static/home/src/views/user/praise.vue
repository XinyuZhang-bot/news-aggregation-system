<template>
  <div class="page_user collect_list" id="user_collect">
    <div class="warp">
      <div class="container">
        <div class="row justify-content-between">
          <div class="col-12 col-md-3">
            <div class="card_menu">
              <list_admin_menu_user />
            </div>
          </div>

          <div class="col-12 col-md-9 user_right_box">
            <div class="filter_block_praise">
              <div class="bar_filter">
                <div style="height: 30px"></div>
              </div>
            </div>
            <el-tabs v-model="activeName" @tab-click="handleClick">
              <el-tab-pane
                :label="item.label"
                :name="item.value"
                v-for="item in type_names"
                :key="item.value"
                ><list_praise :list="list"></list_praise
              ></el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import mixin from "@/mixins/page.js";
// import list_menu_user from "@/components/diy/list_menu_user.vue";
import list_admin_menu_user from "@/components/diy/list_admin_menu_user.vue";
import list_praise from "@/components/diy/list_praise.vue";
import { type_names } from "@/utils/typeManage.js"
export default {
  mixins: [mixin],
  data() {
    return {
      url_get_list: "~/api/praise/get_list?",
      query: {
        user_id: this.$store.state.user.user_id,
        orderby: "create_time asc",
      },
      list: [],
      activeName: "all",
      type_names: type_names,
    };
  },
  methods: {
    /**
     * 筛选选择
     */
    filter_cart(o) {
      this.query.source_table = o.value;
      this.search();
    },
    /**
     * 切换tab
     */
    handleClick(tab) {
      this.activeName = tab.name;
      this.query.source_table = tab.name == "all" ? "" : tab.name;
      this.search();
    },
  },
  mounted() {
    // this.title = "收藏分类";
  },
  methods: {
    /**
     * 筛选选择
     */
    filter_cart(o) {
      this.query.source_table = o.value;
      this.search();
    },
    /**
     * 切换tab
     */
    handleClick(tab) {
      this.activeName = tab.name;
      this.query.source_table = tab.name == "all" ? "" : tab.name;
      this.search();
    },
  },
  mounted() {
    // this.title = "收藏分类";
  },
  components: {
    list_admin_menu_user,
    list_praise,
  },
};
</script>

<style scoped>
.container {
  min-height: 800px;
}
.filter_block {
  display: flex;
  flex-direction: row;
  justify-content: start;
  padding: 10px;
}
.bar_filter {
  display: flex;
  align-items: center;
}
li {
  list-style: none;
}
.bar_sort {
  margin-left: 5px;
}
</style>
