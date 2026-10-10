<template>
  <div class="page_search search_details">
    <div class="warp search_warp">
      <div class="container">
        <div class="row  row_search">
          <div class="col-12">
            <div class="card_result_search">
              <div class="iou">
                <div class="title">搜索结果</div>

                  <!-- 搜索栏 -->
                  <div class="search_box">
                    <b-form-input
                      size="sm"
                      class="mr-sm-2"
                      :placeholder="'继续搜索'+query.search_title"
                      v-model.trim="search_val"
                      @keyup.enter="submit_search"
                    ></b-form-input>
                    <b-button size="sm" @click="submit_search"
                      ><b-icon icon="search"></b-icon
                    ></b-button>
                  </div>
              </div>
              
              <list_result_search
                :list="list_result"
                :title="this.query.source_title"
                :source_table="this.query.search_type"
                :keyword="query.word"
              ></list_result_search>
              <div class="pager">
                <b-pagination
                  v-model="page_result"
                  :total-rows="count"
                  :per-page="size"
                  @change="jumpTo"
                ></b-pagination>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import mixin from "@/mixins/page.js";
import list_result_search from "@/components/diy/list_result_search.vue";

export default {
  mixins: [mixin],
  data() {
    return {
      query: {
        word: "",
        search_key: "",
        search_type: "",
        search_title: "",
        multi_field: false,
      },
      search_val: "",
      list_result: [],
      page_result: 1,
      size: 100,
      count: 0,
    };
  },
  methods: {
    /**
     *  获得结果
     * */
    get_result(page_result = 1) {
      if (word == "") {
        return;
      }
      var params = {};
      var { word, search_key, search_type, multi_field } = this.query;
      if (search_type === "goods" && multi_field) {
        params.page = page_result;
        params.size = this.size;
        this.$get("~/api/" + search_type + "/get_list", params, (res) => {
          if (res.result) {
            var allList = res.result.list || [];
            // 在前端进行多字段过滤
            var filteredList = this.filterGoodsByMultipleFields(allList, word);

            // 处理结果显示
            var processedList = this.processGoodsSearchResult(filteredList, word);
            this.list_result = processedList;
            this.count = filteredList.length;
          }
        });
      }else{
        params[search_key] = word;
        params.page = page_result;
        params.size = this.size;
        this.$get("~/api/" + search_type + "/get_list", params, (res) => {
          if (res.result) {
            var list_result = res.result.list || [];
            list_result.map((o) => {
              var title = o[search_key];
              o.title =title;
            });
            this.list_result = list_result
            this.count = res.result.count;
          }
        });
      }
    },
    filterGoodsByMultipleFields(list, keyword) {
      if (!keyword) return list;

      return list.filter(item => {
        // 搜索title
        if (item.title && item.title.toLowerCase().includes(keyword.toLowerCase())) {
          return true;
        }

        // 搜索description
        if (item.description && item.description.toLowerCase().includes(keyword.toLowerCase())) {
          return true;
        }

        // 搜索customize_field
        if (item.customize_field) {
          try {
            const customFields = JSON.parse(item.customize_field);
            const hasMatch = customFields.some(field =>
              field.field_value && field.field_value.toString().toLowerCase().includes(keyword.toLowerCase())
            );
            if (hasMatch) {
              return true;
            }
          } catch (e) {
            console.error("解析customize_field失败:", e);
          }
        }

        return false;
      });
    },

    /**
     * 处理商品搜索结果，标记匹配字段
     */
    processGoodsSearchResult(list, keyword) {
      return list.map((item) => {
        let matchedFields = [];

        // 检查各个字段是否匹配
        if (item.title && item.title.toLowerCase().includes(keyword.toLowerCase())) {
          matchedFields.push({
            field: "标题",
            value: item.title,
            matched: true
          });
        }
        if (item.description && item.description.toLowerCase().includes(keyword.toLowerCase())) {
          matchedFields.push({
            field: "描述",
            value: item.description,
            matched: true
          });
        }
        if (item.customize_field) {
          try {
            const customFields = JSON.parse(item.customize_field);
            customFields.forEach(fieldObj => {
              if (fieldObj.field_value && fieldObj.field_value.toString().toLowerCase().includes(keyword.toLowerCase())) {
                matchedFields.push({
                  field: fieldObj.field_name || "自定义字段",
                  value: fieldObj.field_value.toString(),
                  matched: true
                });
              }
            });
          } catch (e) {
            console.error("解析customize_field失败:", e);
          }
        }

        // 构建显示信息
        item.title = item.title || "无标题";
        item.matched_fields = matchedFields;
        item.display_title = `${item.title}`;

        return item;
      });
    },
    /**
     *  跳转
     * */
    jumpTo(page_result) {
      this.get_result(page_result);
    },

    /**
     *  搜索
     * */
    submit_search() {
      this.$router.replace({
        path: "/search/details",
        query: {
          word: this.search_val,
          search_key: this.query.search_key,
          search_type: this.query.search_type,
          search_title: this.query.search_title,
          multi_field: this.query.multi_field
        }
      });
    },
    /**
     *  获取地址栏参数
     * */
    getQueryParams(){
      for (const key in this.query) {
        this.query[key] = this.$route.query[key]
      }
    }
  },
  components: { list_result_search },
  mounted() {
    this.getQueryParams();
    this.get_result();
  },
};
</script>

<style scoped>
.card_search {
  text-align: center;
}
.card_result_search > .title {
  text-align: center;
  padding: 10px 0;
}
.pager {
  display: flex;
  justify-content: center;
}
.search_box {
  display: flex;
  margin-bottom: 1rem;
}
</style>
