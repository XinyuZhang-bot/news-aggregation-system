<template>
	<header>
		<div class="warp">
			<el-row>
				<el-col :span="24">
					<div class="action_left">
						<a class="btn_menu" href="javascript:void(0)" @click="$emit('change', !isCollapse)">
							<i :class="{'el-icon-menu' : !isCollapse,  'el-icon-s-grid': isCollapse }"></i>
						</a>
						<Borde/>
					</div>
          <div class="action_center">欢迎使用新闻聚合平台管理端</div>
					<div class="action_right">
					<div class="timess">
							<div>{{ currentDateTime }}</div>
						</div>
											<el-badge :value="msgSum" :hidden="msgSum!=0?false:true" :max="99" class="" style="margin-right: 30px;" v-if="messageInformListAll.length > 0">
							<i class="el-icon-bell" @click="drawer = true" style="font-size: 24px;font-weight: 700;"></i>
						</el-badge>
											<el-dropdown @command="handleCommand">
							<div class="el-dropdown-link" style="margin-right: 2rem;">
								<el-avatar style="margin-top: 0.25rem; width: 2.3rem; overflow: hidden;"
									:src="$fullUrl(user.avatar)">
									<img style="width: 2.3rem; overflow: hidden" src="../../../public/img/error.png" />
								</el-avatar>
								<span style="margin-left: 0.5rem; position: relative;top: -0.75rem;">{{ user.nickname || user.username }}</span>
							</div>
							<el-dropdown-menu slot="dropdown">
								<el-dropdown-item command="/user/info">个人信息</el-dropdown-item>
								<el-dropdown-item command="/user/password">修改密码</el-dropdown-item>
								<el-dropdown-item :command="homeUrl">网站首页</el-dropdown-item>
								<el-dropdown-item command="/quit" divided>退出</el-dropdown-item>
							</el-dropdown-menu>
						</el-dropdown>
					</div>

				</el-col>
			</el-row>
			<Logs></Logs>
			<el-drawer
				title="通知中心"
				size="400px"
				:visible.sync="drawer"
				:modal="false">
				<div style="padding: 0 20px">
					<div style="padding-top: 5px">
						<el-badge v-for="(item,index) in messageTypeList" :key="index" :is-dot="isRead(item)" class="" style="margin-right: 10px;">
							<el-button size="mini" @click="handleClick(item)">{{item}}</el-button>
						</el-badge>
					</div>
					<div style="display: flex;justify-content: flex-end;">
						<el-button type="text" @click="readAll">全部已读</el-button>
						<el-button type="text" @click="clearAll">清除</el-button>
					</div>
					<div style="height: 80vh;overflow: auto;padding: 10px">
						<div v-for="item in messageInformList" :key="item.message_inform_id" @click="setState(item)" style="margin-bottom: 10px;">
							<el-badge :is-dot="item.state==1?true : false" class="item">
								<span style="font-size: 14px;font-weight: 700;color:#333">{{item.title}}</span>
							</el-badge>
							<span style="font-size: 14px;color: #999;white-space: pre-line;">{{item.content}}</span>
							<div style="font-size: 14px;color: #999;">{{ $toTime( item.create_time,"yyyy-MM-dd hh:mm:ss") }}</div>
						</div>
					</div>
				</div>
			</el-drawer>
		</div>
	</header>
</template>


