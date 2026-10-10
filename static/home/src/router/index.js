import Vue from 'vue';
import VueRouter from 'vue-router';
import index from '../views/index.vue'
import login from '../views/account/login.vue';
import store from "@/store/index.js";
import { historyList } from "@/router/historyList.js";
import axios from "axios";
import host_config from '@/plugins/port_config.js'
let host = host_config;
Vue.use(VueRouter)

const routes = [
	// 主页
	{
		path: '/',
		name: 'index',
		component: index
	},
	// 登录
	{
		path: '/account/login',
		name: 'login',
		component: login
	},
	// 忘记密码
	{
		path: '/account/forgot',
		name: 'forgot',
		component: () => import('../views/account/forgot.vue')
	},
	// 注册账号
	{
		path: '/account/register',
		name: 'register',
		component: () => import('../views/account/register.vue')
	},
	{
    path: "/filePreview",
    name: "filePreview",
    component: () => import("../views/filePreview/filePreview.vue"),
    meta: {
			title: "文件预览",
    },
  },
						// 二维码生成结束
		// 媒体图片
	{
		path: '/media/image',
		name: 'media_image',
		component: () => import('../views/media/image.vue')
	},

	// 音乐
	// {
	// 	path: '/media/music',
	// 	name: 'media_music',
	// 	component: () => import('../views/media/music.vue')
	// },
	// 媒体视频
	{
		path: '/media/video',
		name: 'media_video',
		component: () => import('../views/media/video.vue')
	},
	// 媒体视频
	{
		path: '/user_center/index',
		name: 'user_center_index',
		component: () => import('../views/user_center/index.vue')
	},
	// 文章路由
	{
		path: '/article/list',
		name: 'article_list',
		component: () => import('../views/article/list.vue')
	},
	{
		path: '/article/details',
		name: 'article_details',
		component: () => import('../views/article/details.vue')
	},
	// 浏览网站
	// 收藏路由
	{
		path: '/user/collect',
		name: 'collect_list',
		component: () => import('../views/user/collect.vue')
	},
	// 点赞路由
	{
		path: '/user/praise',
		name: 'praise_list',
		component: () => import('../views/user/praise.vue')
	},
	{
		path: "/history/list",
		name: "history_list",
		component: () => import("../views/history/list.vue")
	},

	{
		path: '/comment/table',
		name: 'comment_table',
		component: () => import('../views/comment/table.vue')
	},
	{
		path: '/comment/view',
		name: 'comment_view',
		component: () => import('../views/comment/view.vue')
	},

	


	// 公告路由
	{
		path: '/notice/list',
		name: 'notice_list',
		component: () => import('../views/notice/list.vue')
	},
	{
		path: '/notice/details',
		name: 'notice_details',
		component: () => import('../views/notice/details.vue')
	},
	// 普通用户表格路由
	{
		path: '/ordinary_user/table',
		name: '/ordinary_user_table',
		component: () => import('../views/ordinary_user/table.vue')
	},
	// 普通用户详情路由
	{
		path: '/ordinary_user/view',
		name: '/ordinary_user_view',
		component: () => import('../views/ordinary_user/view.vue')
	},
	
	
	
	
	
	// 编辑人员表格路由
	{
		path: '/compileors/table',
		name: '/compileors_table',
		component: () => import('../views/compileors/table.vue')
	},
	// 编辑人员详情路由
	{
		path: '/compileors/view',
		name: '/compileors_view',
		component: () => import('../views/compileors/view.vue')
	},
	
	
	
	
	
	// 新闻分类表格路由
	{
		path: '/news_class_nameification/table',
		name: '/news_class_nameification_table',
		component: () => import('../views/news_class_nameification/table.vue')
	},
	// 新闻分类详情路由
	{
		path: '/news_class_nameification/view',
		name: '/news_class_nameification_view',
		component: () => import('../views/news_class_nameification/view.vue')
	},
	
	
	
	
	
	// 新闻资源表格路由
	{
		path: '/news_resources/table',
		name: '/news_resources_table',
		component: () => import('../views/news_resources/table.vue')
	},
	// 新闻资源详情路由
	{
		path: '/news_resources/view',
		name: '/news_resources_view',
		component: () => import('../views/news_resources/view.vue')
	},
	
	
	
	
	
	// 新闻资讯表格路由
	{
		path: '/news_information/table',
		name: '/news_information_table',
		component: () => import('../views/news_information/table.vue')
	},
	// 新闻资讯详情路由
	{
		path: '/news_information/view',
		name: '/news_information_view',
		component: () => import('../views/news_information/view.vue')
	},
	
		// 新闻资讯列表路由
	{
		path: '/news_information/list',
		name: '/news_information_list',
		component: () => import('../views/news_information/list.vue')
	},
	// 猜你喜欢（个性化推荐列表）
	{
		path: '/news_information/recommend',
		name: 'news_information_recommend',
		component: () => import('../views/news_information/recommend.vue')
	},
	
		// 新闻资讯详情路由
	{
		path: '/news_information/details',
		name: '/news_information_details',
		component: () => import('../views/news_information/details.vue')
	},
	
	
	

	// 用户路由
	{
		path: '/user/index',
		name: 'user_index',
		component: () => import('../views/user/index.vue')
	},
	// 基本信息
	{
		path: '/user/info',
		name: 'user_info',
		component: () => import('../views/user/info.vue')
	},
	{
	    path: "/user/my_home_page",
	    name: "my_home_page",
	    component: () => import("../views/user/my_home_page.vue"),
	},
	{
	    path: "/user/chat",
	    name: "user_chat",
	    component: () => import("../views/user/chat.vue"),
	},
	// 找回密码
	{
		path: '/user/password',
		name: 'user_password',
		component: () => import('../views/user/password.vue')
	},

	// 搜索
	{
		path: '/search',
		name: 'search',
		component: () => import('../views/search/index.vue')
	},
	// 局部搜索
	{
		path: '/search/details',
		name: 'search_details',
		component: () => import('../views/search/details.vue')
	}
]

