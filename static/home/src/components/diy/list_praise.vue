<template>
  <div class="list_collect">
    <div class="item_collect" v-for="(o, i) in list" :key="i">
      <router-link
        class="collect_box"
        :to="
          '/' +
          o[vm.source_table] +
          '/details?' +
          o[vm.source_field] +
          '=' +
          o[vm.source_id]
        "
      >
        <div class="left_block">
          <img
            style="width: 3rem; height: 3rem"
            :src="o[vm.img] ? $fullUrl(o[vm.img]) : '../../../public/img/default.png'"
          />
        </div>
        <div class="right_block">
          <div class="top_comment">
            <div class="title">
              {{ o[vm.title] }}
            </div>
            <div class="time">
              {{ o[vm.create_time] | formatDate}}
            </div>
          </div>
        </div>
      </router-link>
      <b-icon class="btn_delete" icon="trash" @click="del_praise(o, i)"></b-icon>
    </div>
  </div>
</template>

<script>
import mixin from "@/mixins/page.js";
export default {
  mixins: [mixin],
  props: {
    list: {
      type: Array,
      default: function () {
        return [];
      },
    },
    vm: {
      type: Object,
      default: function () {
        return {
          img: "img",
          title: "title",
          create_time: "create_time",
          praise_id: "praise_id",
          source_table: "source_table",
          source_field: "source_field",
          source_id: "source_id",
        };
      },
    },
  },
  methods: {
    /**
     * 删除收藏
     * @param { Number } praise 收藏
     * @param { Number } index 删除位置
      */
    del_praise(praise, index) {
      this.$get(
        "~/api/praise/del",
        {
          praise_id: praise[this.vm.praise_id],
        },
        (res) => {
          this.list.splice(index, 1);
          this.$get(`~/api/${praise[this.vm.source_table]}/get_obj?article_id=${praise[this.vm.source_id]}`).then((r) => {
            let praise_count = r.result.obj.praise_len - 1;
            this.$post(`~/api/${praise[this.vm.source_table]}/set?article_id=${praise[this.vm.source_id]}`, { praise_len: praise_count } )
          })
        }
      );
    },
  },
};
</script>

<style scoped>
.item_collect {
  position: relative;
  background-color: #ffffff;
  margin-bottom: 0.8rem;
}

.collect_box {
  display: flex;
  padding: 0.3rem 0.6rem;
}

.left_block {
  display: inline-block;
  width: 20%;
  padding: 0.3rem;
  padding-right: 0.5rem;
}

.right_block {
  display: inline-block;
  width: 80%;
}

.time {
  color: #999;
}

.top_comment {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.6rem;
}
.top_comment .title {
  flex: 0 0 55%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.top_comment .time {
  flex: 20%;
  font-size: 0.5rem;
}

.btn_delete {
  position: absolute;
  right: 0.7rem;
  bottom: 0.8rem;
  line-height: 20px;
  font-size: 15px;
}
.btn_delete:hover {
  background: var(--color_primary_b);
  border-color: var(--color_primary_b);
}
</style>
