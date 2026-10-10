import axios from "axios";
import { Message } from "element-ui";

class RequestHelper {
  constructor() {
    this.baseURL = "";
  }
  // 请求
  request(options) {
    //console.log(options)
    let instance = axios.create();
    let opt = Object.assign(this.getDefaultConfig(), options);
    this.interceptors(instance);
    return instance(opt);
  }
  // 默认配置
  getDefaultConfig() {
    let config = {
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {},
    };
    return config;
  }

  // 拦截器
  interceptors(instance) {
    instance.interceptors.request.use(
      (config) => {
              config.headers["Authorization"] = "Bearer sk-afb6a8de44c247e7924b11bf240a759e";
              return config;
      },
      (error) => {
        console.log(error);
        return Promise.reject(error);
      }
    );

    instance.interceptors.response.use(
      (response) => {
        return response.data;
      },
      (error) => {
        if (error.response) {
          switch (error.response.status) {
            case 500:
              Message.error(`服务器错误${error.message}`);
              break;
            case 503:
              Message.error(`服务器错误${error.message}`);
              break;
          }
        } else {
          return Message.error(`请求无响应`);
        }
        return Promise.reject(error);
      }
    );
  }

  post({ data, options = {} }) {
              options.url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        data.model = "qwen-turbo";
          options.data = data;
    options.method = "post";
    return this.request(options);
  }
}
let requestHelper = new RequestHelper();

export default requestHelper;
