<template>
  <div class="page_header mall-header">
    <transition name="fade">
      <div v-show="visible" class="header_warp mall-header__warp">
        <div class="mall-header__topline" aria-hidden="true"></div>
        <div class="container mall-header__inner mall-header__inner--pad">
          <div class="row">
            <div class="col-12">
              <div class="my_header mall-header__layout">

                <div class="conton-top mall-header__toolbar">
                  <router-link to="/" class="mall-header__brand">
                    <span class="mall-header__logo-mark" aria-hidden="true">N</span>
                    <div class="mall-header__brand-text">
                      <div class="logo mall-header__site-name">新闻聚合系统</div>
                    </div>
                  </router-link>

                  <div ref="search" class="search-box mall-header__search">
                  <div class="mall-header__search-inner mall-header__search-pill">
                  <input
                    class="search-txt mall-header__input"
                    v-model.trim="search_val"
                    type="text"
                    placeholder="输入关键词搜索新闻..."
                    @keyup.enter="submit_search"
                  >
                  <button type="button" class="search-btn mall-header__search-icon" @click="submit_search" aria-label="搜索">
                    <svg viewBox="0 0 16 16" width="18" height="18" fill="currentColor" aria-hidden="true">
                      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                    </svg>
                  </button>
                  </div>
                  </div>


                  <div class="user mall-header__user mall-header__user--guest" v-if="!user.user_id">
                    <router-link
                      class="mall-header__auth-btn mall-header__auth-btn--login"
                      :to="not_login_dropdown[0].url"
                    >
                      {{ not_login_dropdown[0].name }}
                    </router-link>
                    <router-link
                      class="mall-header__auth-btn mall-header__auth-btn--register"
                      :to="not_login_dropdown[1].url"
                    >
                      {{ not_login_dropdown[1].name }}
                    </router-link>
                  </div>
                  <div ref="my" v-else class="user mall-header__user">
                            <el-badge :value="msgSum" :hidden="msgSum === 0" :max="99" class="mall-header__notify-wrap">
                      <div class="mall-header__notify" @click="drawer = true">
                        <i class="el-icon-bell mall-header__bell"></i>
                        <span class="mall-header__notify-label">通知</span>
                      </div>
                    </el-badge>
                            <div ref="own" class="own" @click="my()">
                      <div class="user_pr">
                        <div class="img_box" >
                          <img class="user_img" style="width: 40px;" :src="$fullUrl(user_avatar)" alt="">
                        </div>
                        <div class="own_text">
                          <span class="own_text__name">{{ user_nickname }}</span>
                          <span class="caret" v-bind:style="{transform: 'rotate('+ angle2 +'deg)'}"/>
                        </div>
                      </div>

                    </div>
                    <div v-show="my_show" class="dropdown">
                      <div class="my_item" v-for="(o,i) in my_nav">
                        <router-link :to="o.url">
                          {{o.name}}
                        </router-link>
                      </div>
									  <div class="my_item" v-if="my_home_page_auth">
                        <router-link :to="'/user/my_home_page?follower_id=' + user.user_id">
                          我的主页
                        </router-link>
                      </div>
				                      <div class="my_item">
                        <router-link to="/user_center/index">
                          个人中心
                        </router-link>
                      </div>
                      <div class="my_item" @click="sign_out()">
                        <router-link to="/">
                          退出
                        </router-link>
                      </div>
                    </div>
                  </div>

                </div>

                <div ref="nav_target" class="nav_list mall-header__nav">
                  <ul class="nav_ul mall-header__nav-ul">
                    <li class="nav_li" :class="{active:$route.path==='/'}">
                      <router-link to="/" class="nav_a">
                        首页
                      </router-link>
                    </li>
                                                                              <li v-if="isInNavTop('ordinary_user')" class="nav_li" :class="{active:$route.path===getTablePath('ordinary_user')}">
                      <router-link :to="getTablePath('ordinary_user')" class="nav_a">
                        {{getPageTitle('ordinary_user')}}
                      </router-link>
                    </li>
                                                                                  <li v-if="isInNavTop('compileors')" class="nav_li" :class="{active:$route.path===getTablePath('compileors')}">
                      <router-link :to="getTablePath('compileors')" class="nav_a">
                        {{getPageTitle('compileors')}}
                      </router-link>
                    </li>
                                                                                  <li v-if="isInNavTop('news_class_nameification')" class="nav_li" :class="{active:$route.path===getTablePath('news_class_nameification')}">
                      <router-link :to="getTablePath('news_class_nameification')" class="nav_a">
                        {{getPageTitle('news_class_nameification')}}
                      </router-link>
                    </li>
                                                                                  <li v-if="isInNavTop('news_resources')" class="nav_li" :class="{active:$route.path===getTablePath('news_resources')}">
                      <router-link :to="getTablePath('news_resources')" class="nav_a">
                        {{getPageTitle('news_resources')}}
                      </router-link>
                    </li>
                                                                                  <li v-if="isInNavTop('news_information')" class="nav_li" :class="{active:$route.path===getTablePath('news_information')}">
                      <router-link :to="getTablePath('news_information')" class="nav_a">
                        {{getPageTitle('news_information')}}
                      </router-link>
                    </li>
                                                                                  <li
                      class="nav_li"
                      v-if="$check_action('/news_information/list','get')"
                      :class="{active:$route.path==='/news_information/recommend'}"
                    >
                      <router-link to="/news_information/recommend" class="nav_a">
                        猜你喜欢
                      </router-link>
                    </li>
                                                      <li class="nav_li" v-if="$check_action('/article/list','get')" :class="{active:$route.path==='/article/list'}">
                      <router-link to="/article/list" class="nav_a">
                        {{"热点专题" || "新闻通知"}}
                      </router-link>
                    </li>
                                                                              <li class="nav_li" v-if="$check_action('/notice/list','get')" :class="{active:$route.path==='/notice/list'}">
                      <router-link to="/notice/list" class="nav_a">
                        最新公告
                      </router-link>
                    </li>
                                                        </ul>
                </div>

                <div ref="mini" class="mini_nav" @click="open_mini()">
                  <div ref="mini" class="mini">
                    <span class="mini_text">菜单</span>
                    <span class="caret" v-bind:style="
												{transform: 'rotate('+ angle3 +'deg)'}"/>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <el-drawer
      title="通知中心"
      :size="400"
      :visible.sync="drawer"
      :modal="false">
      <div style="padding: 0 20px">
        <div style="padding-top: 5px">
          <el-badge v-for="(item,index) in messageTypeList" :key="index" :is-dot="isRead(item)" class="" style="margin-right: 10px;">
            <el-button size="mini" @click="handleClick(item)">{{item}}</el-button>
          </el-badge>
        </div>
        <div style="display: flex;justify-content: flex-end;">
          <el-button type="text" @click="readAll">全部已读</el-button>
          <el-button type="text" @click="clearAll">清除</el-button>
        </div>
        <div style="height: 80vh;overflow: auto;padding: 10px">
          <div v-if="messageType === '私信'">
            <div
              v-for="item in privateConversationList"
              :key="item.conversation_key"
              @click="openPrivateConversation(item)"
              style="margin-bottom: 10px; padding: 10px; border: 1px solid #eee; border-radius: 8px; cursor: pointer;"
            >
              <el-badge :is-dot="item.unread_count > 0" class="item">
                <span style="font-size: 14px;font-weight: 700;">{{item.peer_nickname}}</span>
              </el-badge>
              <div style="font-size: 14px;color: #666;white-space: pre-line;margin-top: 4px;">{{item.last_message || '暂无消息'}}</div>
              <div style="font-size: 14px;color: #999;">{{ $toTime( item.last_time,"yyyy-MM-dd hh:mm:ss") }}</div>
            </div>
            <div v-if="privateConversationList.length === 0" style="color: #999;padding: 20px 0;">暂无私信会话</div>
          </div>
          <div v-else v-for="item in messageInformList" :key="item.message_inform_id" @click="setState(item)" style="margin-bottom: 10px;">
            <el-badge :is-dot="item.state==1?true : false" class="item">
              <span style="font-size: 14px;font-weight: 700;">{{item.title}}</span>
            </el-badge>
            <span style="font-size: 14px;color: #999;white-space: pre-line;">{{item.content}}</span>
            <div style="font-size: 14px;color: #999;">{{ $toTime( item.create_time,"yyyy-MM-dd hh:mm:ss") }}</div>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>

