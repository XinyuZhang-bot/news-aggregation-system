<template>
	<div class="page_user my_home" id="user_address">
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
							<div class="warp">
								<div class="container-fluid">
									<el-row>
										<div>欢迎来到个人中心</div>
									</el-row>
									<el-row>

          									</el-row>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import list_admin_menu_user from "@/components/diy/list_admin_menu_user.vue";
	export default {
		data() {
			return {
								};
		},
		mounted() {
		},
		methods: {
			async get_nickname(list,flag){
				if (flag) {
					for (let i=0;i<list.length;i++){
						await this.$get(
								"~/api/user/get_obj?user_id="+list[i],
								null,
								(json) => {
									if (json.result) {
										list[i] = json.result.obj.nickname;
									}
								});
					}
				}else {
					for (let i=0;i<list.length;i++){
						await this.$get(
								"~/api/user/get_obj?user_id="+list[i].name,
								null,
								(json) => {
									if (json.result) {
										list[i].name = json.result.obj.nickname;
									}
								});
					}
				}
			},
          		},
		created() {
          		},
		components: {
			list_admin_menu_user
		},
	};
</script>

<style scoped>
	.container {
		min-height: 800px;
	}
	.progress-item {
		width: 100%;
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-bottom: 20px;
	}

	.progress-item .progress-item-content {
		width: 65%;
		display: flex;
		flex-direction: column;
		height: 80px;
		margin-left: 10px;
		font-size: 14px;
	}

	.progress-item .progress-item-content > p {
		margin-bottom: 5px;
	}

	.progress-item .progress-item-content .progress-item-content-progress {
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-top: auto;
	}
</style>
