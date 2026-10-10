<template>
	<el-main class="bg edit_wrap">
		<el-form ref="form" :model="form" :rules="rules" status-icon label-width="120px" v-if="is_view()">
		<el-row class="row_ce">
												<el-col v-if="$check_field('get','news_headlines') || $check_field('add','news_headlines') || $check_field('set','news_headlines')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="新闻标题" prop="news_headlines">
												<el-input id="news_headlines" v-model="form['news_headlines']" placeholder="请输入新闻标题"
							v-if="(form['news_information_id'] && $check_field('set','news_headlines')) || (!form['news_information_id'] && $check_field('add','news_headlines'))" :disabled="disabledObj['news_headlines_isDisabled']">
									</el-input>
					<div v-else-if="$check_field('get','news_headlines')">
						{{form['news_headlines']}}
									</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','publication_date') || $check_field('add','publication_date') || $check_field('set','publication_date')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="发布日期" prop="publication_date">
								<el-date-picker :disabled="disabledObj['publication_date_isDisabled']" v-if="(form['news_information_id'] && $check_field('set','publication_date')) || (!form['news_information_id'] && $check_field('add','publication_date'))" id="publication_date"
						v-model="form['publication_date']" type="date" placeholder="选择日期" value-format="yyyy-MM-dd">
					</el-date-picker>
					<div v-else-if="$check_field('get','publication_date')">{{form['publication_date']}}</div>
										</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','news_pictures') || $check_field('add','news_pictures') || $check_field('set','news_pictures')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="新闻图片" prop="news_pictures">
								<el-upload :disabled="disabledObj['news_pictures_isDisabled']" class="avatar-uploader" drag
						accept="image/gif, image/jpeg, image/png, image/jpg" action="" :http-request="upload_news_pictures"
						:show-file-list="false" v-if="(form['news_information_id'] && $check_field('set','news_pictures')) || (!form['news_information_id'] && $check_field('add','news_pictures'))">
						<img id="news_pictures" v-if="form['news_pictures']" :src="$fullUrl(form['news_pictures'])" class="avatar">
						<i v-else class="el-icon-plus avatar-uploader-icon"></i>
					</el-upload>
					<el-image v-else-if="$check_field('get','news_pictures')" style="width: 100px; height: 100px"
						:src="$fullUrl(form['news_pictures'])" :preview-src-list="[$fullUrl(form['news_pictures'])]">
						<div slot="error" class="image-slot">
							<img src="../../../public/img/error.png" style="width: 90px; height: 90px" />
						</div>
					</el-image>
										</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','news_categories') || $check_field('add','news_categories') || $check_field('set','news_categories')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="新闻分类" prop="news_categories">
								<el-cascader id="news_categories" v-model="form['news_categories']" :options="news_categories_tree" :props="news_categories_cascader" :show-all-levels="false" clearable 
      					placeholder="请选择新闻分类" 
      					v-if="(form['news_information_id'] && $check_field('set', 'news_categories')) || (!form['news_information_id'] && $check_field('add', 'news_categories'))">
   		 			</el-cascader>
					<div v-else-if="$check_field('get','news_categories')">{{form['news_categories']}}</div>
										</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','news_description') || $check_field('add','news_description') || $check_field('set','news_description')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
				<el-form-item label="新闻描述" prop="news_description">
								<el-input type="textarea" id="news_description" v-model="form['news_description']" placeholder="请输入新闻描述"
						v-if="(form['news_information_id'] && $check_field('set','news_description')) || (!form['news_information_id'] && $check_field('add','news_description'))" :disabled="disabledObj['news_description_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','news_description')">{{form['news_description']}}</div>
										</el-form-item>
			</el-col>
													<el-col v-if="$check_field('get','news_body') || $check_field('add','news_body') || $check_field('set','news_body')" :xs="24" :sm="24" :lg="24" class="el_form_editor_warp">
				<el-form-item label="新闻正文" prop="news_body">
					<!-- <quill-editor v-model.number="form['news_body']"
						v-if="(form['news_information_id'] && $check_field('set','news_body')) || (!form['news_information_id'] && $check_field('add','news_body')) ">
					</quill-editor> -->
					<ai_editor
						v-if="(form['news_information_id'] && $check_field('set','news_body')) || (!form['news_information_id'] && $check_field('add','news_body'))"
						class="editor el_form_editor_warp" 
						:key="form.news_information_id" 
						:details="form.news_body"
						:form="form"
						@blur_comment="blur_comment_news_body"
						@update_comment="update_comment_news_body"
						:publish_flag="false" />
					<div v-else-if="$check_field('get','news_body')" v-html="form['news_body']"></div>
				</el-form-item>
			</el-col>
						
	
	
	
		
		
	
	
	
		
		</el-row>
					<el-col :xs="24" :sm="12" :lg="8" class="el_form_btn_warp">
				<el-form-item v-if="$check_action('/news_information/view','set') || $check_action('/news_information/view','add')">
					<el-button type="primary" @click="submit()">提交</el-button>
					<el-button @click="cancel()">取消</el-button>
				</el-form-item>
				<el-form-item v-else>
					<el-button @click="cancel()">返回</el-button>
				</el-form-item>
			</el-col>

		</el-form>
	</el-main>
