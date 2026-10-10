<template>
	<div class="auth-page login-page sign_in" id="account_login">
		<div class="glass-card wrapper">
			<form class="login-form" autocomplete="off" @submit.prevent="submit">
				<h1>新闻聚合系统用户端</h1>

				<div class="input-box">
					<span class="field-icon" aria-hidden="true">
						<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
							<path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z" />
						</svg>
					</span>
					<input
						v-model="form.username"
						type="text"
						required
						name="home-login-username"
						autocomplete="off"
						@blur="onUsernameBlur"
					/>
					<label>Username</label>
				</div>
				<p
					v-if="touched.username && usernameCheck.state !== null"
					class="field-hint"
					:class="{ ok: usernameCheck.state === true, err: usernameCheck.state === false }"
				>
					{{ usernameCheck.message }}
				</p>

				<div class="input-box">
					<span class="field-icon" aria-hidden="true">
						<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
							<path d="M18 8h-1V6a5 5 0 0 0-10 0v2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2zM8 6a4 4 0 1 1 8 0v2H8V6zm8 14H8V10h8v10z" />
						</svg>
					</span>
					<button
						type="button"
						class="field-icon field-icon-toggle"
						aria-label="显示或隐藏密码"
						@click.prevent="showPwd"
					>
						<svg v-if="passwordType === 'password'" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
							<path d="M12 6a9.77 9.77 0 0 1 8.82 5.5 9.647 9.647 0 0 1-2.41 3.12l1.41 1.41A11.253 11.253 0 0 0 23 11.5 11.44 11.44 0 0 0 12 4 11.14 11.14 0 0 0 1 11.5a11.3 11.3 0 0 0 1.18 3.41l1.42-1.42A9.77 9.77 0 0 1 12 6zm-1.06 4.47L14.53 14l1.06-1.06-3.59-3.59-1.06 1.12zm-4.24.06a7.98 7.98 0 0 0 0 2.94l1.53-1.53a5.98 5.98 0 0 1 0-2.94L6.7 10.53zM2.59 2.59 1.18 4l2.47 2.47A12.07 12.07 0 0 0 1 11.5 11.44 11.44 0 0 0 12 19a11.8 11.8 0 0 0 4.29-.8l2.91 2.91 1.41-1.41L2.59 2.59zM12 17a7.98 7.98 0 0 1-6.47-3.35l1.53-1.53A5.98 5.98 0 0 0 12 15a6 6 0 0 0 4.24-1.76l1.53 1.53A7.98 7.98 0 0 1 12 17z" />
						</svg>
						<svg v-else viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
							<path d="M12 6a9.77 9.77 0 0 1 8.82 5.5C19.17 14.87 15.79 19 12 19s-7.17-4.13-8.82-7.5A9.77 9.77 0 0 1 12 6m0-2C5.27 4 0 11.5 0 11.5S5.27 19 12 19s12-7.5 12-7.5S18.73 4 12 4zm0 5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9z" />
						</svg>
					</button>
					<input
						v-model="form.password"
						:type="passwordType"
						required
						name="home-login-password"
						autocomplete="new-password"
						@blur="onPasswordBlur"
					/>
					<label>Password</label>
				</div>
				<p
					v-if="touched.password && passwordCheck.state !== null"
					class="field-hint"
					:class="{ ok: passwordCheck.state === true, err: passwordCheck.state === false }"
				>
					{{ passwordCheck.message }}
				</p>

				<div class="geetest_box">
					<div class="geetest_box_title">验证码</div>
					<div class="geetest_box_content">
						<Verification ref="child" />
					</div>
				</div>

				<div class="row">
					<a href="#" @click.prevent="$router.push('/account/forgot')">忘记密码</a>
				</div>

				<button type="submit" class="btn" :disabled="loading">登录</button>

				<div class="signup-link">
					<p>
						没有账号？
						<router-link to="/account/register">点此创建</router-link>
					</p>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import Verification from "@/components/common/verification.vue";
