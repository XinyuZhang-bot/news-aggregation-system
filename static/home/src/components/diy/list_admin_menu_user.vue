<template>
  <div class="list_menu diy_menu">
    <router-link
            to="/user_center/index"
            class="menu_item"
            :class="{ selected: this.$route.path=== '/user_center/index'}"
     >
      <span class="left_span">个人首页</span>
      <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
    </router-link>
                              <router-link
          to="/ordinary_user/table"
          class="menu_item"
          :class="{ selected: this.$route.path=== '/ordinary_user/table'}"
          v-if="$check_action('/ordinary_user/table','get')">
        <span class="left_span">{{ $page_title("/ordinary_user/table") || "普通用户" }}</span>
        <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
      </router-link>
                                                                                                                                                                                  <router-link
          to="/compileors/table"
          class="menu_item"
          :class="{ selected: this.$route.path=== '/compileors/table'}"
          v-if="$check_action('/compileors/table','get')">
        <span class="left_span">{{ $page_title("/compileors/table") || "编辑人员" }}</span>
        <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
      </router-link>
                                                                                                                                                                                  <router-link
          to="/news_class_nameification/table"
          class="menu_item"
          :class="{ selected: this.$route.path=== '/news_class_nameification/table'}"
          v-if="$check_action('/news_class_nameification/table','get')">
        <span class="left_span">{{ $page_title("/news_class_nameification/table") || "新闻分类" }}</span>
        <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
      </router-link>
                                                                                                                                                                                  <router-link
          to="/news_resources/table"
          class="menu_item"
          :class="{ selected: this.$route.path=== '/news_resources/table'}"
          v-if="$check_action('/news_resources/table','get')">
        <span class="left_span">{{ $page_title("/news_resources/table") || "新闻资源" }}</span>
        <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
      </router-link>
                                                                                                                                                                                  <router-link
          to="/news_information/table"
          class="menu_item"
          :class="{ selected: this.$route.path=== '/news_information/table'}"
          v-if="$check_action('/news_information/table','get')">
        <span class="left_span">{{ $page_title("/news_information/table") || "新闻资讯" }}</span>
        <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
      </router-link>
                                                                                                          <router-link
              to="/user/collect"
              class="menu_item"
              :class="{ selected: this.$route.path=== '/user/collect'}"
              v-if="$check_action('/collect/list','get')">
        <span class="left_span">{{$page_title("/collect/list") || "收藏记录"}}</span>
        <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
  </router-link>
  <router-link
      to="/user/praise"
      class="menu_item"
      :class="{ selected: this.$route.path === '/user/praise' }" 
      v-if="$check_action('/praise/list','get')">
      <span class="left_span">{{$page_title("/praise/list") || "点赞记录"}}</span>
      <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
    </router-link>
	<router-link
	            to="/comment/table"
	            class="menu_item"
	            :class="{ selected: this.$route.path=== '/comment/table'}"
	            v-if="$check_action('/comment/table','get')">
	      <span class="left_span">{{$page_title("/comment/table") || "评论管理"}}</span>
	      <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
	</router-link>
  <router-link
    to="/history/list"
    class="menu_item"
    :class="{ selected: this.$route.path === '/history/list' }"
  >
    <span class="left_span">浏览记录</span>
    <span class="right_span"><b-icon icon="house-fill"></b-icon></span>
  </router-link>
  </div>
</template>

<script>
import mixin from "@/mixins/page.js";
export default {
  mixins: [mixin],
  data() {
    return {
    };
  },
  mounted() {
  },
  methods: {
  },

  components: {
  },
};
</script>

<style scoped>
.list_menu {
  flex: 0 0 25%;
  border-bottom: 1px solid #eee;
}
.menu_item {
  display: flex;
  justify-content: space-between;
  padding: 15px 20px;
  border: 1px solid #eee;
  border-bottom: none;
  background-color: #fff;
}
.menu_item.selected {
  background-color: #000;
}
.menu_item.selected span {
  color: #fff ;
}
.content {
  flex: 0 0 74%;
}
</style>
