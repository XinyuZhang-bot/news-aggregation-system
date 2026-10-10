<template>
	<div class="page_user user_password" id="user_password">
		<div class="warp">
			<div class="container">
				<div class="row justify-content-between">
					<!-- 左侧边栏
					<div class="col-12 col-md-3">
						<div class="card_menu">

							<list_menu_user :list_info="list_info"></list_menu_user>
						</div>
					</div>
					-->
					<div class="col-12 col-md-9">
						<div class="card_password pl-2">
							<div>密码修改</div>
							<!-- 密码修改 -->
							<b-form class="card_pass_form">
								<b-form-group id="input-group-2" label="输入原始密码:" label-for="input-2"
									:state="validation_o_password" invalid-feedback="密码长度为在6-16个字符"
									valid-feedback="校验通过">
									<b-form-input id="input-2" v-model="form.o_password" type="password"
										placeholder="原始密码" trim></b-form-input>
								</b-form-group>
																<b-form-group id="input-group-2" label="设置新密码:" label-for="input-2"
									:state="validation_password" invalid-feedback="密码长度为在6-16个字符" valid-feedback="校验通过">
									<b-form-input id="input-2" v-model="form.password" type="password"
										placeholder="设置新密码" trim></b-form-input>
								</b-form-group>
																<b-form-group id="input-group-2" label="确认密码:" label-for="input-2"
									:state="validation_confirm_password" invalid-feedback="密码不一致" valid-feedback="">
									<b-form-input id="input-2" v-model="confirm_password" type="password"
										placeholder="确认密码" trim></b-form-input>
								</b-form-group>
							</b-form>
							<div class="password_confim">
								<div class="btn_item" @click="change_password()"><span>确认修改</span></div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import mixin from "@/mixins/page.js";
	// import list_menu_user from "@/components/diy/list_menu_user.vue";

	export default {
		mixins: [mixin],

		data() {
			return {
				form: {
					o_password: "",
					password: "",
				},

				confirm_password: "",

				list_info: [{
						title: "个人资料",
						url: "/user/info",
						icon: "house-fill",
						selected: false,
					},
					{
						title: "密码修改",
						url: "/user/password",
						icon: "person-fill",
						selected: true,
					},

					{
						title: "收藏",
						url: "/user/collect",
						icon: "heart-fill",
						selected: false,
					},

				],
			};
		},
		computed: {
			/**
			 * 验证原始密码
			 */
			validation_o_password() {
				var length = this.form.o_password.length;
				if (!length) {
					return null;
				}
				return length >= 6 && length < 16;
			},
			/**
			 * 验证密码
			 */
			validation_password() {
				var length = this.form.password.length;
				if (!length) {
					return null;
				}
							return length >= 6 && length < 16;
						},
			/**
			 * 再次验证密码
			 */
			validation_confirm_password() {
				return this.confirm_password === this.form.password;
			},
		},
		methods: {
			submit_check() {
				if(!this.form.password){
					return "密码不能为空!";
				}
								if(this.form.password.length > 16 || this.form.password.length < 6){
					return "密码长度应为6到16个字符之间！";
				}
								if (this.form.password !== this.confirm_password) {
					return "密码和确认密码不一致！"
				}
				return null;
			},
			/**
			 * 修改密码
			 */
			change_password() {
				let msg = this.submit_check();
				if (msg){
					this.$toast(msg,"error");
					return
				}
				var form = Object.assign({},this.form);

				if(this.form.password === this.confirm_password && this.form.o_password){
					this.$post("~/api/user/change_password?", form, (res) => {
						if (res.result) {
							//弹出更改成功，3秒后调到主页，退出账户
							this.$store.commit("sign_out");
							this.$router.push("/account/login")
						} else if (res.error) {
							console.log(res.error);
							this.$toast(res.error.message,"error");
						}
					});
				}
			},
		},
		components: {
			// list_menu_user,
		},
		mounted() {
			// console.log(this.user);
		},
	};
</script>

<style scoped>
	.container {
		min-height: 800px;
	}

	.btn_item {
		cursor: pointer;
		width: 100%;
		background-color: var(--color_primary);
		color: #fff;
		text-align: center;
		height: 48px;
		line-height: 48px;
	}

	.card_password {
		padding: 10px;
		width: 500px;
		margin: auto;
	}

	.password-strength-container {
		margin-top: 10px;
		padding: 12px;
		border: 1px solid #e9ecef;
		border-radius: 6px;
		background-color: #f8f9fa;
	}

	.password-strength-label {
		font-size: 14px;
		font-weight: 600;
		margin-bottom: 8px;
		color: #495057;
	}

	.password-strength-indicator {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 12px;
	}

	.strength-text {
		font-size: 14px;
		font-weight: 600;
		min-width: 30px;
	}

	.strength-text.weak {
		color: #dc3545;
	}

	.strength-text.medium {
		color: #fd7e14;
	}

	.strength-text.strong {
		color: #28a745;
	}

	.strength-bar {
		flex: 1;
		height: 8px;
		background-color: #e9ecef;
		border-radius: 4px;
		overflow: hidden;
	}

	.strength-fill {
		height: 100%;
		transition: width 0.3s ease, background-color 0.3s ease;
		border-radius: 4px;
	}

	.strength-fill.weak {
		background-color: #dc3545;
	}

	.strength-fill.medium {
		background-color: #fd7e14;
	}

	.strength-fill.strong {
		background-color: #28a745;
	}

	.password-requirements {
		font-size: 12px;
	}

	.requirement {
		color: #6c757d;
		margin-bottom: 4px;
		transition: color 0.3s ease;
	}

	.requirement.met {
		color: #28a745;
	}

	.requirement-note {
		color: #6c757d;
		font-style: italic;
		margin-top: 6px;
		font-size: 11px;
	}
</style>
