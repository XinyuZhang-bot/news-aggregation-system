<template>

	<div class="verification-wrap">

		<el-input

			v-model="val"

			type="text"

			value=""

			class="verification-input"

			placeholder="不区分大小写"

		/>

		<canvas id="canvas" class="verification-canvas" width="100" height="43" @click="dj"></canvas>

	</div>

</template>

<script>

export default {

	name: "verification",

	mounted() {

		this.draw(this.show_num);

		this.$emit("sublim");

	},

	data() {

		return {

			val: "",

			num: "",

			show_num: [],

		};

	},

	methods: {

		sublim() {

			this.num = this.show_num.join("");

			if (this.val == "") {

				this.$message.warning("请输入验证码");

				return false;

			} else if (this.val.toUpperCase() == this.num.toUpperCase()) {

				this.val = "";

				this.draw(this.show_num);

				return true;

			} else {

				this.show_num = [];

				this.draw(this.show_num);

				this.$message.error("验证码错误");

				return false;

			}

		},

		dj() {

			this.draw(this.show_num);

		},

		draw(show_num) {

			var canvas = document.getElementById("canvas");

			if (!canvas) return;

			var canvas_width = canvas.clientWidth;

			var canvas_height = canvas.clientHeight;

			var context = canvas.getContext("2d");

			canvas.width = canvas_width;

			canvas.height = canvas_height;



			context.fillStyle = "#ffffff";

			context.fillRect(0, 0, canvas_width, canvas_height);



			var sCode =

				"A,B,C,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,W,X,Y,Z,1,2,3,4,5,6,7,8,9,q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m";

			var aCode = sCode.split(",");

			var aLength = aCode.length;



			for (var i = 0; i <= 3; i++) {

				var j = Math.floor(Math.random() * aLength);

				var deg = ((Math.random() - 0.5) * 16 * Math.PI) / 180;

				var txt = aCode[j];

				show_num[i] = txt;

				var x = 12 + i * 21;

				var y = 28 + Math.random() * 4;

				context.font = "bold 26px Arial, 微软雅黑, sans-serif";

				context.translate(x, y);

				context.rotate(deg);

				context.fillStyle = this.randomColor(true);

				context.fillText(txt, 0, 0);

				context.rotate(-deg);

				context.translate(-x, -y);

			}

			for (var k = 0; k <= 1; k++) {

				context.strokeStyle = "rgba(160, 170, 190, 0.55)";

				context.lineWidth = 1;

				context.beginPath();

				context.moveTo(Math.random() * canvas_width, Math.random() * canvas_height);

				context.lineTo(Math.random() * canvas_width, Math.random() * canvas_height);

				context.stroke();

			}

			for (var m = 0; m <= 6; m++) {

				context.strokeStyle = "rgba(180, 190, 205, 0.45)";

				context.beginPath();

				var px = Math.random() * canvas_width;

				var py = Math.random() * canvas_height;

				context.moveTo(px, py);

				context.lineTo(px + 1, py + 1);

				context.stroke();

			}

		},

		randomColor(isText) {

			if (isText) {

				var palette = ["#c62828", "#0d47a1", "#1b5e20", "#4a148c", "#e65100", "#006064"];

				return palette[Math.floor(Math.random() * palette.length)];

			}

			return "rgba(180, 190, 205, 0.6)";

		},

	},

};

</script>

<style scoped>

.verification-wrap {

	display: flex;

	align-items: center;

	width: 100%;

	gap: 10px;

}



.verification-input {

	flex: 1;

	min-width: 0;

}



.verification-canvas {

	flex-shrink: 0;

	border: 1px solid rgba(255, 255, 255, 0.85);

	border-radius: 6px;

	background-color: #ffffff;

	cursor: pointer;

	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);

}

</style>

<style>

.verification-input .el-input__inner {

	color: #fff !important;

	background: rgba(255, 255, 255, 0.22) !important;

	border: 1px solid rgba(255, 255, 255, 0.65) !important;

}



.verification-input .el-input__inner::placeholder {

	color: rgba(255, 255, 255, 0.75) !important;

}

</style>

