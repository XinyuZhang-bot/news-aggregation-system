<template>
	<div class="page_root dash-home dash-home--minimal" id="root_index">
		<div class="warp">
			<div class="container-fluid">
				<el-row>
				</el-row>

				<el-row>
					<el-col :class="'home_user'" :span="8">
						<div class="card info">
							<div class="UserInfo">
								<el-row class="UserInfo-row" style="padding: 0 10px;">
								<el-col :span="8"
									><img :src="$fullUrl(user.avatar)" alt=""
								/></el-col>
								<el-col :span="12">
									<p>用户昵称：{{ user.nickname || user.username }}</p>
									<p>用户身份：{{ user_group }}</p>
								</el-col>
								</el-row>
								<div class="UserInfo-btn" style="padding: 0 10px;">
								<el-button @click="$router.push('/user/info')"
									>修改资料</el-button
								>
								<el-button @click="$router.push('/user/password')"
									>修改密码</el-button
								>
								<el-button @click="sign_out_fun">退出</el-button>
								</div>
								<p class="logotime">
								登录时间：{{
									$toTime(user.login_time, "yyyy-MM-dd hh:mm:ss")
								}}
								</p>
							</div>
						</div>
          			</el-col>
					<el-col :class="'home_overview'" v-if="user_group == '管理员'" :span="8">
						<div class="statistics card">
							<el-row>
								<el-col :span="4" v-for="(item, index) in dataScreen" :key="index">
									<div class="sumList">
										<p>{{ item.value }}</p>
										<p>{{ item.label }}</p>
										<p><i class="el-icon-position"></i></p>
									</div>
								</el-col>
							</el-row>
						</div>
					</el-col>
        		</el-row>
        		<el-row>
					<quickMenu />
        		</el-row>

				<template v-if="user_group == '管理员'">
					<el-row :gutter="8" class="dash-row">
						<el-col :xs="24" :sm="12" :lg="8">
							<div class="card chart">
								<newLineChart2
									v-if="chartUserMonthly.values.length > 0"
									class="chartsHeiht"
									:color="['#5b8ff9']"
									idName="dash_user_monthly"
									:timeout="0"
									title="用户数量月度趋势（按月注册）"
									:vm="chartUserMonthly"
								/>
								<div v-else class="chart-empty">暂无用户注册趋势数据</div>
							</div>
						</el-col>
						<el-col :xs="24" :sm="12" :lg="8">
							<div class="card chart">
								<doughnutChart
									v-if="listUserStatusRing.length"
									id="dash_user_status_ring"
									:list="listUserStatusRing"
									title="用户正常/禁用状态"
									type="用户状态"
								/>
								<div v-else class="chart-empty">暂无用户状态数据</div>
							</div>
						</el-col>
						<el-col :xs="24" :sm="12" :lg="8">
							<div class="card chart">
								<newBarChart2
									v-if="vmNewsCategory.values.length > 0"
									idName="dash_news_category_bar"
									title="各新闻分类数量"
									:vm="vmNewsCategory"
								/>
								<div v-else class="chart-empty">暂无新闻分类数据</div>
							</div>
						</el-col>
					</el-row>
					<el-row :gutter="8" class="dash-row">
						<el-col :xs="24" :sm="12" :lg="8">
							<div class="card chart">
								<doughnutChart
									v-if="listNewsOriginPie.length"
									id="dash_news_origin_pie"
									:list="listNewsOriginPie"
									title="各新闻来源占比"
									type="新闻来源"
								/>
								<div v-else class="chart-empty">暂无新闻来源数据</div>
							</div>
						</el-col>
						<el-col :xs="24" :sm="12" :lg="8">
							<div class="card chart">
								<newLineChart2
									v-if="chartCrawlDaily.values.length > 0"
									class="chartsHeiht"
									:color="['#61d9a8']"
									idName="dash_crawl_daily"
									:timeout="0"
									title="爬取新闻趋势"
									:vm="chartCrawlDaily"
								/>
								<div v-else class="chart-empty">暂无爬取趋势数据</div>
							</div>
						</el-col>
						<el-col :xs="24" :sm="12" :lg="8">
							<div class="card chart">
								<newBarChart2
									v-if="vmReadPref.values.length > 0"
									idName="dash_read_pref_bar"
									title="用户阅读偏好分类统计（点击行为）"
									:vm="vmReadPref"
								/>
								<div v-else class="chart-empty">暂无阅读偏好数据</div>
							</div>
						</el-col>
					</el-row>
					<el-row :gutter="8" class="dash-row">
						<el-col :span="24">
							<div class="card chart chart-wide">
								<stackedHorizontalBarChart2
									v-if="vmHotNews.values.length > 0"
									idName="dash_hot_news_rank"
									title="新闻热门浏览排行"
									:vm="vmHotNews"
								/>
								<div v-else class="chart-empty">暂无浏览排行数据</div>
							</div>
						</el-col>
					</el-row>
					<el-row :gutter="8" class="dash-row">
						<el-col :xs="24" :sm="12" :lg="12">
							<div class="card chart">
								<newLineChart2
									v-if="chartReadDaily.values.length > 0"
									class="chartsHeiht"
									:color="['#f6bd16']"
									idName="dash_read_daily"
									:timeout="0"
									title="每日阅读趋势"
									:vm="chartReadDaily"
								/>
								<div v-else class="chart-empty">暂无阅读趋势数据</div>
							</div>
						</el-col>
						<el-col :xs="24" :sm="12" :lg="12">
							<div class="card insight-card">
								<div class="insight-title">趋势亮点与抓取概况</div>
								<p class="insight-line">
									近 7 天增长最快分类：
									<strong>{{ trendHighlights.growing_category.category || "暂无" }}</strong>
									<span v-if="trendHighlights.growing_category.growth > 0">
										（+{{ trendHighlights.growing_category.growth }}）
									</span>
								</p>
								<p class="insight-line">
									近 7 天增长最快新闻：
									<strong>{{ trendHighlights.growing_article.title || "暂无" }}</strong>
								</p>
								<p class="insight-line">
									自 5 月 1 日起抓取运行：成功 {{ crawlRunSummary.success }} 次，失败 {{ crawlRunSummary.failed }} 次，运行中 {{ crawlRunSummary.running }} 次
								</p>
							</div>
						</el-col>
					</el-row>
				</template>

			</div>
		</div>
	</div>
