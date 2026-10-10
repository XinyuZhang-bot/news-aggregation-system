<template>
	<div class="auth-page login-page sign_in">
		<div class="glass-card wrapper">
			<form class="login-form" autocomplete="off" @submit.prevent="sign_in">
				<h1>新闻聚合系统后台端</h1>

				<div class="input-box">
					<i class="fas fa-envelope icon"></i>
					<input
						v-model="form.account"
						type="text"
						required
						name="login-username"
						autocomplete="off"
						@blur="onAccountBlur"
					/>
					<label>Username</label>
				</div>
				<p
					v-if="touched.account && accountCheck.state !== null"
					class="field-hint"
					:class="{ ok: accountCheck.state === true, err: accountCheck.state === false }"
				>
					{{ accountCheck.message }}
				</p>

				<div class="input-box">
					<i class="fas fa-lock icon"></i>
					<i
						class="fas icon icon-toggle"
						:class="passwordType === 'text' ? 'fa-eye' : 'fa-eye-slash'"
						@click.prevent="showPwd"
					></i>
					<input
						v-model="form.password"
						:type="passwordType"
						required
						name="login-password"
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
					<a href="#" @click.prevent="$router.push('./forgot')">忘记密码</a>
				</div>

				<button type="submit" class="btn" :disabled="loading">登录</button>

				<div class="signup-link">
					<p>
						没有账号？
						<router-link to="/register">点此创建</router-link>
					</p>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import Verification from "@/components/common/verification.vue";

export default {
	components: {
		Verification,
	},
	data() {
		return {
			passwordType: "password",
			loading: false,
			allow_user: ["管理员", "编辑人员"],
			form: {
				account: "",
				password: "",
			},
			accountCheck: {
				state: null,
				message: "",
			},
			passwordCheck: {
				state: null,
				message: "",
			},
			touched: {
				account: false,
				password: false,
			},
			remember_me: 1,
		};
	},
	watch: {
		"form.account"() {
			this.accountCheck.state = null;
			this.accountCheck.message = "";
			this.passwordCheck.state = null;
			this.passwordCheck.message = "";
		},
		"form.password"() {
			this.passwordCheck.state = null;
			this.passwordCheck.message = "";
		},
	},
	created() {
		this.form.account = "";
		this.form.password = "";
		this.touched.account = false;
		this.touched.password = false;
	},
	methods: {
		async onAccountBlur() {
			this.touched.account = true;
			await this.checkAccountExists();
		},
		async onPasswordBlur() {
			this.touched.password = true;
			await this.checkPasswordOnly();
		},
		showPwd() {
			this.passwordType = this.passwordType === "password" ? "text" : "password";
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
		async checkAccountExists() {
			const username = (this.form.account || "").trim();
			if (!username) {
				this.accountCheck.state = this.touched.account ? false : null;
				this.accountCheck.message = "请输入账号";
				return false;
			}
			if (!this.isValidUsernameFormat(username)) {
				this.accountCheck.state = false;
				this.accountCheck.message = "账号或密码有误，请重新输入";
				return false;
			}
			const res = await this.$get("~/api/user/get_obj?", { username, like: 0 });
			const obj = res && res.result ? res.result.obj : null;
			if (obj && obj.username === username) {
				this.accountCheck.state = true;
				this.accountCheck.message = "账号存在，可以登录";
				return true;
			}
			this.accountCheck.state = false;
			this.accountCheck.message = "账号或密码有误，请重新输入";
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
				this.passwordCheck.message = "账号或密码有误，请重新输入";
				return false;
			}
			const username = (this.form.account || "").trim();
			if (!username || !this.isValidUsernameFormat(username)) {
				this.passwordCheck.state = false;
				this.passwordCheck.message = "账号或密码有误，请重新输入";
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
				this.passwordCheck.message = "密码正确";
				return true;
			}
			this.passwordCheck.state = false;
			this.passwordCheck.message = "账号或密码有误，请重新输入";
			return false;
		},
		async checkLoginCredential() {
			const accountOk = await this.checkAccountExists();
			const passwordOk = await this.checkPasswordOnly();
			return accountOk && passwordOk;
		},
		async sign_in() {
			this.touched.account = true;
			this.touched.password = true;
			const bool = this.$refs.child.sublim();
			const accountOk = await this.checkAccountExists();
			const passwordOk = await this.checkPasswordOnly();
			if (!accountOk) {
				return this.$message.warning(this.accountCheck.message || "请输入正确账号");
			}
			if (!passwordOk) {
				return this.$message.warning(this.passwordCheck.message || "请输入正确密码");
			}
			if (!bool) {
				return;
			}

			const form = {
				username: (this.form.account || "").trim(),
				password: this.form.password,
			};
			const account = form.username;
			const _this = this;
			this.loading = true;

			this.$post("~/api/user/login?", form, (res) => {
				_this.loading = false;
				if (res.result && res.result.obj) {
					var obj = res.result.obj;
					const userGroup = String(obj.user_group || "").trim();
					const login_time = new Date()
						.toLocaleString("zh-CN")
						.replace(/\//g, "-")
						.replace(/\s/, " ")
						.split(".")[0];
					_this.$post("~/api/user/set?user_id=" + obj.user_id, {
						login_time: login_time,
					});
					obj.login_time = login_time;
					obj.user_group = userGroup;
					if (_this.allow_user.includes(userGroup)) {
						_this.$store.commit("user_set", obj);
						if (_this.remember_me) {
							$.db.set("account", account);
						}
						_this.$get_auth(userGroup, () => {
							var url = _this.$redirect();
							_this.$router.push(url || "/");
						});
						$.db.set("user_group", JSON.stringify(res.result.obj));
					} else {
						_this.$toast("您的账号不支持在管理端登录", "error");
					}
				} else if (res.error) {
					_this.accountCheck.state = false;
					_this.accountCheck.message = "账号或密码有误，请重新输入";
					_this.passwordCheck.state = false;
					_this.passwordCheck.message = "账号或密码有误，请重新输入";
					_this.$toast(res.error.message, "error");
				}
			});
		},
	},
};
</script>

<style scoped>
@import "../../public/css/auth-glass.css";

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

.login-page .input-box .icon {
	position: absolute;
	right: 8px;
	top: 50%;
	transform: translateY(-50%);
	color: #fff;
	font-size: 1.2em;
	line-height: 1;
	cursor: default;
}

.login-page .input-box .icon-toggle {
	right: 36px;
	cursor: pointer;
	font-size: 1em;
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
