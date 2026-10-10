<template>
	<el-main class="bg table_wrap comtabel_t">
		<el-form label-position="right" :model="query" class="form p_4" label-width="120">
			<el-row class="rows row1">



							<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap" v-if="$check_field('get','news_headlines')">
					<el-form-item label="新闻标题">
									<el-input v-model="query.news_headlines"></el-input>
								</el-form-item>
				</el-col>
															<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap" v-if="$check_field('get','news_categories')">
					<el-form-item label="新闻分类">
									<el-cascader v-model="query.news_categories" :options="list_news_categories" :props="news_categories_cascader"
							:show-all-levels="false" clearable collapse-tags placeholder="请选择新闻分类"
							@change="handle_news_categories_change"></el-cascader>
								</el-form-item>
				</el-col>
										</el-row>
	<el-row class="rows row2">

		<el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap search_btns">

				<el-col :xs="24" :sm="10" :lg="8" class="search_btn_1 search_btn_wrap_1 btns">

										<el-button type="primary" @click="search()" class="search_btn_find">查询</el-button>
						<el-button @click="reset()" style="margin-right: 74px;" class="search_btn_reset">重置</el-button>
																						

														<el-button v-if="$check_action('/news_information/table','del') || $check_action('/news_information/view','del')" class="search_btn_del" type="danger" @click="delInfo()">删除</el-button>
								
				</el-col>
		</el-col>
	</el-row >
	<div class="statistics-info" v-if="statisticsData.total > 0">
                                          </div>

		</el-form>
				<el-table :data="list" @selection-change="selectionChange" @sort-change="$sortChange" style="width: 100%" id="dataTable" row-key="news_information_id" :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
			:default-expand-all="isExpandAll" ref="tableRef">
					<el-table-column fixed type="selection" tooltip-effect="dark" width="55">
			</el-table-column>
				<el-table-column prop="news_headlines" @sort-change="$sortChange" label="新闻标题" 				v-if="$check_field('get','news_headlines')" min-width="300">
					<template slot-scope="scope">
							{{ scope.row["news_headlines"] }}
									</template>
					</el-table-column>
					<el-table-column prop="publication_date" @sort-change="$sortChange" label="发布日期" 				v-if="$check_field('get','publication_date')" min-width="300">
		                <template slot-scope="scope">
									                	{{ $toTime(scope.row["publication_date"],"yyyy-MM-dd") }}
														                </template>
					</el-table-column>
					<el-table-column prop="news_categories" @sort-change="$sortChange" label="新闻分类" 				v-if="$check_field('get','news_categories')" min-width="300">
					<template slot-scope="scope">
							{{ scope.row["news_categories"] }}
									</template>
					</el-table-column>
					<el-table-column prop="news_description" @sort-change="$sortChange" label="新闻描述" 				v-if="$check_field('get','news_description')" min-width="300">
					<template slot-scope="scope">
							{{ scope.row["news_description"] }}
									</template>
					</el-table-column>
			
			<el-table-column prop="extra" @sort-change="$sortChange" label="信息" min-width="300" v-if="hasExtraData" >
				<template slot-scope="scope">
					<div v-for="(value, key) in JSON.parse(scope.row.extra || '{}')" :key="key">{{ key }}：{{ value }}</div>
				</template>
			</el-table-column>
            <el-table-column sortable prop="create_time" label="创建时间" min-width="200">
                <template slot-scope="scope">
                	{{ $toTime(scope.row["create_time"],"yyyy-MM-dd hh:mm:ss") }}
                </template>
            </el-table-column>

			<el-table-column sortable prop="update_time" label="更新时间" min-width="200">
                <template slot-scope="scope">
                	{{ $toTime(scope.row["update_time"],"yyyy-MM-dd hh:mm:ss") }}
                </template>
			</el-table-column>







			<el-table-column fixed="right" label="操作" min-width="200" v-if="$check_action('/news_information/table','set') || $check_action('/news_information/view','set') || $check_action('/news_information/view','get')
						" >


				<template slot-scope="scope">
					<div class="view_a">
					<router-link class="e-button el-button--small is-plain el-button--success" style="margin: 5px !important;"
					v-if="$check_action('/news_information/table','set') || $check_action('/news_information/view','set') || $check_action('/news_information/view','get')"
						:to="'./view?' + field + '=' + scope.row[field]"
						 size="small">
						<span>详情</span>
					</router-link>
						<router-link v-if="$check_comment('/news_information/table')" class="e-button el-button--small is-plain el-button--primary"
								  :to="'../comment/table?size=15&page=1&source_table=news_information&source_field=' + field + '&source_id=' + scope.row[field]" size="small">
						<span>查看评论</span>
					</router-link>
					</div>
				</template>
			</el-table-column>

		</el-table>
								<!-- 分页器 -->
		<div class="mt text_center">
			<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
				:current-page="query.page" :page-sizes="[10, 15, 30, 50]" :page-size="query.size"
				layout="total, sizes, prev, pager, next, jumper" :total="count">
			</el-pagination>
		</div>
		<!-- /分页器 -->
								<el-dialog title="重要提醒" :visible.sync="showModal" width="400px" :before-close="closeModal">
			<div style="text-align: center">
				<p style="margin-bottom: 16px; font-size: 16px; color: #333;">
				当前有数据达到预警值！
				</p>
				<p style="color: #666;">{{ message }}</p>
			</div>
			<div slot="footer" class="dialog-footer">
				<el-button @click="closeModal">取消</el-button>
				<el-button type="primary" @click="closeModal">确定</el-button>
			</div>
		</el-dialog>


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
				statisticsData: {
      				total: 0,
            				},
																	news_categories_cascader: {
					value: 'news_categories',
					label: 'news_categories',
					children: 'children',
					emitPath: false,
					expandTrigger: 'hover',
				},
									// 弹框
				showModal: false,
				// 获取数据地址
				url_get_list: "~/api/news_information/get_list",
				url_del: "~/api/news_information/del?",

				// 字段ID
				field: "news_information_id",
									// 查询
				query: {
					"size":  15,
					"page": 1,
								"news_headlines": "",
													"news_categories": "",
										"login_time": "",
					"create_time": "",
					"orderby": `create_time desc`
				},

				// 数据
				list: [],
																	// 新闻分类列表
				list_news_categories: [""],
										message: '',
				// 控制展开状态
				isExpandAll: true,
				// 存储展开的行
				expandKeys: [],
				prevSelection: [],
			}
		},
		methods: {
				previewFile(fileName) {
					if(!fileName){
						return;
					}
					const fileExtension = fileName.split('.').pop().toLowerCase();
					if(fileExtension == 'docx' || fileExtension == 'xlsx' || fileExtension == 'pptx') {
						this.$router.push('/filePreview?url=' + fileName + '&type=' + fileExtension);
						return;
					}
					window.open(this.$fullUrl(fileName), '_blank');
				},
				showPreview(file) {
					if(!file){
						return false;
					}
					let fileType = file.split('.').pop().toLowerCase();
					if(fileType == 'docx' || fileType == 'xlsx' || fileType == 'pptx') {
						return true;
					}else {
						return false;
					}
				},
															// 关闭弹框
			closeModal(){
				this.showModal = false;
				},
			/**
			 * @description 获取到列表事件
			 * @param {Object} res 响应结果
			 */
			get_list_after: function get_list_after(res, func, url) {
				let _this = this
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
						this.list_news_categories = this.build_news_categories_tree(json.result.list, 0);
					} else {
						this.list_news_categories = json.result.list;
					}
			  				}else if (json.error){
					console.log(json.error);
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
			handle_news_categories_change(value) {
				if (value) {
					this.query.news_categories = value;
				} else {
					this.query.news_categories = '';
				}
			},
								



															async delInfo() {
				var list = this.selection;
				if (list.length === 0) {
					this.$message({
						type: 'info',
						message: '选择对象不能为空!'
					});
					return;
				}
				for (let i = 0; i < list.length; i++) {
					let type = list[i];
					let res
																																																																					}
				this.$confirm('删除后数据将无法恢复，请确认是否删除？', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(async () => {
              		await this.delAll(list);
				}).catch(() => {
					this.$message({
						type: 'info',
						message: '已取消删除'
					});
				});
			},
			// 查询方法
			search() {
				this.query.page = 1;
				this.get_list();
							},

			// 重置方法  
			reset() {
				// 原有的重置逻辑
				Object.keys(this.query).forEach(key => {
					if (key !== 'size' && key !== 'page' && key !== 'orderby') {
						if (key.includes('_min') || key.includes('_max')) {
							this.query[key] = '';
						} else {
							this.query[key] = '';
						}
					}
				});
				
																																																															
				this.query.orderby = "create_time desc";
				this.get_list();
							},
	},
		created() {
										// 初始化新闻分类列表
			this.get_list_news_categories();
								},
		computed: {
			hasExtraData() {
				return this.list.some(item => item.extra && item.extra.trim() !== '');
			}
		}
	}
