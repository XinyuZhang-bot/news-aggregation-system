<template>
	<div class="my_home_page" id="my_home_page">
    <div class="my_home">
      <div class="user_info home_user_info">
        <div class="user_info_left">
          <img class="user_avatar" :src="userInfo.avatar?$fullUrl(userInfo.avatar):'http://192.168.1.4:5000/upload/default_avatar.jpg'" />
          <div class="user_name">
            <div class="user_name_item name">{{userInfo.nickname}}</div>
            <div class="user_name_item">账号: {{userInfo.username}}</div>
            <div class="">邮箱: {{userInfo.email}}</div>
          </div>
        </div>
        <div class="user_info_center">
          <div class="user_num_item">
            <div class="user_num">{{myFollow.length}}</div>
            <div class="user_num_name">关注</div>
          </div>
          <div class="user_num_item">
            <div class="user_num">{{followSelf.length}}</div>
            <div class="user_num_name">粉丝</div>
          </div>
        </div>
        <div v-if="now_follower_id != $store.state.user.user_id" class="user_info_right">
          <el-button type="primary" @click="myAttention(userInfo)">{{followState?'已关注':'+ 关注'}}</el-button>
                  <el-button type="primary" plain @click="sendMessage(userInfo)">发私信</el-button>
                </div>
      </div>

      <div class="user_content">
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="动态" name="动态">
            <template v-for="(item) in dynamicList">
								  <div v-if="item.type === 'news_informationProducts'" @click="goPage(item)" class="dynamic">
								    <div class="dynamic_content_title">
			      <div class="title_content">{{item.news_headlines}}</div>
			      <div class="title_time">{{$toTime(item.create_time,"yyyy-MM-dd hh:mm:ss")}}</div>
			    </div>
						    <div class="dynamic_content">
																		      <img v-if="item.news_pictures" class="dynamic_img" :src="$fullUrl(item.news_pictures)" alt="">
						      <div class="dynamic_info">
			        <!--<div class="dynamic_text">{{ item.classification_name }}</div>-->
			        <div class="dynamic_sum">
			          <div class="dynamic_btn">
					            <el-button @click.stop="add_praise(item)" type="primary" size="small" plain v-if="$check_action('/news_information/details','set') && !item.praised">
			              <i class="el-icon-thumb" style="font-size: 14px"></i>
			              <span>点赞</span>
			            </el-button>
                  <el-button @click.stop="add_praise(item)" type="primary" size="small" plain v-if="$check_action('/news_information/details','set') && item.praised">
			              <i class="el-icon-thumb" style="font-size: 14px"></i>
			              <span>已点赞</span>
			            </el-button>
							            <el-button @click.stop="add_collect(item)" type="primary" size="small" v-if="$check_action('/news_information/details','set') && !item.collected">
			              <i class="el-icon-star-off" style="font-size: 14px"></i>
			              <span>收藏</span>
			            </el-button>
                  <el-button @click.stop="add_collect(item)" type="primary" size="small" v-if="$check_action('/news_information/details','set') && item.collected">
			              <i class="el-icon-star-on" style="font-size: 14px"></i>
			              <span>已收藏</span> 
			            </el-button>
					          </div>
			          <div class="dynamic_statistics">
			            <div class="dynamic_statistics_item">点击数: {{item.hits}}</div>
			            <div class="">点赞数: {{item.praise_len}}</div>
			          </div>
			        </div>
			      </div>
			    </div>
			  </div>
	            </template>
          </el-tab-pane>
          <el-tab-pane label="关注" name="关注">
            <div v-for="item in myFollow" :key="item.follow_id" class="attention">
              <div class="attention_user">
                <img class="attention_img" :src="item.followed_avatar?$fullUrl(item.followed_avatar):'http://192.168.1.4:5000/upload/default_avatar.jpg'" alt="" />
                <div>{{item.followed_nickname}}</div>
              </div>
              <div>
                <el-button v-if="now_follower_id == $store.state.user.user_id" type="primary" size="small" round plain @click="cancelAttention(item)">已关注</el-button>
                <el-button type="primary" size="small" round plain @click="goPage(item)">查看主页</el-button>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="粉丝" name="粉丝">
            <div v-for="item in followSelf" :key="item.follow_id" class="attention">
              <div class="attention_user">
                <img class="attention_img" :src="item.follower_avatar?$fullUrl(item.follower_avatar):'http://192.168.1.4:5000/upload/default_avatar.jpg'" alt="" />
                <div>{{item.follower_nickname}}</div>
              </div>
              <div>
                <el-button v-if="now_follower_id == $store.state.user.user_id" type="primary" size="small" round plain @click="attention(item)">{{item.isFollow?'互相关注':'+ 关注'}}</el-button>
                <el-button type="primary" size="small" round plain @click="goPage(item)">查看主页</el-button>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
	</div>
