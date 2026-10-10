<template>
  <el-menu ref="menu" class="side el-menu-vertical-demo" default-active="$route.path" @open="handleOpen" @close="handleClose"
           background-color="#ffffff" text-color="#111827" active-text-color="#2563eb" :collapse="isCollapse" :router="true">

    <span class="hide-avatar" style="display: none;">
      <img :src="$fullUrl($store.state.user.avatar)" alt="avatar">
    </span>
    <span class="hide-username" style="display:none;">
       {{ $store.state.user.nickname || $store.state.user.username }}
    </span>

    <el-menu-item index="/" @click="handleButtonClick('后台首页')">
      <i class="el-icon-s-home"></i>
      <span slot="title">后台首页</span>
    </el-menu-item>

     <el-submenu index="user"
                v-show="user_group == '管理员' || $check_group(['/user/table','/user_group/table'
                                                                        ,'/ordinary_user/table'
                                                                                                ,'/compileors/table'
                                                                                                                                                                                                    ])">
      <template slot="title"><i class="el-icon-s-custom"></i><span ref="customTemplate8">用户账号管理</span></template>
      <el-menu-item index="/user/table" v-show="user_group == '管理员'" @click="handleButtonClick(8)"><span>管理员</span></el-menu-item>
                                  <el-menu-item index="/ordinary_user/table" v-show="$check_action('/ordinary_user/table')" @click="handleButtonClick(8)">
                <span>普通用户</span></el-menu-item>
                                              <el-menu-item index="/compileors/table" v-show="$check_action('/compileors/table')" @click="handleButtonClick(8)">
                <span>编辑人员</span></el-menu-item>
                                                                                      <!-- <el-menu-item index="/user_group/table"><span>用户组</span></el-menu-item> -->
    </el-submenu>

	<el-submenu class="Cust" :index="i.id" v-for="i in auth" :key="i.id" v-show="$check_action(i.path)">
	  <template slot="title">
	    <i class="el-icon-news"></i>
	    <span v-if="!i.children.length">{{ sideGroupTitle(i) }}</span>
	    <span v-else>{{ i.mod_name }}</span>
	  </template>
	  <div v-if="!i.children.length">
	    <el-menu-item menu-trigger :index="i.path" :class="{ active: $route.path === i.path }" @click="handleButtonClick(`${i.mod_name}管理`)">
	      <span>{{ listMenuTitle(i) }}</span>
	    </el-menu-item>
	    <el-menu-item v-if="i.table_name !== 'news_resources' && i.has_add && $check_action(i.path.replace(/(.*)table/, '$1view'), 'add')" :index="i.path.replace(/(.*)table/, '$1view')" :class="{ sactive: $route.path === i.path }" @click="handleButtonClick(` ${i.mod_name}管理`)">
	      <span>{{ addMenuTitle(i) }}</span>
	    </el-menu-item>
				    	  </div>
	  <div v-else>
	    <el-submenu class="Cust" :index="'child'+ item.id" v-for="(item) in i.children" :key="item.id" v-show="$check_action(item.path)">
	      <template slot="title">
	        <i class="el-icon-news"></i>
	        <span>{{ sideGroupTitle(item) }}</span>
	      </template>
	      <div>
	        <el-menu-item menu-trigger :index="item.path" :class="{ active: $route.path === item.path }" @click="handleButtonClick(`${item.mod_name}管理`)">
	          <span>{{ listMenuTitle(item) }}</span>
	        </el-menu-item>
	        <el-menu-item v-if="item.table_name !== 'news_resources' && item.has_add && $check_action(item.path.replace(/(.*)table/, '$1view'), 'add')" :index="item.path.replace(/(.*)table/, '$1view')" :class="{ sactive: $route.path === item.path }" @click="handleButtonClick(` ${item.mod_name}管理`)">
	          <span>{{ addMenuTitle(item) }}</span>
	        </el-menu-item>
										      </div>
	    </el-submenu>
	  </div>
	</el-submenu>

              <el-submenu index="web"
                    v-show="user_group == '管理员' || $check_group(['/nav/table','/link/table','/slides/table','/ad/table','/sensitive_vocabulary/table'])">
          <template slot="title"><i class="el-icon-picture-outline"></i><span ref="customTemplate1">系统管理</span></template>
                      <el-menu-item v-show="user_group == '管理员' || $check_action('/slides/table')" index="/slides/table" @click="handleButtonClick(1)">
            <span>轮播图管理</span>
          </el-menu-item>
                                      <el-menu-item v-show="user_group == '管理员' || $check_action('/sensitive_vocabulary/table')" index="/sensitive_vocabulary/table" @click="handleButtonClick(1)">
                <span>敏感词管理</span>
              </el-menu-item>
                                </el-submenu>

      

    
              <el-submenu index="notic"
                    v-show="$check_group(['/notice/table'])">
          <template slot="title"><i class="el-icon-warning-outline"></i><span ref="customTemplate2">最新公告管理</span>
          </template>
          <el-menu-item v-show="$check_action('/notice/table')" index="/notice/table" @click="handleButtonClick(2)">
            <span>最新公告</span>
          </el-menu-item>
        </el-submenu>
      

                            <el-submenu index="news"
                        v-show="$check_group(['/article/table','/article_type/table','/exam/table','/evaluation/table'])">
              <template slot="title"><i class="el-icon-s-opportunity"></i><span ref="customTemplate3">热点新闻管理</span></template>

                                  <el-menu-item v-show="$check_action('/article/table')" index="/article/table" @click="handleButtonClick(3)">
                    <!-- <span>文章</span> -->
                    <span>{{$page_title("/article/table") || "文章"}}</span>
                  </el-menu-item>
                  <el-menu-item v-show="$check_action('/article_type/table')"
                                index="/article_type/table" @click="handleButtonClick(3)">
                    <!-- <span>文章类型</span> -->
                    <span>{{$page_title("/article_type/table") || "文章分类"}}</span>
                  </el-menu-item>
                                				            </el-submenu>
                            

      


              <el-submenu index="auth"
                    v-show="user_group == '管理员'">
          <template slot="title"><i class="el-icon-s-custom"></i><span ref="customTemplate9">权限管理</span></template>
          <el-menu-item index="/auth/table" v-show="user_group == '管理员'" @click="handleButtonClick(9)"><span>权限列表</span></el-menu-item>
        </el-submenu>
      
	  	    <el-submenu index="operatelog" v-show="user_group == '管理员'">
	      <template slot="title"><i class="el-icon-s-custom"></i><span ref="customTemplate11">操作日志</span></template>
	      <el-menu-item index="/operation_log/table" v-show="user_group == '管理员'" @click="handleButtonClick(11)"><span>日志列表</span></el-menu-item>
	    </el-submenu>
	  
    

  </el-menu>
