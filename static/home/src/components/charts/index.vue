<!-- 客服聊天 -->
<template>
  <div class="support_module" v-if="chatVisible">
    <div class="container" :class="{ small_css: isSmall, big_css: !isSmall }">
      <div class="list-content">
        <div>聊天列表</div>
        <div v-for="item in chatGroupList" :key="item.customer_chat_group_id"
          :class="currentChat === item.customer_chat_group_id ? 'current-chat' : ''" @click="changeChat(item)"
          class="chat-item">
          <div class="chat-avatar">
            <img :src="$fullUrl(getOtherAvatar(item.member))" />
          </div>
          <div class="chat-info">
            <div class="chat-top">
              <span class="chat-name">{{ getOtherNickname(item.member) }}</span>
              <span class="chat-time">{{ formatLastTime(item.last_time) }}</span>
            </div>
            <div class="chat-bottom">
              <span class="last-msg">{{ getLastMessage(item) }}</span>
              <span class="unread-count" v-if="item.unread_count > 0">{{ item.unread_count }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="msg-content">
        <div class="support_module_title">
          <span class="title_btn" @click="scaleSmall">{{
            !isSmall ? "一" : "□"
          }}</span>
          <span class="title_btn" @click="setChatVisible(false)">X</span>
        </div>

        <div class="content" ref="support_content" v-if="chatList">
          <div v-for="(item, index) in chatList.content" :key="index">
            <div class="item item-center">
              <span v-text="$toTime(item.creat_time, 'yyyy-MM-dd hh:mm:ss')"></span>
            </div>
            <div class="item" :class="{
              item_left: item.sender_id !== UserInfo.user_id,
              item_right: item.sender_id === UserInfo.user_id,
            }">
              <div class="avatar" v-if="item.sender_id !== UserInfo.user_id">
                <img :src="$fullUrl(receiver.avatar)" />
              </div>
              <div class="bubble" :class="{ 'bubble-right': item.sender_id === UserInfo.user_id }" v-text="item.msg">
              </div>
              <div class="avatar" v-if="item.sender_id === UserInfo.user_id">
                <img :src="$fullUrl(UserInfo.avatar)" />
              </div>
            </div>
          </div>
        </div>
        <div class="content" v-else></div>
        <div class="input-area">
          <textarea name="text" style="height: 50px" v-model="sendValue" id="textarea" placeholder="输入内容"></textarea>
        </div>
        <div class="button-area">
          <!-- <div style="width: 100px;height:50px;cursor: pointer;" @click="toToggle"></div> -->
          <button id="send-btn" @click="sendChat">发 送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      UserInfo: this.$store.state.user,
      chatVisible: false,
      isSmall: false,
      chatList: null,
      sendValue: "",
      chatGroupList: null,
      currentChat: null,
      receiver: {
        user_id: 1,
        avatar: "/upload/admin_avatar.jpg",
        nickname: "管理员",
      },
    };
  },
  methods: {
    scaleSmall() {
      this.chatVisible = false;
    },
    async getChatGroup() {
      try {
        const res = await this.$get("~/api/customer_chat_group/get_list");
        if (!res.result) return;

        const userChatGroups = await Promise.all(
          res.result.list.map(async (item) => {
            const member = JSON.parse(item.member);
            return await this.processChatGroup(item, member);
          })
        );

        const filteredGroups = userChatGroups.filter((item) =>
          item.member && Array.isArray(item.member) &&
          item.member.some((m) => m && parseInt(m.user_id) === parseInt(this.UserInfo.user_id))
        );

        // 使用 $set 确保数组响应式更新
        this.chatGroupList = filteredGroups.sort((a, b) => new Date(b.last_time) - new Date(a.last_time));

        if (filteredGroups.length > 0) {
          const targetChat = filteredGroups.find(group =>
            group.member.some(m => parseInt(m.user_id) === parseInt(this.receiver.user_id))
          );

          if (targetChat) {
            this.currentChat = targetChat.customer_chat_group_id;
            await this.getChat();
            // 加载完成后自动标记当前聊天为已读
            // await this.markAsRead(this.currentChat);
          } else {
            await this.addChatGroup();
          }
        } else {
          await this.addChatGroup();
        }
      } catch (error) {
        console.error("获取聊天组失败:", error);
      }
    },
    // 处理聊天组数据
    async processChatGroup(item, member) {
      try {
        const chatRes = await this.$get(`~/api/customer_chat_log/get_obj?customer_chat_id=${item.customer_chat_group_id}`);
        let last_time = item.update_time;
        let last_message = '';

        if (chatRes.result && chatRes.result.obj) {
          const content = JSON.parse(chatRes.result.obj.content);
          if (content && content.length > 0) {
            const lastMsg = content[content.length - 1];
            last_time = lastMsg.creat_time || item.update_time;
            last_message = lastMsg.msg || '';
          }
        }

        // 计算当前用户的未读消息数（用于显示）
        let displayUnreadCount = 0;
        const currentUserIndex = member.findIndex(m =>
          parseInt(m.user_id) === parseInt(this.UserInfo.user_id)
        );

        if (currentUserIndex === 0 && item.unread_count > 0) {
          // 当前用户是第一位，显示正数未读
          displayUnreadCount = item.unread_count;
        } else if (currentUserIndex === 1 && item.unread_count < 0) {
          // 当前用户是第二位，显示负数未读的绝对值
          displayUnreadCount = Math.abs(item.unread_count);
        }

        return {
          ...item,
          member: member || [],
          last_time,
          last_message,
          unread_count: displayUnreadCount,  // 显示用的未读数
          original_unread_count: item.unread_count  // 保留数据库原始值
        };
      } catch (error) {
        console.error('处理聊天组失败:', error);
        return {
          ...item,
          member: member || [],
          last_time: item.update_time,
          last_message: '',
          unread_count: 0,
          original_unread_count: item.unread_count
        };
      }
    },

    // 获取对方头像
    getOtherAvatar(members) {
      const other = members.find((m) => m.user_id !== this.UserInfo.user_id);
      return other ? other.avatar : "/upload/default_avatar.jpg";
    },

    // 格式化最后时间
    formatLastTime(time) {
      if (!time) return '';
      const now = new Date();
      const msgTime = new Date(time);
      const isToday = now.toDateString() === msgTime.toDateString();

      if (isToday) {
        return this.$toTime(time, 'hh:mm');
      } else {
        return this.$toTime(time, 'MM-dd');
      }
    },

    // 获取最后一条消息
    getLastMessage(item) {
      return item.last_message || '[暂无消息]';
    },
    addChatGroup() {
      if (parseInt(this.receiver.user_id) === parseInt(this.UserInfo.user_id)) {
        return;
      }
      // if (this.UserInfo.user_id === 1) return;

      console.log("创建新聊天组，接收者ID:", this.receiver.user_id);

      let member = JSON.stringify([
        this.receiver,
        {
          avatar: this.UserInfo.avatar,
          user_id: this.UserInfo.user_id,
          nickname: this.UserInfo.nickname,
        },
      ]);

      this.$post("~/api/customer_chat_group/add", { member }).then((res) => {
        console.log("创建聊天组响应:", res);
        if (res.result) {
          // 创建成功后立即设置为当前聊天
          this.currentChat = res.result;
          this.getChatGroup(); // 重新获取列表
        }
      }).catch(error => {
        console.error("创建聊天组失败:", error);
      });
    },
    getChat() {
      this.$get(
        `~/api/customer_chat_log/get_obj?customer_chat_id=${this.currentChat}`
      ).then((res) => {
        if (res.result) {
          if (res.result.obj) {
            res.result.obj.content = JSON.parse(res.result.obj.content);
          }
          this.chatList = res.result.obj;
        }
      });
    },
    async changeChat(data) {
      this.currentChat = data.customer_chat_group_id;
      this.setReceiver(data);

      // 立即更新本地未读状态（不等待服务器响应）
      if (this.chatGroupList && Array.isArray(this.chatGroupList)) {
        const chatGroup = this.chatGroupList.find(item =>
          parseInt(item.customer_chat_group_id) === parseInt(data.customer_chat_group_id)
        );
        if (chatGroup) {
          this.$set(chatGroup, 'unread_count', 0);
        }
      }

      // 然后标记服务器为已读并获取聊天
      await Promise.all([
        this.markAsRead(data.customer_chat_group_id),
        this.getChat()
      ]);
    },
    // 标记聊天为已读
    async markAsRead(chatGroupId) {
      try {
        const currentGroup = this.chatGroupList.find(item =>
          parseInt(item.customer_chat_group_id) === parseInt(chatGroupId)
        );

        if (currentGroup) {
          // 判断当前用户是第一位还是第二位
          const currentUserIndex = currentGroup.member.findIndex(m =>
            parseInt(m.user_id) === parseInt(this.UserInfo.user_id)
          );

          let newUnreadCount = currentGroup.unread_count;

          if (currentUserIndex === 0 && newUnreadCount > 0) {
            // 当前用户是第一位，清零正数未读
            newUnreadCount = 0;
          } else if (currentUserIndex === 1 && newUnreadCount < 0) {
            // 当前用户是第二位，清零负数未读
            newUnreadCount = 0;
          }

          // 更新服务器状态
          await this.$post(`~/api/customer_chat_group/set?customer_chat_group_id=${chatGroupId}`, {
            last_read_time: new Date().toISOString().slice(0, 19).replace('T', ' '),
            unread_count: newUnreadCount
          });

          // 更新本地状态
          if (this.chatGroupList && Array.isArray(this.chatGroupList)) {
            const chatGroup = this.chatGroupList.find(item =>
              parseInt(item.customer_chat_group_id) === parseInt(chatGroupId)
            );
            if (chatGroup) {
              this.$set(chatGroup, 'unread_count', newUnreadCount);
            }
          }
        }
      } catch (error) {
        console.error('标记已读失败:', error);
      }
    },
    // 发送消息，增加对方未读数
    async sendChat() {
      let content = [];
      if (this.chatList && this.chatList.content) {
        content = this.chatList.content;
      }

      const newMsg = {
        sender_id: this.UserInfo.user_id,
        msg: this.sendValue,
        creat_time: new Date().getTime(),
      };

      content.push(newMsg);

      let obj = {
        content: JSON.stringify(content),
      };

      try {
        if (this.chatList) {
          await this.$post(`~/api/customer_chat_log/set?customer_chat_id=${this.currentChat}`, obj);
        } else {
          obj.customer_chat_id = this.currentChat;
          await this.$post(`~/api/customer_chat_log/add`, obj);
        }

        // 先重新获取最新的聊天组数据
        await this.getChatGroup();

        // 再从更新后的 chatGroupList 中获取 currentGroup
        const currentGroup = this.chatGroupList.find(item =>
          parseInt(item.customer_chat_group_id) === parseInt(this.currentChat)
        );

        if (currentGroup) {
          const currentUserIndex = currentGroup.member.findIndex(m =>
            parseInt(m.user_id) === parseInt(this.UserInfo.user_id)
          );

          let newUnreadCount;
          // 使用 original_unread_count 而不是 unread_count
          const currentUnread = currentGroup.original_unread_count || currentGroup.unread_count;

          if (currentUserIndex === 0) {
            newUnreadCount = parseInt(currentUnread || 0) - 1;
          } else {
            newUnreadCount = parseInt(currentUnread || 0) + 1;
          }

          await this.$post(`~/api/customer_chat_group/set?customer_chat_group_id=${this.currentChat}`, {
            unread_count: newUnreadCount
          });
        }

        // 最后重新获取数据
        await Promise.all([
          this.getChat(),
          this.getChatGroup()
        ]);

        this.sendValue = "";
      } catch (error) {
        console.error('发送消息失败:', error);
      }
    },

    // 获取当前未读数量
    getCurrentUnreadCount() {
      const chatGroup = this.chatGroupList.find(item =>
        parseInt(item.customer_chat_group_id) === parseInt(this.currentChat)
      );
      return chatGroup ? chatGroup.unread_count : 0;
    },
    setChatVisible(val, receiverData) {
      this.chatVisible = val;
      if (val) {
        if (receiverData) {
          if (parseInt(receiverData.user_id) === parseInt(this.UserInfo.user_id)) {
            return;
          }
          this.receiver = {
            user_id: receiverData.user_id || 1,
            avatar: receiverData.avatar || "/upload/admin_avatar.jpg",
            nickname: receiverData.nickname || "管理员"
          };
        }
        this.getChatGroup().then(() => {
          // 聊天窗口打开后，如果有当前聊天，自动标记为已读
          if (this.currentChat) {
            this.markAsRead(this.currentChat);
          }
        });
      }
    },
    setReceiver(data) {
      let id = data.member.filter((item) => {
        return item.user_id !== this.UserInfo.user_id;
      })[0].user_id;
      this.$get("~/api/user/get_obj?user_id=" + id).then((res) => {
        this.receiver = res.result.obj;
      });
    },
    getOtherNickname(members) {
      const other = members.find((m) => m.user_id !== this.UserInfo.user_id);
      return other ? other.nickname : "未知用户";
    },
  },
  mounted() {
    this.getChatGroup();
    this.getChat();
  },
};
</script>

