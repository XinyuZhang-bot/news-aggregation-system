<template>
	<div class="page_root page_mall" id="root_demo">
		<div class="warp banner mall-banner">
		    <div class="container swiper_box mall-banner__inner">
		        <div class="row">
		            <div class="col-12">
		                <div class="mall-banner__hero">
		                    <div class="swiper_img mall-banner__swiper">
		                        <swiper_img :list="list_slide"/>
		                    </div>
		                </div>
		            </div>
		        </div>
		    </div>
		</div>

		<!-- 猜你喜欢：个性化推荐新闻资讯 -->
		<div class="ins warp model1 guess_you_like_section" v-if="$check_action('/news_information/list', 'get')">
		    <div class="container">
		        <div class="row">
		            <div class="col-12">
		                <div class="guess_you_like_recommend mall-section-head">
		                    <div class="title mall-section-head__title">
		                        <span class="mall-section-head__bar" aria-hidden="true"></span>
		                        <span class="mall-section-head__text">猜你喜欢</span>
		                    </div>
		                    <div class="more_box">
		                        <router-link to="/news_information/recommend" class="ins_more more mall-section-head__more">
		                            <span class="mor">更多 &gt;</span>
		                        </router-link>
		                    </div>
		                </div>
		                <p class="guess_you_like_hint" v-if="guess_you_like_hint_guest">
		                    登录后将根据您的浏览、收藏与点赞偏好为您推荐个性化新闻
		                </p>
		                <p class="guess_you_like_hint" v-else-if="show_guess_you_like_hint">
		                    根据您的浏览、收藏与点赞偏好为您推荐<strong class="guess_you_like_hint__cat">{{ guess_you_like_hint_cats }}</strong>类新闻
		                </p>
						<div class="list_guess_you_like_box" v-if="list_guess_you_like.length">
							<list_news_information :list="list_guess_you_like" layout="jd-text" />
						</div>
						<p class="guess_you_like_empty" v-else-if="!guess_you_like_loading">暂无推荐内容</p>
		            </div>
		        </div>
		    </div>
		</div>

		<div class="warp article_s">
		    <!-- 容器 -->
		    <div class="container">
		        <div class="row">
		            <div class="col-12">
		                <!-- 标题栏组件 -->
		                <div class="article_recommend mall-section-head">
		                    <div class="title mall-section-head__title">
		                        <span class="mall-section-head__bar" aria-hidden="true"></span>
		                        <span class="mall-section-head__text">热点专题</span>
		                    </div>
		                    <div class="more_box">
		                        <router-link to="/article/list" class="art_more more mall-section-head__more">
		                            <span class="mor">更多 &gt;</span>
		                        </router-link>
		                    </div>

		                </div>
						<div class="list_article_box">
							<list_article v-if="show_list_article" :list="list_article" layout="hot" />
						</div>

		            </div>
		        </div>
		    </div>
		</div>
							<!-- 推荐新闻资讯模块(开始) -->
		<div class="ins warp model1" v-if="$check_action('/news_information/list', 'get')">
		    <!-- 容器 -->
		    <div class="container">
		        <div class="row">
		            <div class="col-12">
		                <!-- 标题栏组件 -->
		                <div class="diy_recommend mall-section-head">
		                    <div class="title mall-section-head__title">
		                        <span class="mall-section-head__bar" aria-hidden="true"></span>
		                        <span class="mall-section-head__text">新闻资讯</span>
		                    </div>
		                    <div class="more_box">
		                        <router-link to="/news_information/list" class="ins_more more mall-section-head__more">
		                            <span class="mor">更多 &gt;</span>
		                        </router-link>
		                    </div>

		                </div>
		                <!-- 新闻资讯推荐列表组件 -->
						<div class="list_news_information_box" ins_box>
							<list_news_information :list="list_news_information" layout="jd-text" />
						</div>

		            </div>
		        </div>
		    </div>
		</div>
		<!-- 推荐新闻资讯模块(结束) -->
					
	</div>
