<!-- 客服聊天 -->
<template>
  <div class="robotic-container">
    <img
      v-drag
      class="robotic-icon"
      src="../../../public/robot.png"
      alt=""
      @click="showRobotic = true" />
      
    <div class="robotic-content" v-if="showRobotic">
      <div ref="roboticRef">
        <i
          class="robotic-content-close el-icon-close"
          style="font-size: 20px;cursor: pointer;"
          @click="showRobotic = false" />
        <div class="robotic-content-title">
          {{ title }}
        </div>
        <div class="robotic-content-item" v-if="md">
          <div
            v-for="(item, index) in msgList"
            :key="index"
            :class="
              item.role === 'user'
                ? 'robotic-content-item-right'
                : 'robotic-content-item-left'
            "
            v-html="renderMD(item.content)"></div>
          <div class="robotic-content-item-left" v-if="showLoading">
            <div class="robotic-content-item-loading"></div>
          </div>
        </div>
        <div class="robotic-content-send">
          <el-input v-model="contentVal" class="robotic-content-send-input">
            <template #append>
              <el-button @click="sendMsg">发送</el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MarkdownIt from "markdown-it";
import { $aiPost } from "@/api/aiApi";

export default {
  props: {
    title: {
      type: String,
      default: "智能客服聊天"
    }
  },
  data() {
    return {
      showRobotic: false,
      msgList: [],
      contentVal: null,
      showLoading: false,
      md: new MarkdownIt(),
    };
  },
  methods: {
    sendMsg() {
      let content = this.contentVal;
      this.msgList.push({
        content,
        role: "user",
      });
      this.contentVal = null;
      this.showLoading = true;
      this.scrollBottom();
      $aiPost({
        messages: [
          {
            role: "user",
            content,
          },
        ],
      }).then((res) => {
        this.showLoading = false;
        this.msgList.push(res.choices[0].message);
        setTimeout(() => {
          this.scrollBottom();
        }, 50);
      });
    },
    scrollBottom() {
      let scrollElem = this.$refs.roboticRef;
      scrollElem.scrollTo({
        top: scrollElem.scrollHeight,
        behavior: "smooth",
      });
    },
    renderMD(data) {
      let html = this.md.render(data);
      // 为表格添加容器包装，实现水平滚动
      html = html.replace(/<table([^>]*)>/g, '<div class="table-container"><table$1>');
      html = html.replace(/<\/table>/g, '</table></div>');
      return html;
    },
  },
};
</script>

