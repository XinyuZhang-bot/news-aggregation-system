<template>
<el-col v-if="auth.length > 0 || showUserAccountShortcut" :span="24">
  <div class="card quick-menu-card">
    <div class="card QuickMenu">
      <el-row type="flex" justify="center" align="middle" :gutter="16" class="quick-menu-row">
        <el-col
          v-if="showUserAccountShortcut"
          :xs="12"
          :sm="8"
          :md="4"
          :lg="4"
        >
          <div class="quick-menu-item" @click="moreBtn(userAccountPath)">
            <el-button type="primary" icon="el-icon-user-solid" size="large" class="MenuIcon MenuIcon--fixed" />
            <p class="Menutext">用户账号管理</p>
          </div>
        </el-col>
        <el-col
          :xs="12"
          :sm="8"
          :md="4"
          :lg="4"
          v-for="i in auth"
          :key="i.auth_id"
          v-show="$check_action(i.path)"
        >
          <div class="quick-menu-item" @click="moreBtn(i.path)">
            <el-button :type="i.Bgcolor" :icon="i.Icon" size="large" class="MenuIcon" />
            <p class="Menutext">{{ quickMenuTitle(i) }}</p>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</el-col>
</template>
<script>
  import mixin from "@/mixins/page.js";

  export default {
    mixins: [mixin],
    computed: {
      showUserAccountShortcut() {
        const ug = this.user_group || this.$store.state.user.user_group;
        return (
          ug === "管理员" ||
          (this.$check_action && this.$check_action("/ordinary_user/table")) ||
          (this.$check_action && this.$check_action("/user/table")) ||
          (this.$check_action && this.$check_action("/compileors/table"))
        );
      },
      userAccountPath() {
        if (this.$check_action && this.$check_action("/ordinary_user/table")) {
          return "/ordinary_user/table";
        }
        if (this.user_group === "管理员" || (this.$check_action && this.$check_action("/user/table"))) {
          return "/user/table";
        }
        if (this.$check_action && this.$check_action("/compileors/table")) {
          return "/compileors/table";
        }
        return "/ordinary_user/table";
      },
      auth() {
        // 保留原计算属性逻辑
        let tables = this.$store.state.web.auth;
        let lt = [];
        let site_list = [];
        let colorArr = ["success", "primary", "info", "warning", "danger"];
        let IconArr = ["el-icon-edit", "el-icon-document", "el-icon-menu", "el-icon-location", "el-icon-setting", "el-icon-search"];
                                                                  let list = [
          "exam",
          "article",
          "article_type",
          "comment",
                            "notice",
                                ];
                      list.push("ordinary_user");
                        list.push("compileors");
                                                
        for (let i = 0; i < tables.length; i++) {
          let o = tables[i];
          if (o.path && o.path.indexOf("/table") !== -1) {  // 添加path存在性检查
            if (list.indexOf(o.table_name) === -1) {
              o.has_add = site_list.indexOf(o.table_name) === -1;
              o.Bgcolor = colorArr[parseInt(Math.random() * colorArr.length)];
              o.Icon = IconArr[parseInt(Math.random() * IconArr.length)];
              lt.push(o);
            }
          }
        }
        return lt;
      }
    },
    methods: {
      quickMenuTitle(row) {
        if (!row || !row.mod_name) return "";
        if (row.table_name === "news_resources") return "新闻爬虫管理";
        const m = row.mod_name;
        if (m.endsWith("管理")) return m;
        return m + "管理";
      },
      moreBtn(path) {
        this.$router.push(path);  
      }
    },
    mounted() {

    }
  };
</script>

<style scoped>
  .quick-menu-card {
    margin-bottom: 0.25rem;
  }

  .QuickMenu {
    text-align: center;
    display: block;
    width: 100%;
    position: relative;
    padding: 12px 8px 16px;
  }

  .quick-menu-row {
    flex-wrap: wrap;
  }

  .quick-menu-item {
    cursor: pointer;
    padding: 8px 4px;
    border-radius: 10px;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .quick-menu-item:hover {
    background: #f3f4f6;
    transform: translateY(-2px);
  }

  .QuickMenu .MenuIcon {
    width: 72px;
    height: 72px;
    font-size: 28px;
    padding: 1.25rem;
  }

  .QuickMenu .MenuIcon--fixed {
    border: none;
  }

  .QuickMenu .Menutext {
    font-size: 15px;
    padding-top: 8px;
    line-height: 1.35;
    color: #111827;
    font-weight: 500;
  }
</style>