<template>
	<div class="auth-page forgot-page sign_in" id="account_forgot">
		<div class="glass-card glass-card--wide forgot-card">
			<h1 class="auth-title">找回密码</h1>

			<b-form class="auth-forgot-form" autocomplete="off" @submit.prevent="forgot">
				<b-form-group
					label="账号"
					label-for="forgot-username"
					:state="display_username"
					invalid-feedback="账号为 1～16 个字符（支持中文姓名）"
					valid-feedback="校验通过"
				>
					<b-form-input
						id="forgot-username"
						v-model="form.username"
						type="text"
						placeholder="请输入账号"
						trim
						@blur="touch('username')"
					></b-form-input>
				</b-form-group>

				<b-form-group
					label="密码"
					label-for="forgot-password"
					:state="display_password"
					invalid-feedback="密码长度为 6～64 个字符"
					valid-feedback="校验通过"
				>
					<b-form-input
						id="forgot-password"
						v-model="form.password"
						type="password"
						placeholder="请输入新密码"
						trim
						@blur="touch('password')"
					></b-form-input>
				</b-form-group>

				<b-form-group
					label="确认密码"
					label-for="forgot-confirm"
					:state="display_confirm_password"
					invalid-feedback="两次密码不一致"
					valid-feedback="校验通过"
				>
					<b-form-input
						id="forgot-confirm"
						v-model="confirm_password"
						type="password"
						placeholder="请再次输入密码"
						trim
						@blur="touch('confirm_password')"
					></b-form-input>
				</b-form-group>

				<b-form-group
					label="邮箱"
					label-for="forgot-email"
					:state="display_email"
					invalid-feedback="请输入正确的邮箱地址"
					valid-feedback="邮箱格式正确"
				>
					<b-form-input
						id="forgot-email"
						v-model="form.email"
						type="email"
						placeholder="请输入邮箱"
						trim
						@blur="touch('email')"
					></b-form-input>
				</b-form-group>

				<b-form-group
					label="验证码"
					label-for="forgot-code"
					:state="display_code"
					invalid-feedback="请输入验证码"
					valid-feedback="已填写"
				>
					<b-input-group>
						<b-form-input
							id="forgot-code"
							v-model="form.code"
							type="text"
							placeholder="请输入验证码"
							trim
							@blur="touch('code')"
						></b-form-input>
						<b-input-group-append>
							<b-button variant="outline-light" class="send-code-btn" @click="get_code">
								发送验证码
							</b-button>
						</b-input-group-append>
					</b-input-group>
				</b-form-group>

				<div class="auth-btns">
					<button type="submit" class="auth-btn auth-btn--primary" :disabled="loading">
						找回密码
					</button>
				</div>

				<div class="forgot-links">
					<button type="button" class="forgot-link-btn" @click="$router.push('/account/login')">
						返回登录
					</button>
				</div>
			</b-form>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			loading: false,
			form: {
				username: "",
				password: "",
				email: "",
				code: "",
			},
			confirm_password: "",
			token: "",
			submitted: false,
			touched: {
				username: false,
				password: false,
				confirm_password: false,
				email: false,
				code: false,
			},
		};
	},
	computed: {
		display_username() {
			if (!this.touched.username && !this.submitted) return null;
			return this.validation_username;
		},
		display_password() {
			if (!this.touched.password && !this.submitted) return null;
			return this.validation_password;
		},
		display_confirm_password() {
			if (!this.touched.confirm_password && !this.submitted) return null;
			return this.validation_confirm_password;
		},
		display_email() {
			if (!this.touched.email && !this.submitted) return null;
			return this.validation_email;
		},
		display_code() {
			if (!this.touched.code && !this.submitted) return null;
			return this.validation_code;
		},
		validation_username() {
			const u = (this.form.username || "").trim();
			if (!u) return false;
			const len = Array.from(u).length;
			return len >= 1 && len <= 16;
		},
		validation_password() {
			const v = this.form.password || "";
			if (!v) return false;
			return v.length >= 6 && v.length <= 64;
		},
		validation_confirm_password() {
			const v = this.confirm_password || "";
			if (!v) return false;
			return v === this.form.password;
		},
		validation_email() {
			const v = (this.form.email || "").trim();
			if (!v) return false;
			return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
				v
			);
		},
		validation_code() {
			return !!(this.form.code || "").trim();
		},
	},
	methods: {
		touch(field) {
			this.touched[field] = true;
		},
		errorMessage(error) {
			if (!error) return "操作失败";
			return typeof error === "string" ? error : error.message || "操作失败";
		},
		get_code() {
			if (!this.form.username) {
				this.$toast("用户名不能为空!", "error");
				return;
			}
			if (!this.form.email) {
				this.$toast("邮箱不能为空!", "error");
				return;
			}
			if (!this.validation_email) {
				this.$toast("邮箱格式不正确 例：test@test.com", "error");
				return;
			}
			const _this = this;
			_this.$get("~/api/user/get_obj", { username: _this.form.username }, function (user_json) {
				if (user_json.result && user_json.result.obj) {
					if (user_json.result.obj.email === _this.form.email) {
						_this.$get("~/api/code_token/send_email", { email: _this.form.email }, function (json) {
							if (json.result) {
								_this.token = json.token;
								_this.$toast("发送成功！", "success");
							} else if (json.error) {
								_this.$toast(_this.errorMessage(json.error), "error");
							} else {
								_this.$toast("服务器连接失败！");
							}
						});
					} else {
						_this.$toast("用户邮箱不正确！", "error");
					}
				} else {
					_this.$toast("未找到用户！", "error");
				}
			});
		},
		async forgot() {
			this.submitted = true;
			Object.keys(this.touched).forEach((k) => {
				this.touched[k] = true;
			});

			const condition =
				this.validation_username &&
				this.validation_password &&
				this.validation_confirm_password &&
				this.validation_email &&
				this.validation_code;

			if (!condition) {
				this.$toast("输入不合法", "error");
				return;
			}

			if (!this.token) {
				this.$toast("请先发送并填写邮箱验证码", "error");
				return;
			}

			this.loading = true;
			const form = Object.assign({}, this.form);
			try {
				const result = await this.$get("~/api/code_token/verify_email_code", {
					token: this.token,
					code: form.code,
				});
				if (!result.result) {
					this.loading = false;
					if (result.error) {
						this.$toast(this.errorMessage(result.error), "error");
					} else {
						this.$toast("验证码校验失败", "error");
					}
					return;
				}

				this.$post("~/api/user/forget_password?", form, (res) => {
					this.loading = false;
					if (res.result) {
						this.$toast("密码修改成功", "success");
						this.$router.push("/account/login");
					} else if (res.error) {
						this.$toast(this.errorMessage(res.error), "error");
					}
				});
			} catch (e) {
				this.loading = false;
				this.$toast("服务器连接失败！", "error");
			}
		},
	},
};
</script>

