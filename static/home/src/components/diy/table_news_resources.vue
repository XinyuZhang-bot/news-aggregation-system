<template>
  <el-main class="bg table_wrap">
    <el-form label-position="right" :model="query" class="form p_4" label-width="120">
      <el-row class="rows row1">

          
                                        </el-row>
      <el-row class="rows row2">
      	<el-col :xs="24" :sm="24" :lg="24" class="search_btn_wrap search_btns">
         <el-col :xs="24" :sm="10" :lg="8" class="search_btn_1 search_btn_wrap_1 btns">
                                                                    <el-button v-if="$check_action('/news_resources/table','add') || $check_action('/news_resources/view','add')" @click="$router.push('./view?')" class="add">添加</el-button>
            <el-button v-if="$check_action('/news_resources/table','del') || $check_action('/news_resources/view','del')" class="search_btn_del" type="danger" @click="delInfo()">删除</el-button>
                        </el-col>
       
        </el-col>
      </el-row>
    </el-form>
	    <el-table :data="list" @selection-change="selectionChange" @sort-change="$sortChange" style="width: 100%" id="dataTable" row-key="news_resources_id" :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
			:default-expand-all="isExpandAll" ref="tableRef">
	                <el-table-column fixed type="selection" tooltip-effect="dark" width="55">
            </el-table-column>
                                                  <el-table-column prop="title" @sort-change="$sortChange" label="标题"                                v-if="$check_field('get','title')" min-width="200">
                  {
                    <template slot-scope="scope">
                                          {{ scope.row['title'] }}
                                                            </template>
                  }
                                </el-table-column>
                                              <el-table-column prop="url" @sort-change="$sortChange" label="详情链接"                                v-if="$check_field('get','url')" min-width="200">
                                      <template slot-scope="scope">
                      <a :href="scope.row['url']" target="_blank">{{ scope.row['url'] }}</a>
                    </template>
                                </el-table-column>
                                              <el-table-column prop="origin" @sort-change="$sortChange" label="发布来源"                                v-if="$check_field('get','origin')" min-width="200">
                  {
                    <template slot-scope="scope">
                                          {{ scope.row['origin'] }}
                                                            </template>
                  }
                                </el-table-column>
                                              <el-table-column prop="release_time" @sort-change="$sortChange" label="发布时间"                                v-if="$check_field('get','release_time')" min-width="200">
                  {
                    <template slot-scope="scope">
                                          {{ scope.row['release_time'] }}
                                                            </template>
                  }
                                </el-table-column>
                                              <el-table-column prop="content" @sort-change="$sortChange" label="正文内容"                                v-if="$check_field('get','content')" min-width="200">
                  {
                    <template slot-scope="scope">
                                          {{ scope.row['content'] }}
                                                            </template>
                  }
                                </el-table-column>
                                              <el-table-column prop="comment_num" @sort-change="$sortChange" label="评论数量"                                v-if="$check_field('get','comment_num')" min-width="200">
                  {
                    <template slot-scope="scope">
                                          {{ scope.row['comment_num'] }}
                                                            </template>
                  }
                                </el-table-column>
                                              <el-table-column prop="comment" @sort-change="$sortChange" label="最新评论"                                v-if="$check_field('get','comment')" min-width="200">
                  {
                    <template slot-scope="scope">
                                          {{ scope.row['comment'] }}
                                                            </template>
                  }
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

        
        
        
        
                        <el-table-column fixed="right" label="操作" min-width="120" v-if="$check_action('/news_resources/table','set') || $check_action('/news_resources/view','set') || $check_action('/news_resources/view','get')
					 ">
        

      <template slot-scope="scope">
        <router-link class="el-button el-button--small is-plain el-button--success" style="margin: 5px !important;"
                     v-if="$check_action('/news_resources/table','set') || $check_action('/news_resources/view','set') || $check_action('/news_resources/view','get')"
                                 :to="'./view?' + field + '=' + scope.row[field]"
                                 size="small">
          <span>详情</span>
        </router-link>
                                        		  		                    </template>
    </el-table-column>

    </el-table>
									    <!-- 分页器 -->
    <div class="mt text_center">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                     :current-page="query.page" :page-sizes="[7, 10, 30, 100]" :page-size="query.size"
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
									        // 弹框
        showModal: false,
        // 获取数据地址
        url_get_list: "~/api/news_resources/get_list",
        url_del: "~/api/news_resources/del?",

        // 字段ID
        field: "news_resources_id",
					        // 查询
        query: {
          "size":  7,
          "page": 1,
                                                                                                                                                                                                                                                                                                                            "login_time": "",
          "create_time": "",
					"orderby": `news_resources_id desc`
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
              type: 'warning',
              cancelButtonClass: "custom-cancel-btn"
            }).then(async () => {
                      await this.delAll(list);
                    }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消删除'
              });
            });
          },
		      deleteRow(index, rows) {
        rows.splice(index, 1);
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
.el-message-box__btns .custom-cancel-btn{
  color: #606266;
}
</style>