</template>

<script>
	import mixin from "@/mixins/page.js";
						            						
	export default {
		mixins: [mixin],
		components: {
																																		},
		data() {
			return {
				field: "news_information_id",
				url_add: "~/api/news_information/add?",
				url_set: "~/api/news_information/set?",
				url_get_obj: "~/api/news_information/get_obj?",
				url_get_list: "~/api/news_information/get_list?",
				url_upload: "~/api/news_information/upload?",

				query: {
					"news_information_id": 0,
					like: 0,
				},
				rules: {
																																																														},
				form: {
								"news_headlines":  '', // 新闻标题
										"publication_date":  '', // 发布日期
										"news_pictures":  '', // 新闻图片
										"news_categories":  '', // 新闻分类
										"news_description":  '', // 新闻描述
										"news_body":  '', // 新闻正文
												"news_information_id": 0, // ID
													"create_by": this.$store.state.user.user_id,
						},
				disabledObj:{
								"news_headlines_isDisabled": false,
										"publication_date_isDisabled": false,
										"news_pictures_isDisabled": false,
										"news_categories_isDisabled": false,
										"news_description_isDisabled": false,
										"news_body_isDisabled": false,
										},


																														news_categories_cascader: {
					value: 'news_categories',
					label: 'news_categories',
					children: 'children',
					emitPath: false,
					expandTrigger: 'hover',
				},
				// 商品分类树形数据
				news_categories_tree: [],
						// 新闻分类选项列表
				list_news_categories: [""],
																					
									}
		},
		computed: {
			aiForm() {
				let form = {
																																																																				};
				return form;
			},
										},
		methods: {
													  openPreview(file) {
	    window.open(file.url)
	  },
		
	
					
	
							/**
			 * 上传新闻图片
			 * @param {Object} param 图片参数
			 */
			upload_news_pictures(param){
									this.uploadFile(param.file, "news_pictures");
								},
		
	
					
				/**
			 * 获取新闻分类列表
			 */
			async get_list_news_categories() {
				let param = {}
																															var json = await this.$get("~/api/news_class_nameification/get_list?",param);
				if(json.result && json.result.list){
					if (json.result.list.length > 0 && 'type' in json.result.list[0]) {
						json.result.list = json.result.list.filter(item => item.type == 1);
					}
							const hasFatherId = json.result.list.some(item => 'father_id' in item);
					if (hasFatherId) {
						this.news_categories_tree = this.build_news_categories_tree(json.result.list, 0);
					} else {
						this.news_categories_tree = json.result.list;
					}
					if (!this.query.news_information_id && this.news_categories_tree.length > 0) {
										this.form["news_categories"] = this.news_categories_tree[0]["news_categories"];
															}
						}
				else if(json.error){
					console.error(json.error);
				}
			},
					build_news_categories_tree(list, fatherId) {
				const tree = [];
				for (let item of list) {
					if (item.father_id === fatherId) {
					const children = this.build_news_categories_tree(list, item.news_class_nameification_id);
					if (children.length > 0) {
						item.children = children;
					}
					tree.push(item);
					}
				}
				return tree;
			},
							
					
	
					
	
					// 自动计算精度处理
		toFixed: function(num){
			if (!isNaN(num)) {
				return ((num + '').indexOf('.') == -1) ? num : num.toFixed(2);
			}
		},
			/**
			 * 获取对象之前
			 * @param {Object} param
			 */
			get_obj_before(param) {
				var form = "";
																								if(this.form && form){
					Object.keys(this.form).forEach(key => {
						Object.keys(form).forEach(dbKey => {
							// if(dbKey === "charging_standard"){
							// 	this.form['charging_rules'] = form[dbKey];
							// 	this.disabledObj['charging_rules_isDisabled'] = true;
							// };
							if(key === dbKey){
								this.disabledObj[key+'_isDisabled'] = true;
								this.form[key] = form[dbKey]
							}
							if(dbKey === "source_table"){
								this.form['source_table'] = form[dbKey];
							}
							if(dbKey === "source_id"){
								this.form['source_id'] = form[dbKey];
							}
							if(dbKey === "source_user_id"){
								this.form['source_user_id'] = form[dbKey];
							}
						})
					})
				}
				        if (this.form["publication_date"] && JSON.stringify(this.form["publication_date"]).indexOf("-")===-1){
          this.form["publication_date"] = this.$toTime(parseInt(this.form["publication_date"]),"yyyy-MM-dd")
        }
													$.db.del("form");
				return param;
			},

			/**
			 * 获取对象之后
			 * @param {Object} json
			 * @param {Object} func
			 */
			async get_obj_after(json, func){
				if (json.result && json.result.obj) {
					const obj = json.result.obj;
				}

														if(json.result.obj["publication_date"]=="0000-00-00"){
				  json.result.obj["publication_date"] = null;
				}
				if(parseInt(json.result.obj["publication_date"]) > 9999){
					json.result.obj["publication_date"] = this.$toTime(parseInt(json.result.obj["publication_date"]),"yyyy-MM-dd")
				}
																																							


			},

																																																async submit(param, func){
								if (!param) {
					param = this.form;
				}
				if(!this.form.news_information_id){
					param.create_by = this.$store.state.user.user_id;
				}else{
					delete param.create_by;
				}
																var pm = this.events("submit_before", Object.assign({}, param)) || param;
				var msg = await this.events("submit_check", pm);
				var ret;

			
				if (msg) {
					this.$toast(msg, 'danger');
				} else {
																																																										let submitForm = JSON.parse(JSON.stringify(pm));
								ret = this.events("submit_main", submitForm, func);
				}
				return ret;
			},
					submit_after(json, func) {
						let path = this.$route.fullPath
						let skip_Path  = path.replace('/view','/table')
						if(!this.form.news_information_id){
										  		  		  				  		  		  				  		  		  				  		  		  				  		  		  											let message_inform = {
								title: '新闻资讯',
								type: '消息',
								content: this.$store.state.user.username + '-' + this.$store.state.user.nickname + '提交了一条新闻资讯数据',
								state: 1,
								user_id:'9999'
							}
							this.$post("~/api/message_inform/add",message_inform)
									setTimeout(() => {
								this.$router.push(skip_Path);
							}, 1000);
						}else{
							this.$router.push(skip_Path);
						}
					},
			/**
			 * 提交前验证事件
			 * @param {Object} 请求参数
			 * @return {String} 验证成功返回null, 失败返回错误提示
			 */
			async submit_check(param) {
																					if (!param.publication_date){
					return "发布日期不能为空";
				}
																																																						var news_description_SensitiveWords = await this.filterSensitiveWords(param.news_description)
			if(news_description_SensitiveWords.length > 0){
				return '新闻描述中包含敏感词: ' + news_description_SensitiveWords.join(',')
			}
																		var news_body_SensitiveWords = await this.filterSensitiveWords(param.news_body)
			if(news_body_SensitiveWords.length > 0){
				return '新闻正文中包含敏感词: ' + news_body_SensitiveWords.join(',')
			}
								return null;
			},

			is_view(){
				// var bl = this.user_group == "管理员";
				var bl = false;

				if(!bl){
					bl = this.$check_action('/news_information/table','add');
					console.log(bl ? "你有表格添加权限视作有添加权限" : "你没有表格添加权限");
				}
				if(!bl){
					bl = this.$check_action('/news_information/table','set');
					console.log(bl ? "你有表格添加权限视作有修改权限" : "你没有表格修改权限");
				}
				if(!bl){
					bl = this.$check_action('/news_information/view','add');
					console.log(bl ? "你有视图添加权限视作有添加权限" : "你没有视图添加权限");
				}
				if(!bl){
					bl = this.$check_action('/news_information/view','set');
					console.log(bl ? "你有视图修改权限视作有修改权限" : "你没有视图修改权限");
				}
				if(!bl){
					bl = this.$check_action('/news_information/view','get');
					console.log(bl ? "你有视图查询权限视作有查询权限" : "你没有视图查询权限");
				}

				console.log(bl ? "具有当前页面的查看权，请注意这不代表你有字段的查看权" : "无权查看当前页，请注意即便有字段查询权限没有页面查询权限也不行");

				return bl;
			},
			/**
			 * 上传文件
			 * @param {Object} param
			 */
			uploadimg(param) {
				this.uploadFile(param.file, "avatar");
			},
																															blur_comment_news_body(data) {
				this.form['news_body'] = data;
			},
			update_comment_news_body(data) {
				this.form['news_body'] = data;
			},
							},
		created() {
																this.get_list_news_categories();
														},
	}