</template>
<script>
	import mixin from "@/mixins/page.js";
	import newLineChart2 from "@/components/charts/new_line_chart2";
	import quickMenu from "@/components/diy/quick_menu.vue";
	import newBarChart2 from "@/components/charts/new_bar_chart2";
	import doughnutChart from "@/components/charts/doughnut_chart";
	import stackedHorizontalBarChart2 from "@/components/charts/stacked_horizontal_bar_chart2";
	export default {
		mixins: [mixin],
		name: "Home",
		components: {
			newLineChart2,
			quickMenu,
			newBarChart2,
			doughnutChart,
			stackedHorizontalBarChart2
		},
		data() {
			return {
				activeName: "third",
				url_user_count: "~/api/user/count?",
				url_article_hits: "~/api/article/sum?field=hits",
				dataScreen: null,
				sumList: [
					{
						label: "用户总数",
						value: "111",
						icon: "Position",
						field: "user",
					},
					{
						label: "正常账号",
						value: "111",
						icon: "Position",
						field: "normal_user",
					},
					{
						label: "异常账号",
						value: "111",
						icon: "Position",
						field: "freeze_user",
					},
					{
						label: "管理员",
						value: "111",
						icon: "Position",
						field: "admin_user",
					},
								{
						label: "普通用户",
						value: "111",
						icon: "Position",
						field: "ordinary_user",
					},
										{
						label: "编辑人员",
						value: "111",
						icon: "Position",
						field: "compileors",
					},
																					{
						label: "访问总数",
						value: "111",
						icon: "Position",
						field: "hits",
					},
					{
						label: "轮播图数",
						value: "111",
						icon: "Position",
						field: "slides",
					},
										{
						label: "收藏数",
						value: "111",
						icon: "Position",
						field: "collect",
					},
															{
						label: "评论数",
						value: "111",
						icon: "Position",
						field: "comment",
					},
															{
						label: "点赞数",
						value: "111",
						icon: "Position",
						field: "praise",
					},
															{
						label: "公告数",
						value: "111",
						icon: "Position",
						field: "notice",
					},
													],
				chartUserMonthly: {
					type: "usersSums",
					names: ["新增用户"],
					xAxis: [],
					values: [],
					month: [],
					loading: false,
					total: 0,
				},
				listUserStatusRing: [],
				vmNewsCategory: { xAxis: [], values: [] },
				listNewsOriginPie: [],
				chartCrawlDaily: {
					names: ["爬取条数"],
					xAxis: [],
					values: [],
				},
				chartReadDaily: {
					names: ["阅读次数"],
					xAxis: [],
					values: [],
				},
				vmReadPref: { xAxis: [], values: [] },
				vmHotNews: { names: ["浏览量"], xAxis: [], values: [] },
				trendHighlights: {
					growing_category: {},
					growing_article: {},
				},
				crawlRunSummary: {
					success: 0,
					failed: 0,
					running: 0,
				},
		  				  				  				  				  							};
		},
		created() {
			if (this.user_group === "管理员") {
				this.load_admin_dashboard();
			}
			this.get_list_count();
							},
		methods: {
			load_admin_dashboard() {
				this.$get("~/api/user/admin_dashboard", {}, (json) => {
					if (!json || !json.result) {
						return;
					}
					const d = json.result;
					this.chartUserMonthly.xAxis = d.user_monthly.xAxis || [];
					this.chartUserMonthly.values = d.user_monthly.values || [];
					this.listUserStatusRing = d.user_status_ring || [];
					this.vmNewsCategory = {
						xAxis: d.news_category_bar.xAxis || [],
						values: d.news_category_bar.values || [],
					};
					this.listNewsOriginPie = d.news_origin_pie || [];
					this.chartCrawlDaily.xAxis = d.crawl_daily.xAxis || [];
					this.chartCrawlDaily.values = d.crawl_daily.values || [];
					this.chartReadDaily.xAxis = (d.read_daily && d.read_daily.xAxis) || [];
					this.chartReadDaily.values = (d.read_daily && d.read_daily.values) || [];
					this.vmReadPref = {
						xAxis: d.read_pref_bar.xAxis || [],
						values: d.read_pref_bar.values || [],
					};
					const maxRank = 10;
					const rawX = d.hot_news_rank.xAxis || [];
					const rawV = d.hot_news_rank.values || [];
					const n = Math.min(maxRank, rawX.length, rawV.length);
					const hx = rawX.slice(0, n).slice().reverse();
					const hv = rawV.slice(0, n).slice().reverse();
					this.vmHotNews = {
						names: ["浏览量"],
						xAxis: hx,
						values: hv,
					};
					this.trendHighlights = d.trend_highlights || {
						growing_category: {},
						growing_article: {},
					};
					this.crawlRunSummary = d.crawl_run_summary || {
						success: 0,
						failed: 0,
						running: 0,
					};
				});
			},
			// 数据预览模块
			get_list_count() {
				this.dataScreen = [...this.sumList, ...this.auth()];
				for (let i = 0; i < this.dataScreen.length; i++) {
					let url;
					let obj = this.dataScreen[i];
					if (
						obj.field != "normal_user" &&
						obj.field !== "freeze_user" &&
						obj.field !== "admin_user"
					) {
						url = `~/api/${obj.field}/count`;
						this.$get(url).then((json) => {
							if (json.result !== null) {
								obj.value = json.result;
							}
						});
					} else {
						// 正常账户，冻结账户数据获取
						let data = {};
						url = `~/api/user/count`;
						if (obj.field === "normal_user") {
							data = {
								state: 1,
							};
						} else if (obj.field === "freeze_user") {
							data = {
								state: 2,
							};
						} else {
							data = {
								user_group: "管理员",
							};
						}
						this.$get(url, data).then((json) => {
							if (json.result !== null) {
								obj.value = json.result;
							}
						});
					}
				}
			},
			sign_out_fun() {
				this.$get("~/api/user/quit", {}, (res) => {
					this.$store.commit("quit");
					this.$router.push("/login");
				});
			},
			auth() {
				// 从localStorage获取并解析权限数据
				let tables = this.$store.state.web.auth;
				let lt = [];
				let site_list = [];
				let IconArr = [
					"Edit",
					"Document",
					"Menu",
					"Location",
					"Setting",
					"Search",
				];
																																																					
				// 初始化表格列表并添加额外项
				let list = [
											"article",
					"article_type",
					"comment",
														"notice",
																];
															list.push("ordinary_user");
																list.push("compileors");
																																// 处理表格权限数据
				for (let i = 0; i < tables.length; i++) {
					let o = tables[i];
					if (o.path && o.path.indexOf("/table") !== -1) {
						// 添加path存在性检查
						if (list.indexOf(o.table_name) === -1) {
							o.has_add = site_list.indexOf(o.table_name) === -1;
							o.Icon = IconArr[parseInt(Math.random() * IconArr.length)];
							lt.push({
								label: o.mod_name,
								value: "111",
								icon: o.Icon,
								field: o.table_name,
							});
						}
					}
				}
				return lt; // 返回处理后的权限列表
			},
			  		  		  		  		  				},
		computed:{
			recognitionHeight(){
				return "830px"
			},
			recognitionUrl(){
				return "https://www.faceplusplus.com.cn/${model.filter.recognitionType}/"
			}
		}
	};
