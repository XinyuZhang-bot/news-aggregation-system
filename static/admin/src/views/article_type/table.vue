<template>
	<el-main class="bg table_wrap aricle_tyoe">
		<el-form label-position="right" :model="query" class="form p_4" label-width="120">
			<el-row class="rows row1">
				<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap">
					<el-form-item label="类型名称">
						<el-input v-model="query.name"></el-input>
					</el-form-item>
				</el-col>
			</el-row>
			<el-row class="rows row2">
				<el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap">
					<el-col :xs="24" :sm="12" :lg="12" class="search_btn_1 btns">

						<el-button type="primary" @click="search()" class="search_btn_find">查询</el-button>
						<el-button @click="reset()" class="search_btn_reset">重置</el-button>
						<el-button v-if="$check_action('/article_type/table', 'del')" class="float-right search_btn_del"
							type="danger" @click="delInfo()">删除</el-button>

						<el-button v-if="$check_action('/article_type/view')" class="float-right  search_btn_add"
							@click="$router.push('./view?')">添加</el-button>
					</el-col>

				</el-col>
			</el-row>
		</el-form>
		<el-table border :data="list" @selection-change="selectionChange" @sort-change="$sortChange" style="width: 100%"
			stripe>

			<el-table-column fixed type="selection" tooltip-effect="dark" width="50">
			</el-table-column>

			<el-table-column fixed prop="name" label="类型名称" min-width="120">
			</el-table-column>

			<!--<el-table-column prop="description" label="描述" min-width="180">
			</el-table-column>

			<el-table-column prop="url" label="外链地址" min-width="180">
			</el-table-column>-->

			<el-table-column sortable prop="create_time" label="创建时间" min-width="200">
				<template slot-scope="scope">
					{{ $toTime(scope.row["create_time"], "yyyy-MM-dd hh:mm:ss") }}
				</template>
			</el-table-column>

			<el-table-column sortable prop="update_time" label="更新时间" min-width="200">
				<template slot-scope="scope">
					{{ $toTime(scope.row["update_time"], "yyyy-MM-dd hh:mm:ss") }}
				</template>
			</el-table-column>

			<!-- 操作 -->
			<el-table-column fixed="right" label="操作" width="200">
				<template slot-scope="scope">
					<div class="view_a">
						<router-link class="e-button el-button--small is-plain el-button--primary"
							:to="'./view?' + field + '=' + scope.row[field]" size="small">
							<span>详情</span>
						</router-link>
					</div>
				</template>
			</el-table-column>
			<!-- /操作 -->

		</el-table>

		<!-- 分页器 -->
		<div class="mt text_center">
			<el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
				:current-page="query.page" :page-sizes="[10, 15, 30, 50]" :page-size="query.size"
				layout="total, sizes, prev, pager, next, jumper" :total="count">
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
			// 获取数据地址
			url_get_list: "~/api/article_type/get_list",
			url_del: "~/api/article_type/del?",

			// 字段ID
			field: "type_id",

			// 查询
			query: {
				size: 15,
				page: 1,
				name: "",
			},

			// 数据
			list: [],

			list_is: [{ name: "否", value: 0 }, { name: "是", value: 1 }]

		}
	},
	methods: {
		deleteRow(index, rows) {
			rows.splice(index, 1);
		},
		table_class({ row, column, rowIndex, columnIndex }) {
			return "table_class";
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
			// 检查是否有文章关联
			for (let i = 0; i < list.length; i++) {
				let type = list[i];
				let res = await this.$get("~/api/article/get_list?", {
					type: type.name
				});

				if (res.result && res.result.list && res.result.list.length > 0) {
					this.$message({
						type: 'error',
						message: `类型"${type.name}"下有关联的内容，无法删除！`
					});
					return;
				}
			}

			this.$confirm('此操作将永久删除该分类, 是否继续?', '提示', {
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
		}
	},
	created() {
	}
}
</script>

<style type="text/css"></style>
