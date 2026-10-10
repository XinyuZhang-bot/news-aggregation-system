<template>
	<div class="auth-page register-page">
		<div class="glass-card glass-card--wide register-card">
			<h1 class="auth-title">账号注册</h1>

			<el-form
				ref="form"
				:model="form"
				:rules="rules"
				label-width="5em"
				class="auth-form register-form"
				autocomplete="off"
			>
				<!-- 吸收浏览器自动填充，避免写入真实表单项 -->
				<input
					type="text"
					tabindex="-1"
					autocomplete="username"
					class="autofill-trap"
					aria-hidden="true"
				/>
				<input
					type="password"
					tabindex="-1"
					autocomplete="current-password"
					class="autofill-trap"
					aria-hidden="true"
				/>

				<el-form-item label="账号" prop="username">
					<el-input
						v-model="form.username"
						placeholder="5～16 位用户名"
						maxlength="16"
						clearable
						name="reg-username"
						autocomplete="off"
						:readonly="blockAutofill"
						@focus="unlockAutofill"
					/>
				</el-form-item>

				<el-form-item label="昵称" prop="nickname">
					<el-input
						v-model="form.nickname"
						placeholder="选填，默认同账号"
						maxlength="16"
						clearable
						name="reg-nickname"
						autocomplete="off"
						:readonly="blockAutofill"
						@focus="unlockAutofill"
					/>
				</el-form-item>

				<el-form-item label="角色" prop="user_group">
					<el-select v-model="form.user_group" placeholder="请选择" style="width: 100%">
						<el-option label="编辑人员（可登录本后台）" value="编辑人员" />
						<el-option label="普通用户（前台使用）" value="普通用户" />
					</el-select>
				</el-form-item>

				<el-form-item label="手机" prop="phone">
					<el-input
						v-model="form.phone"
						placeholder="选填，用于扩展资料"
						maxlength="11"
						clearable
						name="reg-phone"
						autocomplete="off"
						:readonly="blockAutofill"
						@focus="unlockAutofill"
					/>
				</el-form-item>

				<el-form-item label="密码" prop="password">
					<el-input
						:type="passwordType"
						v-model="form.password"
						placeholder="6～64 位"
						name="reg-password"
						autocomplete="new-password"
						:readonly="blockAutofill"
						@focus="unlockAutofill"
					/>
				</el-form-item>

				<el-form-item label="确认" prop="password2">
					<el-input
						:type="passwordType"
						v-model="form.password2"
						placeholder="再次输入密码"
						name="reg-password2"
						autocomplete="new-password"
						:readonly="blockAutofill"
						@focus="unlockAutofill"
					/>
				</el-form-item>

				<el-form-item label="验证码" required class="register-captcha-item">
					<Verification ref="child" />
				</el-form-item>

				<div class="auth-btns">
					<button type="button" class="auth-btn auth-btn--primary" @click="submit">注册</button>
					<button type="button" class="auth-btn auth-btn--ghost" @click="$router.push('/login')">
						返回登录
					</button>
				</div>
			</el-form>
		</div>
	</div>
</template>

<script>
import Verification from "@/components/common/verification.vue";

export default {
	components: { Verification },
	data() {
		const samePwd = (rule, value, callback) => {
			if (value !== this.form.password) {
				callback(new Error("两次密码不一致"));
			} else {
				callback();
			}
		};
		return {
			passwordType: "password",
			blockAutofill: true,
			form: {
				username: "",
				nickname: "",
				user_group: "编辑人员",
				phone: "",
				password: "",
				password2: "",
			},
			rules: {
				username: [
					{ required: true, message: "请输入账号", trigger: "blur" },
					{ min: 2, max: 16, message: "长度 2～16 个字符（支持中文）", trigger: "blur" },
				],
				user_group: [{ required: true, message: "请选择角色", trigger: "change" }],
				password: [
					{ required: true, message: "请输入密码", trigger: "blur" },
					{ min: 6, max: 64, message: "长度 6～64 个字符", trigger: "blur" },
				],
				password2: [
					{ required: true, message: "请确认密码", trigger: "blur" },
					{ validator: samePwd, trigger: "blur" },
				],
				phone: [
					{
						validator: (rule, value, cb) => {
							const v = (value || "").trim();
							if (!v) return cb();
							if (!/^1\d{10}$/.test(v)) return cb(new Error("请输入 11 位手机号"));
							cb();
						},
						trigger: "blur",
					},
				],
			},
		};
	},
	created() {
		this.resetFormFields();
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
		unlockAutofill() {
			this.blockAutofill = false;
		},
		resetFormFields() {
			this.form.username = "";
			this.form.nickname = "";
			this.form.phone = "";
			this.form.password = "";
			this.form.password2 = "";
			this.form.user_group = "编辑人员";
			if (this.$refs.form) {
				this.$refs.form.clearValidate();
			}
		},
		submit() {
			this.$refs.form.validate((valid) => {
				if (!valid) return;
				if (!this.$refs.child.sublim()) return;
				const payload = {
					username: (this.form.username || "").trim(),
					password: this.form.password,
					user_group: this.form.user_group,
					nickname: (this.form.nickname || "").trim() || (this.form.username || "").trim(),
					phone: (this.form.phone || "").trim(),
				};
				this.$post("~/api/user/register?", payload, (res) => {
					if (res.result && res.result.bl) {
						this.$message.success(res.result.message || "注册成功");
						this.$router.push("/login");
					} else if (res.error) {
						this.$toast(res.error.message || "注册失败", "error");
					}
				});
			});
		},
	},
};
</script>

<style scoped>
@import "../../public/css/auth-glass.css";

.register-page .register-card {
	padding: 32px 36px 28px;
}

.register-page .register-form {
	width: 100%;
	position: relative;
}

.register-page {
	--register-label-width: 5em;
}

.register-page ::v-deep .el-form-item__label {
	width: var(--register-label-width) !important;
	box-sizing: border-box;
	position: relative;
	padding-left: 14px !important;
	padding-right: 12px !important;
	text-align: right !important;
	line-height: 40px;
}

/* 必填星号固定在标签列最左侧，文字右对齐后落在同一条竖线上 */
.register-page ::v-deep .el-form-item__label::before {
	position: absolute;
	left: 0;
	margin-right: 0 !important;
}

/* 非必填项用透明星号占位，与必填项文字起始竖线对齐 */
.register-page ::v-deep .el-form-item:not(.is-required) > .el-form-item__label::before {
	content: "*";
	color: transparent !important;
}

.register-page ::v-deep .register-captcha-item .test-v {
	display: flex !important;
	align-items: center;
	width: 100%;
}

.register-page ::v-deep .register-captcha-item .test-v .el-input {
	flex: 1;
	margin-right: 12px !important;
	margin-left: 0 !important;
}

.register-page ::v-deep .register-captcha-item .test-v .el-input__inner {
	width: 100%;
}

.register-page ::v-deep .register-captcha-item #canvas {
	flex-shrink: 0;
}

.autofill-trap {
	position: absolute;
	opacity: 0;
	height: 0;
	width: 0;
	pointer-events: none;
	overflow: hidden;
}
</style>
