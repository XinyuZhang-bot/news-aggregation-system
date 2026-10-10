import Vue from 'vue';
import VueRouter from 'vue-router';
import index from '../views/index.vue';
import login from '../views/login.vue';
import forgot from '../views/forgot.vue';
import register from '../views/register.vue';
Vue.use(VueRouter)

const routes = [
    // 主页
    {
        path: '/',
        name: 'index',
        component: index,
        meta: {
            index: 0,
            title: '首页'
        }
    },

    // 登录
    {
        path: '/login',
        name: 'login',
        component: login,
        meta: {
            index: 0,
            title: '登录'
        }
    },
    {
        path: "/filePreview",
        name: "filePreview",
        component: () => import("../views/filePreview/filePreview.vue"),
        meta: {
            title: "文件预览",
        },
    },
                    
    
	    
    // 忘记密码
    {
        path: '/forgot',
        name: "forgot",
        component: forgot,
        meta: {
            index: 0,
            title: '忘记密码'
        }
    },
    {
        path: '/register',
        name: 'register',
        component: register,
        meta: {
            index: 0,
            title: '注册'
        }
    },

    // 修改密码
    {
        path: '/user/password',
        name: "password",
        component: () => import("../views/user/password.vue"),
        meta: {
            index: 0,
            title: '修改密码'
        }
    },

            // 权限路由
        {
            path: '/auth/table',
            name: 'auth_table',
            component: () => import('../views/auth/table.vue'),
            meta: {
                index: 0,
                title: '权限列表'
            }
        },
        {
            path: '/auth/view',
            name: 'auth_view',
            component: () => import('../views/auth/view.vue'),
            meta: {
                index: 0,
                title: '权限详情'
            }
        },
    
    
                // 轮播图路由
        {
            path: '/slides/table',
            name: 'slides_table',
            component: () => import('../views/slides/table.vue'),
            meta: {
                index: 0,
                title: '轮播图列表'
            }
        },
        {
            path: '/slides/view',
            name: 'slides_view',
            component: () => import('../views/slides/view.vue'),
            meta: {
                index: 0,
                title: '轮播图详情'
            }
        },
                    // 文章路由
            {
                path: '/article/table',
                name: 'article_table',
                component: () => import('../views/article/table.vue'),
                meta: {
                    index: 0,
                    title: '热点专题列表'
                }
            },
            {
                path: '/article/view',
                name: 'article_view',
                component: () => import('../views/article/view.vue'),
                meta: {
                    index: 0,
                    title: '热点专题详情'
                }
            },

            // 文章分类路由
            {
                path: '/article_type/table',
                name: 'article_type_table',
                component: () => import('../views/article_type/table.vue'),
                meta: {
                    index: 0,
                    title: '热点专题分类列表'
                }
            },
            {
                path: '/article_type/view',
                name: 'article_type_view',
                component: () => import('../views/article_type/view.vue'),
                meta: {
                    index: 0,
                    title: '热点专题分类详情'
                }
            },
                        // 敏感词路由
        {
            path: '/sensitive_vocabulary/table',
            name: 'sensitive_vocabulary_table',
            component: () => import('../views/sensitive_vocabulary/table.vue'),
            meta: {
                index: 0,
                title: '敏感词列表'
            }
        },
        {
            path: '/sensitive_vocabulary/view',
            name: 'sensitive_vocabulary_view',
            component: () => import('../views/sensitive_vocabulary/view.vue'),
            meta: {
                index: 0,
                title: '敏感词详情'
            }
        },
                    
    
    
            // 公告路由
        {
            path: '/notice/table',
            name: 'notice_table',
            component: () => import('../views/notice/table.vue'),
            meta: {
                index: 0,
                title: '最新公告列表'
            }
        },
        {
            path: '/notice/view',
            name: 'notice_view',
            component: () => import('../views/notice/view.vue'),
            meta: {
                index: 0,
                title: '最新公告详情'
            }
        },
            	        
            // 评论路由
        {
            path: '/comment/table',
            name: 'comment_table',
            component: () => import('../views/comment/table.vue'),
            meta: {
                index: 0,
                title: '评论列表'
            }
        },
        {
            path: '/comment/view',
            name: 'comment_view',
            component: () => import('../views/comment/view.vue'),
            meta: {
                index: 0,
                title: '评论详情'
            }
        },
        	            // 普通用户路由
        {
            path: '/ordinary_user/table',
            name: 'ordinary_user_table',
            component: () => import('../views/ordinary_user/table.vue'),
            meta: {
                index: 0,
                title: '普通用户列表'
            }
        },
        {
            path: '/ordinary_user/view',
            name: 'ordinary_user_view',
            component: () => import('../views/ordinary_user/view.vue'),
            meta: {
                index: 0,
                title: '普通用户详情'
            }
        },
		                				            // 编辑人员路由
        {
            path: '/compileors/table',
            name: 'compileors_table',
            component: () => import('../views/compileors/table.vue'),
            meta: {
                index: 0,
                title: '编辑人员列表'
            }
        },
        {
            path: '/compileors/view',
            name: 'compileors_view',
            component: () => import('../views/compileors/view.vue'),
            meta: {
                index: 0,
                title: '编辑人员详情'
            }
        },
		                				            // 新闻分类路由
        {
            path: '/news_class_nameification/table',
            name: 'news_class_nameification_table',
            component: () => import('../views/news_class_nameification/table.vue'),
            meta: {
                index: 0,
                title: '新闻分类列表'
            }
        },
        {
            path: '/news_class_nameification/view',
            name: 'news_class_nameification_view',
            component: () => import('../views/news_class_nameification/view.vue'),
            meta: {
                index: 0,
                title: '新闻分类详情'
            }
        },
		                				            // 新闻资源路由
        {
            path: '/news_resources/table',
            name: 'news_resources_table',
            component: () => import('../views/news_resources/table.vue'),
            meta: {
                index: 0,
                title: '新闻爬虫'
            }
        },
        {
            path: '/news_resources/view',
            name: 'news_resources_view',
            component: () => import('../views/news_resources/view.vue'),
            meta: {
                index: 0,
                title: '新闻爬虫详情'
            }
        },
        {
            path: '/crawl_run/table',
            name: 'crawl_run_table',
            component: () => import('../views/crawl_run/table.vue'),
            meta: {
                index: 0,
                title: '抓取运行记录'
            }
        },
        {
            path: '/crawl_run/view',
            name: 'crawl_run_view',
            component: () => import('../views/crawl_run/view.vue'),
            meta: {
                index: 0,
                title: '抓取运行详情'
            }
        },
        {
            path: '/recommend_insight/table',
            name: 'recommend_insight_table',
            component: () => import('../views/recommend_insight/table.vue'),
            meta: {
                index: 0,
                title: '推荐效果分析'
            }
        },
		                				            // 新闻资讯路由
        {
            path: '/news_information/table',
            name: 'news_information_table',
            component: () => import('../views/news_information/table.vue'),
            meta: {
                index: 0,
                title: '新闻列表'
            }
        },
        {
            path: '/news_information/view',
            name: 'news_information_view',
            component: () => import('../views/news_information/view.vue'),
            meta: {
                index: 0,
                title: '新闻发布'
            }
        },
		                				    			// 操作日志路由
		{
		    path: '/operation_log/table',
		    name: 'operation_log_table',
		    component: () => import('../views/operation_log/table.vue'),
		    meta: {
		        index: 0,
		        title: '操作日志'
		    }
		},
	        // 用户路由
    {
        path: '/user/table',
        name: 'user_table',
        component: () => import('../views/user/table.vue'),
        meta: {
            index: 0,
            title: '用户列表'
        }
    },
    {
        path: '/user/view',
        name: 'user_view',
        component: () => import('../views/user/view.vue'),
        meta: {
            index: 0,
            title: '用户详情'
        }
    },
    {
        path: '/user/info',
        name: 'user_info',
        component: () => import('../views/user/info.vue'),
        meta: {
            index: 0,
            title: '个人信息'
        }
    },
    // 用户组路由
    {
        path: '/user_group/table',
        name: 'user_group_table',
        component: () => import('../views/user_group/table.vue'),
        meta: {
            index: 0,
            title: '用户组列表'
        }
    },
    {
        path: '/user_group/view',
        name: 'user_group_view',
        component: () => import('../views/user_group/view.vue'),
        meta: {
            index: 0,
            title: '用户组详情'
        }
    }
]

const router = new VueRouter({
    mode: 'hash',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    let token = to.query.token;
    if (token) {
        $.db.set("token", token, 120);
    }
    next();
})

router.afterEach((to) => {
    const base = "新闻聚合平台管理端";
    const sub = to.meta && to.meta.title ? String(to.meta.title) : "";
    document.title = sub ? `${sub} | ${base}` : base;
})

// 解决重载报错
const VueRouterPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return VueRouterPush.call(this, location).catch((err) => err);
};

export default router
