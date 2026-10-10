<template>
	<div class="diy_list page_news_information page_news_information--jd" id="news_information_list">
		<div class="warp jd-news-page">
			<div class="container diy_list_container">
				<div class="jd-page-title">
					<span class="jd-page-title__line" aria-hidden="true"></span>
					<span class="jd-page-title__text">新闻资讯列表</span>
					<span class="jd-page-title__line" aria-hidden="true"></span>
				</div>

				<div class="jd-toolbar">
					<b-form-input
						class="jd-toolbar__input"
						placeholder="新闻标题搜索"
						v-model="query['news_headlines']"
						@keyup.enter="search()"
					/>
					<b-form-input
						class="jd-toolbar__input"
						placeholder="新闻分类搜索"
						v-model="query['news_categories']"
						@keyup.enter="search()"
					/>
					<b-button class="jd-toolbar__search" @click="search()">
						<b-icon icon="search" />
						<span class="jd-toolbar__search-text">搜索</span>
					</b-button>
				</div>

				<div class="jd-filters">
					<el-cascader
						v-model="news_categories_value"
						:options="list_news_categories"
						:show-all-levels="false"
						:props="news_categories_cascader"
						placeholder="全部"
						clearable
						@change="handle_news_categories_change"
						class="jd-filters__cascader"
					/>
					<el-select
						v-model="selectedSortValue"
						placeholder="按发布时间排序"
						@change="set_sort"
						class="jd-filters__select"
					>
						<el-option
							v-for="item in list_sort"
							:key="item.value"
							:label="item.name"
							:value="item.value"
						/>
					</el-select>
				</div>

				<div class="row diy_list_box jd-list-wrap">
					<div class="col">
						<list_news_information ref="news_information" :list="list" layout="jd-text" />
					</div>
				</div>

				<div class="row diy_list_page_box jd-pagination-wrap">
					<div class="col overflow-auto flex_cc">
						<b-pagination
							v-model="query.page"
							:total-rows="count"
							:per-page="query.size"
							@change="goToPage"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import list_news_information from "@/components/diy/list_news_information.vue";
	import diy_pager from "@/components/diy/diy_pager";
	import mixin from "@/mixins/page.js";

	export default {
		mixins: [mixin],
		components: {
			diy_pager,
			list_news_information,
		},
		data() {
			return {
				url_get_list: "~/api/news_information/get_list",

				// 查询条件
				query: {
					keyword: "",
					page: 1,
					size: 12,
					news_headlines: "",
					news_categories: "",
					orderby: "create_time desc",
				},
				news_categories_value: "全部",
				news_categories_cascader: {
					value: 'news_categories',
					label: 'news_categories',
					children: 'children',
					emitPath: false,
					expandTrigger: 'hover',
				},
				selectedSortValue: "create_time desc",
				// 排序内容
				list_sort: [{
						name: "创建时间从高到低",
						value: "create_time desc",
					},
					{
						name: "创建时间从低到高",
						value: "create_time asc",
					},
					{
						name: "更新时间从高到低",
						value: "update_time desc",
					},
					{
						name: "更新时间从低到高",
						value: "update_time asc",
					},
										],

											// 新闻分类列表
				"list_news_categories": [""],
						
			}
		},
		methods: {
			toDetails(o) {
						let query = { news_information_id: o['news_information_id'] };
							this.$router.push({    
					path: `/news_information/details`,
					query: query,
				});
			},
      get_list_before(param) {
      },
			/**
			 * 筛选选择
			 */
			filter_set(o,key) {
			    if (o == "全部") {
			        this.query[key] = "";
			    } else {
			        this.query[key] = o;
			    }
			    this.search();
			},

			/**
			 * 排序
			 */
			set_sort(o) {
			    this.query.orderby = o;
			    this.search();
			},
				/**
				 * 获取列表后
				 * @param {Object} json
				 * @param {Object} func
				 */
				get_list_after(json ,func){
						
				},
													/**
			 * 获取新闻分类列表
			 */
			async get_list_news_categories() {
				var json = await this.$get("~/api/news_class_nameification/get_list?");
				if (json.result && json.result.list) {
					if (json.result.list.length > 0 && 'type' in json.result.list[0]) {
						json.result.list = json.result.list.filter(item => item.type == 1);
					}
					const hasFatherId = json.result.list.some(item => 'father_id' in item);
					let classificationTree = []
					if (hasFatherId) {
						classificationTree = this.build_news_categories_tree(json.result.list, 0);
					} else {
						classificationTree = json.result.list;
					}
					this.list_news_categories = [
						{
							news_categories: '全部',
						},
						...classificationTree
					];
				} else if (json.error) {
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
				if (value && value !== '全部') {
					this.query.news_categories = value;
				} else {
					this.query.news_categories = '';
				}
				this.search();
			},
						/**
			 * 筛选
			 */
														filter_news_categories(o) {
				if (o == "全部") {
					this.query["news_categories"] = "";
				} else {
					this.query["news_categories"] = o;
				}
				this.search();
			},
										/**
			 * 重置
			 */
			reset() {
							this.query.news_headlines = ""
												this.query.news_categories = ""
									this.search();
			},

			// 返回条数
			toSize(i){
				this.query.size = i;
				this.first();
			},

			// 返回页数
			toPage(i){
				this.query.page = i;
				this.first();
			},

      goToPage(v){
        this.query.page = v;
        this.goToNew(v)
      },

		},
		computed: {
		},
		created() {
										/**
			 * 获取新闻分类列表
			 */
			this.get_list_news_categories();
								}
	}
</script>

<style>
.el-date-editor--datetimerange.el-input, .el-date-editor--datetimerange.el-input__inner,.el-date-editor--daterange.el-input, .el-date-editor--daterange.el-input__inner, .el-date-editor--timerange.el-input, .el-date-editor--timerange.el-input__inner{
	width: 100%;
}
.el-date-editor .el-range-separator{
	width: 11% !important;
}
.num_range {
  display: flex;
  align-items: center;
}

.num_range_span {
  font-size: 28px;
}
</style>

<style scoped>
.jd-news-page {
	background: #f4f4f4;
	padding-bottom: 2rem;
}

.page_news_information--jd .diy_list_container {
	max-width: 1200px;
}

.jd-page-title {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 16px;
	margin: 28px 0 24px;
}

.jd-page-title__line {
	flex: 1;
	height: 1px;
	background: linear-gradient(90deg, transparent, #ddd 20%, #ddd 80%, transparent);
	max-width: 120px;
}

.jd-page-title__text {
	font-size: 22px;
	font-weight: 700;
	color: #1a1a1a;
	white-space: nowrap;
}

.jd-toolbar {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 12px;
	margin-bottom: 16px;
	padding: 16px 18px;
	background: #fff;
	border-radius: 8px;
	border: 1px solid #eee;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.jd-toolbar__input {
	flex: 1;
	min-width: 160px;
	max-width: 280px;
	height: 40px !important;
	border-radius: 8px !important;
	border: 1px solid #e0e0e0 !important;
}

.jd-toolbar__search {
	height: 40px;
	padding: 0 20px;
	border-radius: 8px !important;
	background: #e4393c !important;
	border: none !important;
	color: #fff !important;
	display: inline-flex;
	align-items: center;
	gap: 6px;
	font-weight: 600;
}

.jd-toolbar__search:hover {
	background: #c81623 !important;
	color: #fff !important;
}

.jd-filters {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 12px;
	margin-bottom: 20px;
	padding: 0 2px;
}

.jd-filters__cascader,
.jd-filters__select {
	min-width: 200px;
}

.jd-list-wrap {
	margin-top: 4px;
}

.jd-list-wrap .col {
	background: transparent;
	padding-left: 0;
	padding-right: 0;
}

.jd-pagination-wrap {
	margin-top: 28px;
}

.page_news_information--jd >>> .pagination {
	margin-bottom: 0;
}

.page_news_information--jd >>> .page-link {
	border-radius: 8px;
	margin: 0 4px;
	color: #666;
	border: 1px solid #e0e0e0;
	min-width: 40px;
	text-align: center;
}

.page_news_information--jd >>> .page-item.active .page-link {
	background-color: #e4393c !important;
	border-color: #e4393c !important;
	color: #fff !important;
}

.page_news_information--jd >>> .page-item .page-link:hover {
	color: #e4393c;
	border-color: #e4393c;
	background: #fff5f5;
}
</style>
