<template>
  <div class="private-chat-page">
    <div class="chat-shell">
      <div class="chat-sidebar">
        <div class="chat-sidebar-title">私信会话</div>
        <div v-if="conversationList.length" class="chat-conversation-list">
          <div
            v-for="item in conversationList"
            :key="item.conversation_key"
            class="chat-conversation-item"
            :class="{ active: activePeerId === item.peer_id }"
            @click="openConversation(item.peer_id)"
          >
            <img class="chat-avatar" :src="item.peer_avatar ? $fullUrl(item.peer_avatar) : defaultAvatar" />
            <div class="chat-conversation-main">
              <div class="chat-conversation-top">
                <span class="chat-name">{{ item.peer_nickname }}</span>
                <span class="chat-time">{{ formatTime(item.last_time) }}</span>
              </div>
              <div class="chat-conversation-bottom">
                <span class="chat-last-message">{{ item.last_message || "暂无消息" }}</span>
                <span v-if="item.unread_count" class="chat-unread-badge">{{ item.unread_count > 99 ? "99+" : item.unread_count }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="chat-empty-side">
          <div class="chat-empty-title">暂无私信会话</div>
          <div class="chat-empty-tip">去用户主页关注对方后，就可以发起聊天。</div>
        </div>
      </div>

      <div class="chat-main">
        <div v-if="peerInfo.user_id" class="chat-main-inner">
          <div class="chat-header">
            <img class="chat-avatar large" :src="peerInfo.avatar ? $fullUrl(peerInfo.avatar) : defaultAvatar" />
            <div class="chat-peer-info">
              <div class="chat-peer-name">{{ peerInfo.nickname || peerInfo.username }}</div>
              <div class="chat-peer-tip">仅在你已关注对方时可发送私信</div>
            </div>
          </div>

          <div ref="messageList" class="chat-message-list">
            <div
              v-for="item in messageList"
              :key="item.private_message_id"
              class="chat-message-row"
              :class="{ mine: Number(item.sender_id) === Number(currentUserId) }"
            >
              <div class="chat-bubble">
                <div class="chat-content">{{ item.content }}</div>
                <div class="chat-meta">
                  {{ $toTime(item.create_time, "yyyy-MM-dd hh:mm:ss") }}
                </div>
              </div>
            </div>
          </div>

          <div class="chat-editor">
            <el-input
              type="textarea"
              :rows="3"
              resize="none"
              maxlength="1000"
              show-word-limit
              ref="composerInput"
              v-model.trim="draftMessage"
              placeholder="输入内容后按 Enter 发送，Shift + Enter 换行"
              @keydown.enter.native.exact.prevent="sendMessage"
            />
            <div class="chat-actions">
              <el-button type="primary" :loading="sending" @click="sendMessage">发送</el-button>
            </div>
          </div>
        </div>

        <div v-else class="chat-placeholder">
          <div class="chat-empty-title">请选择一个会话</div>
          <div class="chat-empty-tip">你可以从左侧会话列表进入，也可以从用户主页直接发起私信。</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import mixin from "@/mixins/page.js";

export default {
  mixins: [mixin],
  data() {
    return {
      conversationList: [],
      messageList: [],
      activePeerId: 0,
      peerInfo: {},
      draftMessage: "",
      sending: false,
      defaultAvatar: "http://192.168.1.4:5000/upload/default_avatar.jpg",
    };
  },
  computed: {
    routePeerId() {
      return Number(this.$route.query.user_id || 0);
    },
    currentUser() {
      return (this.$store && this.$store.state && this.$store.state.user) ? this.$store.state.user : {};
    },
    currentUserId() {
      return Number((this.currentUser && this.currentUser.user_id) || 0);
    },
  },
  watch: {
    "$route.query.user_id": {
      immediate: true,
      handler() {
        this.bootstrapChat();
      },
    },
    currentUserId: {
      immediate: true,
      handler() {
        this.bootstrapChat();
      },
    },
  },
  methods: {
    async bootstrapChat() {
      if (!this.currentUserId) {
        return;
      }
      await this.loadConversationList();
      if (this.routePeerId) {
        await this.openConversation(this.routePeerId, true);
        return;
      }
      if (this.conversationList.length > 0) {
        await this.openConversation(this.conversationList[0].peer_id, true);
      }
    },
    async loadConversationList() {
      const res = await this.$get("~/api/private_message/conversation_list");
      this.conversationList = (res && res.result && res.result.list) ? res.result.list : [];
    },
    async ensurePeerInfo(userId) {
      const found = this.conversationList.find((item) => Number(item.peer_id) === Number(userId));
      if (found) {
        this.peerInfo = {
          user_id: found.peer_id,
          nickname: found.peer_nickname,
          username: found.peer_username,
          avatar: found.peer_avatar,
        };
        return;
      }
      const res = await this.$get("~/api/user/get_obj", { user_id: userId, like: 0 });
      this.peerInfo = (res && res.result && res.result.obj) ? res.result.obj : {};
    },
    async openConversation(userId, skipRoutePush = false) {
      const targetId = Number(userId || 0);
      if (!targetId) {
        return;
      }
      this.activePeerId = targetId;
      await this.ensurePeerInfo(targetId);
      const res = await this.$get("~/api/private_message/conversation_detail", { user_id: targetId });
      this.messageList = (res && res.result && res.result.list) ? res.result.list : [];
      await this.$post("~/api/private_message/mark_read", { user_id: targetId });
      await this.loadConversationList();
      if (!skipRoutePush) {
        this.$router.push(`/user/chat?user_id=${targetId}`);
      }
      this.$nextTick(() => {
        this.scrollToBottom();
        this.focusComposer();
      });
    },
    async sendMessage() {
      if (!this.activePeerId) {
        this.$message.warning("请先选择聊天对象");
        return;
      }
      if (!this.currentUserId) {
        this.$message.warning("用户未登录");
        return;
      }
      if (!this.draftMessage) {
        this.$message.warning("请输入私信内容");
        return;
      }
      this.sending = true;
      const res = await this.$post("~/api/private_message/send_message", {
        receiver_id: this.activePeerId,
        content: this.draftMessage,
      });
      this.sending = false;
      if (res && res.result) {
        this.draftMessage = "";
        await this.openConversation(this.activePeerId, true);
        this.$message.success("发送成功");
      } else if (res && res.error) {
        this.$message.error(res.error.message || "发送失败");
      }
    },
    focusComposer() {
      const input = this.$refs.composerInput;
      if (input && typeof input.focus === "function") {
        input.focus();
      }
    },
    scrollToBottom() {
      const box = this.$refs.messageList;
      if (box) {
        box.scrollTop = box.scrollHeight;
      }
    },
    formatTime(value) {
      if (!value) return "";
      return this.$toTime(value, "yyyy-MM-dd hh:mm");
    },
  },
};
</script>

<style scoped>
.private-chat-page {
  padding: 20px 0;
}
.chat-shell {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  min-height: 700px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 10px;
  overflow: hidden;
}
.chat-sidebar {
  width: 320px;
  border-right: 1px solid #ebeef5;
  background: #fafafa;
}
.chat-sidebar-title {
  padding: 18px 16px;
  font-size: 16px;
  font-weight: 700;
  border-bottom: 1px solid #ebeef5;
}
.chat-conversation-list {
  height: 640px;
  overflow-y: auto;
}
.chat-conversation-item {
  display: flex;
  padding: 14px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f2f2f2;
}
.chat-conversation-item.active {
  background: #ecf5ff;
}
.chat-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}
.chat-avatar.large {
  width: 50px;
  height: 50px;
}
.chat-conversation-main {
  margin-left: 12px;
  min-width: 0;
  flex: 1;
}
.chat-conversation-top,
.chat-conversation-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-name {
  font-weight: 600;
}
.chat-time,
.chat-meta,
.chat-peer-tip {
  color: #999;
  font-size: 12px;
}
.chat-last-message {
  color: #666;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 180px;
}
.chat-unread-badge {
  min-width: 20px;
  height: 20px;
  line-height: 20px;
  padding: 0 6px;
  text-align: center;
  border-radius: 10px;
  background: #f56c6c;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  margin-left: 8px;
}
.chat-main {
  flex: 1;
  background: #f5f7fa;
}
.chat-main-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.chat-header {
  display: flex;
  align-items: center;
  padding: 18px 20px;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}
.chat-peer-info {
  margin-left: 14px;
}
.chat-peer-name {
  font-size: 18px;
  font-weight: 700;
}
.chat-message-list {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
.chat-message-row {
  display: flex;
  margin-bottom: 14px;
}
.chat-message-row.mine {
  justify-content: flex-end;
}
.chat-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.chat-message-row.mine .chat-bubble {
  background: #409eff;
  color: #fff;
}
.chat-message-row.mine .chat-meta {
  color: rgba(255, 255, 255, 0.8);
}
.chat-editor {
  padding: 16px 20px;
  background: #fff;
  border-top: 1px solid #ebeef5;
}
.chat-actions {
  margin-top: 12px;
  text-align: right;
}
.chat-placeholder,
.chat-empty-side {
  color: #999;
  padding: 24px;
}
.chat-empty-title {
  font-size: 18px;
  font-weight: 700;
  color: #606266;
  margin-bottom: 10px;
}
.chat-empty-tip {
  font-size: 14px;
  line-height: 1.8;
}
</style>