</template>
<script>
// import mixin from "@/mixins/component.js";
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
	data() {
		return {
			activeName: '动态',
			userInfo: {},
			dynamicList: [],
			followList: [],
			followSelf: [],
			myFollow: [],
			oneSelf: null,
			followState: false,
			now_follower_id: 0,
      query: {
        orderby: `create_time desc`,
      }
		}
	},
  watch: {
    '$route.query': {
      handler(newQuery) {
        if(newQuery.follower_id) {
          this.now_follower_id = newQuery.follower_id;
          
          this.getUserInfo(this.now_follower_id);
          this.getDynamicList(this.now_follower_id);
        }
      },
      immediate: true,
      deep: true
    }
  },
	mounted() {
		// this.now_follower_id = this.$route.query.follower_id || UserInfo.user_id;
		// this.getUserInfo(this.now_follower_id);
	},
	methods: {
    sendMessage() {
      if(!this.user_group) {
        this.$message.warning("用户未登录!");
        return
      }
      if(!this.followState) {
        this.$message.warning("请先关注对方后再发送私信");
        return
      }
      this.$router.push('/user/chat?user_id=' + this.now_follower_id);
    },
		handleClick(tab, event) {
			console.log(tab, event);
		},
		async getUserInfo(userId) {
			let res = await this.$get("~/api/user/get_obj",{user_id: userId})
			this.userInfo = res.result.obj;
			this.getFollowList();
		},
		async getFollowList() {
			let res = await this.$get('~/api/follow/get_list',this.query)
			this.followList = res.result.list;
			this.myFollow = res.result.list.filter(item => item.follower_id == this.now_follower_id);
			this.oneSelf = res.result.list.filter(item => item.follower_id == this.$store.state.user.user_id && item.followed_id == this.now_follower_id)[0];
			this.followSelf = res.result.list.filter(item => item.followed_id == this.now_follower_id).map(item => {
				// 根据myFollow遍历是否互相关注
				let isFollow = this.myFollow.some(item2 => item2.follower_id === item.followed_id && item2.followed_id === item.follower_id);
				return {
				...item,
				  isFollow: isFollow
				}
			});

			if(this.oneSelf) {
				this.followState = true;
			}else{
				this.followState = false;
			}
			console.log(this.myFollow,'我的关注');
			console.log(this.followSelf,'我的粉丝');
		},
    async getDynamicList(userId) {
						  let params5 = Object.assign({}, this.query, { create_by: userId });
	  let news_informationProducts = await this.$get('~/api/news_information/get_list', params5);
	  let news_informationProductsList = await Promise.all(news_informationProducts.result.list.map(async (item) => {
        const new_news_informationItem = {
          ...item,
          type: 'news_informationProducts',
        };
        await this.checkCollect(new_news_informationItem);
        await this.checkPraise(new_news_informationItem);
        return new_news_informationItem;
    }));
	      this.dynamicList = [
							   ...news_informationProductsList,
			];
    },
    async attention(obj) {
      let param = {
        follower_id: this.$store.state.user.user_id,
        follower_avatar: this.$store.state.user.avatar,
        follower_nickname: this.$store.state.user.nickname,
        followed_id: obj.follower_id || obj.user_id,
        followed_avatar: obj.follower_avatar || obj.avatar,
        followed_nickname: obj.follower_nickname || obj.nickname,
      }
      if(obj.isFollow || this.followState) {
      	this.$confirm("不再关注该用户？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(async () => {
          let oneself = this.myFollow.find(item => item.followed_id === obj.follower_id && item.follower_id === obj.followed_id);
          let res = await this.$get(`~/api/follow/del?follow_id=${oneself.follow_id}`);
          if(res.result) {
            this.getUserInfo(this.now_follower_id);
            this.getDynamicList(this.now_follower_id);
            this.$message.success("取消关注");
          }
        }).catch(() => {})
      }else {
        let res = await this.$post('~/api/follow/add', param);
        if(res.result) {
          this.getUserInfo(this.now_follower_id);
          this.getDynamicList(this.now_follower_id);
          this.$message.success("关注成功");
        }
      }
    },
    cancelAttention(obj) {
    	this.$confirm("不再关注该用户？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(async () => {
      	let res = await this.$get(`~/api/follow/del?follow_id=${obj.follow_id}`);
        if(res.result) {
          this.getUserInfo(this.now_follower_id);
          this.getDynamicList(this.now_follower_id);
          this.$message.success("取消关注");
        }
      })
    },
    async myAttention(obj) {
      if(!this.user_group) {
        this.$message.warning("用户未登录!");
        return
      }
    	let param = {
        follower_id: this.$store.state.user.user_id,
        follower_avatar: this.$store.state.user.avatar,
        follower_nickname: this.$store.state.user.nickname,
        followed_id: obj.follower_id || obj.user_id,
        followed_avatar: obj.follower_avatar || obj.avatar,
        followed_nickname: obj.follower_nickname || obj.nickname,
    	}
      if(this.followState) {
      	this.$confirm("不再关注该用户？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).then(async () => {
        	let res = await this.$get(`~/api/follow/del?follow_id=${this.oneSelf.follow_id}`);
          if(res.result) {
            this.getUserInfo(this.now_follower_id);
            this.getDynamicList(this.now_follower_id);
            this.$message.success("取消关注");
          }
        })
      }else {
        let res = await this.$post('~/api/follow/add', param);
        if(res.result) {
          this.getUserInfo(this.now_follower_id);
          this.getDynamicList(this.now_follower_id);
          this.$message.success("关注成功");
        }
      }
    },
    goPage(obj) {
      if(this.activeName === '关注') {
        this.$router.push('/user/my_home_page?follower_id=' + obj.followed_id);
      }else if(this.activeName === '粉丝') {
        this.$router.push('/user/my_home_page?follower_id=' + obj.follower_id);
      }else if(this.activeName === '动态') {
							if(obj.type === 'news_informationProducts') {
          this.$router.push('/news_information/details?news_information_id=' + obj.news_information_id);
        }
	      }
    },
    async checkPraise(obj) {
					      if (obj.type === 'news_informationProducts') {
        let res = await this.$get('~/api/praise/count', {
            source_table: 'news_information',
            source_field: 'news_information_id',
            source_id: obj.news_information_id,
            user_id: this.$store.state.user.user_id,
          });
          this.$set(obj, 'praised', res.result !== 0);
      }
      },
    async add_praise(obj) {
						  if(obj.type === 'news_informationProducts') {
      	let res = await this.$get("~/api/praise/count",{
          source_table: "news_information",
          source_field: "news_information_id",
          source_id: obj.news_information_id,
          user_id: this.$store.state.user.user_id,
        })
        if (res.result || res.result === 0) {
          console.log("sadsfasf", res.result);
          let check_praised = res.result? true : false;
          let param = {
            source_table: "news_information",
            source_field: "news_information_id",
            source_id: obj.news_information_id,
            user_id: this.$store.state.user.user_id,
          }
          if (!check_praised) {
            let praiseRes = await this.$post("~/api/praise/add", param);
            if (praiseRes.result) {
              let praise_len = obj.praise_len += 1;
              let news_informationRes = await this.$post("~/api/news_information/set?news_information_id=" + obj.news_information_id, {
                praise_len,
              })
              if (news_informationRes.result) {
                console.log("添加点赞数状态：", news_informationRes.result);
              } else if (news_informationRes.error) {
                console.error(news_informationRes.error);
              }
              this.getDynamicList(this.now_follower_id)
              this.$message.success("点赞成功");
            }else if (praiseRes.error) {
              this.$message.error(praiseRes.error.message);
              console.error(praiseRes.error);
            }
          }else {
            let res = await this.$get("~/api/praise/del?",param);
            if (res.result) {
              if(obj.praise_len > 0) {
              	obj.praise_len -= 1;
              }else{
              	obj.praise_len = 0;
              }
              let praise_len = obj.praise_len;
              let news_informationRes = await this.$post("~/api/news_information/set?news_information_id=" + obj.news_information_id, {
                praise_len,
              })
              if (news_informationRes.result) {
                console.log("取消点赞数状态：", news_informationRes.result);
              } else if (news_informationRes.error) {
                console.error(news_informationRes.error);
              }
              this.getDynamicList(this.now_follower_id)
              this.$message.success("取消点赞");
            }else if (res.error) {
              this.$message.error(res.error.message);
              console.error(res.error);
            }
          }
        }else if (res.error) {
          this.$message.error(res.error.message);
          console.error(res.error);
        }
      }
	    },
    async checkCollect(obj) {
					      if (obj.type === 'news_informationProducts') {
        let res = await this.$get('~/api/collect/count', {
            source_table: 'news_information',
            source_field: 'news_information_id',
            source_id: obj.news_information_id,
            user_id: this.$store.state.user.user_id,
          });
          this.$set(obj, 'collected', res.result !== 0);
      }
      },
    async add_collect(obj) {
						  if(obj.type === 'news_informationProducts') {
      	let res = await this.$get("~/api/collect/count",{
          source_table: "news_information",
          source_field: "news_information_id",
          source_id: obj.news_information_id,
          user_id: this.$store.state.user.user_id,
        })
        let check_collected = res.result;
        let { title, img, news_information_id } = obj;
        let body = {
	  		          title: obj.news_headlines,
					  					  				          img: obj.news_pictures,
			  					  					  					            source_table: "news_information",
          source_field: "news_information_id",
          source_id: news_information_id,
          user_id: this.$store.state.user.user_id,
        }
        if (!check_collected) {
          await this.$post("~/api/collect/add", body);
          this.$set(obj, 'collected', true);
          this.$message.success("收藏成功");
        }else {
          await this.$get("~/api/collect/del", {
            user_id: this.$store.state.user.user_id,
            source_id: news_information_id,
          });
          this.$set(obj, 'collected', false);
          this.$message.success("取消收藏");
        }
      }
	    }
	}
}
</script>

