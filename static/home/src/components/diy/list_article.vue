<template>
	<nav v-if="layout === 'jd-text'" class="jd-article-cards jd-article-cards--typo">
		<router-link
			class="jd-article-cards__item"
			v-for="(o, i) in list"
			:key="i"
			:to="'/article/details?' + vm.article_id + '=' + o[vm.article_id]"
		>
			<div class="jd-article-cards__head">
				<span v-if="tagLabel(o)" class="jd-article-cards__tag" :class="tagClass(o)">{{ tagLabel(o) }}</span>
				<h3 class="jd-article-cards__title">
					{{ o[vm.title] }}
				</h3>
			</div>
			<div class="jd-article-cards__meta">
				<span class="jd-article-cards__meta-item">
					<b-icon icon="clock" class="jd-article-cards__ico" />
					{{ formatRelative(o[vm.create_time]) }}
				</span>
				<span class="jd-article-cards__meta-item">
					<b-icon icon="eye" class="jd-article-cards__ico" />
					{{ formatHits(o[vm.hits]) }}
				</span>
			</div>
			<p class="jd-article-cards__summary">{{ cardSummary(o) }}</p>
			<div class="jd-article-cards__foot">
				<span class="jd-article-cards__more">阅读全文 &gt;</span>
			</div>
		</router-link>
	</nav>
	<nav v-else-if="layout === 'hot'" class="list_article hot-article-grid">
		<router-link
			class="hot-card"
			v-for="(o, i) in list"
			:key="i"
			:to="'/article/details?' + vm.article_id + '=' + o[vm.article_id]"
		>
			<div class="hot-card__media">
				<span v-if="tagLabel(o)" class="article-tag hot-card__tag" :class="tagClass(o)">{{ tagLabel(o) }}</span>
				<img
					:src="o[vm.img] ? $fullUrl(o[vm.img]) : '../../../public/img/default.png'"
					v-default-img="'../../../public/img/default.png'"
					alt=""
				/>
			</div>
			<div class="hot-card__body">
				<p class="hot-card__summary">{{ cardSummary(o) }}</p>
				<div class="hot-card__meta">
					<span class="hot-card__meta-item">
						<b-icon icon="clock" class="hot-card__ico" />
						{{ formatRelative(o[vm.create_time]) }}
					</span>
					<span class="hot-card__meta-item">
						<b-icon icon="eye" class="hot-card__ico" />
						{{ formatHits(o[vm.hits]) }}
					</span>
				</div>
				<h3 class="hot-card__title">
					{{ o[vm.title] }}
				</h3>
			</div>
		</router-link>
	</nav>
	<nav v-else class="list_article list list-x item-tb jd-article-grid">
		<router-link
			class="article_warp"
			v-for="(o, i) in list"
			:key="i"
			:to="'/article/details?' + vm.article_id + '=' + o[vm.article_id]"
		>
			<div class="article">
				<div class="media">
					<div class="icon">
						<span v-if="tagLabel(o)" class="article-tag" :class="tagClass(o)">{{ tagLabel(o) }}</span>
						<img
							:src="o[vm.img] ? $fullUrl(o[vm.img]) : '../../../public/img/default.png'"
							v-default-img="'../../../public/img/default.png'"
							alt=""
						/>
					</div>
				</div>
				<div class="doc">
					<div class="title ellipsis_2 article-title">
						{{ o[vm.title] }}
					</div>
					<p class="article-summary ellipsis_2">{{ cardSummary(o) }}</p>
					<div class="article-footer">
						<span class="article-footer__meta">
							<b-icon icon="clock" class="article-footer__ico" />
							{{ formatRelative(o[vm.create_time]) }}
						</span>
						<span class="article-footer__meta">
							<b-icon icon="eye" class="article-footer__ico" />
							{{ formatHits(o[vm.hits]) }}
						</span>
					</div>
				</div>
			</div>
		</router-link>
	</nav>
</template>