</template>

<script>
	import mixin from "@/mixins/page.js";
						import list_news_information from "@/components/diy/list_news_information.vue";
		import bar_title from "@/components/diy/bar_title.vue";
	import list_article from "@/components/diy/list_article.vue";
	import swiper_img from "@/components/diy/swiper_img.vue";

	export default {
		mixins: [mixin],
		components: {
								list_news_information,
				bar_title,
			list_article,
			swiper_img,
		},
		data() {
			return {
				isSmall: false,
				sendValue: "",
				chatList:[],
				showChat: false,
				isAdmin: false,
				token:"",
				// 文章模型数组
				list_article: [],
				vm_arr_article: [
					"article_id",
					"img",
					"title",
					"praise_len",
					"hits",
					"type",
					"create_time",
				],
				show_list_article: true,
									list_news_information: [],
					list_guess_you_like: [],
					guess_you_like_loading: false,
					guess_you_like_hint_cats: "热门",
					show_guess_you_like_hint: false,
					guess_you_like_hint_guest: false,
					list_slide: [],
				list_menu: [],
			};
		},
		created(){
			this.get_token();
		},
		methods: {
					getHashParams() {
				let key = "token";
				// / 获取所有参数
				let query = window.location.search.substring(1);
				let hash = window.location.hash.substring(1);
				// 如果锚点后面有参数，把锚点后面的参数加入到search参数中
				if(hash.indexOf("?") > -1){
					query += "&" + hash.split("?")[1];
				}
				let key_values = query.split("&");
				let params = {};
				// 遍历参数并存入params对象
				key_values.map(function (key_val){
					let key_val_arr = key_val.split("=");
					params[key_val_arr[0]] = key_val_arr[1];
				});
				// 如果找到了key对应的参数，返回对应值
				if(typeof params[key]!="undefined"){
					return params[key];
				}
				// 如果没找到，返回空字符串
				return "";
			},
			get_token(){
				// let token = this.$route.query.token
				let token = this.getHashParams();
				console.log(token)
				if (token){
					$.db.set("token",token,120);
					let new_href = window.location.href.replaceAll("?token="+encodeURIComponent(token));
					location.href = new_href
				}
			},
					// toggle
			toToggle(){
				this.isAdmin = !this.isAdmin;
			},

			_resolve_user_id() {
				const fromStore = this.$store.state.user && this.$store.state.user.user_id;
				if (fromStore) {
					return String(fromStore);
				}
				const fromSession = sessionStorage.getItem("user_id");
				return fromSession ? String(fromSession) : "";
			},

			_set_guess_you_like_hint(categoryInput) {
				let list = [];
				if (Array.isArray(categoryInput)) {
					list = categoryInput;
				} else {
					list = String(categoryInput || "")
						.split("、")
						.map((s) => s.trim())
						.filter(Boolean);
				}
				this.guess_you_like_hint_cats = list.slice(0, 2).join("、") || "热门";
				this.show_guess_you_like_hint = true;
				this.guess_you_like_hint_guest = false;
			},

			/** 猜你喜欢：仅走个性化推荐接口 get_hits_list */
			get_guess_you_like() {
				this.guess_you_like_loading = true;
				const user_id = this._resolve_user_id();
				const param = {
					user_id: user_id,
					top_k: 6,
					page: 1,
					size: 6,
				};
				if (user_id) {
					this._set_guess_you_like_hint("热门");
					this.$get("~/api/news_information/recommend_advice?", { user_id }, (adv) => {
						if (adv.result) {
							let cats = [];
							if (Array.isArray(adv.result.categories) && adv.result.categories.length) {
								cats = adv.result.categories.slice(0, 2);
							} else if (adv.result.cat_text) {
								cats = String(adv.result.cat_text)
									.split("、")
									.map((s) => s.trim())
									.filter(Boolean)
									.slice(0, 2);
							}
							if (cats.length) {
								this._set_guess_you_like_hint(cats);
							}
						}
					});
				} else {
					this.show_guess_you_like_hint = false;
					this.guess_you_like_hint_guest = true;
				}
				this.$get("~/api/news_information/get_hits_list?", param, (json) => {
					this.guess_you_like_loading = false;
					if (json.result && json.result.list) {
						this.list_guess_you_like = json.result.list;
					} else {
						this.list_guess_you_like = [];
					}
				});
			},

			/** 新闻资讯：最新列表（非个性化，与猜你喜欢区分） */
			get_news_information() {
				const param = {
					page: 1,
					size: 12,
					orderby: "create_time desc",
				};
				this.$get("~/api/news_information/get_list?", param, (json) => {
					if (json.result) {
						this.list_news_information = json.result.list;
					}
				});
			},
	
			/**
			 * 当前年月日时分秒方法
			 * @param {Object} fmt
			 */
			dateFormat(fmt) {
				var myDate = new Date();
				var o = {
					"M+": myDate.getMonth() + 1, // 月份
					"d+": myDate.getDate(), // 日
					"h+": myDate.getHours(), // 小时
					"m+": myDate.getMinutes(), // 分
					"s+": myDate.getSeconds(), // 秒
					"q+": Math.floor((myDate.getMonth() + 3) / 3), // 季度
					"S": myDate.getMilliseconds() // 毫秒
				};
				if (/(y+)/.test(fmt))
					fmt = fmt.replace(RegExp.$1, (myDate.getFullYear() + "").substr(4 - RegExp.$1.length));
				for (var k in o)
					if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
						return fmt;
			},

			// 获取轮播图
			get_slides() {
			    this.$get("~/api/slides/get_list?", {}, (json) => {
			        if (json.result) {
			            this.list_slide = json.result.list;
			        }
			    });
			},
			// 获取导航栏
			get_menu() {
				var user_group = this.user_group;
			    this.$get(
			        "~/api/auth/get_list?",
			        {
			            page: "",
						user_group,
						get: 1,
						position: "top"
			        },
			        (json) => {
			            if (json.result) {
			                this.list_menu = json.result.list;
			            }
			        }
			    );
			},
			// 获取文章
			get_article() {
			    this.$get(
			        "~/api/article/get_list?",
			        {
			            page: 1,
			            size: 6,
			        },
			        (json) => {
			            if (json.result) {
			                var list_article = json.result.list;
			                this.list_article = list_article;
			            }
			        }
			    );
			},
			to_details(key,o,id) {
				if(!id){
					id = key + "_id";
				}
			    this.$router.push('/' + key + '/details?' + id + '=' + o[id]);
			},
		},
		mounted() {
			document.body.classList.add("page-home-white");
								this.get_guess_you_like();
				this.get_news_information();
				this.get_menu();
			this.get_slides();
			this.get_article();
		},
		beforeDestroy() {
			document.body.classList.remove("page-home-white");
		},
	};
