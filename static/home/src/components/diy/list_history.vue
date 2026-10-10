<!--增加前台用户的浏览记录开始 -->
<!--浏览记录列表页 -->
<template>
  <div class="page_history" id="history_list">
    <el-row>
      <el-col :span="24">
        <div class="history_list_title">
          <span class="title">浏览记录</span>
          <el-tabs type="border-card">
            <el-tab-pane v-for="(item,index) in list" :key="index" :label="item.type">
              <div class="history_card">
                <el-empty style="width: 100%" v-if="item.data.length === 0" :image-size="80" description="暂无数据" />
                <div v-else class="history_item" v-for="h in item.data" :key="h.history_id" @click="toPage(h)">
                  <el-image style="width: 100%;background-color:#d7d7d7;max-height: 250px;" :src="$fullUrl(h.img)" alt="">
                    <template #error>
                      <div class="image-slot">
                        <el-empty :image-size="80" description="暂无图片" />
                      </div>
                    </template>
                  </el-image>
                  <div class="history_content">
                    <div class="history_content_title">
                      <span>{{ h.title }}</span>
                      <i class="el-icon-delete" style="color: #dc112a;cursor: pointer;" @click.stop="delHistory(h)"></i>
                    </div>
                    <div class="history_content_time">{{ $toTime( h.update_time,"yyyy-MM-dd hh:mm:ss") }}</div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { historyList } from "@/router/historyList.js";
export default {
  data() {
    return {
      list: [],
      query: {}
    };
  },
  mounted() {
    this.query.user_id = this.$store.state.user.user_id
    this.get_tpl_list();
  },
  methods: {
    get_tpl_list() {
      this.$get('~/api/history/get_list',this.query,(res) => {
        if(res.result){
          this.list = JSON.parse(JSON.stringify(historyList))
          // list.value 根据type去重
          this.list = this.list.filter((item, index, self) => {
            return self.findIndex((t) => t.type === item.type) === index;
          });
          this.list.forEach((item, index) => {
            item.data = []
            // 遍历list，将type相同的放到一个数组中，赋值给ite
            res.result.list.forEach((item2, index2) => {
              if (item.type == item2.type) {
                item.data.push(item2)
              }
            });
          })
          this.list = this.list.filter((item) => item.data.length > 0)
        }
      })
    },
    delHistory(h) {
      this.$get(`~/api/history/del?history_id=${h.history_id}`).then((res) => {
        if (res.result) {
          this.$message({
	          type: "success",
	          message: "删除成功!"
	        });
          this.get_tpl_list();
        }
      })
    },
    toPage(h) {
      if(h.path == 'audio') return
      const specialList = ['/novel_chapters/read','/movie_episode/playvideo']
      if(h.path.indexOf('?') == -1){
        this.$router.push({
          path: h.path
        });
      }else{
        let pathArr = h.path.split('?')
        let path = pathArr[0]
        // 处理多个查询参数
        let query = {}
        let queryString = pathArr[1]
        let queryPairs = queryString.split('&')
        queryPairs.forEach(pair => {
          let [key, value] = pair.split('=')
          query[key] = value
        })
        if(specialList.indexOf(path)!= -1){
          let params = JSON.parse(h.params)
          query.currentChapterIndex = params.currentChapterIndex
        }
        this.$router.push({
          path,
          query
        });
      }
    }
  },
  components: {},
};
</script>

<style scoped lang="less">
.page_history {
  width: 90%;
  margin: 1% auto;
  .bar_filter {
    display: flex;
    align-items: center;
  }
  .arrow-up,
  .arrow-down {
    position: absolute;
    left: 50%;
    margin-left: -5px;
  }

  .arrow-up {
    top: -10px; /* 向上的位置 */
  }

  .arrow-down {
    bottom: -10px; /* 向下的位置 */
  }
  .history_list_title {
    margin: 0.5rem 0;
    text-align: center;
  }
  .title {
    font-size: 1.5rem;
    font-weight: bold;
    padding-left: 1rem;
  }
  .search_box {
    width: 100%;
    text-align: center;
    margin-top: 1rem;
  }

  .flex_cc {
    margin-top: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  // 排行榜
  .list_rank {
  }
  .list_rank_item {
    margin: 0 1rem;
    margin-bottom: 1rem;
    padding: 1rem;
    border: 1px solid var(--primary_color);
  }

  // [class*="list_rank_"] {
  //   padding: 0.5rem;
  // }
  .history_list h4 {
    font-size: 20px;
  }

  .history_list {
    padding-left: 1px;
  }

  .container {
    min-height: 800px;
  }

  .list_hot h4 {
    font-size: 20px;
  }

  .filter_block {
    margin: 1rem 0.5rem 0.5rem 0.5rem;
    display: flex;
    flex-direction: row;
    justify-content: start;
  }

  .bar_filter {
    display: flex;
    align-items: center;
  }

  li {
    list-style: none;
  }

  .bar_sort {
    margin-left: 5px;
  }
  .history_card {
    display: flex;
    flex-wrap: wrap;
  }
  .history_item {
    width: 23%;
    border: 1px solid #ccc;
    padding: 0.5rem;
    margin: 0.5rem;
  }
  .history_content {
    font-size: 14px;
    text-align: left;
  }
  .history_content_title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0.5rem 0;
  }
  .history_content_time {
    font-size: 12px;
    color: #999;
    margin-bottom: 0.5rem;
  }
}
</style>
<!--增加前台用户的浏览记录结束 -->