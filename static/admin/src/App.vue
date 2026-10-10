<template>
	<div class="app" id="app">
		<div class="page" v-if="$store.state.user.user_id === 0 || url.indexOf($route.path) !== -1 || $route.path.includes('/qrcodeDetails')">
			<router-view />
		</div>
		<div class="page page-dashboard" v-else>
			<div class="tech-bg">
				<div class="tech-orb orb-a"></div>
				<div class="tech-orb orb-b"></div>
				<div class="tech-grid"></div>
			</div>
			<div class="layout-shell">
				<!-- 侧边栏 -->
				<aside class="sidebar-shell">
					<div class="sidebar-brand">
						<div class="brand-title">新闻聚合平台管理端</div>
						<div class="brand-sub">News Admin Console</div>
					</div>
					<page_side :isCollapse="isCollapse"></page_side>
				</aside>
				<!-- 主体 -->
				<main class="content-shell">
					<!-- 页头 -->
					<section class="header-shell">
						<page_header v-model="isCollapse" />
					</section>
					<article :class="{ 'article--home-soft': $route.path === '/' }">
						<transition name="dash-page-fade" mode="out-in">
							<router-view :key="$route.fullPath" />
						</transition>
					</article>
				</main>
			</div>
		</div>
	</div>
</template>

<style>
	@import "../public/css/base.css";
	@import "../public/css/theme.css";

	.mr-1 {
		margin-right: 1rem;
	}

	.quill-editor {
		background: #FFFFFF;
	}

	.ql-editor {
		min-height: 25rem;
	}

	.editor {
		min-height: 500px;
	}

	.el-dialog {
		width: calc(100% - 1rem);
		max-width: 80rem;
	}

	.field_action {
		text-align: center;
	}

	.field_action .el-transfer {
		display: inline-block;
		text-align: left;
	}

	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		-webkit-appearance: none;
	}

	input[type=number] {

		&::-webkit-outer-spin-button,
		&::-webkit-inner-spin-button {
			-webkit-appearance: none;
		}

		-moz-appearance: textfield;
	}

	@media (min-width: 576px) {
		::-webkit-scrollbar-track-piece {
			background-color: #f8f8f8;
		}

		/* 滚动条的宽度 */
		::-webkit-scrollbar {
			width: .5rem;
			height: .5rem;
		}

		/* 滚动条的设置 */
		::-webkit-scrollbar-thumb {
			background-color: rgba(0, 0, 0, 0.5);
			background-clip: padding-box;
			min-height: 1rem;
			border-radius: 0.5rem;
		}
	}

	.avatar-uploader .el-upload-dragger {
		width: 178px;
	}

	table a {
		color: inherit;
		text-decoration: none;
	}

	.el-input {
		max-width: 22.625rem;
	}

	body {
		padding: 0;
		margin: 0;
		background-color: #eef1f6;
		font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
		color: #1f2937;
	}

	main {
		margin: 0 auto;
		overflow-x: hidden;
		width: 100%;
		background: #f3f5f9;
	}


	header i {
		font-size: 1.75rem;
	}

	article {
		box-sizing: border-box;
		height: calc(100vh - 3.375rem);
		padding: 1rem;
		overflow-y: auto;
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		background: #ffffff;
		box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
		color: #111827;
		transition: box-shadow 0.2s ease, border-color 0.2s ease;
	}

	article.article--home-soft {
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		background: #fafbfc;
		box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
	}

	.dash-page-fade-enter-active,
	.dash-page-fade-leave-active {
		transition: opacity 0.22s ease, transform 0.22s ease;
	}

	.dash-page-fade-enter,
	.dash-page-fade-leave-to {
		opacity: 0;
		transform: translateY(6px);
	}

	button i::before {
		font-weight: bold;
	}

	.el-breadcrumb {
		padding: .5rem;
	}


	.page {
		display: flex;
		align-items: stretch;
		width: 100%;
		height: 100%;
	}

	.page-dashboard {
		position: relative;
		overflow: hidden;
	}

	.tech-bg {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 0;
	}

	.tech-grid {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(rgba(15, 23, 42, 0.04) 1px, transparent 1px),
			linear-gradient(90deg, rgba(15, 23, 42, 0.04) 1px, transparent 1px);
		background-size: 28px 28px;
		mask-image: radial-gradient(circle at 50% 30%, rgba(0, 0, 0, 0.06), transparent 85%);
	}

	.tech-orb {
		position: absolute;
		border-radius: 999px;
		filter: blur(40px);
		opacity: 0.35;
	}

	.orb-a {
		width: 360px;
		height: 360px;
		left: -110px;
		top: -100px;
		background: radial-gradient(circle, rgba(37, 99, 235, 0.12) 0%, rgba(37, 99, 235, 0) 72%);
	}

	.orb-b {
		width: 420px;
		height: 420px;
		right: -150px;
		bottom: -140px;
		background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0) 74%);
	}

	.layout-shell {
		position: relative;
		z-index: 1;
		display: flex;
		width: 100%;
		height: 100vh;
		padding: 12px;
		gap: 12px;
		box-sizing: border-box;
	}

	.sidebar-shell {
		display: flex;
		flex-direction: column;
		width: auto;
		min-width: 64px;
		background: #ffffff;
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
		overflow: hidden;
		transition: box-shadow 0.25s ease;
	}

	.sidebar-brand {
		padding: 14px 16px 10px;
		border-bottom: 1px solid #e5e7eb;
		background: #ffffff;
	}

	.brand-title {
		font-size: 15px;
		font-weight: 700;
		color: #111827;
		letter-spacing: 0.5px;
	}

	.brand-sub {
		margin-top: 4px;
		font-size: 11px;
		color: #6b7280;
		letter-spacing: 0.3px;
	}

	.content-shell {
		display: flex;
		flex-direction: column;
		flex: 1;
		min-width: 0;
		background: transparent;
	}

	.header-shell {
		padding-bottom: 10px;
	}

	.app {
		color: #1f2937;
	}

	.btn_full {
		width: 100%;
	}

	.el-table .cell {
		white-space: nowrap;
	}

	.ql-editor {
		height: 300px;
	}

	.diy_panel .el-radio {
		padding: 9px 15px 9px 15px;
	}

	.diy_panel .el-checkbox {
		padding: 9px 15px 9px 15px;
	}

	.bg {
		background: #ffffff;
		border-radius: 12px;
		border: 1px solid #e5e7eb;
		box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
		color: #111827;
	}

	.form.p_4 {
		padding: 1rem;
	}

	/* 通用卡片布局视觉统一（浅色管理端） */
	.el-card,
	.card {
		border-radius: 12px !important;
		border: 1px solid #e5e7eb !important;
		box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06) !important;
		background: #ffffff !important;
		color: #111827;
	}

	.el-table {
		border-radius: 10px;
		overflow: hidden;
		border: 1px solid #e5e7eb;
		background-color: #ffffff !important;
		color: #111827;
	}

	.el-table th {
		background: #f3f4f6 !important;
		color: #374151;
		font-weight: 600;
	}

	.el-table td {
		color: #1f2937;
		background: #ffffff !important;
		border-bottom-color: #e5e7eb !important;
	}

	.el-input__inner,
	.el-textarea__inner,
	.el-select .el-input__inner {
		border-radius: 8px;
		border-color: #d1d5db;
		background: #ffffff;
		color: #111827;
	}

	.el-input__inner:focus,
	.el-textarea__inner:focus {
		border-color: #2563eb;
		box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
	}

	.el-button--primary {
		background: #2563eb;
		border-color: #2563eb;
		box-shadow: none;
	}

	.el-button--primary:hover {
		background: #1d4ed8;
		border-color: #1d4ed8;
		opacity: 1;
	}

	.el-button--default {
		background: #ffffff;
		border-color: #d1d5db;
		color: #374151;
	}

	.el-button--default:hover {
		color: #111827;
		border-color: #2563eb;
		background: #f9fafb;
	}

	.form .el-input {
		width: initial;
	}

	.mt {
		margin-top: 1rem;
	}

	.float-right {
		float: right;
	}

	.mr-1 {
		margin-right: 1rem;
	}

	.el-table .table_class {
		background: rgba(150, 150, 150, 0.1);
		text-align: center;
	}

	.text_center {
		text-align: center;
	}

	.float-right {
		float: right;
	}

	.warp {
		width: 100%;
	}

	.el-col {
		overflow: hidden;
	}

	.ql-picker {
		height: initial !important;
	}

	@import "../public/css/diy.css";

	@media (max-width: 1200px) {
		.layout-shell {
			padding: 8px;
			gap: 8px;
		}
	}

</style>

<script>
	export default {
		data() {
			return {
				isCollapse: false,
				url: ['/login', '/forgot', '/register','/screen/index','/otherLogin']
			}
		},
		methods: {
			init() {
				var token = $.db.get('token');
				if (token) {
					this.$store.commit('user_set', {
						token
					});
				}
			}
		},
    watch: {
      $route(to, from) {
        let currentPath = window.location.hash.slice(1)
        if (this.$route.path !== currentPath) {
          this.$router.push(currentPath)
        }
      }
    },
		created() {
			this.init();
		}
	}
</script>