</template>

<script>

  import mixin from "@/mixins/component.js";

  const OFFSET_HEIGHT = 110;
  export default {

    mixins: [mixin],

    data() {
      return {
              drawer: false,
        messageType: "通知",
        messageInformList: [],
        messageInformListAll: [],
        messageTypeList: [],
        privateConversationList: [],
        msgList: [],
        msgSum: 0,
        getMessageInformListTimer: null,
              top_max: 15,
        angle1: 0,
        angle2: 0,
        angle3: 0,
        visible: true,
        show: false,
        my_show: false,
        nav_top: [],
        my_cart:[
                   ],
        my_nav: [
          {
            name: "我的账户",
            url: "/user/index",
          },


        ],
        not_login_dropdown: [{
          name: "登录",
          url: "/account/login",
        },
                          {
                name: "注册",
                url: "/account/register",
              },
                    ],
        showInput: false,
        search_val: "",
        logo: "",
        user_nickname:'',
        user_avatar:'',
        my_home_page_auth_list: [
          "forum",
                                                                                                    "news_information",
                          ],
              };
    },
    computed: {
      my_home_page_auth() {
        return this.my_home_page_auth_list.some(item =>
          this.$check_action('/' + item + '/list', 'get')
        );
      }
    },
    updated(){
      this.up_gd()
    },

    methods: {
        async getPrivateConversationList() {
        if(!this.user || !this.user.user_id) {
          this.privateConversationList = []
          return
        }
        let res = await this.$get("~/api/private_message/conversation_list")
        this.privateConversationList = (res && res.result && res.result.list) ? res.result.list : []
      },
        async getMessageInformList() {
        if(!this.user || !this.user.user_id) {
          this.messageInformList = []
          this.messageInformListAll = []
          this.messageTypeList = []
          this.privateConversationList = []
          this.msgSum = 0
          return
        }
        await this.getPrivateConversationList()
        if(this.user.user_group == '管理员') {
          let list = await this.$get("~/api/message_inform/get_list",{type: '消息'})
          this.msgList = list.result.list
        }
        let listAll = await this.$get("~/api/message_inform/get_list?user_id=" + this.user.user_id + "&like=0")
        this.messageInformListAll = [...listAll.result.list,...this.msgList]
        this.msgSum = 0
        this.messageInformListAll.forEach(item => {
          if(item.state == 1) {
            this.msgSum++
          }
        })
        this.privateConversationList.forEach(item => {
          this.msgSum += Number(item.unread_count || 0)
        })
        let arr = this.messageInformListAll.map(item => {
					return item.type
				})
        // 去重
				this.messageTypeList = [...new Set(arr)]
        this.messageTypeList = ['私信', ...this.messageTypeList.filter(item => item !== '私信')]

        let list = await this.$get("~/api/message_inform/get_list?user_id=" + this.user.user_id + "&like=0",{type: this.messageType})
        if(this.messageType == '消息') {
          this.messageInformList = this.msgList
        }else if(this.messageType == '私信') {
          this.messageInformList = []
        }else {
          this.messageInformList = list.result.list
        }
        this.handleClick(this.messageTypeList[0])
      },

      async handleClick(type) {
        this.messageType = type
        if(type == '私信') {
          await this.getPrivateConversationList()
          return
        }
        if(type == '消息') {
          this.messageInformList = this.msgList
          return
        }
        let res = await this.$get("~/api/message_inform/get_list?user_id=" + this.user.user_id + "&like=0", {
          type,
        })
        this.messageInformList = res.result.list
      },

      isRead(type) {
        if(type == '私信') {
          return this.privateConversationList.some(item => Number(item.unread_count || 0) > 0)
        }
        let state = false
        let list = this.messageInformListAll.filter(item => {
          return item.type == type
        })
        if(list.length == 0) {
          state = false
          return state
        }
        list.forEach(item => {
          if(item.state == 1) {
            state = true
          }
        });
        return state
      },

      readAll() {
        if(this.messageType == '私信') {
          this.privateConversationList.forEach(async item => {
            await this.$post('~/api/private_message/mark_read', { user_id: item.peer_id })
          })
          this.getMessageInformList()
          return
        }
        this.messageInformList.forEach(async item => {
          await this.$post('~/api/message_inform/set?message_inform_id=' + item.message_inform_id,{state: 0})
        })
        this.getMessageInformList()
      },

      clearAll() {
        if(this.messageType == '私信') {
          this.$message.info("私信会话不支持在通知中心直接清除，请进入聊天页查看")
          return
        }
        this.messageInformList.forEach(async item => {
          await this.$get('~/api/message_inform/del?message_inform_id=' + item.message_inform_id)
        })
        this.getMessageInformList()
      },

      async setState(item) {
        await this.$post('~/api/message_inform/set?message_inform_id=' + item.message_inform_id,{state: 0})
        this.getMessageInformList()
      },
      async openPrivateConversation(item) {
        if(item.unread_count) {
          await this.$post('~/api/private_message/mark_read', { user_id: item.peer_id })
        }
        this.drawer = false
        this.$router.push('/user/chat?user_id=' + item.peer_id)
      },
        up_gd(){
        if (this.$store.state.user){
          let avatar = this.$store.state.user.avatar
          this.user_avatar = avatar
          let u_nickname = this.$store.state.user.nickname
          this.user_nickname = u_nickname
        }
      },

      async get_user_GD(){
       let sd = await this.$get("~/api/user/get_list?")

        let userD = sd.result.list

        let userG = this.$store.state.user.user_group

        for (let i = 0; i < userD.length; i++) {
          const dara = userD[i];

          if (dara.user_group === userG) {
           sessionStorage.setItem('avatar',dara.avatar)
            sessionStorage.setItem('nickname',dara.nickname)
            return
          }
        }

      },


      to_admin() {
        this.$router.push("/user_center/index");
      },

      // 获取导航栏
      async get_nav_top() {
        var auth = this.$store.state.web.auth;

        if (auth.length > 0) {
          var arr = [];
          for (var i = 0; i < auth.length; i++) {
            var o = auth[i];
            if (o["position"] == "top") {
              arr.push(o);
            }
          }
          this.nav_top = arr;
        } else {
          var user_group = this.$store.state.user.user_group || $.db.get("user_group") || "游客";
          var res = await this.$get("~/api/auth/get_list?like=0", {
            user_group,
            "get": 1,
            "position": "top",
            "page": ""
          });
          if (res.result && res.result.list) {
            this.nav_top = res.result.list;
          }
        }
      },

      sign_out() {
        this.$store.commit("sign_out");
        this.$get("~/api/user/quit?", {}, (res) => {
          console.log(res);
        })
        sessionStorage.removeItem('nickname');
        sessionStorage.removeItem('avatar');
        sessionStorage.removeItem('user_id');
        location.reload();
        // location.href = location.href
      },

      submit_search() {
        if (this.search_val.trim() === '') {
          return;
        }
        this.$router.push("/search?word=" + encodeURIComponent(this.search_val.trim()));
      },

      change() {
        var _this = this;

        _this.show = !_this.show;
        var angle = _this.angle1;
        angle = angle + 180;
        if (angle === 360) {
          _this.angle1 = 0;
        } else {
          _this.angle1 = angle;
        }
      },

      my() {
        var _this = this;
        if (_this.angle3 === 180) {
          _this.$refs.nav_target.style.display = 'none';
          _this.$refs.search.style.display = 'none';
          _this.angle3 = 0;
        }
        _this.my_show = !_this.my_show;
        var angle = _this.angle2;
        angle = angle + 180;
        if (angle === 360) {
          _this.angle2 = 0
        } else {
          _this.angle2 = angle;
        }
      },

      open_mini() {
        var _this = this;
        if (_this.my_show) {
          _this.my_show = false;
        }
        var angle = _this.angle3;
        angle = angle + 180;
        if (angle === 360) {
          _this.$refs.nav_target.style.display = 'none';
          _this.$refs.search.style.display = 'none';
          _this.angle3 = 0;
        } else {
          _this.$refs.nav_target.style.display = 'block';
          _this.$refs.search.style.display = 'flex';
          _this.angle3 = angle;
        }
      },

      // 滚动隐藏
      handleScroll() {
        const offsetTop = window.pageYOffset || document.documentElement.scrollTop;
        this.visible = offsetTop < OFFSET_HEIGHT;
      },

      keep(width) {
        var _this = this;
        var display = _this.$refs.nav_target.style.display;
        if (width >= 960 && display === 'none') {
          _this.$refs.nav_target.style.display = 'block';
          this.$refs.search.style.display = 'flex';
        }
      },
      isInNavTop(table_name) {
        // 使用 some 方法检查是否有匹配的 table_name
        return this.nav_top.some(item => item.table_name === table_name);
      },
      getTablePath(table_name) {
        const matchedItem = this.nav_top.find(item => item.table_name === table_name);
        return matchedItem ? matchedItem.path : null;
      },
      getPageTitle(table_name) {
        const matchedItem = this.nav_top.find(item => item.table_name === table_name);
        return matchedItem ? matchedItem.page_title : null;
      },
          },

    created() {
      this.get_nav_top();
      this.logo = document.logo
      if(!this.user.user_id) {
        this.$get_auth('游客')
      }
    },

    mounted() {
        this.get_user_GD()
      this.getMessageInformListTimer && clearTimeout(this.getMessageInformListTimer)
    this.getMessageInformListTimer = setTimeout(() => {
      this.getMessageInformList()
    },500)
  
      window.onresize = () => {
        return (() => {
          this.keep(document.body.clientWidth);
        })();
      };
      window.addEventListener('scroll', this.handleScroll);
      document.addEventListener('mouseup', (e) => {
        const _this = this;
        let tree = _this.$refs.more;
        let my = _this.$refs.my;
        if (tree) {
          if (!tree.contains(e.target)) {
            _this.show = false;
            _this.angle1 = 0;
          }
        }
        if (my) {
          if (!my.contains(e.target)) {
            _this.my_show = false;
            _this.angle2 = 0;
          }
        }
      });
    },

    destroyed() {
      window.removeEventListener('scroll', this.handleScroll);
    },

  };

