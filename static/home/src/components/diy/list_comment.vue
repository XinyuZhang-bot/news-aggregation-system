<template>
  <div class="list_comment">
    <div class="item_comment_box" v-for="(o, i) in sortList" :key="i">
      <div class="comment">
        <div class="left_block">
          <img
            style="width: 4rem; height: 4rem"
            :src="$fullUrl(o[vm.avatar])"
            v-default-img="'../../../public/img/default.png'"
          />
        </div>
        <div class="right_block">
          <div class="top_comment">
            <div class="nickname">
              {{ o[vm.nickname] }}
              <el-tag v-if="o.sticky">置顶</el-tag>
            </div>
            <div class="time_block">
              <div class="time">
                {{ o[vm.create_time] | formatDate }}
              </div>
              <el-popover v-if="self" placement="bottom" trigger="click" ref="popover">
                <span class="comment-options" slot="reference" type="text">
                  <i class="el-icon-more-outline"></i>
                </span>
                <div class="comment-options-btn">
                  <el-button type="text" size="mini" @click="handleSticky(o)">{{
                    o.sticky ? "取消置顶" : "置顶"
                  }}</el-button>
                  <el-button style="margin-left: 0px;margin-top: 5px;" type="text" size="mini" @click="handleHidden(o)"
                    >屏蔽</el-button
                  >
                </div>
              </el-popover>
            </div>
          </div>
          <div v-html="o[vm.content]" class="content"></div>
          <div class="comment_reply" v-if="Object.keys(obj).length">
            <b-button variant="outline" @click="reply_to_sb(o)">回复</b-button>
			<b-button variant="outline" @click="del_reply(o)" type="text" v-if="user_id === o.user_id && ($check_action('/comment/list','del') || $check_action('/comment/details','del'))" style="margin-left: 10px;">删除</b-button>
          </div>
        </div>
      </div>
      <div class="list_reply ml-5" v-if="o.list_reply">
        <div class="mb" v-for="(obj, idx) in o.list_reply" :key="idx">
          <div v-if="!obj.hidden">
            <div class="fl"><span class="nickname">{{ obj[vm.nickname] }}</span></div>
            <div class="fr">
              <span class="time">{{ obj[vm.create_time] | formatDate }}</span>
              <b-button variant="outline" @click="del_reply(obj)" type="text" v-if="user_id === obj.user_id && ($check_action('/comment/list','del') || $check_action('/comment/details','del'))">删除</b-button>
              <span v-else style="margin-left:30px"></span>

              <el-popover v-if="self" placement="bottom" trigger="click" ref="popover">
                <span class="comment-options" slot="reference" type="text">
                  <i class="el-icon-more-outline"></i>
                </span>
                <div class="comment-options-btn">
                  <el-button type="text" size="mini" @click="handleHidden(obj)"
                    >屏蔽</el-button
                  >
                </div>
              </el-popover>
            </div>
            <div class="ml-5" v-html="obj[vm.content]"></div>
            <div class="ml-5 reply_action" v-if="$store.state.user.user_id">
              <b-button variant="outline" @click="reply_to_sb(obj)" size="sm">回复TA</b-button>
            </div>
          </div>
        </div>
      </div>
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
    obj: {
      type: Object,
      default: function () {
        return {};
      },
    },
    vm: {
      type: Object,
      default: function () {
        return {
          avatar: "avatar",
          nickname: "nickname",
          content: "content",
          create_time: "create_time",
        };
      },
    },
    self: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      text: "",
    };
  },
  methods: {
    reply_to_sb(o) {
      this.obj.reply_to_id = o.comment_id;
    },
    del_reply(o) {
      // this.obj.reply_to_id = o.comment_id;
      this.$confirm("是否删除评论？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        cancelButtonClass: "custom-cancel-btn"
      })
        .then(async () => {
          var bl = await this.$get("~/api/comment/del?", {
            user_id: this.$store.state.user.user_id,
            comment_id: o.comment_id
          });
          if (o.error) {
            this.$message.error("删除失败" + o.error.message);
          } else if (bl) {
            this.$message({
              type: "success",
              message: "删除成功!"
            });
            this.$emit('reset');
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    handleHidden(o) {
      this.$refs.popover.forEach((item) => {
        item.doClose();
      });
      this.$confirm("确定要屏蔽这条评论吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          this.$post("~/api/comment/set?comment_id=" + o.comment_id, {
            hidden: 1,
          }).then((res) => {
            if (res.result) {
              this.$message.success("操作成功");
              this.$emit("update-comment");
            }
          });
        })
        .catch(() => {
        });
    },
    handleSticky(o) {
      this.$refs.popover.forEach((item) => {
        item.doClose();
      });
      let sticky = o.sticky ? 0 : 1;
      this.$post("~/api/comment/set?comment_id=" + o.comment_id, {
        sticky,
      }).then((res) => {
        if (res.result) {
          this.$message.success("操作成功");
          this.$emit("update-comment");
        }
      });
    },
  },
  computed: {
    user_id() {
      return this.$store.state.user.user_id;
    },
    sortList() {
      return this.list
        .filter((item) => item.hidden !== 1)
        .sort((a, b) => {
          if (a.sticky === 1 && b.sticky !== 1) return -1;
          if (a.sticky !== 1 && b.sticky === 1) return 1;
          return 0;
        });
    },
  },
  components: {},
};
</script>

<style lang="less">
.list_comment {
  padding: 2rem 0.6rem;
}
.item_comment_box{
	overflow: hidden;
}
.item_comment_box .comment {
  display: flex;
  width: 100%;
  padding: 0.5rem 0;
}

.item_comment_box + .item_comment_box {
  border-top: 1px solid #dbdbdb;
}

.list_comment .left_block {
  padding: 0.3rem;
  padding-right: 0.5rem;
}

.list_comment .right_block {
  flex-basis: calc(100% - 76px);
}


.top_comment {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 0.6rem;
}

.list_comment .time {
  display: inline-block;
  color: #999;
  text-align: right;
  font-size: 15px;
  transform: scale(0.8);
}

.list_comment .nickname {
  color: var(--color_grey);
  font-size: 0.8rem;
}

.list_comment .content {
  float: left;
  font-size: 0.8rem;
}
.comment_reply {
  float: right;
}

.comment-options {
  cursor: pointer;
  > i {
    transform: rotate(90deg);
  }
}
.comment-options-btn {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.list_reply .mb >div{
  clear: both;
}
.reply_action {
  margin-top: 6px;
}
.el-message-box__btns .custom-cancel-btn{
  color: #606266;
}
</style>