</template>

<script>
  export default {
    props: {
      isCollapse: {
        trye: Boolean,
        default: false
      }
    },
    data: function () {
      return {
        user_group: this.$store.state.user.user_group
      }
    },
    methods: {
      sideGroupTitle(row) {
        if (!row) return "";
        if (row.table_name === "news_resources") return "新闻爬虫管理";
        const m = row.mod_name || "";
        if (m.endsWith("管理")) return m;
        return m + "管理";
      },
      listMenuTitle(row) {
        if (!row) return "";
        if (row.table_name === "news_resources") return "新闻爬虫";
        if (row.table_name === "news_information") return "新闻列表";
        return (row.page_title || "") + "列表";
      },
      addMenuTitle(row) {
        if (!row) return "";
        if (row.table_name === "news_information") return "新闻发布";
        if (row.table_name === "news_resources") return "";
        return (row.page_title || "") + "添加";
      },
      handleOpen(key, keyPath) {
        // console.log(key, keyPath);
      },

      handleClose(key, keyPath) {
        // console.log(key, keyPath);
      },
       handleButtonClick(buttonId) {
      let lis_title;
      const templateRefs = [
        null, // 索引 0 不使用
        this.$refs.customTemplate1,
        this.$refs.customTemplate2,
        this.$refs.customTemplate3,
        this.$refs.customTemplate4,
        this.$refs.customTemplate5,
        this.$refs.customTemplate6,
        this.$refs.customTemplate7,
        this.$refs.customTemplate8,
        this.$refs.customTemplate9,
        this.$refs.customTemplate10,
        this.$refs.customTemplate11,
        this.$refs.customTemplate12,
      ];

      if (buttonId >= 1 && buttonId <= templateRefs.length) {
        lis_title = templateRefs[buttonId];
        sessionStorage.setItem('title-text', buttonId.toString());
      } else {
        sessionStorage.setItem('title-text', buttonId);
      }

      if (lis_title) {
        this.text = lis_title.innerText;
        console.log(this.text);
        sessionStorage.setItem('title-text', this.text);
      }
      // sessionStorage.setItem('title-text', buttonId)
    }

    },
    computed: {
      auth() {
        var tables = this.$store.state.web.auth;
        var lt = [];
        let site_list = []
		    let map_list = []
        let forecast_list = []
        let seat_list = []
                                                                                                                                                                                                                                                                let list = ["exam", 'evaluation', "article", "article_type", "comment", "notice"];
                                      list.push("ordinary_user");
                                        list.push("compileors");
                                                                                for (var i = 0; i < tables.length; i++) {
          var o = tables[i];
          if (o.path.indexOf("/table") !== -1) {
            if (list.indexOf(o.table_name) === -1) {
              o.has_add = site_list.indexOf(o.table_name) === -1;
			                                lt.push(o);
            }
          }
        }

        let lt2 = [];
        for (var i = 0; i < lt.length; i++) {
          const o = lt[i];
          const id = `${o.parent}-${o.mod_name}-${o.auth_id}-${i}`
          if (!o.parent) {
            lt2.push({ ...o, id, children: [] });
          } else {
            const parentIndex = lt2.findIndex((el) => el.mod_name === o.parent);
            if (parentIndex !== -1) {
              lt2[parentIndex].children.push({...o, id});
            } else {
              lt2.push({
                ...o,
                // path: '/' + o.parent + o.mod_name + o.auth_id,
                mod_name: o.parent,
                children: [{...o, id}],
                id
              });
            }
          }
        }
        console.log('lt======', lt2);

        return lt2.sort((a, b) => a.parent_sort - b.parent_sort);
      }
    },
	watch: {
	    $route: {
	      handler(to) {
	        // 路由变化时更新当前激活菜单
	        this.$nextTick(() => {
	          if(this.$refs.menu) {
	            this.$refs.menu.activeIndex = to.path;
	          }
	        });
	      },
	      immediate: true
	    }
	}
  }
