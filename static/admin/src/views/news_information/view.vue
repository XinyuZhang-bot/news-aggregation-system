<template>
	<el-main class="bg edit_wrap comtable_e">
		<el-form ref="form" :model="form" status-icon label-width="120px" v-if="is_view()">
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
					<div
						v-if="crawlTimeDisplay"
						style="margin-top: 6px; font-size: 12px; color: #606266;"
					>
						新闻爬取时间：{{ crawlTimeDisplay }}
					</div>
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
			<!-- 阅读原文 -->
			<el-col :xs="24" :sm="12" :lg="8" class="el_form_item_warp" v-if="sourceUrl">
				<el-form-item label="原文链接">
					<el-button type="primary" plain @click="openSourceUrl">阅读原文</el-button>
					<div style="margin-top: 6px; font-size: 12px; opacity: 0.85; word-break: break-all;">
						{{ sourceUrl }}
					</div>
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
						:details="form.news_body"
						:form="form"
						@blur_comment="blur_comment_news_body"
						@update_comment="update_comment_news_body"
						:publish_flag="false" />
					<div
						v-else-if="$check_field('get','news_body')"
						class="news_body_display"
						v-html="stripImageTags(form['news_body'])"
					></div>
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
	import { collectSpiderServiceBaseCandidates } from "@/utils/spiderServiceBase.js";
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
				// 原文链接：仅用于界面“阅读原文”，不参与提交（不改业务表结构）
				sourceUrl: "",
				// 仅用于管理端展示，不参与提交/发布
				crawlTimeDisplay: "",
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
			openSourceUrl() {
				const u = this.sanitizeUrl(this.sourceUrl);
				if (!u) return;
				window.open(u, "_blank");
			},
			sanitizeUrl(url) {
				if (!url) return "";
				let u = String(url).trim();
				u = u.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
				const m = u.match(/https?:\/\/[^\s"'<>]+/i);
				if (m) u = m[0];
				if (!/^https?:\/\//i.test(u)) return "";
				return u;
			},
			extractSourceUrlFromBodyAndStrip() {
				if (!this.form) return;
				const body = this.form.news_body ? String(this.form.news_body) : "";
				let su = "";
				const mTag = body.match(/\[SOURCE_URL\]([\s\S]*?)\[\/SOURCE_URL\]/i);
				if (mTag && mTag[1]) {
					su = this.sanitizeUrl(mTag[1]);
				} else {
					const mOld = body.match(/<!--\s*source_url\s*:\s*(https?:\/\/[^>\s]+)\s*-->/i);
					if (mOld && mOld[1]) su = this.sanitizeUrl(mOld[1]);
				}
				this.sourceUrl = su;
				this.form.news_body = body
					.replace(/\[SOURCE_URL\][\s\S]*?\[\/SOURCE_URL\]/gi, "")
					.replace(/<!--\s*source_url\s*:[\s\S]*?-->/gi, "")
					.trim();
			},
			async tryPrefillFromSourceUrl() {
				const meta = $.db.get("news_resource_meta");
				if (!meta || typeof meta !== "object") return;
				const url = (meta.source_url || "").trim();
				this.crawlTimeDisplay = (meta.crawl_time || "").trim();
				if (!url) return;
				this.sourceUrl = url;
				$.db.del("news_resource_meta");

				try {
					let resp = null;
					const bases = collectSpiderServiceBaseCandidates();
					for (let b = 0; b < bases.length; b++) {
						const base = bases[b];
						for (let i = 0; i < 2; i++) {
							try {
								resp = await this.$axios.get(
									`${base}/extract?url=${encodeURIComponent(url)}`,
									{ timeout: 45000 },
								);
								if (resp && resp.data && resp.data.ok) {
									break;
								}
							} catch (e) {
								/* try next retry or base */
							}
						}
						if (resp && resp.data && resp.data.ok) break;
					}
					const data = resp && resp.data ? resp.data : null;
					if (!data || !data.ok) {
						const err = (data && data.error) || (resp && resp.data && resp.data.error) || "extract 接口未返回 ok";
						this.appendImageToBodyHtml(this.form.news_pictures);
						// 不弹窗以免演示/日常编辑被打断；失败时仍保留资源页已预填的摘要等，可手动编辑或点「阅读原文」
						console.warn("[原文预填] 爬虫 extract 未成功，已使用资源摘要。原因：", err);
						return;
					}

					// 源发布时间优先写入发布日期（仅保留日期）
					if (data.release_time) {
						const d = String(data.release_time).trim().slice(0, 10);
						if (d) this.form.publication_date = d;
					}

					// 标题/正文（含多图）
					if (data.title && !this.form.news_headlines) {
						this.form.news_headlines = data.title;
					}
					if (data.body_html && String(data.body_html).trim()) {
						const su = (data.final_url || url || "").trim();
						// 新建页不在正文里注入标记，避免编辑器出现 [SOURCE_URL] 文本污染正文。
						// 链接由 sourceUrl 单独保存，提交时再回写标记。
						this.sourceUrl = this.sanitizeUrl(su);
						// 只要接口返回了 body_html 就写入；勿再用纯文本长度门槛（短稿/截断稿会误判为空）
						this.form.news_body = data.body_html;
					}

					// 首图填充到“新闻图片”
					const img = data.primary_img || (data.images && data.images.length ? data.images[0] : "");
					if (img) {
						this.form.news_pictures = this.normalizeImageUrl(img);
					}
					// extract 成功但正文未带图时，兜底注入封面图，确保发布后正文可见图片。
					this.appendImageToBodyHtml(this.form.news_pictures);
				} catch (e) {
					const msg =
						(e && e.response && e.response.data && e.response.data.error) ||
						(e && e.message) ||
						"网络异常或服务未启动";
					this.appendImageToBodyHtml(this.form.news_pictures);
					console.warn("[原文预填] 请求 extract 异常，当前为资源摘要。原因：", msg, e);
				}
			},
						
									openPreview(file) {
			    window.open(file.url)
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
					if (!this.query.news_information_id && !this.form["news_categories"] && this.news_categories_tree.length > 0) {
										this.form["news_categories"] = this.news_categories_tree[0]["news_categories"];
															}
					if (this.form["news_categories"]) {
						this.form["news_categories"] = this.resolveCategoryValue(this.form["news_categories"]);
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
			normalizeImageUrl(url) {
				const v = (url || "").trim();
				if (!v) return "";
				if (v.startsWith("//")) return `https:${v}`;
				return v;
			},
			stripImageTags(html) {
				if (!html) {
					return "";
				}
				return String(html)
					.replace(/<img\b[^>]*>/gi, "")
					.replace(/<picture\b[^>]*>[\s\S]*?<\/picture>/gi, "");
			},
			appendImageToBodyHtml() {
				return;
			},
			resolveCategoryValue(raw) {
				const current = (raw || "").trim();
				if (!current) return current;
				const list = [];
				const walk = (arr) => {
					(arr || []).forEach((i) => {
						if (i && i.news_categories) list.push(i.news_categories);
						if (i && i.children && i.children.length) walk(i.children);
					});
				};
				walk(this.news_categories_tree || []);
				if (list.includes(current)) return current;
				const map = {
					"综合": ["综合", "要闻", "热点"],
					"时政": ["时政", "要闻", "政策"],
					"国际": ["国际", "国际新闻", "外交", "海外", "全球", "台海", "东海", "南海"],
					"社会": ["社会", "民生", "热点"],
					"科技": ["科技", "互联网", "数码"],
					"健康": ["健康", "医疗", "卫生"],
					"教育": ["教育", "校园"],
					"文化": ["文化", "读书", "艺术"],
					"娱乐": ["娱乐", "文娱", "明星", "体育", "足球", "篮球"],
					"财经": ["财经", "经济", "金融"],
					"军事": ["军事", "国防"],
				};
				for (const [k, arr] of Object.entries(map)) {
					if (k === current || arr.includes(current)) {
						const matched = list.find(v => v === k || arr.includes(v));
						if (matched) return matched;
					}
				}
				const fuzzy = list.find(v => current.includes(v) || v.includes(current));
				return fuzzy || current;
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
				// When navigating from other modules, caller can prefill data via `$.db.set("form", ...)`.
				var cached = $.db.get("form");
				if (cached && this.form && typeof cached === "object") {
					Object.keys(cached).forEach((key) => {
						if (key in this.form) {
							this.form[key] = cached[key];
						}
					});
					this.form["news_pictures"] = this.normalizeImageUrl(this.form["news_pictures"]);
					this.form["news_categories"] = this.resolveCategoryValue(this.form["news_categories"]);
					this.extractSourceUrlFromBodyAndStrip();
					$.db.del("form");
				}
		        if (this.form["publication_date"] && JSON.stringify(this.form["publication_date"]).indexOf("-")===-1){
          this.form["publication_date"] = this.$toTime(parseInt(this.form["publication_date"]),"yyyy-MM-dd")
        }

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
														if(this.form["publication_date"]=="0000-00-00"){
				  this.form["publication_date"] = null;
				}
				if(parseInt(this.form["publication_date"]) > 9999){
					this.form["publication_date"] = this.$toTime(parseInt(this.form["publication_date"]),"yyyy-MM-dd")
				}
				this.extractSourceUrlFromBodyAndStrip();
																																							
			},

			submit_before(param) {
				// 提交前回写原文链接标记，保证前台/后续查看可解析“阅读原文”
				const su = this.sanitizeUrl(this.sourceUrl);
				if (!su) return param;
				let body = (param.news_body || "").toString();
				body = body
					.replace(/\[SOURCE_URL\][\s\S]*?\[\/SOURCE_URL\]/gi, "")
					.replace(/<!--\s*source_url\s*:[\s\S]*?-->/gi, "")
					.trim();
				param.news_body = `${body}\n[SOURCE_URL]${su}[/SOURCE_URL]`;
				return param;
			},

																																																						async submit(param, func){
								if (!param) {
					param = this.form;
				}
				if(!this.form.news_information_id){
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
								if(!this.form.news_information_id){
						  		  							  		  							  		  							  		  							  		  														let message_inform = {
								title: '新闻资讯',
								type: '消息',
								content: this.$store.state.user.username + '-' + this.$store.state.user.nickname + '提交了一条新闻资讯数据',
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
					
																				if (!param.publication_date){
					return "发布日期不能为空";
				}
																																																										let news_description_SensitiveWords = await this.filterSensitiveWords(param.news_description)
				if(news_description_SensitiveWords.length > 0){
					return '新闻描述中包含敏感词: ' + news_description_SensitiveWords.join(',')
				}
																									let news_body_SensitiveWords = await this.filterSensitiveWords(param.news_body)
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
																															blur_comment_news_body(data) {
				this.form['news_body'] = data;
			},
			update_comment_news_body(data) {
				this.form['news_body'] = data;
			},
							},
		created() {
																this.get_list_news_categories();
														// If coming from `news_resources`, prefill data as early as possible.
														if ($.db.get("form")) {
															let cached = $.db.get("form");
															if (cached && typeof cached === "object") {
																Object.keys(cached).forEach((key) => {
																	if (key in this.form) {
																		this.form[key] = cached[key];
																	}
																});
																this.form["news_pictures"] = this.normalizeImageUrl(this.form["news_pictures"]);
																this.form["news_categories"] = this.resolveCategoryValue(this.form["news_categories"]);
																this.extractSourceUrlFromBodyAndStrip();
																$.db.del("form");
															}
														}
														// 拉取原文链接与含图正文（用于“阅读原文”按钮 + 多图正文）
														this.tryPrefillFromSourceUrl();
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