</script>

<style scoped="scoped">

  .header_warp {
    background-color: var(--color_primary);
    height: 4rem;
    color: white;
    font-weight: 600;
    box-shadow: 0 0.1rem 0.3rem rgba(0, 0, 0, 0.15);
  }

  .my_header {
    display: block;
    height: 4rem;
  }

  .my_header .active {
    background-color: transparent;
  }

  .logo {
    font-size: 1.3rem;
    float: left;
    height: 4rem;

    display: flex;
    justify-content: center;
    align-items: center;
  }

  .nav_list {
    float: left;
  }

  .caret {
    margin-left: 0.875rem;
    display: inline-block;
    width: 0;
    height: 0;
    vertical-align: middle;
    border-top: 4px dashed;
    border-right: 4px solid transparent;
    border-left: 4px solid transparent;
    transition: transform 0.2s;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: all 0.5s;
  }

  .fade-enter,
  .fade-leave-to {
    transform: translateY(-110px);
  }

  ul {
    margin: 0;
    padding: 0;
  }

  li {
    float: left;
    list-style: none;
  }

  li a {
    color: #ddd;
    height: 4rem;
    width: 5rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .more {
    height: 4rem;
    width: 4rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .caret:hover,
  .more:hover {
    cursor: pointer;
    color: #909399;
  }

  .dropdown {
    position: absolute;
    top: 5rem;
    left: -1.5rem;
    height: auto;
    background-color: white;
    width: 8rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
    display: flex;
    border-radius: 0.3rem;
    flex-direction: column;
    font-size: 0.8rem;
  }

  .dropdown .my_item a {
    color: #000 !important;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 3rem;
  }

  .dropdown .my_item a:hover {
    border-radius: 0.3rem;
    color: #fff !important;
  }

  .dropdown .my_item div {
    color: #000 !important;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 3rem;
    cursor: pointer;
  }

  .dropdown .my_item div:hover {
    border-radius: 0.3rem;
    color: #fff !important;
  }

  .dropdown .my_item:hover {
    background-color: #909399;
  }

  .dropdown .item a {
    color: #000 !important;
    margin: auto;
    height: 3rem;
    width: 100%;
  }

  .dropdown .item a:hover {
    border-radius: 0.3rem;
    color: #fff !important;
    background-color: #909399;
  }

  .user {
    position: relative;
    margin-left: 2rem;
    height: 4rem;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    float: right;
   /* width: 6rem;*/
    margin-right: 1rem;
  }

  .own:hover {
    color: #909399;
    cursor: pointer;
  }

  .search-box {
    width: 15rem;
    height: 4rem;
    float: right;
    position: relative;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }

  .search_pic {
    width: 1rem;
    height: 1rem;
  }

  .user_pr {
    display: flex;
}

.img_box {
    width: 50px;
    height: 50px;
}

img.user_img {
    width: 100%;
    object-fit: contain;
}

span.own_text {
    display: block;
    text-align: center;
    line-height: 50px;
    padding-left: 15px;
}



  .search-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    background: #909399;
    border: 0;
    opacity: 1;
    border-radius: 0 4px 4px 0;
  }

  .search-btn:hover {
    cursor: pointer;
  }

  .search-txt {
    height: 2.5rem;
    background: #FFFFFF;
    border: 1px solid #ddd;
    opacity: 1;
    border-right: none;
    border-radius: 4px 0 0 4px;
    width: 12.5rem
  }

  .mini_nav {
    display: none;
  }

  @media (max-width: 1200px) {

    .search-box {
      width: 10rem;
    }

    .search-txt {
      width: 7.5rem
    }

    .user {
      margin-left: 0;
    }
  }

  @media (max-width: 960px) {

    .nav_list {
      color: var(--color_primary);
      padding-top: 3.5rem;
      background-color: white;
      display: none;
      position: absolute;
      top: 8.5rem;
      right: 6rem;
      width: 12rem;
      /*height: 20rem;*/
      border-radius: 0.5rem;
      box-shadow: 0 0.1rem 0.3rem rgba(0, 0, 0, 0.15);
    }

    .nav_list ul {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    .dropdown {
      left: -2rem;
    }

    .search-box {
      position: absolute;
      top: 8.5rem;
      right: 7rem;
      display: none;
    }


    .mini_nav {
      float: right;
      width: 4rem;
      height: 4rem;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .dropdown {
      left: -4rem;
      width: 12rem;
    }

    .user .dropdown {
      left: -3rem;
      width: 8rem;
    }

    .mall-header .nav_list.mall-header__nav .nav_a {
      color: #333 !important;
    }

  }

  /* 门户风顶栏：白底、居中搜索、红色主操作 */
  .mall-header__topline {
    height: 2px;
    background: linear-gradient(90deg, #e4393c, #ff7875);
  }

  .mall-header .header_warp.mall-header__warp {
    position: sticky;
    top: 0;
    z-index: 1001;
    background-color: #fff !important;
    color: #333 !important;
    height: auto !important;
    min-height: auto !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  }

  .mall-header .mall-header__inner--pad {
    padding-left: 20px;
    padding-right: 40px;
    max-width: 1200px;
    box-sizing: border-box;
  }

  .mall-header .my_header.mall-header__layout {
    height: auto !important;
  }

  .mall-header .mall-header__toolbar {
    display: flex !important;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px 32px;
    padding: 14px 0 10px;
    float: none !important;
    width: 100%;
  }

  .mall-header .mall-header__brand {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: #333 !important;
    min-width: 0;
    flex: 0 0 auto;
    margin-right: 12px;
    font-style: normal !important;
  }

  .mall-header .mall-header__brand .mall-header__site-name.logo {
    font-style: normal !important;
  }

  .mall-header .mall-header__brand-text {
    font-style: normal !important;
  }

  .mall-header__logo-mark {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: linear-gradient(145deg, #e4393c, #ff6b6b);
    color: #fff;
    font-weight: 800;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(228, 57, 60, 0.35);
  }

  .mall-header__brand-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2px;
  }

  .mall-header .mall-header__site-name.logo {
    float: none !important;
    height: auto !important;
    font-size: 18px;
    font-weight: 700;
    color: #1a1a1a !important;
    letter-spacing: 0.02em;
    display: block;
    justify-content: flex-start;
    align-items: flex-start;
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  }

  .mall-header .search-box.mall-header__search {
    flex: 1 1 280px;
    min-width: 200px;
    max-width: 520px;
    height: auto !important;
    float: none !important;
    position: relative !important;
    display: flex !important;
    flex-direction: column;
    align-items: stretch;
    margin: 0 28px;
  }

  .mall-header__search-pill {
    display: flex;
    align-items: center;
    width: 100%;
    border: 1px solid #e0e0e0;
    border-radius: 999px;
    background-color: #ffffff;
    box-shadow: none !important;
    -webkit-box-shadow: none !important;
    padding: 4px 6px 4px 18px;
    gap: 8px;
  }

  .mall-header__input {
    flex: 1;
    height: 38px !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 8px 0 0;
    font-size: 14px;
    background-color: #ffffff !important;
    background-image: none !important;
    color: #333;
    box-shadow: none !important;
    -webkit-box-shadow: none !important;
    -webkit-appearance: none;
    appearance: none;
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  }

  .mall-header__input::placeholder {
    color: #aaa;
  }

  .mall-header .search-btn.mall-header__search-icon {
    width: 36px !important;
    min-width: 36px;
    height: 36px !important;
    border-radius: 50% !important;
    background: #e4393c !important;
    color: #fff !important;
    border: none;
    cursor: pointer;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    margin-right: 8px;
  }

  .mall-header .search-btn.mall-header__search-icon:hover {
    background: #c81623 !important;
    box-shadow: 0 2px 10px rgba(228, 57, 60, 0.45);
  }

  .mall-header__notify-wrap {
    margin-right: 20px !important;
    cursor: pointer;
  }

  .mall-header__notify {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    padding: 4px 8px;
    border-radius: 8px;
    transition: background 0.2s;
  }

  .mall-header__notify:hover {
    background: #f5f5f5;
  }

  .mall-header__bell {
    font-size: 22px !important;
    color: #444 !important;
  }

  .mall-header__notify-label {
    font-size: 12px;
    color: #666;
    font-weight: 500;
  }

  .mall-header .user.mall-header__user {
    margin-left: auto !important;
    margin-right: 12px;
    padding-right: 8px;
    float: none !important;
    height: auto !important;
    min-height: 40px;
    align-self: center;
  }

  .mall-header .mall-header__user--guest {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .mall-header .mall-header__auth-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 72px;
    height: 36px;
    padding: 0 18px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 600;
    line-height: 1;
    text-decoration: none !important;
    box-sizing: border-box;
    transition: background 0.2s, color 0.2s, border-color 0.2s;
  }

  .mall-header .mall-header__auth-btn--login,
  .mall-header .mall-header__auth-btn--register {
    background: #e4393c !important;
    color: #fff !important;
    border: 1px solid #e4393c !important;
  }

  .mall-header .mall-header__auth-btn--login:hover,
  .mall-header .mall-header__auth-btn--register:hover {
    background: #c81623 !important;
    color: #fff !important;
    border-color: #c81623 !important;
  }

  .mall-header .user .ml {
    color: #666 !important;
  }

  .mall-header .user .ml:hover {
    color: #e4393c !important;
  }

  .mall-header .own_text {
    color: #333 !important;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    line-height: 1.3;
    text-align: left;
    padding-left: 10px;
  }

  .mall-header .own_text .own_text__name {
    font-weight: 600;
  }

  .mall-header .own:hover {
    color: #e4393c !important;
  }

  .mall-header .el-icon-bell.mall-header__bell {
    color: #444 !important;
  }

  .mall-header .nav_list.mall-header__nav {
    float: none !important;
    width: 100%;
    border-top: 1px solid #eee;
    padding: 0 0 4px;
    margin-top: 4px;
    background: #ffffff;
  }

  .mall-header .mall-header__nav-ul {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 4px 8px;
  }

  .mall-header .mall-header__nav .nav_li {
    float: none !important;
  }

  .mall-header .mall-header__nav .nav_a {
    color: #666 !important;
    height: 44px !important;
    width: auto !important;
    padding: 0 16px;
    border-radius: 4px 4px 0 0;
    font-size: 15px;
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
  }

  .mall-header .mall-header__nav .nav_li.active .nav_a {
    color: #e4393c !important;
    font-weight: 700;
    box-shadow: inset 0 -4px 0 #e4393c;
  }

  .mall-header .mall-header__nav .nav_a:hover {
    color: #e4393c !important;
    background: rgba(228, 57, 60, 0.06);
  }

  .mall-header .dropdown {
    top: 3.25rem;
  }

</style>