<script>
export default {
	props: {
		list: {
			type: Array,
			default: function () {
				return [];
			},
		},
		layout: {
			type: String,
			default: "image",
		},
		vm: {
			type: Object,
			default: function () {
				return {
					img: "img",
					article_id: "article_id",
					title: "title",
					type: "type",
					description: "description",
					create_time: "create_time",
					content: "content",
					praise_len: "praise_len",
					hits: "hits",
				};
			},
		},
	},
	methods: {
		stripHtml(s) {
			if (s == null || s === "") {
				return "";
			}
			return String(s)
				.replace(/<[^>]+>/g, " ")
				.replace(/\s+/g, " ")
				.trim();
		},
		cardSummary(o) {
			const d = this.stripHtml(o[this.vm.description]);
			if (d) {
				return d;
			}
			const c = this.stripHtml(o[this.vm.content]);
			return c ? c.slice(0, 120) : "";
		},
		formatHits(n) {
			const v = Number(n) || 0;
			if (v >= 10000) {
				const w = v / 10000;
				const t = w >= 10 ? w.toFixed(0) : w.toFixed(1).replace(/\.0$/, "");
				return t + "万";
			}
			return String(v);
		},
		formatRelative(val) {
			if (!val) {
				return "";
			}
			const t = new Date(val).getTime();
			if (Number.isNaN(t)) {
				return "";
			}
			const sec = Math.floor((Date.now() - t) / 1000);
			if (sec < 60) {
				return "刚刚";
			}
			if (sec < 3600) {
				return Math.floor(sec / 60) + "分钟前";
			}
			if (sec < 86400) {
				return Math.floor(sec / 3600) + "小时前";
			}
			if (sec < 172800) {
				return "昨天";
			}
			if (sec < 86400 * 7) {
				return Math.floor(sec / 86400) + "天前";
			}
			return this.$toTime(val, "yyyy-MM-dd");
		},
		tagLabel(o) {
			const t = String(o[this.vm.type] || "").trim();
			if (!t) {
				return "热点";
			}
			return t.length > 4 ? t.slice(0, 4) : t;
		},
		tagClass(o) {
			const t = String(o[this.vm.type] || "");
			if (/财经/.test(t)) {
				return "article-tag--finance";
			}
			if (/科技|技术|互联网|AI|数码/.test(t)) {
				return "article-tag--tech";
			}
			if (/民生/.test(t)) {
				return "article-tag--people";
			}
			return "article-tag--hot";
		},
	},
};
</script>

<style scoped>
/* 首页热点专题：左图右文，2×3 网格 */
.hot-article-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 18px 20px;
	margin: 0;
	padding: 4px 2px 12px;
	font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.hot-card {
	display: flex;
	flex-direction: row;
	align-items: stretch;
	background: #fff;
	border: 1px solid #e8e8e8;
	border-radius: 14px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.07);
	overflow: hidden;
	text-decoration: none !important;
	color: inherit !important;
	transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
	min-height: 128px;
}

.hot-card:hover {
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
	transform: translateY(-2px);
	border-color: rgba(228, 57, 60, 0.25);
}

.hot-card__media {
	position: relative;
	flex: 0 0 38%;
	max-width: 42%;
	min-height: 120px;
	background: #f0f0f0;
	overflow: hidden;
}

.hot-card__media img {
	display: block;
	width: 100%;
	height: 100%;
	min-height: 120px;
	object-fit: cover;
}

.hot-card__tag.article-tag {
	top: 8px;
	left: 8px;
}

.hot-card__body {
	flex: 1;
	min-width: 0;
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	gap: 6px;
	padding: 12px 14px 14px 12px;
}

.hot-card__summary {
	margin: 0;
	font-size: 13px;
	line-height: 1.55;
	color: #666;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.hot-card__meta {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	justify-content: space-between;
	gap: 6px 10px;
	font-size: 12px;
	color: #999;
}

.hot-card__meta-item {
	display: inline-flex;
	align-items: center;
	gap: 4px;
}

.hot-card__ico {
	font-size: 12px;
	opacity: 0.9;
}