<style scoped>
@import "../../../public/css/auth-glass.css";

.forgot-page .forgot-card {
	padding: 32px 36px 28px;
}

.forgot-page .auth-forgot-form {
	width: 100%;
}

.forgot-page {
	--forgot-label-width: 84px;
}

.forgot-page ::v-deep .form-group {
	display: flex;
	flex-wrap: wrap;
	align-items: flex-start;
	margin-bottom: 16px;
}

.forgot-page ::v-deep .form-group > label,
.forgot-page ::v-deep .col-form-label {
	flex-shrink: 0;
	width: var(--forgot-label-width);
	min-width: var(--forgot-label-width);
	margin-bottom: 0;
	padding: 8px 8px 8px 0;
	font-size: 14px;
	line-height: 36px;
	color: rgba(255, 255, 255, 0.96) !important;
	text-align: left !important;
}

.forgot-page ::v-deep .form-group > div:last-child {
	flex: 1;
	min-width: 0;
}

.forgot-page ::v-deep .valid-feedback,
.forgot-page ::v-deep .invalid-feedback {
	display: none;
	margin-top: 6px !important;
	margin-left: calc(-1 * var(--forgot-label-width) - 8px) !important;
	width: calc(100% + var(--forgot-label-width) + 8px) !important;
	padding-left: 0 !important;
	text-align: left;
	font-size: 13px;
	font-weight: 600;
	line-height: 1.45;
	text-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
}

.forgot-page ::v-deep .form-group.is-valid .valid-feedback {
	display: block;
}

.forgot-page ::v-deep .form-group.is-invalid .invalid-feedback {
	display: block;
}

.forgot-page ::v-deep .valid-feedback {
	color: #b9f6ca !important;
}

.forgot-page ::v-deep .invalid-feedback {
	color: #ff8a80 !important;
}

.forgot-page ::v-deep .form-control {
	background: rgba(255, 255, 255, 0.12) !important;
	border: 1px solid rgba(255, 255, 255, 0.38) !important;
	color: #fff !important;
	border-radius: 8px;
	height: 40px;
}

.forgot-page ::v-deep .form-control::placeholder {
	color: rgba(255, 255, 255, 0.55);
}

.forgot-page ::v-deep .form-control:focus {
	border-color: rgba(255, 255, 255, 0.75) !important;
	box-shadow: none;
}

.forgot-page ::v-deep .input-group .form-control {
	border-top-right-radius: 0;
	border-bottom-right-radius: 0;
}

.forgot-page ::v-deep .send-code-btn {
	height: 40px;
	border: 1px solid rgba(255, 255, 255, 0.55) !important;
	color: #fff !important;
	background: rgba(255, 255, 255, 0.15) !important;
	border-top-left-radius: 0;
	border-bottom-left-radius: 0;
	white-space: nowrap;
	font-size: 13px;
	padding: 0 12px;
}

.forgot-page ::v-deep .send-code-btn:hover,
.forgot-page ::v-deep .send-code-btn:focus {
	background: rgba(255, 255, 255, 0.28) !important;
	color: #fff !important;
	box-shadow: none;
}

.forgot-links {
	margin-top: 16px;
	text-align: center;
}

.forgot-link-btn {
	background: none;
	border: none;
	padding: 0;
	color: rgba(255, 255, 255, 0.92);
	font-size: 13px;
	cursor: pointer;
	text-decoration: underline;
}

.forgot-link-btn:hover {
	color: #fff;
}
</style>