<style scoped lang="less">
.support_module .container {
  /* height: 650px; */
  height: 60%;
  width: 800px;
  border-radius: 4px;
  border: 0.5px solid #e0e0e0;
  background-color: #f5f5f5;
  /* display: flex;
        flex-flow: column; */
  overflow: hidden;
  position: fixed;
  /* top: 100px; */
  padding: 0;
  margin-left: -350px;
  z-index: 99999999;
  display: flex;
  flex-direction: row;

  .list-content {
    width: 25%;
    background-color: #fff;
    border-right: 1px solid #ccc;
    display: flex;
    flex-direction: column;

    >div {
      width: 100%;
      padding: 15px;
      box-sizing: border-box;
      cursor: pointer;
      font-size: 16px;

      &:nth-child(1) {
        text-align: center;
        font-weight: bold;
      }
    }

    .current-chat {
      background-color: #f5f5f5;
    }
  }

  .msg-content {
    width: 75%;
  }
}

.support_module .small_css {
  height: 40px;
  width: 200px;
  right: 0;
  bottom: 0px;
}

.support_module .big_css {
  top: 50%;
  transform: translateY(-50%);
  left: 50%;
}

.support_module .content {
  width: calc(100% - 0px);
  padding: 20px 30px;
  overflow-y: scroll;
  height: 70%;
}