<script>
	import Logs from "@/components/diy/diy_log";
	import Borde from "../diy/diy_Breadcrumb.vue"
	export default {
		model: {
			event: 'change',
			prop: 'isCollapse'
		},
		props: {
			isCollapse: {
				trye: Boolean,
				default: true
			}
		},
		data() {
			return {
				drawer: false,
				messageType: "通知",
				messageInformList: [],
				messageInformListAll: [],
				messageTypeList: [],
				msgList: [],
				msgSum: 0,
				getMessageInformListTimer: null,
				activeIndex: '1',
				activeIndex2: '1',
				user: this.$store.state.user,
				search: "",
				currentDateTime: "",
				homeUrl:""
			};
		},
		components:{
			Logs,
			Borde
		},
		methods: {
			async getMessageInformList() {
				if(this.user.user_group == '管理员') {
					let list = await this.$get("~/api/message_inform/get_list",{type: '消息'})
					this.msgList = list.result.list
				}
				let listAll = await this.$get("~/api/message_inform/get_list?user_id=" + this.user.user_id + "&like=0")
				this.messageInformListAll = [...listAll.result.list,...this.msgList]
				this.msgSum = 0
				this.messageInformListAll.forEach(item => {
					if(item.state == 1) {
						this.msgSum++
					}
				})
				let arr = this.messageInformListAll.map(item => {
					return item.type
				})
				// 去重
				this.messageTypeList = [...new Set(arr)]

				let list = await this.$get("~/api/message_inform/get_list?user_id=" + this.user.user_id + "&like=0",{type: this.messageType})
				if(this.messageType == '消息') {
					this.messageInformList = this.msgList
				}else {
					this.messageInformList = list.result.list
				}
				this.handleClick(this.messageTypeList[0])
			},

			async handleClick(type) {
				this.messageType = type
				if(type == '消息') {
					this.messageInformList = this.msgList
					return
				}
				let res = await this.$get("~/api/message_inform/get_list?user_id=" + this.user.user_id + "&like=0", {
					type,
				})
				this.messageInformList = res.result.list
			},

			isRead(type) {
				let state = false
				let list = this.messageInformListAll.filter(item => {
					return item.type == type
				})
				if(list.length == 0) {
					state = false
					return state
				}
				list.forEach(item => {
					if(item.state == 1) {
						state = true
					}
				});
				return state
			},

			readAll() {
				this.messageInformList.forEach(async item => {
					await this.$post('~/api/message_inform/set?message_inform_id=' + item.message_inform_id,{state: 0})
				})
				this.getMessageInformList()
			},

			clearAll() {
				this.messageInformList.forEach(async item => {
					await this.$get('~/api/message_inform/del?message_inform_id=' + item.message_inform_id)
				})
				this.getMessageInformList()
			},

			async setState(item) {
				await this.$post('~/api/message_inform/set?message_inform_id=' + item.message_inform_id,{state: 0})
				this.getMessageInformList()
			},
			handleSelect(key, keyPath) {
				console.log(key, keyPath);
			},
			handleCommand(command) {
				if (command === "/quit") {
					this.$get("~/api/user/quit",{},(res)=>{
						this.$store.commit("quit");
						this.$router.push("/login");
					});
				} else if(command.indexOf("http")!==-1){
					let token = $.db.get("token");
					if (token){
						location.href = command+"?token="+encodeURIComponent(token);
					}
				}
				else {
					this.$router.push(command);
				}
			},
			updateDateTime() {
			const now = new Date();
			const year = now.getFullYear();
			const month = String(now.getMonth() + 1).padStart(2, "0");
			const day = String(now.getDate()).padStart(2, "0");
			const hours = String(now.getHours()).padStart(2, "0");
			const minutes = String(now.getMinutes()).padStart(2, "0");
			const seconds = String(now.getSeconds()).padStart(2, "0");

			this.currentDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
			}
		},
		beforeDestroy() {
    		// 在组件销毁前清除定时器
    		clearInterval(this.timer);
		},
		mounted() {
			this.getMessageInformListTimer && clearTimeout(this.getMessageInformListTimer)
			this.getMessageInformListTimer = setTimeout(() => {
				this.getMessageInformList()
			},500)
			this.updateDateTime();
    		// 在组件挂载后，每秒更新一次时间
   		 	this.timer = setInterval(this.updateDateTime, 1000);
   		 	this.homeUrl =  window.location.origin+window.location.pathname.replace("/admin/dist","/home/dist")
  		},

	}
</script>

<style scoped="scoped">
	header {
		background: #ffffff;
		border-bottom: 1px solid #e5e7eb;
		color: #111827;
		box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
		transition: box-shadow 0.2s ease;
	}

  .action_left {
    float: left;
    width: 30%;
	display:flex;
	align-items: center;
  }

  .action_center {
    float: left;
    line-height: 51px;
    width: 40%;
    text-align: center;
	font-weight: 600;
	color: #111827;
  }

  .action_right {
	text-align: right;
    float: right;
    display: flex;
    width: 30%;
    align-items: center;
    justify-content: space-around;
	color: #374151;
  }

	.el-dropdown {
		color: #374151;
	}

	.btn_menu {
		display: inline-block;
		padding: 0.625rem;
		color: #374151;
		border-radius: 8px;
		transition: background-color .2s ease, color .2s ease;
	}

	.btn_menu:hover {
		background: #f3f4f6;
		color: #111827;
	}

	.el-badge.item {
		display: block !important;
	}

	.timess {
		padding: 6px 10px;
		border-radius: 8px;
		background: #f9fafb;
		border: 1px solid #e5e7eb;
		font-size: 12px;
		color: #000000;
	}

	.timess div {
		color: #000000;
	}

	::v-deep .el-drawer {
		background: #ffffff;
		color: #111827;
		border-left: 1px solid #e5e7eb;
	}

	::v-deep .el-drawer__header {
		color: #111827;
	}
</style>
