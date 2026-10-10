<template>
	<div class="diy_details_box diy_div_news_information">
		<div class="warp diy_warp news_read_warp">
			<div class="container">
				<div class="news_read_layout">
					<div class="news_read_main">
						<h1 class="news_headline">{{ obj.news_headlines || "新闻详情" }}</h1>
						<div class="news_meta">
							<span v-if="obj.news_categories" class="meta_tag">{{ obj.news_categories }}</span>
							<span v-if="obj.publication_date" class="meta_item">{{ $toTime(obj.publication_date, "yyyy-MM-dd") }}</span>
							<span class="meta_item">阅读 {{ hitsLen || 0 }}</span>
							<span class="meta_item">点赞 {{ praiseLen || 0 }}</span>
						</div>

						<div @click="goPage" class="user_box">
							<div class="user_avatar user_avatar--text" aria-hidden="true">{{ avatarLetter }}</div>
							<div class="user_info">
								<span class="user_nickname">{{ followUserInfo.nickname || "发布者" }}</span>
								<span class="user_fans">共{{followList.length}}个粉丝关注</span>
							</div>
							<el-button v-if="this.$store.state.user.user_id && followUserInfo.user_id != $store.state.user.user_id" @click.stop="attention(followUserInfo)" type="primary" size="small" plain round>{{followState?'已关注':'+ 关注'}}</el-button>
						</div>

						<div class="news_desc" v-if="obj.news_description">
							{{ obj.news_description }}
						</div>

						<div class="news_body diy_html" v-html="sanitizedNewsBody"></div>

						<div class="read_source_wrap" v-if="sourceUrl">
							<el-button type="primary" size="small" @click="openSourceUrl">阅读原文</el-button>
						</div>

						<div class="btns_add" v-if="this.$store.state.user.user_id && $check_action('/news_information/details','set')">
							<div v-if="state_praise" class="praise_btn" @click="change_praise()">
								<b-icon icon="hand-thumbs-up-fill" class="icon icon_change"></b-icon><span class="word_change">已点赞</span>
							</div>
							<div v-else class="praise_btn" @click="change_praise()">
								<b-icon icon="hand-thumbs-up" class="icon"></b-icon><span>点赞</span>
							</div>
							<div v-if="state_collect" class="collect_btn" @click="change_collect()">
								<b-icon icon="heart-fill" class="icon icon_change"></b-icon><span class="word_change">已收藏</span>
							</div>
							<div v-else class="collect_btn" @click="change_collect()">
								<b-icon icon="heart" class="icon"></b-icon><span>收藏</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import mixin from "@/mixins/component.js";
	import mixinPage from "@/mixins/page.js";
	
	export default {
		mixins: [mixin,mixinPage],
		components: {

		},
		props: {
			obj: {
				type: Object,
				default: function() {
					return {};
				},
			}
		},
		data() {
			return {
				praiseLen: this.obj["praise_len"],
				hitsLen: this.obj["hits"],
				imgList: [
						{
							title: "新闻图片",
							name: "news_pictures",
							type: "图片"
						},
				],
				itemList: [
							{
							title: "新闻标题",
							name: "news_headlines",
							type: "文本",
																		},
								{
							title: "发布日期",
							name: "publication_date",
							type: "日期",
																		},
								{
							title: "新闻分类",
							name: "news_categories",
							type: "下寻",
																		},
					],
				richList: [
						{
							title: "新闻描述",
							name: "news_description",
							type: "多文本"
						},
						{
							title: "新闻正文",
							name: "news_body",
							type: "编辑"
						},
							],
				sourceUrl: "",
				renderedNewsBody: "",
										state_praise:false,
				state_collect:false,
				followUserInfo: {},
				followList: [],
				followState: false,
				oneself: null,
			};
		},
		computed: {
			avatarLetter() {
				const n = (this.followUserInfo && this.followUserInfo.nickname) ? String(this.followUserInfo.nickname).trim() : "";
				if (!n) {
					return "发";
				}
				return n.charAt(0).toUpperCase();
			},
			sanitizedNewsBody() {
				const raw = this.renderedNewsBody || (this.obj && this.obj.news_body) || "";
				return this.stripNewsMediaMarkup(raw);
			},
		},
		methods: {
			/** 与后端 strip_news_media_markup 一致：正文仅保留文字与常规标签 */
			stripNewsMediaMarkup(html) {
				if (!html) {
					return "";
				}
				let s = String(html);
				const blocks = [
					/<picture\b[^>]*>[\s\S]*?<\/picture>/gi,
					/<figure\b[^>]*>[\s\S]*?<\/figure>/gi,
					/<video\b[^>]*>[\s\S]*?<\/video>/gi,
					/<audio\b[^>]*>[\s\S]*?<\/audio>/gi,
					/<iframe\b[^>]*>[\s\S]*?<\/iframe>/gi,
					/<object\b[^>]*>[\s\S]*?<\/object>/gi,
					/<svg\b[^>]*>[\s\S]*?<\/svg>/gi,
				];
				blocks.forEach((re) => {
					s = s.replace(re, "");
				});
				s = s.replace(/<iframe\b[^>]*\/>/gi, "");
				s = s.replace(/<embed\b[^>]*\/?>/gi, "");
				s = s.replace(/<img\b[^>]*(?:\/>|>)/gi, "");
				s = s.replace(/<image\b[^>]*(?:\/>|>)/gi, "");
				s = s.replace(/<source\b[^>]*(?:\/>|>)/gi, "");
				s = s.replace(/!\[[^\]]*\]\([^)]+\)/g, "");
				s = s.replace(/<p>\s*(?:<br\s*\/?>|\s)*<\/p>/gi, "");
				return s.trim();
			},
			openSourceUrl() {
				const u = this.sanitizeUrl(this.sourceUrl);
				if (!u) return;
				window.open(u, "_blank");
			},
			sanitizeUrl(url) {
				if (!url) return "";
				let u = String(url).trim();
				// decode common html entities
				u = u.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
				// strip trailing comment bits if any
				u = u.replace(/-->.*/g, "").trim();
				// keep only the first http(s) url
				const m = u.match(/https?:\/\/[^\s"'<>]+/i);
				if (m) u = m[0];
				if (!/^https?:\/\//i.test(u)) return "";
				return u;
			},
			extractSourceUrlFromBody() {
				// 从 news_body 中解析原文链接（隐藏 <a> 优先，其次兼容旧的 HTML 注释标记）
				const body = (this.obj && this.obj.news_body) ? String(this.obj.news_body) : "";
				// 优先解析稳定标记：[SOURCE_URL]...[/SOURCE_URL]
				const mTag = body.match(/\[SOURCE_URL\]([\s\S]*?)\[\/SOURCE_URL\]/i);
				if (mTag && mTag[1]) {
					this.sourceUrl = this.sanitizeUrl(mTag[1]);
				} else {
					// 兼容旧标记：<!--source_url:...-->
					const m = body.match(/<!--\s*source_url\s*:\s*(https?:\/\/[^>\s]+)\s*-->/i);
					if (m && m[1]) {
						this.sourceUrl = this.sanitizeUrl(m[1]);
					} else {
						// 兜底：取正文里第一个 http(s) 链接
						const m2 = body.match(/https?:\/\/[^\s"'<>]+/i);
						if (m2) {
							this.sourceUrl = this.sanitizeUrl(m2[0]);
						}
					}
				}

				// 渲染正文时剔除标记本身，避免显示出来
				this.renderedNewsBody = body
					.replace(/\[SOURCE_URL\][\s\S]*?\[\/SOURCE_URL\]/gi, "")
					.replace(/<!--\s*source_url\s*:[\s\S]*?-->/gi, "")
					.trim();
			},
			previewFile(fileName) {
				const fileExtension = fileName.split('.').pop().toLowerCase();
				if(fileExtension == 'docx' || fileExtension == 'xlsx' || fileExtension == 'pptx') {
					this.$router.push('/filePreview?url=' + fileName + '&type=' + fileExtension);
					return;
				}
				window.open(this.$fullUrl(fileName), '_blank');
			},
			async getUserInfo() {
			  let res = await this.$get("~/api/user/get_obj",{user_id: this.obj.create_by});
			  this.followUserInfo = res.result.obj;
			  this.getFollowList(this.followUserInfo);
			},
			async getFollowList(followUserInfo) {
			  let res = await this.$get("~/api/follow/get_list", {
				followed_id: followUserInfo.user_id
			  });
			  this.followList = res.result.list;
			  this.oneself = this.followList.find(item => item.follower_id === this.$store.state.user.user_id);
			  
			  if(this.oneself) {
				this.followState = true;
			  }else {
				this.followState = false;
			  }
			},
			async attention(obj) {
			  let parnm = {
				follower_id: this.$store.state.user.user_id,
				follower_avatar: this.$store.state.user.avatar,
				follower_nickname: this.$store.state.user.nickname,
				followed_id: obj.user_id,
				followed_avatar: obj.avatar,
				followed_nickname: obj.nickname,
			  }
			  if(this.followState) {
				this.$confirm("不再关注该用户？", "提示", {
				  confirmButtonText: "确定",
				  cancelButtonText: "取消",
				  type: "warning",
				})
				.then(async () => {
				  let res = await this.$get("~/api/follow/del", {
					follow_id: this.oneself.follow_id
				  });
				  if(res.result) {
					this.getUserInfo();
					this.$message({
					  type: "success",
					  message: "取消关注",
					});
				  }
				})
			  }else {
				let res = await this.$post("~/api/follow/add", parnm);
				if(res.result) {
				  this.getUserInfo();
				  this.$message({
					type: "success",
					message: "关注成功",
				  });
				}
			  }
			},
			goPage() {
			  this.$router.push("/user/my_home_page?follower_id="+this.followUserInfo.user_id);
			},
									get_user_info(name,id){
				var obj = null;
										var ret = "";
				if(obj){
					ret = obj.nickname+"-"+obj.username;
					// if(obj.nickname){
					// 	ret = obj.nickname;
					// }
					// else{
					// 	ret = obj.username;
					// }
				}
				return ret;
			},
				/**
			 * 改变点赞数
			 */
			change_praise(obj) {
				var user_id = this.user.user_id;

				var query = {
					source_table: "news_information",
					source_field: "news_information_id",
					source_id: this.obj["news_information_id"],
					user_id
				};

				var _this = this;

				// 点赞状态
				if (this.state_praise) {
					this.state_praise = false;
					this.$get('~/api/praise/del?', query, (res) => {
						if(res.result){
              _this.praiseLen = parseInt(_this.praiseLen)-1;
              var praise_len = _this.praiseLen;
							this.$post('~/api/news_information/set?news_information_id=' + _this.obj["news_information_id"], {
								praise_len
							}, (res) => {
								if(res.result){
									console.log("添加点赞数状态：" ,res.result);
								}
								else if(res.error){
									console.error(res.error);
								}
							});
							// this.$toast("取消点赞");
							this.$message.success("取消点赞")
						}
						else if (res.error){
							this.$toast(res.error.message);
							console.error(res.error);
						}
					});
				} else {
					this.state_praise = true;
								query.title = this.obj.news_headlines
																			query.img = this.obj.news_pictures
																							this.$post('~/api/praise/add?', query, (res) => {
						if (res.result) {
              _this.praiseLen = parseInt(_this.praiseLen)+1;
              var praise_len = _this.praiseLen;
							this.$post('~/api/news_information/set?news_information_id=' + _this.obj["news_information_id"], {
								praise_len
							}, (res) => {
								if(res.result){
									console.log("添加点赞数状态：" ,res.result);
								}
								else if(res.error){
									console.error(res.error);
								}
							});
													// this.$toast("点赞成功");
							this.$message.success("点赞成功")
						}
						else if (res.error) {
							this.$toast(res.error.message);
							console.error(res.error);
						}
					});
				};
			},
      /**
       * 获取点赞
       */
      get_praise() {
        var user_id = this.$store.state.user.user_id;
        this.$get("~/api/praise/count?", {
          source_table: "news_information",
          source_field: "news_information_id",
          source_id: this.obj.news_information_id,
          user_id
        }, (res) => {
          if (res.result || res.result === 0) {
            console.log("sadsfasf"+JSON.stringify(res))
            this.state_praise = res.result ? true : false;
            console.log("点赞状态：" ,this.state_praise);
          }
          else if (res.error){
            this.$toast(res.error.message);
            console.error(res.error);
          }
        })
      },

				/**
			 * 改变收藏状态
			 */
			change_collect() {
				var user_id = this.user.user_id;

				var query = {
					source_table: "news_information",
					source_field: "news_information_id",
					source_id: this.obj["news_information_id"],
					user_id
				};

				// 收藏状态
				if (this.state_collect) {
					this.state_collect = false;
					this.$get('~/api/collect/del?', query, (res) => {
						if(res.result){
							// this.$toast("取消收藏");
							this.$message.success("取消收藏")
						}
						else if (res.error){
							this.$toast(res.error.message);
							console.error(res.error);
						}
					});
				} else {
					this.state_collect = true;
								query.title = this.obj.news_headlines
																			query.img = this.obj.news_pictures
																							this.$post('~/api/collect/add?', query, (res) => {
						if (res.result) {
													// this.$toast("收藏成功");
							this.$message.success("收藏成功")
						}
						else if (res.error) {
							this.$toast(res.error.message);
							console.error(res.error);
						}
					});
				};
			},
      check_collect() {
        var user_id = this.$store.state.user.user_id;
        var news_information_id = this.obj.news_information_id;
        this.$get('~/api/collect/count?', {
          user_id,
          source_table: "news_information",
          source_field: "news_information_id",
          source_id: news_information_id
        }, (res) => {
          this.state_collect = res.result
        });
      },
	get_obj_after(json, func) {
		},
	  },
		created() {
						      setTimeout(() => {
        this.get_praise();
        this.check_collect();
      }, 1000);
			this.extractSourceUrlFromBody();
		},
		watch:{
			obj:{
				deep: true,
				handler(newVal){
					this.praiseLen = this.obj["praise_len"]
					this.hitsLen = this.obj["hits"]
																									this.getUserInfo();
					this.extractSourceUrlFromBody();
									}
			},
		},
	};
</script>

<style>
.news_read_warp {
	padding: 24px 0;
}
.news_read_layout {
	display: flex;
	justify-content: center;
}
.news_read_main {
	width: 100%;
	max-width: 860px;
	background: #fff;
	padding: 24px 28px;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}
.news_headline {
	font-size: 32px;
	line-height: 1.35;
	font-weight: 700;
	color: #202020;
	margin-bottom: 16px;
}
.news_meta {
	display: flex;
	flex-wrap: wrap;
	gap: 8px 14px;
	align-items: center;
	margin-bottom: 14px;
	color: #777;
	font-size: 13px;
}
.meta_tag {
	background: #eef5ff;
	color: #1d5cff;
	border-radius: 4px;
	padding: 2px 8px;
	font-size: 12px;
}
.news_desc {
	background: #f5f7fb;
	border-left: 4px solid #1d5cff;
	padding: 12px;
	margin: 14px 0 22px;
	color: #444;
	line-height: 1.8;
}
.news_body {
	color: #222;
	font-size: 17px;
	line-height: 1.9;
}
.btns_add {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-wrap: wrap;
	margin: 20px 0 8px;
	font-size: 0.875rem;
}
.collect_btn,
.praise_btn {
	margin-right: 10px;
	display: flex;
	align-items: center;
	white-space: nowrap;
	padding: 6px 14px;
	border-radius: 20px;
	color: #1d5cff;
	border: 1px solid #a9c3ff;
	cursor: pointer;
	background: #f4f8ff;
}
.icon { font-size: 15px; margin-right: 5px; }
.word_change, .icon_change { color: #1d5cff; font-weight: 600; }
.user_box {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  cursor: pointer;
}
.user_avatar {
  width: 40px !important;
  height: 40px !important;
  border-radius: 100%;
  margin-right: 10px;
}
.user_avatar--text {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e8eaed;
  color: #555;
  font-size: 16px;
  font-weight: 700;
}

.user_info {
  display: flex;
  flex-direction: column;
  margin-right: 20px;
}

.user_nickname {
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
}
.user_fans {
  font-size: 12px;
  color: #999;
}

.read_source_wrap{
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
