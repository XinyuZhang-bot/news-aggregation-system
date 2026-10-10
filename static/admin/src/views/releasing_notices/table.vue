<template>
	<el-main class="bg table_wrap sides">
		<el-form label-position="right" :model="query" class="form p_4" label-width="120">
			<el-row class="rows row1">
				<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
					<el-form-item label="通知标题">
						<el-input v-model="query.title"></el-input>
					</el-form-item>
				</el-col>
			</el-row>
			<el-row class="rows row2">
				<el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap">
					<el-col :xs="24" :sm="12" :lg="12" class="search_btn_1">
							<el-button type="primary" @click="$router.push('./view')" class="search_btn_find">添加</el-button>
							<el-button type="primary" @click="search()" class="search_btn_find">查询</el-button>
							<el-button @click="reset()" class="search_btn_reset">重置</el-button>
							<el-button v-if="user_group == '管理员'" class="float-right search_btn_del" type="danger" @click="delInfo()">删除</el-button>
					</el-col>
					
				</el-col>

			</el-row>
		</el-form>

		<el-table border :data="list" @selection-change="selectionChange" @sort-change="$sortChange" style="width: 100%" stripe>
			<!-- 多选按钮 -->
			<el-table-column fixed type="selection" tooltip-effect="dark" width="55">
			</el-table-column>
			<!-- /多选按钮 -->
			<el-table-column label="通知标题" prop="title" width="150">
			</el-table-column>

			<el-table-column label="通知方式" prop="type" width="200">
			</el-table-column>
			<el-table-column label="通知内容" prop="content">
			</el-table-column>
			<el-table-column label="创建时间" prop="create_time" width="250">
				<template slot-scope="scope">
				  {{ $toTime(scope.row["create_time"], "yyyy-MM-dd hh:mm:ss") }}
				</template>
			</el-table-column>
			<el-table-column label="更新时间" prop="update_time" width="250">
				<template slot-scope="scope">
				  {{ $toTime(scope.row["update_time"], "yyyy-MM-dd hh:mm:ss") }}
				</template>
			</el-table-column>
		</el-table>

		<!-- 分页器 -->
		<div class="mt text_center">
			<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.page"
			 :page-sizes="[10, 15, 30, 50]" :page-size="query.size" layout="total, sizes, prev, pager, next, jumper" :total="count">
			</el-pagination>
		</div>
		<!-- /分页器 -->

	</el-main>
</template>

<script>
	import mixin from "@/mixins/page.js";

	export default {
		mixins: [mixin],
		data() {
			return {
				field: "notices_id",
				url_get_list: "~/api/releasing_notices/get_list",
				url_del: "~/api/releasing_notices/del?",

				query: {
					size: 15,
					page: 1,
					title: "",
				},

				// 数据
				list: [],

				// 获取用户信息
				list_user: [],
			}
		},
		methods: {
			table_class({row, column, rowIndex, columnIndex}){
				return "table_class";
			},
		 	export_db() {
				// 创建一个新的表格用于导出
				const exportTable = document.createElement('table');
				const thead = document.createElement('thead');
				const tbody = document.createElement('tbody');

				// 添加表头
				const headerRow = document.createElement('tr');
				const headers = ['角色', '账户', '操作模块', '操作时间'];
				headers.forEach(header => {
					const th = document.createElement('th');
					th.textContent = header;
					headerRow.appendChild(th);
				});
				thead.appendChild(headerRow);

				// 添加数据行
				this.list.forEach(item => {
					const row = document.createElement('tr');
					const cells = [
						item.user_group,
						item.user_name,
						item.routes,
						this.$toTime(item.create_time, "yyyy-MM-dd hh:mm:ss")
					];
					cells.forEach(cell => {
						const td = document.createElement('td');
						td.textContent = cell || '';
						row.appendChild(td);
					});
					tbody.appendChild(row);
				});

				exportTable.appendChild(thead);
				exportTable.appendChild(tbody);

				// 导出为Excel
				const uri = 'data:application/vnd.ms-excel;base64,';
				const template = '<html><head><meta charset="UTF-8"></head><body>{table}</body></html>';
				const base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) };
				const format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) };

				const ctx = {
					table: exportTable.outerHTML
				};
				const downloadLink = document.createElement('a');
				downloadLink.href = uri + base64(format(template, ctx));
				downloadLink.download = '操作日志.xls';
				document.body.appendChild(downloadLink);
				downloadLink.click();
				document.body.removeChild(downloadLink);
			}
		},
		created() {

		}
	}
</script>

<style>
	.float-right {
		float: right;
	}

	.mr-1 {
		margin-right: 1rem;
	}

	.el-table .table_class {
		background: rgba(150, 150, 150, 0.1);
		text-align: center;
	}
</style>