<style lang="less" scoped>
.my_home_page {
  margin-left: 5%;
  .my_home {
    width: 60%;
    margin: 100px auto 20px;
    .home_user_info {
      display: flex;
      align-items: end;
      justify-content: space-between;
      margin-bottom: 30px;
      flex-direction: row;
      .user_info_left {
       display: flex;
       align-items: end;
       .user_avatar {
          width: 80px !important;
          height: 80px !important;
          border-radius: 4px;
          margin-right: 20px
        }
        .user_name {
         font-size: 14px;
         color: #bababa;
         .user_name_item {
          margin-bottom: 8px;
         }
         .name {
          font-size: 18px;
          font-weight: 600;
          color: #303133;
         }
        }
      }
      .user_info_center {
       width: 20%;
       display: flex;
       align-items: center;
       justify-content: space-around;
       .user_num_item {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        .user_num {
          font-size: 18px;
          font-weight: 600;
          color: #303133;
          margin-bottom: 12px;
        }
       .user_num_name {
          font-size: 14px;
        }
       }
      }
    }
    .user_content {
      min-height: 600px;
      .dynamic {
        margin-bottom: 40px;
        .dynamic_content_title {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin: 14px 0;
          .title_content {
            font-size: 16px;
            font-weight: 600;
            color: #303133;
          }
        .title_time {
            font-size: 14px;
            color: #bababa;
          }
        }
        .dynamic_content {
          display: flex;
          align-items: start;
          justify-content: start;
          .dynamic_img {
            width: 200px;
            height: 140px;
            border-radius: 4px;
            margin-right: 20px;
          }
          .dynamic_info {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 140px;
            .dynamic_text {
              line-height: 24px;
            }
            .dynamic_sum {
              display: flex;
              align-items: center;
              justify-content: space-between;
              // .dynamic_btn {}
              .dynamic_statistics {
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-size: 14px;
                color: #bababa;
                .dynamic_statistics_item {
                margin-right: 20px;
                }
              }
            }
          }
        }
      }
      .attention {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
       .attention_user {
          display: flex;
          align-items: center;
          justify-content: start;
         .attention_img {
            width: 60px;
            height: 60px;
            border-radius: 100%;
            margin-right: 20px;
          }
       }
      }
    }
    .my_home_pagination {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
