<template>
	<div class="auth-page register-page" id="account_register">
		<div class="glass-card glass-card--wide register-card">
			<h1 class="auth-title">账号注册</h1>

			<b-form class="auth-register-form" autocomplete="off" @submit.prevent="submit()">
				<input type="text" tabindex="-1" autocomplete="username" class="autofill-trap" aria-hidden="true" />
				<input type="password" tabindex="-1" autocomplete="current-password" class="autofill-trap" aria-hidden="true" />

				<div class="diy_forms">
					<b-form-group
						label="账号"
						label-for="input-1"
						:state="display_username"
						:invalid-feedback="usernameFeedback"
						:valid-feedback="usernameValidFeedback"
					>
						<b-form-input
							id="input-1"
							v-model="form.username"
							type="text"
							placeholder="请输入账号"
							name="home-reg-username"
							autocomplete="off"
							:readonly="blockAutofill"
							trim
							@focus="unlockAutofill"
							@blur="onUsernameBlur"
						></b-form-input>
					</b-form-group>

					<b-form-group
						label="设置密码"
						label-for="input-2"
						:state="display_password"
						invalid-feedback="密码长度需为 6～64 个字符"
						valid-feedback="密码格式正确"
					>
						<b-form-input
							id="input-2"
							v-model="form.password"
							type="password"
							placeholder="请输入密码"
							name="home-reg-password"
							autocomplete="new-password"
							:readonly="blockAutofill"
							trim
							@focus="unlockAutofill"
							@blur="touch('password')"
						></b-form-input>
					</b-form-group>

					<b-form-group
						label="确认密码"
						label-for="input-3"
						:state="display_confirm_password"
						invalid-feedback="两次密码不一致"
						valid-feedback="两次密码一致"
					>
						<b-form-input
							id="input-3"
							v-model="confirm_password"
							type="password"
							placeholder="请再次输入密码"
							name="home-reg-password2"
							autocomplete="new-password"
							:readonly="blockAutofill"
							trim
							@focus="unlockAutofill"
							@blur="touch('confirm_password')"
						></b-form-input>
					</b-form-group>

					<b-form-group
						label="昵称"
						label-for="input-4"
						:state="display_nickname"
						invalid-feedback="昵称长度应为 2～12 个字符"
						valid-feedback="昵称格式正确"
					>
						<b-form-input
							id="input-4"
							v-model="form.nickname"
							type="text"
							placeholder="2个字符到12个字符"
							autocomplete="off"
							trim
							@blur="touch('nickname')"
						></b-form-input>
					</b-form-group>

					<b-form-group
						label="邮箱"
						label-for="input-5"
						:state="display_email"
						invalid-feedback="请输入正确的邮箱地址"
						valid-feedback="邮箱格式正确"
					>
						<b-form-input
							id="input-5"
							v-model="form.email"
							type="email"
							placeholder="例: example@123.com"
							autocomplete="off"
							trim
							@blur="touch('email')"
						></b-form-input>
					</b-form-group>

					<b-form-group
						label="身份"
						label-for="input-7"
						:state="display_user_group"
						invalid-feedback="请选择身份"
					>
						<b-form-select
							id="user_group"
							v-model="form.user_group"
							:options="list_user_group"
							placeholder="请选择身份"
							@change="touch('user_group')"
							@blur="touch('user_group')"
						></b-form-select>
					</b-form-group>
				</div>

				<form_ordinary_user v-if="form.user_group === '普通用户'" :form="form_sub"></form_ordinary_user>

				<div class="auth-btns">
					<button type="submit" class="auth-btn auth-btn--primary">注册</button>
				</div>

				<div class="register-links">
					<button type="button" class="register-link-btn" @click="$router.push('/account/login')">
						是否已经拥有一个账户？<span>去登录</span>
					</button>
					<button type="button" class="register-link-btn register-link-btn--minor" @click="$router.push('/account/forgot')">
						找回密码
					</button>
				</div>
			</b-form>
		</div>
	</div>
