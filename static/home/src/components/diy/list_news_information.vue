<template>
	<div class="diy_home diy_list diy_news_information" id="diy_news_information_list">
		<div v-if="layout === 'jd-text'" class="jd-news-cards jd-news-cards--typo">
			<article
				v-for="(o, i) in localList"
				:key="o.news_information_id != null ? o.news_information_id : i"
				class="jd-news-cards__item"
				@click="toDetails(o)"
			>
				<h3 class="jd-news-cards__title">
					{{ o.news_headlines || "无标题" }}
				</h3>
				<div class="jd-news-cards__meta">
					<span class="jd-news-cards__meta-item">
						<b-icon icon="calendar2-week" class="jd-news-cards__ico" />
						{{ formatNewsDate(o) }}
					</span>
					<span class="jd-news-cards__meta-item">
						<b-icon icon="folder2-open" class="jd-news-cards__ico" />
						{{ o.news_categories || "资讯" }}
					</span>
				</div>
				<p class="jd-news-cards__summary">{{ jdCardSummary(o) }}</p>
				<div class="jd-news-cards__foot">
					<span class="jd-news-cards__more">阅读全文 &gt;</span>
				</div>
			</article>
		</div>
	</div>
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
			choose_date: {
				type: String,
				default: "",
			},
			layout: {
				type: String,
				default: "jd-text",
			},
		},
		data() {
			return {
				localList: [],
				listTimer: null,
			};
		},
		watch: {
			list: {
				immediate: true,
				deep: true,
				handler(newList) {
					this.listTimer && clearTimeout(this.listTimer);
					this.listTimer = setTimeout(() => {
						this.localList = (newList || []).map((l) => ({
							...l,
							checked: false,
							score: l.score || 0,
						}));
					}, 120);
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
			formatNewsDate(o) {
				if (!o) {
					return "";
				}
				if (o.publication_date) {
					return this.$toTime(o.publication_date, "yyyy-MM-dd");
				}
				if (o.create_time) {
					return this.$toTime(o.create_time, "yyyy-MM-dd");
				}
				return "";
			},
			jdCardSummary(o) {
				const max = 120;
				const d = this.stripHtml(o.news_description);
				if (d) {
					return d.length > max ? d.slice(0, max) + "…" : d;
				}
				const b = this.stripHtml(o.news_body || "");
				if (!b) {
					return "";
				}
				return b.length > max ? b.slice(0, max) + "…" : b;
			},
			toDetails(o) {
				const query = { news_information_id: o["news_information_id"] };
				if (this.$props.choose_date) {
					query["choose_date"] = this.$props.choose_date;
				}
				this.$router.push({
					path: `/news_information/details`,
					query,
				});
			},
		},
	};
</script>

<style scoped>
	.jd-news-cards--typo {
		font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif;
	}

	.jd-news-cards {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 20px;
		padding: 4px 2px 8px;
	}

	.jd-news-cards__item {
		background: #fff;
		border-radius: 8px;
		border: 1px solid #eee;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
		padding: 18px 18px 16px;
		cursor: pointer;
		transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
		display: flex;
		flex-direction: column;
		min-height: 200px;
	}

	.jd-news-cards__item:hover {
		transform: translateY(-5px);
		box-shadow: 0 12px 28px rgba(0, 0, 0, 0.14);
		border-color: rgba(228, 57, 60, 0.35);
	}

	.jd-news-cards__title {
		margin: 0 0 10px;
		font-size: 18px;
		font-weight: 700;
		line-height: 1.45;
		color: #000000;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}

	.jd-news-cards__meta {
		display: flex;
		flex-wrap: wrap;
		gap: 14px 18px;
		margin-bottom: 10px;
		font-size: 12px;
		color: #999;
	}

	.jd-news-cards__meta-item {
		display: inline-flex;
		align-items: center;
		gap: 6px;
	}

	.jd-news-cards__ico {
		font-size: 12px;
		opacity: 0.9;
	}

	.jd-news-cards__summary {
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

	.jd-news-cards__foot {
		margin-top: auto;
		padding-top: 4px;
	}

	.jd-news-cards__more {
		font-size: 14px;
		font-weight: 600;
		color: #e4393c;
	}

	@media (max-width: 992px) {
		.jd-news-cards {
			grid-template-columns: repeat(2, 1fr);
			gap: 16px;
		}
	}

	@media (max-width: 576px) {
		.jd-news-cards {
			grid-template-columns: 1fr;
		}
	}
</style>
