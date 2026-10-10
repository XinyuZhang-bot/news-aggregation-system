<template>
	<div class="page_user" id="user_address">
		<div class="warp">
			<div class="container">
				<div class="row justify-content-between">
					<div class="col-12 col-md-3">
						<div class="card_menu">
							<!-- 左侧边栏 -->
							<list_admin_menu_user></list_admin_menu_user>
						</div>
					</div>
					<div class="col-12 col-md-9">
						<div class="card_addres pl-2">
							<!-- 新闻分类 -->
							<div><span>新闻分类</span></div>
							<view_news_class_nameification v-if="$check_action('/news_class_nameification/view','get')"></view_news_class_nameification>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>


<script>
	import list_admin_menu_user from "@/components/diy/list_admin_menu_user.vue";
	import view_news_class_nameification from "../../components/diy/view_news_class_nameification.vue";
	export default {
		data() {
			return {
			};
		},
		mounted() {
		},
		methods: {
		},
		components: {
			list_admin_menu_user,
			view_news_class_nameification,
		},
	};
</script>

<style scoped>
	.container {
		min-height: 800px;
	}
</style>