</script>

<style>
	.avatar-uploader .el-upload {
		border: 1px dashed #d9d9d9;
		border-radius: 6px;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}

	.avatar-uploader .el-upload:hover {
		border-color: #409EFF;
	}

	.avatar-uploader-icon {
		font-size: 28px;
		color: #8c939d;
		width: 178px;
		height: 178px;
		line-height: 178px;
		text-align: center;
	}

	.avatar {
		width: 178px;
		height: 178px;
		display: block;
	}
	
	.img_multiple{
		overflow: hidden;
	}
	.img_multiple .img_block{
		float: left;
		margin-right: 5px;
		margin-bottom: 5px;
		position: relative;
	}
	.img_multiple .img_block img{
		height: 100px;
		width: auto;
	}
	.img_multiple .img_del{
		position: absolute;
		top: 5px;
		right: 5px;
		width: 20px;
		height: 20px;
		background: #0000008a;
		color: #fff;
		line-height: 20px;
		text-align: center;
		border-radius: 100%;
		cursor: pointer;
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
		background-color: #fff;
		line-height: 100%;
		position: relative;
		margin: 10px 0;
		border: 1px solid #000;
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
		margin-bottom: 10px;
		text-align: left;
		font-size: 16px;
	}
	.check-item-list .check-item-li .check-item .check-item-title > p:nth-child(2) {
		width: 100%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.check-item-list .check-item-li .check-item .check-item-btn {
		margin-left: auto;
		display: flex;
		flex-direction: row;
		align-items: center;
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
		border: 1px solid #409eff;
		overflow: hidden;
	}
	.check-item-list .check-item-li .check-item-complete:before {
		content: "";
		position: absolute;
		right: 0;
		top: 0;
		border: 15px solid #409eff;
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
	.ccc {
		color: #ccc;
	}
	.image-slot {
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		color: #ccc;
		font-size: 24px;
	}
</style>