</script>


<style scoped="scoped">
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 16rem;
  }

  .side {
    float: left;
    background: #ffffff;
    color: #111827;
    overflow-y: scroll;
    height: 100vh;
    border-right: none;
    box-shadow: none;
  }
.active {
  color: #2563eb !important;
}

.sactive {
  color: #2563eb !important;
}
  .side::-webkit-scrollbar {
    display: none;
  }

	/* 侧栏菜单视觉优化（保持功能不变） */
	::v-deep .el-menu {
		border-right: none;
		background: transparent !important;
	}

	::v-deep .el-menu-item,
	::v-deep .el-submenu__title {
		color: #111827 !important;
		height: 44px;
		line-height: 44px;
		margin: 4px 8px;
		border-radius: 8px;
		border: 1px solid transparent;
		transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
	}

	::v-deep .el-menu-item:hover,
	::v-deep .el-submenu__title:hover {
		background: #f3f4f6 !important;
		border-color: #e5e7eb;
	}

	::v-deep .el-menu-item.is-active {
		background: #eff6ff !important;
		color: #1d4ed8 !important;
		font-weight: 600;
		border-color: #bfdbfe;
	}

	::v-deep .el-submenu .el-menu-item {
		background: #ffffff !important;
	}

	::v-deep .el-menu-item i,
	::v-deep .el-submenu__title i {
		color: #6b7280;
	}
</style>