.support_module .content::-webkit-scrollbar {
  display: none;
}

.support_module_title {
  text-align: right;
  height: 40px;
  line-height: 40px;
  border-bottom: 1px solid #ccc;
}

.support_module_title .title_btn {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
  color: #888;
}

.support_module .content:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
}

.support_module .bubble {
  max-width: 400px;
  padding: 10px;
  border-radius: 5px;
  position: relative;
  color: #000;
  word-wrap: break-word;
  word-break: normal;
  font-size: 14px;
  font-weight: normal;
}

.support_module .item_left .bubble {
  margin-left: 15px;
  background-color: #fff;
}

.support_module .item_left .bubble:before {
  content: "";
  position: absolute;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-top: 10px solid transparent;
  border-right: 10px solid #fff;
  border-bottom: 10px solid transparent;
  left: -20px;
}

.support_module .item_right .bubble {
  margin-right: 15px;
  background-color: #9eea6a;
}

.support_module .item_right .bubble:before {
  content: "";
  position: absolute;
  width: 0;
  height: 0;
  border-left: 10px solid #9eea6a;
  border-top: 10px solid transparent;
  border-right: 10px solid transparent;
  border-bottom: 10px solid transparent;
  left: none;

  right: -20px;
}

.support_module .item {
  margin-top: 15px;
  display: flex;
  width: 100%;
}