</template>

<script>
import mixin from "@/mixins/page.js";
import form_ordinary_user from "@/components/diy/form_ordinary_user";

export default {
	components: {
		form_ordinary_user,
	},
	mixins: [mixin],
	data() {
		return {
			blockAutofill: true,
			url_submit: "~/api/user/register?",
			form: {
				username: "",
				password: "",
				nickname: "",
				email: "",
				user_group: "普通用户",
				avatar: "",
			},
			confirm_password: "",
			form_sub: {},
			list_user_group: [],
			user_group: [],
			usernameCheck: {
				state: null,
				message: "账号格式：2～16位；可用中文/英文/数字及混合；不能为纯数字；不能包含空格或符号（如 _ - . @）",
			},
			touched: {
				username: false,
				password: false,
				confirm_password: false,
				nickname: false,
				email: false,
				user_group: false,
			},
			submitted: false,
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
		display_nickname() {
			if (!this.touched.nickname && !this.submitted) return null;
			return this.validation_nickname;
		},
		display_email() {
			if (!this.touched.email && !this.submitted) return null;
			return this.validation_email;
		},
		display_user_group() {
			if (!this.touched.user_group && !this.submitted) return null;
			return this.validation_user_group;
		},
		validation_username() {
			return this.usernameCheck.state;
		},
		usernameFeedback() {
			return this.usernameCheck.message;
		},
		usernameValidFeedback() {
			return this.usernameCheck.state === true ? this.usernameCheck.message : "";
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
		validation_nickname() {
			const v = (this.form.nickname || "").trim();
			if (!v) return null;
			const len = Array.from(v).length;
			return len >= 2 && len <= 12;
		},
		validation_email() {
			const v = (this.form.email || "").trim();
			if (!v) return null;
			return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v);
		},
		validation_user_group() {
			return this.form.user_group ? true : false;
		},
	},
	watch: {
		"form.username"() {
			this.usernameCheck.state = null;
			this.usernameCheck.message =
				"账号格式：2～16位；可用中文/英文/数字及混合；不能为纯数字；不能包含空格或符号（如 _ - . @）";
		},
	},
	created() {
		this.resetFormFields();
		this.get_list_user_group();
	},
	mounted() {
		this.$nextTick(() => {
			setTimeout(this.resetFormFields, 100);
			setTimeout(this.resetFormFields, 400);
			setTimeout(() => {
				this.resetFormFields();
				this.blockAutofill = false;
			}, 600);
		});
	},
	methods: {
		touch(field) {
			this.touched[field] = true;
		},
		onUsernameBlur() {
			this.touched.username = true;
			this.checkRegisterUsername();
		},
		unlockAutofill() {
			this.blockAutofill = false;
		},
		resetFormFields() {
			this.form.username = "";
			this.form.password = "";
			this.form.nickname = "";
			this.form.email = "";
			this.form.user_group = "普通用户";
			this.confirm_password = "";
			this.usernameCheck.state = null;
			this.submitted = false;
			Object.keys(this.touched).forEach((k) => {
				this.touched[k] = false;
			});
		},
		getUsernameLength(v) {
			return Array.from((v || "").trim()).length;
		},
		isValidUsernameFormat(v) {
			const value = (v || "").trim();
			if (!value) return false;
			const len = this.getUsernameLength(value);
			if (len < 2 || len > 16) return false;
			if (!/^[A-Za-z0-9\u4e00-\u9fa5]+$/.test(value)) return false;
			if (/^\d+$/.test(value)) return false;
			return true;
		},
		get_list_user_group() {
			this.$get("~/api/user_group/get_list?register_max=3&register_min=2", {}, (res) => {
				if (res.result.list) {
					var lt = [];
					var list = res.result.list;
					list.map((x) => {
						lt.push({
							value: x.name,
							text: x.name,
						});
					});
					this.list_user_group = lt;
					this.user_group = list;
					if (!lt.some((x) => x.value === this.form.user_group)) {
						const normal = lt.find((x) => x.value === "普通用户");
						this.form.user_group = normal ? normal.value : lt.length ? lt[0].value : "普通用户";
					}
				} else if (res.error) {
					this.$toast(res.error.message, "error");
				}
			});
		},
		async checkRegisterUsername() {
			const username = (this.form.username || "").trim();
			if (!username) {
				this.usernameCheck.state = false;
				this.usernameCheck.message = "请输入账号";
				return false;
			}
			if (!this.isValidUsernameFormat(username)) {
				this.usernameCheck.state = false;
				this.usernameCheck.message =
					"账号格式：2～16位；可用中文/英文/数字及混合；不能为纯数字；不能包含空格或符号（如 _ - . @）";
				return false;
			}
			const res = await this.$get("~/api/user/get_obj?", { username, like: 0 });
			const obj = res && res.result ? res.result.obj : null;
			if (obj && obj.username === username) {
				this.usernameCheck.state = false;
				this.usernameCheck.message = "该账号已注册";
				return false;
			}
			this.usernameCheck.state = true;
			this.usernameCheck.message = "该账号可以注册";
			return true;
		},
		async submit(param, func) {
			this.submitted = true;
			if (!param) {
				param = this.form;
			}
			param.avatar = param.avatar == "" ? "/static/upload/default_avatar.jpg" : param.avatar;
			var pm = this.events("submit_before", Object.assign({}, param)) || param;
			var msg = await this.events("submit_check", pm);
			var ret;
			if (msg) {
				this.$toast(msg, "danger");
			} else {
				ret = this.events("submit_main", pm, func);
			}
			return ret;
		},
		submit_before(param) {
			var user_group = param.user_group;
			if (user_group === "普通用户") {
			}
		},
		async submit_check(param) {
			var ret = null;
			var email_regular =
				/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			var { username, password, nickname, user_group, email } = param;
			var confirm_password = this.confirm_password;

			if (!(await this.checkRegisterUsername())) {
				return this.usernameFeedback;
			} else if (!password) {
				ret = "密码不能为空!";
			} else if (password.length > 64 || password.length < 6) {
				ret = "密码长度应为 6～64 个字符！";
			} else if (nickname && (Array.from(nickname.trim()).length > 12 || Array.from(nickname.trim()).length < 2)) {
				ret = "昵称长度应为 2～12 个字符（支持中文）";
			} else if (email && !email_regular.test(email)) {
				ret = "请输入正确的邮箱地址 例：test@test.com!";
			} else if (password != confirm_password) {
				ret = "确认密码与密码不一致！";
			} else if (!user_group) {
				ret = "请选择用户身份!";
			}
			if (!ret && user_group === "普通用户") {
				var form_sub = Object.assign({}, this.form_sub);
				let phone_regular = /^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/;
				if (form_sub.users_mobile_phone && !phone_regular.test(form_sub.users_mobile_phone)) {
					return "手机号格式错误";
				}
			}
			return ret;
		},
		submit_after(json, func) {
			var form = Object.assign({}, this.form);
			delete form.password;
			var table = this.user_group.getVal("source_table", { name: form.user_group });
			if (table) {
				this.get_submit(form, table);
			} else {
				this.$toast("注册成功!", "success");
				this.$router.push("/");
			}
		},
		get_submit(form, table) {
			var form_sub = this.form_sub;
			this.$get("~/api/user/get_obj?", form, (res) => {
				if (res.result && res.result.obj) {
					form_sub.user_id = res.result.obj.user_id;
					form_sub.create_by = res.result.obj.user_id;
					this.submit_sub(form_sub, table);
				} else if (res.error) {
					this.$toast(res.error.message, "error");
				}
			});
		},
		submit_sub(form, table) {
			for (var key in form) {
				try {
					var value = form[key];
					if (value && value instanceof Date) {
						form[key] = this.$toTime(value, "yyyy-MM-dd hh:mm:ss");
					}
					if ("ordinary_user" == table) {
						let ordinary_user_field = ["user_id", "create_by", "users_mobile_phone"];
						if (ordinary_user_field.indexOf(key) == -1) {
							delete form[key];
						}
					}
					if ("compileors" == table) {
						let compileors_field = ["user_id", "create_by", "users_phone"];
						if (compileors_field.indexOf(key) == -1) {
							delete form[key];
						}
					}
				} catch (err) {}
			}
			this.$post("~/api/" + table + "/add?", form, (res) => {
				if (res.result) {
					this.$toast("注册成功!", "success");
					this.$router.push("/");
				} else if (res.error) {
					this.$toast(res.error.message);
				}
			});
		},
	},
};
</script>

<style scoped>
@import "../../../public/css/auth-glass.css";

.register-page .register-card {
	padding: 32px 36px 28px;
}

.register-page .auth-register-form {
	position: relative;
	width: 100%;
}

.autofill-trap {
	position: absolute;
	opacity: 0;
	height: 0;
	width: 0;
	pointer-events: none;
	overflow: hidden;
}

.register-page {
	--register-label-width: 84px;
}

.register-page ::v-deep .form-group {
	display: flex;
	flex-wrap: wrap;
	align-items: flex-start;
	margin-bottom: 16px;
}

.register-page ::v-deep .form-group > label,
.register-page ::v-deep .col-form-label {
	flex-shrink: 0;
	width: var(--register-label-width);
	min-width: var(--register-label-width);
	margin-bottom: 0;
	padding: 8px 8px 8px 0;
	font-size: 14px;
	line-height: 36px;
	color: rgba(255, 255, 255, 0.96) !important;
	text-align: left !important;
}

.register-page ::v-deep .form-group > div:last-child {
	flex: 1;
	min-width: 0;
}

.register-page ::v-deep .valid-feedback,
.register-page ::v-deep .invalid-feedback {
	display: none;
	margin-top: 6px !important;
	margin-left: calc(-1 * var(--register-label-width) - 8px) !important;
	width: calc(100% + var(--register-label-width) + 8px) !important;
	padding-left: 0 !important;
	text-align: left;
	font-size: 13px;
	font-weight: 600;
	line-height: 1.45;
	text-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
}

.register-page ::v-deep .form-group.is-valid .valid-feedback {
	display: block;
}

.register-page ::v-deep .form-group.is-invalid .invalid-feedback {
	display: block;
}

.register-page ::v-deep .valid-feedback {
	color: #b9f6ca !important;
}

.register-page ::v-deep .invalid-feedback {
	color: #ff8a80 !important;
}

.register-page ::v-deep .diy_form .form-group > label {
	width: var(--register-label-width);
	min-width: var(--register-label-width);
}

.register-page ::v-deep .form-control,
.register-page ::v-deep .custom-select {
	background: rgba(255, 255, 255, 0.12) !important;
	border: 1px solid rgba(255, 255, 255, 0.38) !important;
	color: #fff !important;
	border-radius: 8px;
	height: 40px;
}

.register-page ::v-deep .form-control::placeholder {
	color: rgba(255, 255, 255, 0.55);
}

.register-page ::v-deep .form-control:focus,
.register-page ::v-deep .custom-select:focus {
	border-color: rgba(255, 255, 255, 0.75) !important;
	box-shadow: none;
}

.register-page ::v-deep .custom-select option {
	color: #1a1a1a;
	background: #fff;
}

.register-links {
	display: flex;
	flex-wrap: wrap;
	justify-content: space-between;
	gap: 8px;
	margin-top: 16px;
}

.register-link-btn {
	background: none;
	border: none;
	padding: 0;
	color: rgba(255, 255, 255, 0.92);
	font-size: 13px;
	cursor: pointer;
	text-align: left;
}

.register-link-btn span {
	font-weight: 600;
	text-decoration: underline;
}

.register-link-btn--minor {
	color: rgba(255, 255, 255, 0.75);
	font-size: 12px;
	margin-left: auto;
}

.register-link-btn:hover {
	color: #fff;
}
</style>
