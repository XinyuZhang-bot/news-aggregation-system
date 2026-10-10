<template>
	<el-main class="bg table_wrap comtabel_t">
		<el-form label-position="right" :model="query" class="form p_4" label-width="120">
			<el-row class="rows row1">



							
									<el-col :xs="24" :sm="24" :lg="8" class="el_form_search_wrap" v-if="$check_field('get','users_mobile_phone') || $check_field('get','user_name')">
					<el-form-item label="昵称或手机号">
									<el-input v-model="query.nickname_or_phone" clearable placeholder="支持用户昵称、手机号（含账号表）"></el-input>
								</el-form-item>
				</el-col>
				</el-row>
	<el-row class="rows row2">

		<el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap search_btns">

				<el-col :xs="24" :sm="10" :lg="8" class="search_btn_1 search_btn_wrap_1 btns">

										<el-button type="primary" @click="search()" class="search_btn_find">查询</el-button>
						<el-button @click="reset()" style="margin-right: 74px;" class="search_btn_reset">重置</el-button>
																						
						<el-button v-if="$check_action('/ordinary_user/table','add') || $check_action('/ordinary_user/view','add')" @click="$router.push('./view?')">添加</el-button>

						

														<el-button v-if="$check_action('/ordinary_user/table','del') || $check_action('/ordinary_user/view','del')" class="search_btn_del" type="danger" @click="delInfo()">删除</el-button>
								
				</el-col>
		</el-col>
	</el-row >
	<div class="statistics-info" v-if="statisticsData.total > 0">
                  </div>

		</el-form>
				<el-table :data="list" @selection-change="selectionChange" @sort-change="$sortChange" style="width: 100%" id="dataTable" row-key="ordinary_user_id" :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
			:default-expand-all="isExpandAll" ref="tableRef">
					<el-table-column fixed type="selection" tooltip-effect="dark" width="55">
			</el-table-column>
			<el-table-column prop="user_id" label="用户ID" width="80">
			</el-table-column>
			<el-table-column prop="username" label="用户名" width="120">
			</el-table-column>
			<el-table-column prop="email" label="邮箱" min-width="240">
				<template slot-scope="scope">
					{{ formatEmail(scope.row["email"]) }}
				</template>
			</el-table-column>
				<el-table-column fixed prop="nickname" label="昵称" min-width="220">
					<template slot-scope="scope">
						<div class="nick_cell">
							<img v-if="scope.row.avatar" class="nick_avatar" :src="$fullUrl(scope.row.avatar)" alt="" />
							<div v-else class="nick_avatar nick_avatar_placeholder"></div>
							<div class="nick_text">{{ nicknameWithAccountStatus(scope.row) }}</div>
						</div>
					</template>
				</el-table-column>
		
					
					<el-table-column prop="users_mobile_phone" @sort-change="$sortChange" label="手机号" 				v-if="$check_field('get','users_mobile_phone')" min-width="300">
					<template slot-scope="scope">
							{{ formatPhone(scope.row["users_mobile_phone"]) }}
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







			<el-table-column fixed="right" label="操作" min-width="200" v-if="$check_action('/ordinary_user/table','set') || $check_action('/ordinary_user/view','set') || $check_action('/ordinary_user/view','get')
						" >


				<template slot-scope="scope">
					<div class="view_a">
					<router-link class="e-button el-button--small is-plain el-button--success" style="margin: 5px !important;"
					v-if="$check_action('/ordinary_user/table','set') || $check_action('/ordinary_user/view','set') || $check_action('/ordinary_user/view','get')"
						:to="'./view?user_id=' + scope.row['user_id']"

						 size="small">
						<span>详情</span>
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
																// 弹框
				showModal: false,
				// 获取数据地址
				url_get_list: "~/api/ordinary_user/get_list",
				url_del: "~/api/ordinary_user/del?",

				// 字段ID
				field: "ordinary_user_id",
									// 查询
				query: {
					"size":  15,
					"page": 1,
								"user_name": "",
											"nickname_or_phone": "",
								"login_time": "",
					"create_time": "",
					"orderby": `create_time desc`
				},

				// 数据
				list: [],
										message: '',
				// 控制展开状态
				isExpandAll: true,
				// 存储展开的行
				expandKeys: [],
				prevSelection: [],
			}
		},
		methods: {
				formatPhone(phone) {
					const value = String(phone || '').trim();
					if (!value || /^0+$/.test(value)) {
						return '该用户未填写手机号';
					}
					return value;
				},
				formatEmail(email) {
					const value = String(email || '').trim();
					if (!value) {
						return '该用户未填写邮箱';
					}
					return value;
				},
				formatAccountState(state) {
					const map = { 1: '可用', 2: '异常', 3: '已冻结', 4: '已注销' };
					if (state === undefined || state === null || state === '') {
						return '可用';
					}
					const s = Number(state);
					return Object.prototype.hasOwnProperty.call(map, s) ? map[s] : '未知';
				},
				nicknameWithAccountStatus(row) {
					const nick = String(row && row.nickname != null ? row.nickname : '').trim() || '—';
					const label = this.formatAccountState(row && row.user_account_state);
					return `${nick}（账号状态：${label}）`;
				},
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
			delInfo() {
			    var list = this.selection;
			    if (list.length === 0) {
			        this.$message({
			            type: 'info',
			            message: '选择对象不能为空!'
			        });
			        return;
			    }
			    this.$confirm('删除后数据将无法恢复，请确认是否删除？', '提示', {
			        confirmButtonText: '确定',
			        cancelButtonText: '取消',
			        type: 'warning'
			    }).then(async () => {
			        await this.delAll(list ,async (list)=>{
						var bl = true;
						for(var i=0; i < list.length; i++){
							var user_id = list[i].user_id;
							var res = await this.$get("~/api/user/del?",{user_id});
							if(res.result){
								console.log("删除成功" + i);
							}
							else{
								console.log("删除失败" + i);
								bl = false;
								break;
							}
						}
						if(bl){
							this.$message({
							    type: 'success',
							    message: '删除成功!'
							});
							this.get_list();
						}

					});
			    }).catch(() => {
			        this.$message({
			            type: 'info',
			            message: '已取消删除'
			        });
			    });
			},
			get_list_after(param){
				const rows = this.list || [];
				for (let i = 0; i < rows.length; i++) {
					const uid = rows[i].user_id;
					this.$get("~/api/user/get_obj?", { user_id: uid }, (json) => {
						if (!(json && json.result && json.result.obj)) return;
						const o = json.result.obj;
						const idx = rows.findIndex((r) => Number(r.user_id) === Number(uid));
						if (idx < 0) return;
						const row = rows[idx];
						this.$set(row, "username", o.username);
						this.$set(row, "nickname", o.nickname);
						this.$set(row, "avatar", o.avatar);
						this.$set(row, "email", o.email || "");
						this.$set(row, "users_mobile_phone", o.phone || "");
						this.$set(row, "user_account_state", o.state);
					});
				}
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

	.nick_cell{
		display:flex;
		align-items:center;
		gap:10px;
	}
	.nick_avatar{
		width:28px;
		height:28px;
		border-radius:50%;
		object-fit:cover;
		border:1px solid rgba(255,255,255,0.35);
		background: rgba(255,255,255,0.08);
	}
	.nick_avatar_placeholder{
		background: #cfd5dd;
		border: 1px solid rgba(0,0,0,0.08);
	}
	.nick_text{
		line-height: 1.2;
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