</script>

<style scoped="scoped">
	/* 后台首页：浅色卡片，保证统计与图表文字对比度 */
	.dash-home--minimal .card {
		border: 1px solid #e5e7eb !important;
		box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06) !important;
		background: #ffffff !important;
		color: #111827;
	}

	.dash-home--minimal .chart {
		padding: 1rem 1.1rem 1.25rem;
	}

	.dash-home--minimal .UserInfo p {
		color: #374151;
	}

	.dash-home--minimal .statistics {
		background: transparent;
		border: none;
	}

	.dash-home--minimal .statistics .sumList {
		border: 1px solid #e5e7eb;
		background: #f9fafb;
		color: #111827;
		border-radius: 10px;
		padding: 8px 6px;
		box-shadow: none;
	}

	.dash-home--minimal .statistics .sumList > p:nth-child(2) {
		color: #6b7280;
		font-size: 11px;
	}

	.dash-home--minimal .UserInfo .logotime {
		border-top-color: #e5e7eb;
		color: #6b7280;
	}

	.chart {
		display: block;
		width: 100%;
		height: 400px;
		padding: 1rem;
		position: relative;
	}

	.chart-wide {
		height: 460px;
	}

	.chart-empty {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 360px;
		color: #909399;
		font-size: 14px;
	}

	.dash-row {
		margin-bottom: 0.5rem;
	}

	.el-col {
		padding: 0.5rem;
	}

	.card {
		overflow: hidden;
	}

	.insight-card {
		height: 400px;
		padding: 20px 24px;
		color: #374151;
	}

	.insight-title {
		font-size: 18px;
		font-weight: 600;
		margin-bottom: 18px;
		color: #111827;
	}

	.insight-line {
		line-height: 1.9;
		margin-bottom: 12px;
		color: #4b5563;
	}

	.iframe_box ,.iframe_box_change{
		width: 100%;
		height: 1180px;
		position: relative;
		margin-top: 25px;
	}
	.iframe_box_change{
		height: 580px;
		padding-top: 50px;
	}
	.iframe_box	.iframe_box_content, .iframe_box_change .iframe_box_content{
		width: 100%;
		height: 100%;
	}
	.iframe_box_top{
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100px;
		font-size: 25px;
		line-height: 100px;
		background: #fff;
		z-index: 999;
		padding-left: 50px;
	}
	#iframe_box_face div::before {
		content: '';
		width: 100px;
		position: absolute;
		top: 154px;
		right: 129px;
		z-index: 999;
		height: 20px;
		background-color: #FFFFFF;
	}

	#iframe_box_face>h1 {
		margin-top: 100px;
		margin-bottom: 20px;
	}
	.UserInfo p {
		line-height: 30px;
	}

	.UserInfo img {
		width: 100px;
		height: 100px;
	}

	.UserInfo .logotime {
		text-align: center;
		font-size: 14px;
		line-height: 30px;
		border-top: 1px #d9d9d9 solid;
		margin: 10px 0;
	}

	.statistics {
		width: 100%;
		height: 240px;
		overflow-y: auto;
		background-color: #fff;
	}

	.statistics .sumList {
		text-align: center;
		font-size: 12px;
		color: gray;
		border-radius: 8px;
		padding: 5px;
		border: 1px solid gainsboro;
	}
	.home_user .card {
		min-height: 240px;
	}
	.progress-item {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 20px;
  }

  .progress-item .progress-item-content {
    width: 65%;
    display: flex;
    flex-direction: column;
    height: 80px;
    margin-left: 10px;
    font-size: 14px;
  }

  .progress-item .progress-item-content > p {
    margin-bottom: 5px;
  }

  .progress-item .progress-item-content .progress-item-content-progress {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: auto;
  }
</style>
