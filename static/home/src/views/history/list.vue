  <!-- // 增加前台用户的浏览记录开始 -->
<template>
  <div class="page_user collect_list" id="user_collect">
    <div class="warp">
      <div class="container">
        <div class="row justify-content-between">
        
          <div class="col-12 col-md-3">
            <div class="card_menu">
              <list_admin_menu_user/>
            </div>
          </div>
        
          <div class="col-12 col-md-9 user_right_box">
            <list_history></list_history>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import list_admin_menu_user from "@/components/diy/list_admin_menu_user.vue";
import list_history from "@/components/diy/list_history.vue";
export default {
  data() {
    return {
    };
  },
  methods: {
  },
  mounted() {
    
  },
  components: {
   // list_menu_user,
   list_admin_menu_user,
   list_history,
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
  <!-- // 增加前台用户的浏览记录结束 -->
