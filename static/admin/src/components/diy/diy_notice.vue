<template>
  <div class="log_box">
    <p class="log_bntx">
      {{ bntx_text }}
      <el-button text class="moreBtn" @click="moreBtn">更多+</el-button>
    </p>
    <div class="log_conter" v-for="(item, index) in notice_log" :key="index">
      {{ index + 1 }}. {{ item.title
      }}<span class="time">{{
        $toTime(item.create_time, "yyyy-MM-dd hh:mm:ss")
      }}</span>
    </div>
  </div>
</template>
<script>
import mixin from "@/mixins/page.js";
export default {
  mixins: [mixin],
  data() {
    return {
      notice_log: [],
      bntx_text: "公告",
      user_group: this.$store.state.user.user_group,
    };
  },
  mounted() {
    this.getNoticeList();
  },
  methods: {
    getNoticeList() {
      let params = {
        size: 10,
        page: 1,
        like: 0,
        orderby: "create_time desc",
      };
      this.$get("~/api/notice/get_list", params).then((res) => {
        this.notice_log = res.result.list;
      });
    },
    moreBtn() {
      this.$router.push("./notice/table");
    },
  },
};
</script>

<style scoped>
.log_box {
  overflow-y: auto;
}

.log_box .log_bntx {
  height: 40px;
  text-align: center;
  font-size: 18px;
  font-weight: 700;
}

.log_conter {
  width: 80%;
  color: #141414;
  line-height: 30px;
}

.moreBtn {
  position: absolute;
  right: 20px;
}

.time {
  display: inline-block;
  float: right;
  left: 10px;
  font-size: 14px;
}

.hs {
  width: 220px;
}
</style>
