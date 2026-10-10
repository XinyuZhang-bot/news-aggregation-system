<template>
  <div>
    <div class="log_box">
        <!-- <button class="log_bntx" @click="visLog" >x{{ bntx_text }}</button>
        <div class="log_conter" v-for="item in  History_log" >

          <span class="texts nm"   v-show="showRentPrise">{{ item }}</span>
        
        </div>
       
        <div class="log_conter" v-for="item in  mode_names" >

            <span class="texts nm"   v-show="showRentPrise">{{ item }}</span>
          
        </div> -->
    </div>
    
  </div>
  
</template>
 
<script>


export default {

  data() {
    return {
      // uesr_names:this.$store.state.web.auth[0].user_group,//用户名称
      mode_names:[],//模块
      History_log:[],//历史
      showRentPrise:true,
      bntx_text:'',
      
    }
    
  },
  methods: {
 //    visLog(){
 //      this.showRentPrise =!this.showRentPrise
 //      console.log(this.showRentPrise);
 //      if(this.showRentPrise===true){
 //        this.bntx_text = '隐藏日志'
 //        console.log(this.bntx_text);
 //      }else if(this.showRentPrise===false){
 //        this.bntx_text = '显示日志'
 //      }
 //      console.log(this.$store.state.user.user_group);
 //    },
	// getHistoryLog(){
	// 	if (this.$store.state.user.user_group === '管理员') {
		
	// 		let data_hory = sessionStorage.getItem('log_msg');
	// 		this.History_log = data_hory ? JSON.parse(data_hory) : []
	// 	} else {
	// 		sessionStorage.clear("log_msg")
	// 	}
	// 	if (this.$store.state.user.user_group === '商城用户') {
	// 		let data_hory = sessionStorage.getItem('log_msg');
	// 		this.History_log = data_hory ? JSON.parse(data_hory) : []
	// 	} else {
	// 		sessionStorage.clear("log_msg")
	// 	}
	// 	if (this.$store.state.user.user_group === '卖家') {
	// 		let data_hory = sessionStorage.getItem('log_msg');
	// 		this.History_log = data_hory ? JSON.parse(data_hory) : []
	// 	} else {
	// 		sessionStorage.clear("log_msg")
	// 	}
	// },
	updateLog(){
		const routes = this.$route.matched;
		let time = this.getTime();
		this.mode_names.push(this.$store.state.user.user_group + '--' + routes[0].meta.title + time)
		sessionStorage.setItem('log_msg', JSON.stringify(this.mode_names));
		let form = {
			user_name: this.$store.state.user.username,
			user_group: this.$store.state.user.user_group,
			routes: routes[0].meta.title
		}
		this.$post('~/api/operation_log/add', form, res => {
		  console.log(res);
		})
	},
	getTime(){
		var timeOne = new Date();
		let year = timeOne.getFullYear();
		let month = timeOne.getMonth() + 1;
		let day = timeOne.getDate();
		let hour = timeOne.getHours();
		let minute = timeOne.getMinutes();
		let second = timeOne.getSeconds();
		month = month > 9 ? month : '0' + month
		hour = hour > 9 ? hour : '0' + hour
		minute = minute > 9 ? minute : '0' + minute
		second = second > 9 ? second : '0' + second
		let logs = ` ${year}-${month}-${day} ${hour}:${minute}:${second}`;
		return logs;
	}
  },

  mounted() {
    // this.getHistoryLog();
	this.updateLog();
  },
 
  // 动态获取模块
  watch: {
    $route(to, from) {
      this.updateLog();
    }
    
    
 },
 

 

}
  
</script>

<style  scoped>
    .log_box{
    height: 157px;
    position: absolute;
    right: 2px;
    background-color: transparent;
    bottom: 2px;
    overflow-y: scroll;
    z-index: 5;
    }
    .log_conter{}
    
    .texts{
      
      height: 40px;
      font-size: 15px;
      font-weight: 700;
      color: #141414;
      display: block;
      background-color: #fffefe;
      border-radius:5px;
      box-sizing: border-box;
      text-align: center;
      line-height: 20px;
      margin-top: 10px;
      box-shadow: 1px 1px 1px rgba(0,0,0,0.5);
      position: relative;
      padding: 10px;
    }
    .hs{
      width: 220px;
    }

</style>