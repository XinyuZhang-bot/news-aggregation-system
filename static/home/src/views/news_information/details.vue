<template>
	<div class="diy_details page_news_information" id="news_information_details">

		<div class='warp_dt_box'>
		<div class='warp'>
			<div class='container'>
				<div class='news_layout'>
					<div class='news_main_col'>
						<div class='card_news_information'>
							<div_news_information :obj="obj"></div_news_information>

						</div>
					</div>
					<div class='news_side_col'>
						<div class="quick_panel">
							<div class="quick_title">快讯</div>
							<div class="quick_item" v-for="item in quick_news" :key="item.news_information_id" @click="to_news_detail(item.news_information_id)">
								<div class="quick_text">{{ item.news_headlines }}</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		
		<!-- 评论区 -->
		<div class="warp" v-if="$check_action('/comment/list', 'get')">
			<div class="container">
				<div class="row review">
					<!-- 评论区 -->
					<div class="col">
						<bar_title class="mt" title="评论区"	v-if="list_comment.length"/>
						<div class="comment_box"	v-if="list_comment.length">
							<list_comment
									class="w-100"
									:list="list_comment"
									:obj="form_comment" 
									@reset="update_comment()"
									@update-comment="update_comment"
									:self="isSelf"
							/>
							<b-pagination-nav
									:base-url="$route.path"
									:number-of-pages="count_pages"
									:link-gen="link_gen"
									@change="change_page"
									first-number
									last-number
							/>
						</div>

						<!-- 发表评论 -->
						<div class="form_editor form_edit_box">
							<div class="details_form_editor_title">发表评论</div>
							<div class="fl ml-3 answer_title" v-show="form_comment.reply_to_id">
								对 <i>{{ respondent }}</i> 回复:
							</div>
							<div class="fr mr-3" v-show="form_comment.reply_to_id">
								<b-button
										variant="outline-primary reset_answer_personnel"
										size="sm"
										@click="form_comment.reply_to_id = 0"
								>重置回复人
								</b-button
								>
							</div>
							<form_editor
									class="fn"
									:form="form_comment"
									@update_comment="update_comment"
							/>
						</div>
					</div>
				</div>
			</div>
		</div>
</div>
	</div>
</template>

