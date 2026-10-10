<template>
	<el-main class="bg edit_wrap comtable_e">
		<el-form ref="form" :model="form" status-icon label-width="120px" v-if="is_view()">
		<el-row class="row_ce"> 
												<el-col v-if="$check_field('get','title') || $check_field('add','title') || $check_field('set','title')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="标题" prop="title">
															<el-input id="title" v-model="form['title']" placeholder="请输入标题"
							  v-if="(form['news_resources_id'] && $check_field('set','title')) || (!form['news_resources_id'] && $check_field('add','title'))" :disabled="disabledObj['title_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','title')">
						{{form['title']}}
				  					</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','url') || $check_field('add','url') || $check_field('set','url')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="详情链接" prop="url">
															<el-input id="url" v-model="form['url']" placeholder="请输入详情链接"
							  v-if="(form['news_resources_id'] && $check_field('set','url')) || (!form['news_resources_id'] && $check_field('add','url'))" :disabled="disabledObj['url_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','url')">
						{{form['url']}}
				  					</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','read_num') || $check_field('add','read_num') || $check_field('set','read_num')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="阅读量" prop="read_num">
															<el-input id="read_num" v-model="form['read_num']" placeholder="请输入阅读量"
							  v-if="(form['news_resources_id'] && $check_field('set','read_num')) || (!form['news_resources_id'] && $check_field('add','read_num'))" :disabled="disabledObj['read_num_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','read_num')">
						{{form['read_num']}}
				  					</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','origin') || $check_field('add','origin') || $check_field('set','origin')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="发布来源" prop="origin">
															<el-input id="origin" v-model="form['origin']" placeholder="请输入发布来源"
							  v-if="(form['news_resources_id'] && $check_field('set','origin')) || (!form['news_resources_id'] && $check_field('add','origin'))" :disabled="disabledObj['origin_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','origin')">
						{{form['origin']}}
				  					</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','release_time') || $check_field('add','release_time') || $check_field('set','release_time')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="发布时间" prop="release_time">
															<el-input id="release_time" v-model="form['release_time']" placeholder="请输入发布时间"
							  v-if="(form['news_resources_id'] && $check_field('set','release_time')) || (!form['news_resources_id'] && $check_field('add','release_time'))" :disabled="disabledObj['release_time_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','release_time')">
						{{form['release_time']}}
				  					</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','content') || $check_field('add','content') || $check_field('set','content')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="正文内容" prop="content">
											<el-input type="textarea" id="content" v-model="form['content']" placeholder="请输入正文内容"
						v-if="(form['news_resources_id'] && $check_field('set','content')) || (!form['news_resources_id'] && $check_field('add','content'))" :disabled="disabledObj['content_isDisabled']"></el-input>
					<div v-else-if="$check_field('get','content')">{{form['content']}}</div>
										</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','comment_num') || $check_field('add','comment_num') || $check_field('set','comment_num')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="评论数量" prop="comment_num">
															<el-input id="comment_num" v-model="form['comment_num']" placeholder="请输入评论数量"
							  v-if="(form['news_resources_id'] && $check_field('set','comment_num')) || (!form['news_resources_id'] && $check_field('add','comment_num'))" :disabled="disabledObj['comment_num_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','comment_num')">
						{{form['comment_num']}}
				  					</div>
														</el-form-item>
			</el-col>
																<el-col v-if="$check_field('get','comment') || $check_field('add','comment') || $check_field('set','comment')" :xs="24" :sm="12" :lg="8" class="el_form_item_warp">
							<el-form-item label="最新评论" prop="comment">
															<el-input id="comment" v-model="form['comment']" placeholder="请输入最新评论"
							  v-if="(form['news_resources_id'] && $check_field('set','comment')) || (!form['news_resources_id'] && $check_field('add','comment'))" :disabled="disabledObj['comment_isDisabled']">
				  					</el-input>
					<div v-else-if="$check_field('get','comment')">
						{{form['comment']}}
				  					</div>
														</el-form-item>
			</el-col>
									
	
	
	
		
		
	
	
	
		
		
		
		</el-row>
					<el-col :xs="24" :sm="12" :lg="8" class="el_form_btn_warp">
				<el-form-item v-if="$check_action('/news_resources/view','set') || $check_action('/news_resources/view','add')">
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
				field: "news_resources_id",
				url_add: "~/api/news_resources/add?",
				url_set: "~/api/news_resources/set?",
				url_get_obj: "~/api/news_resources/get_obj?",
				url_get_list: "~/api/news_resources/get_list?",
				url_upload: "~/api/news_resources/upload?",

				query: {
					"news_resources_id": 0,
					like: 0,
				},

				form: {
								"title":  '', // 标题
										"url":  '', // 详情链接
										"img":  '', // 图片链接
										"read_num":  '', // 阅读量
										"origin":  '', // 发布来源
										"release_time":  '', // 发布时间
										"content":  '', // 正文内容
										"comment_num":  '', // 评论数量
										"comment":  '', // 最新评论
												"news_resources_id": 0, // ID
																		"create_by": this.$store.state.user.user_id,
				},
				disabledObj:{
								"title_isDisabled": false,
										"url_isDisabled": false,
										"img_isDisabled": false,
										"read_num_isDisabled": false,
										"origin_isDisabled": false,
										"release_time_isDisabled": false,
										"content_isDisabled": false,
										"comment_num_isDisabled": false,
										"comment_isDisabled": false,
										},

																																																															

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
																																																																								
			},

																																																																											async submit(param, func){
								if (!param) {
					param = this.form;
				}
				if(!this.form.news_resources_id){
					param.create_by = this.$store.state.user.user_id;
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
					async submit_after(json, func) {
						let path = this.$route.fullPath
						let skip_Path  = path.replace('/view','/table')
								if(!this.form.news_resources_id){
						  		  							  		  							  		  							  		  							  		  														let message_inform = {
								title: '新闻资源',
								type: '消息',
								content: this.$store.state.user.username + '-' + this.$store.state.user.nickname + '提交了一条新闻资源数据',
								state: 1,
								user_id:'9999'
							}
							this.$post("~/api/message_inform/add",message_inform)
									this.$message.success("提交成功!");
							setTimeout(() => {
								this.$router.push(skip_Path);
							}, 1000);
						}else{
							this.$message.success("提交成功!");
							this.$router.push(skip_Path);
						}
					},
			
			/**
			 * 提交前验证事件
			 * @param {Object} 请求参数
			 * @return {String} 验证成功返回null, 失败返回错误提示
			 */
						async submit_check(param) {
					
																																																																																																		let content_SensitiveWords = await this.filterSensitiveWords(param.content)
				if(content_SensitiveWords.length > 0){
					return '正文内容中包含敏感词: ' + content_SensitiveWords.join(',')
				}
																																					return null;
			},

			is_view(){
				// var bl = this.user_group == "管理员";
				var bl = false;

				if(!bl){
					bl = this.$check_action('/news_resources/table','add');
					console.log(bl ? "你有表格添加权限视作有添加权限" : "你没有表格添加权限");
				}
				if(!bl){
					bl = this.$check_action('/news_resources/table','set');
					console.log(bl ? "你有表格添加权限视作有修改权限" : "你没有表格修改权限");
				}
				if(!bl){
					bl = this.$check_action('/news_resources/view','add');
					console.log(bl ? "你有视图添加权限视作有添加权限" : "你没有视图添加权限");
				}
				if(!bl){
					bl = this.$check_action('/news_resources/view','set');
					console.log(bl ? "你有视图修改权限视作有修改权限" : "你没有视图修改权限");
				}
				if(!bl){
					bl = this.$check_action('/news_resources/view','get');
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
			handlePictureCardPreview(file) {
				this.previewImageUrl = file.url;
				this.previewVisible = true;
			},
			uploadExceed() {
				this.$message({
					message: "最多可设置5张主图",
					type: "warning",
				});
			},
																																																},
		created() {
																																						},
	}
</script>

<style scoped>
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
	.mul-upload-container{
		display: flex;
	}
	.mul-upload-container .el-form-item__content{
		margin-left: 0 !important;
	}
	.upload-container.hide-upload .el-upload--picture-card {
		display: none;
	}
	.el-upload--picture-card{
		width: 180px;
    	height: 180px;
		line-height: 180px;
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