const router = new VueRouter({
	mode: 'hash',
	base: process.env.BASE_URL,
	routes
})

router.afterEach((to, from, next) => {
	let title = "新闻聚合系统-home";
	document.title = title;
	document.logo = "新闻聚合系统"
})

let formatDate = (date) => {
	var date = new Date(date);
	var YY = date.getFullYear() + '-';
	var MM = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
	var DD = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate());
	var hh = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
	var mm = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
	var ss = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
	return YY + MM + DD +" "+hh + mm + ss;
}

// 记录历史记录防抖5秒延迟
let historyTimer = null;
// 特殊名单
const specialList = ['/novel_chapters/read','/movie_episode/playvideo'];

router.beforeEach((to, from, next) => {
	const historyItem = historyList.find(item => item.path == to.path);
	historyTimer && clearTimeout(historyTimer);
	if(historyItem){
		historyTimer = setTimeout(() => {
			const vm = new Vue();
			let user_id = store.state.user.user_id;
			const url = to.path.split('/')[1];
			var token = store.state.user.token || $.db.get("token") || null;

			axios.get(`${host}api/${url}/get_obj`,{
				params: to.query,
				headers: {
					'x-auth-token': token
				}
			}).then(obj => {
				let isSpecial = specialList.includes(to.path);
				axios.get(`${host}api/history/get_list`,{ user_id: user_id },{
					headers: {
						'x-auth-token': token
					}
				}).then(history => {
					const list = history.data.result.list;
					// 判断是否存在历史记录
          let isExist = list.find(item => {
            // 特殊的名单处理
            if(isSpecial){
              const fullPath = to.fullPath;
              const path = fullPath.replace(/&currentChapterIndex=\d+/, '');
              return item.path == path;
            }
            return item.path == to.fullPath;
          })
					// 如果存在历史记录，则更新
          if(isExist){
						const param = {
              update_time: formatDate(new Date())
            };
						axios.post(`${host}api/history/set?history_id=${isExist.history_id}`,param,{
							headers: {
								'x-auth-token': token,
								'Content-Type': 'application/json'
							}
						}).then((res) => {
              console.log("更新历史结果：", res);
            });
					}else{
            const param = {
              user_id: user_id,
              title: historyItem.titleKey ? obj.data.result.obj[historyItem.titleKey] : null,
              img: historyItem.imgKey ? obj.data.result.obj[historyItem.imgKey] : null,
              path: to.fullPath,
              type: historyItem.type,
              source_table: obj.data.result.obj.source_table || url,
              source_field: obj.data.result.obj.source_field || url + '_id',
              source_id: isSpecial ? to.query.move_info_id || to.query.novel_reading_id : to.query[url + '_id'],
              params: JSON.stringify(obj.data.result.obj)
            };
			if (isSpecial && historyItem.sourceKey) {
				const sourceIdValue = to.query[historyItem.sourceIdKey];
				axios.get(`${host}api/${historyItem.sourceKey}/get_obj`, {
					params: { [historyItem.sourceId]: sourceIdValue },
					headers: { 'x-auth-token': token }
				}).then(sourceRes => {
					const sourceTableData = sourceRes.data.result.obj;
					param.title = sourceTableData[historyItem.sourceTitleKey] + "-" + param.title;
					param.img = sourceTableData[historyItem.sourceImgKey];
					axios.post(`${host}api/history/add`, param, {
						headers: {'x-auth-token': token,'Content-Type': 'application/json'}
					}).then((res) => {
						console.log("添加历史结果：", res);
					});
				});
			}else{
            	axios.post(`${host}api/history/add`, param, {
					headers: {'x-auth-token': token,'Content-Type': 'application/json'}
				}).then((res) => {
					console.log("添加历史结果：", res);
				});
			}
          }
				})
			})
		}, 3000);	
	}
  window.scrollTo(0, 0);
  next();
});

export default router