import mixin from "@/mixins/page.js";

export default {
	mixins: [mixin],
	components: {
		Verification,
	},
	data() {
		return {
			loading: false,
			passwordType: "password",
			touched: {
				username: false,
				password: false,
			},
			allow_user: ["管理员", "普通用户", "编辑人员"],
			form: {
				username: "",
				password: "",
			},
			usernameCheck: {
				state: null,
				message: "账号支持中文、英文、数字及其混合，长度 2～16，不能为纯数字",
			},
			passwordCheck: {
				state: null,
				message: "请输入正确密码",
			},
		};
	},
	computed: {
		validation_username() {
			return this.usernameCheck.state;
		},
		validation_password() {
			return this.passwordCheck.state;
		},
		usernameFeedback() {
			return this.usernameCheck.message;
		},
		passwordFeedback() {
			return this.passwordCheck.message;
		},
	},
	watch: {
		"form.username"() {
			this.usernameCheck.state = null;
			this.usernameCheck.message =
				"账号支持中文、英文、数字及其混合，长度 2～16，不能为纯数字";
			this.passwordCheck.state = null;
			this.passwordCheck.message = "请输入正确密码";
		},
		"form.password"() {
			this.passwordCheck.state = null;
			this.passwordCheck.message = "请输入正确密码";
		},
	},
	created() {
		this.form.username = "";
		this.form.password = "";
		this.touched.username = false;
		this.touched.password = false;
	},
	methods: {
		showPwd() {
			this.passwordType = this.passwordType === "password" ? "text" : "password";
		},
		async onUsernameBlur() {
			this.touched.username = true;
			await this.checkUsernameExists();
		},
		async onPasswordBlur() {
			this.touched.password = true;
			await this.checkPasswordOnly();
		},
		getUsernameLength(v) {
			return Array.from((v || "").trim()).length;
		},
		isValidUsernameFormat(v) {
			const value = (v || "").trim();
			if (!value) return false;
			const len = this.getUsernameLength(value);
			if (len < 2 || len > 16) return false;
			if (!/^[A-Za-z0-9\u4e00-\u9fff]+$/.test(value)) return false;
			if (/^\d+$/.test(value)) return false;
			return true;
		},
		isValidPasswordFormat(v) {
			const len = String(v || "").length;
			return len >= 6 && len <= 64;
		},
		async checkUsernameExists() {
			const username = (this.form.username || "").trim();
			if (!username) {
				this.usernameCheck.state = this.touched.username ? false : null;
				this.usernameCheck.message = "请输入账号";
				return false;
			}
			if (!this.isValidUsernameFormat(username)) {
				this.usernameCheck.state = false;
				this.usernameCheck.message =
					"账号需为 2～16 个字符，支持中文/英文/数字混合，但不能为纯数字";
				return false;
			}
			const res = await this.$get("~/api/user/get_obj?", { username, like: 0 });
			const obj = res && res.result ? res.result.obj : null;
			if (obj && obj.username === username) {
				this.usernameCheck.state = true;
				this.usernameCheck.message = "账号存在，可继续登录";
				return true;
			}
			this.usernameCheck.state = false;
			this.usernameCheck.message = "账号不存在，请先注册或检查输入";
			return false;
		},
		async checkPasswordOnly() {
			const password = this.form.password || "";
			if (!password) {
				this.passwordCheck.state = false;
				this.passwordCheck.message = "请输入密码";
				return false;
			}
			if (!this.isValidPasswordFormat(password)) {
				this.passwordCheck.state = false;
				this.passwordCheck.message = "密码长度需为 6～64 个字符";
				return false;
			}
			const username = (this.form.username || "").trim();
			if (!username || !this.isValidUsernameFormat(username)) {
				this.passwordCheck.state = false;
				this.passwordCheck.message = "请先填写正确账号";
				return false;
			}
			const res = await this.$get("~/api/user/get_obj?", {
				username,
				password,
				like: 0,
			});
			const obj = res && res.result ? res.result.obj : null;
			if (obj && obj.username === username) {
				this.passwordCheck.state = true;
				this.passwordCheck.message = "账号密码匹配";
				return true;
			}
			this.passwordCheck.state = false;
			this.passwordCheck.message = "账号或密码错误";
			return false;
		},
		async checkLoginCredential() {
			const usernameOk = await this.checkUsernameExists();
			const passwordOk = await this.checkPasswordOnly();
			return usernameOk && passwordOk;
		},
		async submit() {
			this.touched.username = true;
			this.touched.password = true;
			const bool = this.$refs.child.sublim();
			const usernameOk = await this.checkUsernameExists();
			const passwordOk = await this.checkPasswordOnly();
			if (!usernameOk) {
				return this.$message.warning(this.usernameFeedback || "请输入正确账号");
			}
			if (!passwordOk) {
				return this.$message.warning(this.passwordFeedback || "请输入正确密码");
			}
			if (!bool) {
				return;
			}
			const form = Object.assign({}, this.form, {
				username: (this.form.username || "").trim(),
			});
			this.loading = true;
			this.$post("~/api/user/login?", form, (res) => {
				this.loading = false;
				if (res.result && res.result.obj) {
					var obj = res.result.obj;
					const login_time = new Date()
						.toLocaleString("zh-CN")
						.replace(/\//g, "-")
						.replace(/\s/, " ")
						.split(".")[0];
					this.$post("~/api/user/set?user_id=" + obj.user_id, {
						login_time: login_time,
					});
					obj.login_time = login_time;
					if (this.allow_user.includes(obj.user_group)) {
						$.db.set("token", obj.token);
						this.$store.commit("user_set", obj);
						sessionStorage.setItem("user_id", obj.user_id);
						this.$get_auth(obj.user_group, () => {
							this.$router.push("/");
							location.reload();
						});
						this.$message.success("登录成功！");
					} else {
						this.$message.error("您的账号不支持在用户端登录！");
					}
				} else if (res.error) {
					this.passwordCheck.state = false;
					this.passwordCheck.message = res.error.message || "账号或密码错误";
					this.$message.error(res.error.message);
				}
			});
		},
	},
};
</script>

<style scoped>
@import "../../../public/css/auth-glass.css";

.login-page .wrapper {
	min-height: 480px;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 36px 0 28px;
	max-width: 400px;
}

.login-page .login-form {
	width: 100%;
	padding: 0 45px;
	box-sizing: border-box;
}

.login-page .login-form h1 {
	font-size: 1.25em;
	color: #fff;
	text-align: center;
	margin: 0 0 14px;
	font-weight: 600;
	line-height: 1.35;
}

.login-page .input-box {
	position: relative;
	width: 100%;
	max-width: 310px;
	margin: 24px auto 6px;
	border-bottom: 2px solid rgba(255, 255, 255, 0.85);
}

.login-page .input-box input {
	width: 100%;
	height: 50px;
	background: transparent;
	outline: none;
	border: none;
	font-size: 1em;
	color: #fff;
	padding: 0 72px 0 5px;
	font-family: inherit;
}

.login-page .input-box label {
	position: absolute;
	top: 50%;
	left: 5px;
	transform: translateY(-50%);
	font-size: 1em;
	color: #fff;
	pointer-events: none;
	transition: 0.3s;
}

.login-page .input-box input:focus ~ label,
.login-page .input-box input:valid ~ label {
	top: -5px;
	font-size: 0.85em;
}

.login-page .input-box .field-icon {
	position: absolute;
	right: 8px;
	top: 50%;
	transform: translateY(-50%);
	color: #fff;
	line-height: 0;
	cursor: default;
	width: auto !important;
	height: auto;
	background: none !important;
	background-size: unset !important;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	border: none;
	padding: 0;
}

.login-page .input-box .field-icon-toggle {
	right: 36px;
	cursor: pointer;
	background: transparent !important;
}

.login-page .input-box input:-webkit-autofill,
.login-page .input-box input:-webkit-autofill:hover,
.login-page .input-box input:-webkit-autofill:focus,
.login-page .input-box input:-webkit-autofill:active {
	-webkit-box-shadow: 0 0 0 1000px transparent inset !important;
	box-shadow: 0 0 0 1000px transparent inset !important;
	-webkit-text-fill-color: #fff !important;
	caret-color: #fff;
	transition: background-color 99999s ease-out 0s;
}

.login-page .field-hint {
	width: 100%;
	max-width: 310px;
	margin: 0 auto 4px;
	font-size: 0.8em;
	line-height: 1.4;
	color: rgba(255, 255, 255, 0.85);
	text-align: left;
	font-weight: 600;
	text-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
}

.login-page .field-hint.ok {
	color: #b9f6ca;
}

.login-page .field-hint.err {
	color: #ff8a80;
}

.login-page .geetest_box {
	width: 100%;
	max-width: 310px;
	margin: 16px auto 8px;
	display: flex;
	flex-direction: row;
	flex-wrap: nowrap;
	align-items: center;
	gap: 10px;
}

.login-page .geetest_box_title {
	flex-shrink: 0;
	width: auto !important;
	min-width: 4.5em;
	white-space: nowrap;
	font-size: 0.9em;
	color: #fff;
	text-align: left;
	line-height: 1.4;
}

.login-page .geetest_box_title::before {
	content: "*";
	color: #ff3131;
	margin-right: 4px;
}

.login-page .geetest_box_content {
	flex: 1;
	min-width: 0;
	width: 100%;
}

.login-page ::v-deep .geetest_box_content .verification-wrap {
	width: 100%;
}

.login-page .row {
	width: 100%;
	max-width: 310px;
	margin: 8px auto 12px;
	font-size: 0.9em;
	color: #fff;
	display: flex;
	justify-content: flex-start;
}

.login-page .row a {
	color: #fff;
	text-decoration: none;
	cursor: pointer;
}

.login-page .row a:hover {
	text-decoration: underline;
}

.login-page .btn {
	display: block;
	width: 100%;
	max-width: 310px;
	margin: 10px auto 0;
	height: 40px;
	background: #fff;
	outline: none;
	border: none;
	border-radius: 40px;
	cursor: pointer;
	font-size: 1em;
	font-weight: 500;
	color: #000;
	font-family: inherit;
	transition: background 0.2s;
}

.login-page .btn:hover:not(:disabled) {
	background: #ffffea;
}

.login-page .btn:disabled {
	opacity: 0.7;
	cursor: not-allowed;
}

.login-page .signup-link {
	font-size: 0.9em;
	color: #fff;
	text-align: center;
	margin: 20px 0 0;
}

.login-page .signup-link a {
	color: #fff;
	text-decoration: none;
	font-weight: 600;
}

.login-page .signup-link a:hover {
	text-decoration: underline;
}

.login-page ::v-deep .geetest_box_content .el-input__inner {
	background: rgba(255, 255, 255, 0.22) !important;
	border: 1px solid rgba(255, 255, 255, 0.65) !important;
	color: #fff !important;
}

.login-page ::v-deep .geetest_box_content .el-input__inner::placeholder {
	color: rgba(255, 255, 255, 0.75) !important;
}

.login-page ::v-deep #canvas {
	border: 1px solid rgba(255, 255, 255, 0.85) !important;
	border-radius: 6px;
	background-color: #ffffff !important;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
}

@media (max-width: 360px) {
	.login-page .wrapper {
		width: 100%;
		min-height: 100vh;
		border: none;
		border-radius: 0;
	}

	.login-page .login-form {
		padding: 0 24px;
	}
}
</style>