<script>
	import div_news_information from "@/components/diy/div_news_information.vue";
	import list_comment from "@/components/diy/list_comment.vue";
	import bar_title from "@/components/diy/bar_title.vue";
	import form_editor from "@/components/diy/form_editor.vue";
	import mixin from "@/mixins/page.js";
	export default {
		mixins:[mixin],
		components:{
			list_comment,
			bar_title,
			form_editor,
			div_news_information
		},
		data(){
			return{
				url_get_obj: "~/api/news_information/get_obj?",

				field: "news_information_id",

				obj: {
					"praise_len": 0,
				},

				query: {
						"news_headlines": "",
							"publication_date": "",
							"news_pictures": "",
							"news_categories": "",
							"news_description": "",
							"news_body": "",
						"news_information_id":0,
					like: 0,
				},
				// 点赞
				praise: 0,
				// 点赞状态
				state_praise: false,
				// 收藏状态
				state_collect: false,
				list_comment: [],
				form_comment: {
					source_table: "news_information",
					source_field: "news_information_id",
					source_id: 0,
					reply_to_id: 0,
				},
				count_pages: 1, // 页面数
				quick_news: [],
			}
		},
		methods:{
			to_news_detail(news_information_id) {
				this.$router.push({ path: "/news_information/details", query: { news_information_id }});
			},
			get_quick_news() {
				this.$get("~/api/news_information/get_list?", {
					page: 1,
					size: 10,
					orderby: "hits desc"
				}, (json) => {
					if (json.result) {
						const curId = Number(this.$route.query.news_information_id || 0);
						this.quick_news = (json.result.list || []).filter(i => i.news_information_id !== curId);
					}
				});
			},
			/**
			 * 添加访问量
			 */
			add_hits(obj) {
				obj["hits"] = obj["hits"] + 1;
				var hits = obj["hits"];
				this.$post('~/api/news_information/set?news_information_id=' + obj["news_information_id"], {
					hits
				}, (res) => {
					if(res.result){
						console.log("添加访问量状态：" ,res.result);
						var body = {
							source_table: "news_information",
							source_field: "news_information_id",
							source_id: this.obj.news_information_id,
							user_id: this.$store.state.user.user_id,
						};
						this.$post("~/api/hits/add?", body, (res) => {
							console.log(res);
						});
					}
					else if(res.error){
						console.error(res.error);
					}
				});
			},
			async get_obj_after(json) {
				// 判断是否获取到数据
				if (json && json.result && json.result.obj) {
					console.log(json.result.obj)
									if(json.result.obj["publication_date"]=="0000-00-00"){
					  json.result.obj["publication_date"] = null;
					}
					if(parseInt(json.result.obj["publication_date"]) > 9999){
						json.result.obj["publication_date"] = this.$toTime(parseInt(json.result.obj["publication_date"]),"yyyy-MM-dd")
					}
														var obj = json.result.obj;
					this.obj = obj
					// 增加点击数
					this.add_hits(obj);
					// 获取点赞数
					this.get_praise(obj);
					// 初始化收藏状态
					this.get_collect(obj);
					this.get_comment(obj);
					this.form_comment.source_id = this.obj.news_information_id;
										}
			},
									/**
			 * 初始化收藏状态
			 * @param {Object} obj
			 */
			get_collect(obj) {
				var user_id = this.user.user_id;

				var query = {
					source_table: "news_information",
					source_field: "news_information_id",
					source_id: obj["news_information_id"],
					user_id
				};

				this.$get('~/api/collect/count?', query, (res) => {
					console.log(res);
					if (res.result || res.result === 0) {
						var bl = res.result ? true : false;
						this.state_collect = bl;
						console.log("收藏状态：" + bl);
					}
					else if(res.error) {
						console.error(res.error);
					}
				});
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
							var collect = _this.obj.collect-1
							this.$post('~/api/news_information/set?news_information_id=' + _this.obj["news_information_id"], {
								collect
							}, (res) => {
								if(res.result){
									console.log("添加收藏数状态：" ,res.result);
								}
								else if(res.error){
									console.error(res.error);
								}
							});
							this.$toast("取消收藏");
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
							var collect = _this.obj.collect+1
							this.$post('~/api/news_information/set?news_information_id=' + _this.obj["news_information_id"], {
								collect
							}, (res) => {
								if(res.result){
									console.log("添加收藏数状态：" ,res.result);
								}
								else if(res.error){
									console.error(res.error);
								}
							});
							this.$toast("收藏成功");
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
			 * @param {Object} obj
			 */
			get_praise(obj) {
				var user_id = this.user.user_id;

				this.$get("~/api/praise/count?", {
					source_table: "news_information",
					source_field: "news_information_id",
					source_id: obj["news_information_id"]
				}, (res) => {
					if (res.result || res.result === 0) {
						this.praise = res.result;
						console.log("点赞数：" ,res.result);
					}
					else if (res.error){
						this.$toast(res.error.message);
						console.error(res.error);
					}
				});

				this.$get("~/api/praise/count?", {
					source_table: "news_information",
					source_field: "news_information_id",
					source_id: obj["news_information_id"],
					user_id
				}, (res) => {
					if (res.result || res.result === 0) {
						this.state_praise = res.result ? true : false;
						console.log("点赞状态：" ,res.result);
					}
					else if (res.error){
						this.$toast(res.error.message);
						console.error(res.error);
					}
				})
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
        _this.obj.praise_len = parseInt(_this.obj.praise_len)
				// 点赞状态
				if (this.state_praise) {
					this.state_praise = false;
					this.$get('~/api/praise/del?', query, (res) => {
						if(res.result){
							var praise_len = _this.obj.praise_len-1
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
							this.$toast("取消点赞");
						}
						else if (res.error){
							this.$toast(res.error.message);
							console.error(res.error);
						}
					});
				} else {
					this.state_praise = true;
					this.$post('~/api/praise/add?', query, (res) => {
						if (res.result) {
							var praise_len = _this.obj.praise_len+1
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
							this.$toast("点赞成功");
						}
						else if (res.error) {
							this.$toast(res.error.message);
							console.error(res.error);
						}
					});
				};
			},
			/**
			 * 分页器
			 * @param { Number } page_num 分页数
			 * @return { Object } 查询对象
			 */
			link_gen(page_num) {
				return {
					query: this.query,
				};
			},
			/**
			 *加载下一页
			 */
			change_page(page_num) {
				this.get_comment(this.obj, page_num);
				this.form_comment.reply_to_id = 0;
			},
			/**
			 * 更新评论
			 */
			update_comment() {
				this.get_comment(this.obj);
			},
			/**
			 * 获取评论
			 * @param { Object } obj 文章对象
			 * @param { Number } page 分页数
			 * @param { Number } size 评论显示条数
			 */
			get_comment(obj, page = 1, size = 5) {
				this.$get(
						"~/api/comment/get_list?",
						{
							source_table: "news_information",
							source_field: "news_information_id",
							source_id: this.obj["news_information_id"],
							page,
							size,
							reply_to_id: "0",
							orderby: "create_time desc",
						},
						(json) => {
							if (json.result) {
								var list_comment = json.result.list;
								list_comment.map((o) => {
									o.list_reply = [];
								});
								this.add_reply(list_comment).then((list) => {
									this.list_comment = list;
								});
								this.count_pages = Math.ceil(json.result.count / size) || 1
							}
						}
				);
			},
			/**
			 * @param { Array } list 评论列表
			 * 添加回复到评论列表
			 */
			add_reply(list) {
				return new Promise((resolve) => {
					for (let idx = 0; idx < list.length; idx++) {
						const obj = list[idx];
						this.$get(
								"~/api/comment/get_list?",
								{
									source_table: "news_information",
									source_field: "news_information_id",
									source_id: this.obj["news_information_id"],
									orderby: "create_time desc",
									reply_to_id: obj.comment_id,
								},
								(res) => {
									if (res.result) {
										obj.list_reply = res.result.list;
									}
								}
						);
					}
					resolve(list);
				});
			},

		},
		computed: {
			respondent() {
				var reply_to_id = this.form_comment.reply_to_id;
				var respondent = "";
				this.list_comment.map((o) => {
					if (o.comment_id === reply_to_id) {
						respondent = o.nickname;
					}
					if (!respondent && o.list_reply && o.list_reply.length) {
						const matched = o.list_reply.find((r) => r.comment_id === reply_to_id);
						if (matched) {
							respondent = matched.nickname;
						}
					}
				});
				return respondent;
			},
			isSelf() {
				return (this.obj.create_by === this.user.user_id) || this.user.user_group == '管理员';
			}
		},

		mounted() {
			this.get_quick_news();
		},

		watch: {
			"$route.query.news_information_id"() {
				this.get_quick_news();
			}
		}
	}
</script>

<style>
.news_layout {
	display: grid;
	grid-template-columns: minmax(0, 1fr) 320px;
	gap: 20px;
	align-items: start;
}
.news_main_col,
.news_side_col {
	min-width: 0;
}
.quick_panel {
	background: #fff;
	border-radius: 8px;
	padding: 14px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
	position: sticky;
	top: 12px;
	max-height: calc(100vh - 24px);
	overflow-y: auto;
}
.quick_title {
	font-size: 28px;
	font-weight: 700;
	margin-bottom: 10px;
}
.quick_item {
	display: block;
	padding: 10px 0;
	border-bottom: 1px solid #f0f0f0;
	cursor: pointer;
}
.quick_item:last-child {
	border-bottom: 0;
}
.quick_text {
	font-size: 14px;
	color: #222;
	line-height: 1.45;
}
@media (max-width: 1200px) {
	.news_layout {
		grid-template-columns: 1fr;
	}
	.quick_panel {
		position: static;
		max-height: none;
	}
}
.qecode {
  display: flex;
  align-content: center;
  width: 270px;
  background: white;
  position: absolute;
  left: 20%;
  top: 20px;
  z-index: 999;
}
.qecodeImg {
  display: flex;
  flex-direction: column;
  align-content: center;
  text-align: center;
  padding-top: 10px;
  margin: 0 auto;
}
.btn_share{
	display: inline-block;
	position: relative;
	top: 15px;
	background: rgb(240, 238, 238);
	border: 1px solid #ccc;
	height: 38px;
	margin-left: 10px;
	padding: 3px 10px;
	cursor: pointer;
	overflow: hidden;
	border-radius: 5px;
}
.btn_share_icon{
	width: 30px;
	height: 28px;
	float: left;
	margin-right: 10px;
}
.share_box{
	display: none;
	float: left;
}
.share_box img{
	width: 30px;
	height: 28px;
	margin-right: 10px;
}
.btn_share:hover .share_box{
	display: block;
}

.chek-box {
  margin-top: 20px;
  padding: 1.5rem 0;
  box-sizing: border-box;
}
.check-item-list {
  width: 100%;
}
.check-item-list .check-item-li .check-item {
  width: 100%;
  height: 70px;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 10px;
  box-sizing: border-box;
  background-color: #f0f0f0;
  line-height: 100%;
  position: relative;
  margin: 10px 0;
  cursor: pointer;
}
.check-item-list .check-item-li .check-item .image-container {
  display: block;
  width: 50px;
  height: 50px;
}
.check-item-list .check-item-li .check-item .check-item-title {
  width: 60%;
  margin-left: 10px;
}
.check-item-list .check-item-li .check-item .check-item-title > p:nth-child(1) {
  font-weight: bold;
  text-align: left;
  font-size: 16px;
}
.check-item-list .check-item-li .check-item .check-item-title > div {
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-top: 10px;
}
.check-item-list .check-item-li .check-item .check-item-btn {
  margin-left: auto;
}
.check-item-list .check-item-li .check-item-form {
  width: 100%;
  background-color: #fff;
  margin-top: 10px;
  padding: 10px 0;
  box-sizing: border-box;
}
.check-item-list .check-item-li .check-item-form form {
  margin: 0 auto !important;
}
.check-item-list .check-item-li .check-item-form form .el-form-item {
  margin-bottom: 15px;
}
.check-item-list .check-item-li .check-item-complete {
  border: 1px solid #007bff;
  overflow: hidden;
  position: relative;
}
.check-item-list .check-item-li .check-item-complete:before {
  content: "";
  position: absolute;
  right: 0;
  top: 0;
  border: 15px solid #007bff;
  border-bottom-color: transparent;
  border-left-color: transparent;
}
.check-item-list .check-item-li .check-item-complete:after {
  content: "";
  width: 8px;
  height: 4px;
  position: absolute;
  right: 3px;
  top: 3px;
  border: 2px solid #fff;
  border-bottom-color: transparent;
  border-left-color: transparent;
  transform: rotate(135deg);
}
.check-progress {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.check-progress > p {
  margin-right: 10px;
}
.check-box {
  display: flex;
  flex-direction: column;
  padding: 15px;
  box-sizing: border-box;
}
.check-box .check-box-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
}
.check-box-desc img{
	width: 100%;
}
</style>