.support_module .item.item_right {
  justify-content: flex-end;
  min-width: 400px;
}

.support_module .item.item-center {
  justify-content: center;
}

.support_module .item.item-center span {
  font-size: 12px;
  padding: 2px 4px;
  color: #fff;
  background-color: #dadada;
  border-radius: 3px;
  -moz-user-select: none;
  /*火狐*/
  -webkit-user-select: none;
  /*webkit浏览器*/
  -ms-user-select: none;
  /*IE10*/
  -khtml-user-select: none;
  /*早期浏览器*/
  user-select: none;
}

.support_module .avatar img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
}

.support_module .input-area {
  border-top: 0.5px solid #e0e0e0;
  height: 16%;

  background-color: #fff;
}

.support_module textarea {
  flex: 1;
  padding: 10px;
  font-size: 14px;
  border: none;
  overflow-y: auto;
  overflow-x: hidden;
  outline: none;
  resize: none;
  width: 102%;
  height: 100%;
  min-height: 100%;
  max-height: 100%;
}

.support_module .button-area {
  display: flex;
  height: 40px;
  line-height: 40px;
  padding: 5px;
  justify-content: flex-end;
  text-align: right;
  width: 75%;
  background: #fff;
  position: absolute;
  bottom: 0;
}

.support_module .button-area button {
  width: 60px;
  height: 30px;
  line-height: 30px;
  border: none;
  outline: none;
  border-radius: 4px;
  float: right;
  cursor: pointer;
  background: #9eea6a;
  color: #333;
  margin: 0px;
  font-size: 13px;
}

.list-header {
  text-align: center;
  font-weight: bold;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.chat-item {
  display: flex;
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  align-items: center;

  &:hover {
    background-color: #f9f9f9;
  }

  &.current-chat {
    background-color: #f0f8ff;
  }
}

.chat-avatar {
  width: 45px;
  height: 45px;
  margin-right: 12px;

  img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
}

.chat-info {
  flex: 1;
  min-width: 0;
}

.chat-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.chat-name {
  font-weight: bold;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-time {
  font-size: 12px;
  color: #999;
  flex-shrink: 0;
}

.chat-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.last-msg {
  font-size: 12px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  font-weight: normal;
}

.unread-count {
  background-color: #ff3b30;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 11px;
  min-width: 18px;
  text-align: center;
  margin-left: 8px;
}
</style>