<style scoped lang="less">
.robotic-container {
  .robotic-icon {
    position: fixed;
    top: 166px;
    left: -4px;
    width: 50px;
    height: 50px;
    cursor: pointer;
    z-index: 99999;
  }

  .robotic-content {
    width: 500px;
    height: 600px;
    position: fixed;
    top: calc(50% - 300px);
    left: calc(50% - 250px);
    border-radius: 20px;
    background-color: #fff;
    z-index: 99999;
    box-shadow: 0px 0px 10px 3px #ccc;

    > div {
      width: 100%;
      height: 100%;
      overflow-y: scroll;

      .robotic-content-close {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 9999;
      }

      .robotic-content-title {
        width: 100%;
        height: 50px;
        line-height: 50px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
      }

      .robotic-content-item {
        padding: 10px;
        padding-bottom: 100px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        position: relative;

        > div {
          width: fit-content;
          margin-bottom: 10px;
          border-radius: 10px;
          padding: 10px;
          box-sizing: border-box;
        }

        .robotic-content-item-left {
          background-color: #f0f0f0;
          max-width: 80%;
          
          ::v-deep h1, ::v-deep h2, ::v-deep h3, ::v-deep h4, ::v-deep h5, ::v-deep h6 {
            margin: 10px 0 8px 0 !important;
            color: #333 !important;
            font-weight: bold !important;
          }
          
          ::v-deep h1 { font-size: 20px !important; }
          ::v-deep h2 { font-size: 18px !important; }
          ::v-deep h3 { font-size: 16px !important; }
          ::v-deep h4 { font-size: 14px !important; }
          ::v-deep h5 { font-size: 13px !important; }
          ::v-deep h6 { font-size: 12px !important; }
          
          ::v-deep p {
            margin: 8px 0 !important;
            line-height: 1.6 !important;
            color: #555 !important;
          }
          
          ::v-deep .table-container {
            overflow-x: auto !important;
            margin: 15px 0 !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            /* 自定义滚动条样式 */
            scrollbar-width: thin !important;
            scrollbar-color: #4a90e2 #f1f1f1 !important;
          }
          
          ::v-deep .table-container::-webkit-scrollbar {
            height: 8px !important;
          }
          
          ::v-deep .table-container::-webkit-scrollbar-track {
            background: #f1f1f1 !important;
            border-radius: 4px !important;
          }
          
          ::v-deep .table-container::-webkit-scrollbar-thumb {
            background: #4a90e2 !important;
            border-radius: 4px !important;
          }
          
          ::v-deep .table-container::-webkit-scrollbar-thumb:hover {
            background: #357abd !important;
          }
          
          ::v-deep table {
            width: 100% !important;
            min-width: 400px !important;
            border-collapse: collapse !important;
            margin: 0 !important;
            background-color: #fff !important;
            border-radius: 8px !important;
            overflow: hidden !important;
          }
          
          ::v-deep th {
            background-color: #4a90e2 !important;
            color: white !important;
            padding: 12px 8px !important;
            text-align: left !important;
            font-weight: bold !important;
            font-size: 14px !important;
          }
          
          ::v-deep td {
            padding: 10px 8px !important;
            border-bottom: 1px solid #e8e8e8 !important;
            color: #333 !important;
            font-size: 13px !important;
            line-height: 1.5 !important;
          }
          
          ::v-deep tr:nth-child(even) {
            background-color: #f8f9fa !important;
          }
          
          ::v-deep tr:hover {
            background-color: #e3f2fd !important;
          }
          
          ::v-deep strong {
            color: #2c3e50 !important;
            font-weight: 600 !important;
          }
          
          ::v-deep ul, ::v-deep ol {
            margin: 10px 0 !important;
            padding-left: 20px !important;
          }
          
          ::v-deep li {
            margin: 5px 0 !important;
            line-height: 1.5 !important;
            color: #555 !important;
          }
          
          ::v-deep code {
            background-color: #f1f3f4 !important;
            padding: 2px 4px !important;
            border-radius: 3px !important;
            font-family: 'Courier New', monospace !important;
            font-size: 12px !important;
            color: #d73a49 !important;
          }
          
          ::v-deep pre {
            background-color: #f6f8fa !important;
            padding: 12px !important;
            border-radius: 6px !important;
            overflow-x: auto !important;
            margin: 10px 0 !important;
          }
          
          ::v-deep pre code {
            background: none !important;
            padding: 0 !important;
            color: #24292e !important;
          }
          
          ::v-deep blockquote {
            border-left: 4px solid #4a90e2 !important;
            margin: 10px 0 !important;
            padding: 8px 12px !important;
            background-color: #f8f9fa !important;
            color: #666 !important;
            font-style: italic !important;
          }
          
          ::v-deep hr {
            border: none !important;
            height: 2px !important;
            background: linear-gradient(to right, #4a90e2, transparent) !important;
            margin: 20px 0 !important;
          }
        }

        .robotic-content-item-right {
          margin-left: auto;
          background-color: #8aceff;
          color: #fff;
          ::v-deep p {
            margin-bottom: 0 !important;
          }
        }
        .robotic-content-item-loading {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          border: 2px solid transparent;
          border-top: 2px solid #8aceff;
          border-left: 2px solid #8aceff;
          animation: rotate 3s infinite linear;
        }
      }

      .robotic-content-send {
        width: 100%;
        height: 60px;
        background-color: #fff;
        border-radius: 20px;
        padding: 10px;
        box-sizing: border-box;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        position: absolute;
        bottom: 0;

        .robotic-content-send-input {
          width: 100%;
        }
      }
    }
  }
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

/* 隐藏垂直滚动条 */
::-webkit-scrollbar {
  width: 0;
}
/* 隐藏水平滚动条 */
::-webkit-scrollbar {
  height: 0;
}
/* 隐藏滚动条的轨道 */
::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0);
}
/* 隐藏滚动条的滑块 */
::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0);
}
</style>