</script>

<style scoped>
.page_root{
	position: relative;
}
.support_entry{
	position: fixed;
	top: 400px;
	right: 20px;
	width: 80px;
	height: 80px;
	cursor: pointer;
	z-index: 99999;
}
.support_module .container{
        /* height: 650px; */
        height: 70%;
        width: 700px;
        border-radius: 4px;
        border: 0.5px solid #e0e0e0;
        background-color: #f5f5f5;
        /* display: flex;
        flex-flow: column; */
        overflow: hidden;
				position: fixed;
				/* top: 100px; */
				padding: 0;
				margin-left: 0;
				z-index: 99999999;
    }
	.support_module	.small_css{
		height: 40px;
		width: 200px;
		right: 0;
		bottom: 0px;
	}
	.support_module	.big_css{
				top: 60px;
				left: calc(50% - 350px);
				}
    .support_module .content{
        width: calc(100% - 0px);
        padding: 20px 30px;
        overflow-y: scroll;
				height: 70%;
    }
		.support_module .content::-webkit-scrollbar{
	display: none
}
.support_module_title{
	text-align: right;
	height: 40px;
	line-height: 40px;
	border-bottom: 1px solid #ccc;

}
.support_module_title .title_btn{
	font-size: 20px;
	cursor: pointer;
	margin-right: 20px;
	color: #888;

}
    .support_module .content:hover::-webkit-scrollbar-thumb{
        background:rgba(0,0,0,0.1);
    }
    .support_module .bubble{
        max-width: 400px;
        padding: 10px;
        border-radius: 5px;
        position: relative;
        color: #000;
        word-wrap:break-word;
        word-break:normal;
    }
    .support_module .item_left .bubble{
        margin-left: 15px;
        background-color: #fff;
    }
    .support_module .item_left .bubble:before{
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
    .support_module .item_right .bubble{
        margin-right: 15px;
        background-color: #9eea6a;
    }
    .support_module .item_right .bubble:before{
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
    .support_module .item{
        margin-top: 15px;
        display: flex;
        width: 100%;
    }
    .support_module .item.item_right{
        justify-content: flex-end;
				min-width: 400px;
    }
    .support_module .item.item-center{
        justify-content: center;
    }
    .support_module .item.item-center span{
        font-size: 12px;
        padding: 2px 4px;
        color: #fff;
        background-color: #dadada;
        border-radius: 3px;
        -moz-user-select:none; /*火狐*/
        -webkit-user-select:none; /*webkit浏览器*/
        -ms-user-select:none; /*IE10*/
        -khtml-user-select:none; /*早期浏览器*/
        user-select:none;
    }

    .support_module .avatar img{
        width: 42px;
        height: 42px;
        border-radius: 50%;
    }
    .support_module .input-area{
        border-top:0.5px solid #e0e0e0;
        height: 16%;

        background-color: #fff;
    }
    .support_module textarea{
        flex: 1;
        padding: 10px;
        font-size: 14px;
        border: none;
        overflow-y: auto;
        overflow-x: hidden;
        outline:none;
        resize:none;
				width: 102%;
				height: 100%;
				min-height: 100%;
				max-height: 100%;
    }
    .support_module .button-area{
      display: flex;
    height: 50px;
    line-height: 50px;
    padding: 5px;
    justify-content: flex-end;
    text-align: right;
    width: 100%;
		background: #fff;
    }
    .support_module .button-area button{
        width: 80px;
				height: 40px;
				line-height: 40px;
        border: none;
        outline: none;
        border-radius: 4px;
        float: right;
        cursor: pointer;
				background: #9eea6a;
				color: #333;
				margin: 0px;
    }

    /* 设置滚动条的样式 */
    ::-webkit-scrollbar {
        width:10px;
    }
    /* 滚动槽 */
    ::-webkit-scrollbar-track {
        -webkit-box-shadow:inset006pxrgba(0,0,0,0.3);
        border-radius:8px;
    }
    /* 滚动条滑块 */
    ::-webkit-scrollbar-thumb {
        border-radius:10px;
        background:rgba(0,0,0,0);
        -webkit-box-shadow:inset006pxrgba(0,0,0,0.5);
    }

	.sw_no {
	    margin: 0.5rem;
	    display: flex;
	    flex-wrap: wrap;
	}

	.swiper_img {
	    width: 60%;
	    height: 18.75rem;
	}

	.card_notice {
	    width: 40%;
	    padding-left: 1rem;
	    height: 18.75rem;
	}

	.notice_title {
	    font-size: 1.2rem;
	    font-weight: bold;
	    color: white;
	    display: flex;
		justify-content: space-between;
	    align-items: center;
	    background-color: #d2d2d2;
	    height: 3rem;
	    padding: 0 1.5rem;
	}

	.article_recommend > * {
	    display: flex;
	    justify-content: center;
	    align-items: center;
	}

	.article_recommend {
	    display: block;
	    margin: 1.5rem 0.5rem;
	    height: 4rem;
	    border-radius: 0.5rem;
	    background-color: var(--color_primary);
	}

	.diy_recommend > * {
	    display: flex;
	    justify-content: center;
	    align-items: center;
	}

	.diy_recommend {
	    display: block;
	    margin: 1.5rem 0.5rem;
	    height: 4rem;
	    border-radius: 0.5rem;
	    background-color: var(--color_primary);
	}

	.title {
	    float: left;
	    height: 4rem;
	    color: white;
	    font-size: 1.5rem;
	    font-weight: bold;
	    padding-left: 1rem;
	}

	.more_box {
	    float: right;
	    height: 4rem;
	    color: white;
	    font-size: 1.5rem;
	    padding-right: 1rem;
	}

	.more_box .more {
	    border-radius: 0.5rem;
	    border: 0.125rem solid white;
	    display: flex;
	    align-items: center;
	    font-size: 1.2rem;
	    justify-content: center;
	    height: 3rem;
	    width: 3.5rem;
	}

	.switch {
	    float: right;
	    height: 4rem;
	    color: white;
	    padding-right: 1rem;
	}

	.switch_box {
	    border-radius: 0.5rem;
	    border: 0.125rem solid white;
	    display: flex;
	    align-items: center;
	    font-size: 1.2rem;
	    justify-content: center;
	    height: 3rem;
	    width: 6rem;
	}

	.switch_box:hover, .more:hover {
	    background-color: white;
	    color: var(--color_primary) !important;
	}

	.overflow-auto .table th,
	.overflow-auto .table td {
	    text-align: center;
	    text-wrap: normal;
	    font-size: 1rem;
	    vertical-align: middle;
	}

	/*.page_index {*/
	/*    margin: 0 auto;*/
	/*    max-width: 1200px;*/
	/*}*/

	/*.main {*/
	/*    display: flex;*/
	/*    justify-content: space-between;*/
	/*}*/

	/*.content {*/
	/*    flex: 0 0 79%;*/
	/*}*/

	/*.aside {*/
	/*    flex: 0 0 20%;*/
	/*}*/

	.card_ad {
	    margin-top: 1rem;
	}

	@media (max-width: 996px) {
	    .swiper_img {
	        width: 100%;
	        height: 12.5rem;
	    }

	    .card_notice {
	        width: 100%;
	        padding-left: 0;
	    }
	}
.emergency_icon {
  width: 41px;
  height: 41px;
  position: fixed;
  right: 45px;
  bottom: 190px;
  z-index: 9999;
  cursor: pointer;
}

/* 首页：纯白底；区块标题条 */
.page_mall {
	background: #ffffff;
	font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.page_mall.page_root#root_demo {
	background: #ffffff !important;
}

/* 覆盖 diy.css .banner 的 #e5ebe8，轮播整条区域纯白 */
.page_mall .warp.banner.mall-banner {
	background: #ffffff !important;
}

.mall-banner {
	padding-top: 12px;
	padding-bottom: 4px;
}

.page_mall .mall-banner .container {
	max-width: 1200px;
}

/* 轮播在 1200 内容区内拉满，仅保留窄边距；四角圆角 */
.mall-banner__hero {
	width: 100%;
	padding: 0 12px;
	box-sizing: border-box;
	display: block;
}

.mall-banner__swiper {
	width: 100% !important;
	max-width: none;
	margin-left: 0 !important;
	margin-right: 0 !important;
	height: auto !important;
	min-height: 0;
}

.mall-banner__swiper >>> .carousel-hero {
	border-radius: 14px;
	overflow: hidden;
	box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.mall-banner__grid {
	align-items: stretch;
}

.page_mall .mall-section-head {
	display: flex !important;
	align-items: center;
	justify-content: space-between;
	flex-wrap: wrap;
	gap: 12px;
	margin: 1.5rem 0 0.75rem !important;
	padding: 0 6px !important;
	height: auto !important;
	min-height: 0;
	background: transparent !important;
	border: none !important;
	box-shadow: none !important;
}

.page_mall .mall-section-head__title {
	float: none !important;
	display: flex !important;
	align-items: center;
	gap: 10px;
	height: auto !important;
	padding: 0 !important;
	color: #1a1a1a !important;
}

.page_mall .mall-section-head__bar {
	display: inline-block;
	width: 4px;
	height: 20px;
	border-radius: 2px;
	background: #e4393c;
	flex-shrink: 0;
}

.page_mall .mall-section-head__text {
	font-size: 20px;
	font-weight: 700;
	color: #1a1a1a !important;
	line-height: 1.3;
}

.page_mall .mall-section-head .more_box {
	float: none !important;
	height: auto !important;
	padding: 0 !important;
	position: static !important;
	top: auto !important;
	right: auto !important;
	width: auto !important;
	margin: 0 !important;
	background: transparent !important;
	border-radius: 0 !important;
}

/* 覆盖 diy：标题两侧 title_img 花边 */
.page_mall .article_recommend.mall-section-head .title:before,
.page_mall .article_recommend.mall-section-head .title:after,
.page_mall .diy_recommend.mall-section-head .title:before,
.page_mall .diy_recommend.mall-section-head .title:after,
.page_mall .guess_you_like_recommend.mall-section-head .title:before,
.page_mall .guess_you_like_recommend.mall-section-head .title:after {
	display: none !important;
	content: none !important;
	background: none !important;
	background-image: none !important;
	width: 0 !important;
	height: 0 !important;
}

/* 覆盖 diy：标题内 span 的蓝色与过大左右 padding */
.page_mall .mall-section-head .title span.mall-section-head__text {
	color: #1a1a1a !important;
	padding: 0 !important;
}

.page_mall .mall-section-head .title span.mall-section-head__bar {
	padding: 0 !important;
}

/* 覆盖 diy：「更多」蓝底框与伪元素省略号 */
.page_mall .article_recommend.mall-section-head .more_box .more:after,
.page_mall .diy_recommend.mall-section-head .more_box .more:after,
.page_mall .guess_you_like_recommend.mall-section-head .more_box .more:after {
	content: none !important;
}

.guess_you_like_section {
	padding-top: 8px;
}

.guess_you_like_hint {
	margin: -4px 0 14px;
	padding: 0 4px;
	font-size: 13px;
	font-weight: 600;
	color: #666;
	line-height: 1.5;
}

.guess_you_like_hint__cat {
	font-weight: 700;
	color: #333;
}

.guess_you_like_empty {
	margin: 0 4px 24px;
	padding: 28px 16px;
	text-align: center;
	font-size: 14px;
	color: #999;
	background: #fafafa;
	border-radius: 8px;
	border: 1px dashed #e8e8e8;
}

/* 「更多」统一京东红（热点专题、新闻资讯） */
.page_mall .mall-section-head__more,
.page_mall .mall-section-head__more .mor {
	border: none !important;
	background: transparent !important;
	color: #e4393c !important;
	font-size: 14px;
	font-weight: 600;
	width: auto !important;
	height: auto !important;
	min-height: 0;
	padding: 0.25rem 0 !important;
}

.page_mall .mall-section-head__more:hover {
	background: transparent !important;
}

.page_mall .mall-section-head__more:hover .mor {
	text-decoration: none;
	color: #c81623 !important;
}

.page_mall .list_article_box {
	background: transparent;
	border-radius: 0;
	padding: 4px 6px 20px;
	box-shadow: none;
	margin-bottom: 0.25rem;
}

.page_mall .list_news_information_box {
	background: #fff;
	border-radius: 8px;
	padding: 8px 6px 16px;
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
	margin-bottom: 0.5rem;
}

.page_mall.page_root .ins.model1 {
	background: #ffffff !important;
}

.page_mall .warp.model1 {
	background: #ffffff;
}
</style>

<style>
body.page-home-white {
	background-color: #ffffff !important;
}
</style>