</script>

<style type="text/css">
	.bg {
		background: white;
	}

	.form.p_4 {
		padding: 1rem;
	}

	.form .el-input {
		width: initial;
	}

	.mt {
		margin-top: 1rem;
	}

	.text_center {
		text-align: center;
	}

	.float-right {
		float: right;
	}


	.modal_wrap{
		width: 100vw;
		height: 100vh;
		position: fixed;
		top: 0;
		left: 0;
		background: rgba(0,0,0,0.5);
		z-index: 9999999999;
	}
	.el-date-editor .el-range-separator{
		width: 10% !important;
	}
	.num_range {
	  display: flex;
	  align-items: center;
	}

	.num_range_span {
	  font-size: 28px;
	}
	td > .cell > a, td > .cell > span, td > .cell {
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 3;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.expand-all {
		margin-top: 10px;
	}
	.el-table__indent, .el-table__placeholder {
		display: inline-block !important;
	}
.route-map-dialog {
  display: flex;
  height: 500px;
}

.route-map-left {
  flex: 1;
  position: relative;
  height: 100%;
  background: #f5f5f5;
}

.route-map-container {
  width: 100%;
  height: 100%;
}

.route-map-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  color: #409eff;
  font-size: 14px;
}

.route-map-right {
  width: 320px;
  padding-left: 20px;
  overflow-y: auto;
  border-left: 1px solid #eee;
}

.route-map-info-row {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.route-map-info-label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.route-map-info-value {
  color: #666;
  line-height: 1.5;
  font-size: 14px;
}
</style>