.hot-card__title {
	margin: 0;
	margin-top: auto;
	font-size: 16px;
	font-weight: 700;
	line-height: 1.4;
	color: #000000;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}


@media (max-width: 576px) {
	.hot-article-grid {
		grid-template-columns: 1fr;
	}

	.hot-card__media {
		flex: 0 0 36%;
		max-width: 44%;
	}
}

.jd-article-cards--typo {
	font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.jd-article-cards {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 20px;
	padding: 4px 2px 8px;
	margin: 0;
}

.jd-article-cards__item {
	background: #fff;
	border-radius: 8px;
	border: 1px solid #eee;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
	padding: 18px 18px 16px;
	text-decoration: none !important;
	color: inherit !important;
	cursor: pointer;
	transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
	display: flex;
	flex-direction: column;
	min-height: 200px;
	box-sizing: border-box;
}

.jd-article-cards__item:hover {
	transform: translateY(-4px);
	box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
	border-color: rgba(228, 57, 60, 0.35);
}

.jd-article-cards__head {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	gap: 8px;
	margin-bottom: 8px;
}

.jd-article-cards__tag {
	display: inline-block;
	padding: 2px 10px;
	border-radius: 4px;
	font-size: 12px;
	font-weight: 600;
	color: #fff;
	line-height: 1.3;
}

.jd-article-cards__tag.article-tag--hot {
	background: #e4393c;
}

.jd-article-cards__tag.article-tag--tech {
	background: #43a047;
}

.jd-article-cards__tag.article-tag--people {
	background: #1e88e5;
}

.jd-article-cards__tag.article-tag--finance {
	background: #f9a825;
	color: #333;
}

.jd-article-cards__title {
	margin: 0;
	font-size: 18px;
	font-weight: 700;
	line-height: 1.45;
	color: #000000;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}


.jd-article-cards__meta {
	display: flex;
	flex-wrap: wrap;
	gap: 14px 18px;
	margin-bottom: 10px;
	font-size: 12px;
	color: #999;
}

.jd-article-cards__meta-item {
	display: inline-flex;
	align-items: center;
	gap: 6px;
}

.jd-article-cards__ico {
	font-size: 12px;
	opacity: 0.9;
}

.jd-article-cards__summary {
	margin: 0 0 12px;
	flex: 1;
	font-size: 14px;
	line-height: 1.6;
	color: #666;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.jd-article-cards__foot {
	margin-top: auto;
	padding-top: 4px;
}

.jd-article-cards__more {
	font-size: 14px;
	font-weight: 600;
	color: #e4393c;
}

@media (max-width: 992px) {
	.jd-article-cards {
		grid-template-columns: repeat(2, 1fr);
		gap: 16px;
	}
}

@media (max-width: 576px) {
	.jd-article-cards {
		grid-template-columns: 1fr;
	}
}

.jd-article-grid {
	font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.icon {
	position: relative;
	overflow: hidden;
	border-radius: 8px 8px 0 0;
}

.icon img {
	display: block;
	width: 100%;
	vertical-align: middle;
}

.article-tag {
	position: absolute;
	top: 10px;
	left: 10px;
	z-index: 2;
	padding: 3px 10px;
	border-radius: 4px;
	font-size: 12px;
	font-weight: 600;
	color: #fff;
	line-height: 1.2;
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.article-tag--hot {
	background: #e4393c;
}

.article-tag--tech {
	background: #43a047;
}

.article-tag--people {
	background: #1e88e5;
}

.article-tag--finance {
	background: #f9a825;
	color: #333;
}

.article-title {
	font-size: 18px;
	font-weight: 700 !important;
	color: #000000 !important;
	line-height: 1.45;
	min-height: 2.45rem;
}


.article-summary {
	margin: 8px 0 10px;
	font-size: 14px;
	line-height: 1.6;
	color: #666;
	min-height: 2.6rem;
}

.article-footer {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-top: auto;
	padding-top: 6px;
	font-size: 12px;
	color: #999;
}

.article-footer__meta {
	display: inline-flex;
	align-items: center;
	gap: 4px;
}

.article-footer__ico {
	font-size: 12px;
	opacity: 0.9;
}

.article_warp {
	display: flex;
	width: calc(33.333% - 1rem);
	margin: 0.5rem;
	flex-direction: column;
	justify-content: space-between;
	background-color: #fff;
	border-radius: 8px;
	border: 1px solid #eee;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
	transition: box-shadow 0.22s ease, transform 0.22s ease, border-color 0.22s ease;
}

.article_warp:hover {
	border-color: rgba(228, 57, 60, 0.45);
	box-shadow: 0 12px 28px rgba(0, 0, 0, 0.14);
	transform: translateY(-5px);
}

.article_warp:hover img {
	filter: none;
}

.article {
	width: 100%;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

.doc {
	padding: 12px 14px 14px;
	display: flex;
	flex-direction: column;
	flex: 1;
}

.ellipsis_2 {
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
}

@media (max-width: 992px) {
	.article_warp {
		width: calc(33% - 1rem);
	}
}

@media (max-width: 768px) {
	.article_warp {
		width: calc(50% - 1rem);
	}
}
</style>
