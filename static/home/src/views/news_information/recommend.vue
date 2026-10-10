<template>
	<div class="diy_list page_news_information page_news_information--jd page_news_recommend" id="news_information_recommend">
		<div class="warp jd-news-page">
			<div class="container diy_list_container">
				<div class="jd-page-title">
					<span class="jd-page-title__line" aria-hidden="true"></span>
					<span class="jd-page-title__text">猜你喜欢</span>
					<span class="jd-page-title__line" aria-hidden="true"></span>
				</div>

				<p class="recommend-page-hint" v-if="hint_guest">
					登录后将根据您的浏览、收藏与点赞偏好为您推荐个性化新闻
				</p>
				<p class="recommend-page-hint" v-else-if="show_hint">
					根据您的浏览、收藏与点赞偏好为您推荐<strong class="recommend-page-hint__cat">{{ hint_cats }}</strong>类新闻
				</p>

				<div class="row diy_list_box jd-list-wrap">
					<div class="col">
						<list_news_information :list="list" layout="jd-text" />
					</div>
				</div>

				<p class="recommend-page-empty" v-if="!loading && count === 0">暂无推荐内容</p>

				<div class="row diy_list_page_box jd-pagination-wrap" v-if="count > 0">
					<div class="col overflow-auto flex_cc">
						<b-pagination
							v-model="query.page"
							:total-rows="count"
							:per-page="query.size"
							@change="goToPage"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import list_news_information from "@/components/diy/list_news_information.vue";
	import mixin from "@/mixins/page.js";

	export default {
		mixins: [mixin],
		components: {
			list_news_information,
		},
		data() {
			return {
				url_get_list: "~/api/news_information/get_hits_list",
				query: {
					page: 1,
					size: 12,
				},
				hint_cats: "热门",
				show_hint: false,
				hint_guest: false,
			};
		},
		methods: {
			_resolve_user_id() {
				const fromStore = this.$store.state.user && this.$store.state.user.user_id;
				if (fromStore) {
					return String(fromStore);
				}
				const fromSession = sessionStorage.getItem("user_id");
				return fromSession ? String(fromSession) : "";
			},

			_set_hint(categoryInput) {
				let list = [];
				if (Array.isArray(categoryInput)) {
					list = categoryInput;
				} else {
					list = String(categoryInput || "")
						.split("、")
						.map((s) => s.trim())
						.filter(Boolean);
				}
				this.hint_cats = list.slice(0, 2).join("、") || "热门";
				this.show_hint = true;
				this.hint_guest = false;
			},

			load_recommend_hint(user_id) {
				if (!user_id) {
					this.show_hint = false;
					this.hint_guest = true;
					return;
				}
				this.hint_guest = false;
				this._set_hint("热门");
				this.$get("~/api/news_information/recommend_advice?", { user_id }, (adv) => {
					if (!adv.result) {
						return;
					}
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
						this._set_hint(cats);
					}
				});
			},

			get_list_before(param) {
				const user_id = this._resolve_user_id();
				param.user_id = user_id;
				this.load_recommend_hint(user_id);
				return param;
			},

			goToPage(v) {
				this.query.page = v;
				this.goToNew(v);
			},
		},
	};
</script>

<style scoped>
.jd-news-page {
	background: #f4f4f4;
	padding-bottom: 2rem;
}

.page_news_information--jd .diy_list_container {
	max-width: 1200px;
}

.jd-page-title {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 16px;
	margin: 28px 0 24px;
}

.jd-page-title__line {
	flex: 1;
	height: 1px;
	background: linear-gradient(90deg, transparent, #ddd 20%, #ddd 80%, transparent);
	max-width: 120px;
}

.jd-page-title__text {
	font-size: 22px;
	font-weight: 700;
	color: #1a1a1a;
	white-space: nowrap;
}

.jd-list-wrap {
	margin-top: 4px;
}

.jd-list-wrap .col {
	background: transparent;
	padding-left: 0;
	padding-right: 0;
}

.jd-pagination-wrap {
	margin-top: 28px;
}

.recommend-page-hint {
	text-align: center;
	color: #666;
	font-size: 14px;
	margin: -8px 0 20px;
	line-height: 1.6;
}

.recommend-page-hint__cat {
	font-weight: 600;
	color: #1a1a1a;
}

.recommend-page-empty {
	text-align: center;
	color: #999;
	padding: 48px 0;
	font-size: 15px;
}

.page_news_information--jd >>> .pagination {
	margin-bottom: 0;
}

.page_news_information--jd >>> .page-link {
	border-radius: 8px;
	margin: 0 4px;
	color: #666;
	border: 1px solid #e0e0e0;
	min-width: 40px;
	text-align: center;
}

.page_news_information--jd >>> .page-item.active .page-link {
	background-color: #e4393c !important;
	border-color: #e4393c !important;
	color: #fff !important;
}

.page_news_information--jd >>> .page-item .page-link:hover {
	color: #e4393c;
	border-color: #e4393c;
	background: #fff5f5;
}
</style>
