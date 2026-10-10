<template>
	<div class="diy_home diy_list diy_compileors" id="diy_compileors_list">
		<!-- 列表 -->
		<div class="diy_view_list list list-x">
					<div class="diy_card goods diy_list_box_wrap" v-for="(o, i) in localList" :key="i" @click="toDetails(o)">
										<!-- 图片 -->
				<div class="diy_list_img_box" v-if="imgList.length" >
					<div class="diy_row" v-for="(item,index) in imgList" :key="item+index" v-show="$check_field('get',item.name,'/compileors/details') && +item.is_img_list">
						<div class="diy_title diy_list_img_title">
							<span>{{item.title}}:</span>
						</div>
						<div class="diy_field diy_img">
							<img :src="$fullUrl(o[item.name])" style="width:100%;height:100%" />
						</div>
					</div>
				</div>
				<!-- 内容 -->
				<div class="diy_list_item_box">
					<div class="diy_list_item_content" v-for="(item,index) in showItemList" :key="item+index">
						<div class="diy_row" :class="{[item.name]:true,'diy-main-title': item.pattern === '主标题','diy-sub-title': item.pattern === '副标题','diy-create-by': item.pattern === '发布人','diy-list-time': item.pattern === '时间','diy-list-price': item.pattern === '价格','diy-tag-type': item.pattern === '分类标签'}" v-if="($check_field('get',item.name,'/compileors/details') && +item.is_img_list)">
							<div class="diy_title">
								<span>{{item.title}}:</span>
							</div>
							<div class="diy_field diy_text">
																																			<span v-if="item.type == '日期' || item.type == '日后'" v-text="item.hide_str ? $hide_str($toTime(o[item.name],'yyyy-MM-dd')) : $toTime(o[item.name],'yyyy-MM-dd')"></span>
								<span v-if="item.type == '时间'" v-text="item.hide_str ? $hide_str($toTime(o[item.name],'hh:mm:ss')) : $toTime(o[item.name],'hh:mm:ss')"></span>
								<span v-if="item.type == '日长'" v-text="item.hide_str ? $hide_str($toTime(o[item.name],'yyyy-MM-dd hh:mm:ss')) : $toTime(o[item.name],'yyyy-MM-dd hh:mm:ss')"></span>
								<span v-if="item.type != 'UID' && item.type != '日期' && item.type != '日后' && item.type != '日长' && item.type != '时间' && item.type != '评分'" v-text="item.hide_str ? $hide_str(o[item.name]) : o[item.name]+item.units"></span>
							</div>
						</div>
					</div>
								</div>
							</div>
		</div>


		<!-- 表格 -->
		<div class="diy_view_table">
			<table class="diy_table">
				<tr class="diy_row">
						</tr>
								<tr class="diy_row" v-for="(o,i) in localList" :key="o+i" @click="to_detail(o)">
										</tr>
			</table>
		</div>
		<!-- 轮播 -->

		 <div class="carousel ins_s">
                <div class="slider" ref="slider">
				                <div  v-for="(o, i) in localList" :key="i" class="slide" >
				                    
                    <router-link :to="'/compileors/details?compileors_id=' + o['compileors_id']" class="lis_cont">
						                        <div class="diy_list_img_box" v-if="imgList.length" >
    					        <div class="diy_row" v-for="(item, index) in imgList" :key="item + index" v-show="$check_field('get',item.name,'/compileors/details') && +item.is_img_list">
    						<div class="diy_title diy_list_img_title">
							
    						</div>
    						<div class="diy_field diy_img">
    							<img :src="$fullUrl(o[item.name])" style="width:100%;height:100%" />
    						</div>
                      
    					</div>
                        </div>
                           
                    <div class="context">
                        <div class="diy_list_item_content" v-for="(item,index) in showItemList" :key="item+index">
						<div class="diy_row" :class="{[item.name]:true,'diy-main-title': item.pattern === '主标题','diy-sub-title': item.pattern === '副标题','diy-create-by': item.pattern === '发布人','diy-list-time': item.pattern === '时间','diy-list-price': item.pattern === '价格','diy-tag-type': item.pattern === '分类标签'}"  v-if="$check_field('get',item.name,'/compileors/details') && +item.is_img_list">
							<div class="diy_title">
								<span>{{item.title}}:</span>
							</div>
							<div class="diy_field diy_text">
																																			<span v-if="item.type == '日期' || item.type == '日后'" v-text="$toTime(o[item.name],'yyyy-MM-dd')"></span>
								<span v-if="item.type == '时间'" v-text="$toTime(o[item.name],'hh:mm:ss')"></span>
								<span v-if="item.type == '日长'" v-text="$toTime(o[item.name],'yyyy-MM-dd hh:mm:ss')"></span>
								<span v-if="item.type != 'UID' && item.type != '日期' && item.type != '日后' && item.type != '日长' && item.type != '时间' && item.type != '评分'" v-text="o[item.name]+item.units"></span>
							</div>
						</div>
					</div>
                             
                    </div>
		                </router-link>
                </div>
                </div>
                	<button class="prev" @click="prevSlide">&lt;</button>
                	<button class="next" @click="nextSlide">&gt;</button>
				<div class="paginations" >
					<button v-for="page in pagarr" :key="page" @click="handleButtonClick(page)" :class="{ pag_btn:page, active: page === activePage }">{{ page }}</button>
 		 		</div>
            </div>
	</div>
</template>

<script>
	export default {
		props: {
			list: {
				type: Array,
				default: function() {
					return [];
				},
			},
			choose_date: {
				type: String,
				default: ''
			},
		},
		data() {
			return {
				 translateX: 0,
                currentIndex: 0,	
                timer: null,
				pagarr:[],
				activePage: 1,
				currentPage: 1,
      			itemsPerPage: 3,
				totalItems: 3,
				localList: [],
				listTimer: null,
						imgList: [
						],
						itemList: [
								{
									title: "用户名/账号",
									name: "username",
									type: "文本",
										units: "",
											pattern: "",
									is_img_list: "0"
								},
								{
									title: "用户手机",
									name: "users_phone",
									type: "手机",
										units: "",
											pattern: "",
									is_img_list: "0"
								},
						],
						richList: [
						],
						userInfoCache: {}, // 格式: { user_id: { nickname: "xxx", avatar: "url" } }
			};
		},
		 mounted() {
			 let lang = this.localList.length;

			 // 指定每次循环添加的数量
			 let pagarrLength = Math.ceil(lang / 3);

			 // 添加页数
			 for (let i = 1; i <= pagarrLength; i++) {
				 this.pagarr.push(i);
			 }
        },
		watch:{
						'list'(val){
				let lang = this.list.length;
				// 指定每次循环添加的数量
				let pagarrLength = Math.ceil(lang / 3);
			
				// 添加页数
				for (let i = 1; i <= pagarrLength; i++) {
					this.pagarr.push(i);
				}
			}
					},
		methods: {
			toDetails(o) {
						let query = { compileors_id: o['compileors_id'] };
			if (this.$props.choose_date) {
				query['choose_date'] = this.$props.choose_date;
			}
				this.$router.push({    
					path: `/compileors/details`,
					query: query,
				});
			},
						 	handleButtonClick(index){

				this.activePage = index;
				if (index == 1  ) {
					
					this.translateX = -this.currentIndex * 0;

				}
				if (index == 2  ) {

					this.translateX = -99.99;
					
				}

				if(index == 3 ){
					this.translateX = -199.98
				}
				if(index == 4){
					this.translateX = -299.96999999999997
					
				}
				this.$nextTick(() => {
							this.$refs.slider.classList.add('slide-transition');
							
							this.$refs.slider.style.transform = `translateX(${this.translateX}%)`;
						});
				},

				prevSlide() {

				if (this.currentIndex === 0) {
					this.currentIndex = this.localList.length - 3;
				} else {
					this.currentIndex--;
				}
				this.translateX = -this.currentIndex * 33.33;

				this.$nextTick(() => {
							this.$refs.slider.classList.add('slide-transition');
							if (this.currentIndex ==9) {
								this.$refs.slider.classList.remove('slide-transition');
							}
							this.$refs.slider.style.transform = `translateX(${this.translateX}%)`;
						});

				},
				nextSlide() {

					if (this.currentIndex===8) {
						this.$refs.slider.classList.remove('slide-transition');
					}
					if ( this.currentIndex === this.localList.length - 3) {
						
						this.currentIndex = 0
						
					} else {
						this.currentIndex++;
					}

					this.translateX = -this.currentIndex * 33.33;
					
						this.$nextTick(() => {
							
							this.$refs.slider.classList.add('slide-transition');
							if (this.currentIndex ==0) {
								this.$refs.slider.classList.remove('slide-transition');
							}
							this.$refs.slider.style.transform = `translateX(${this.translateX}%)`;
					});

			},
			to_detail(v){
				this.$router.push("/compileors/details?compileors_id="+v.compileors_id)
			},
			get_user_name(name,id){
				var obj = null;
						var ret = "";
				if(obj){
					ret = obj.nickname+"-"+obj.username;
					// if(obj.nickname){
					// 	ret = obj.nickname;
					// }
					// else{
					// 	ret = obj.username;
					// }
				}
				return ret;
			},
						},
		created() {
				},
		computed:{
			showItemList(){
				let arr = [];
				let _type = ["视频","音频","文件"];
				this.itemList.forEach(item => {
					if(_type.indexOf(item.type) === -1 && !!+item.is_img_list){
						arr.push(item)
					}
				})
				return arr.slice(0,4);
			}
		},
		watch: {
			list: {
				immediate: true, // 初始化立即执行
				handler(newList) {
				this.listTimer && clearTimeout(this.listTimer);
				this.listTimer = setTimeout(() => {
									this.localList = newList.map(l => ({ ...l, checked: false, score: l.score || 0 }));
																	},500)
				},
				deep: true
			}
		}
	};
</script>

<style scoped>
	.media {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		flex-basis: 75%;
		min-height: 10rem;
	}

	.goods {
		display: flex;
		width: calc(25% - 1rem);
		margin: 0.5rem;
		padding: 0.5rem;
		flex-direction: column;
		justify-content: space-between;
		background-color: white;
		border-radius: 0.5rem;
	}

	.goods:hover {
		border: 0.2rem solid #909399;
		box-shadow: 0 0.1rem 0.3rem rgba(0, 0, 0, 0.15);
	}

	.goods:hover img {
		filter: blur(1px);
	}

	.price {
		font-size: 1rem;
		margin-right: 3px;
	}

	.price_ago {
		text-decoration: line-through;
		font-size: 0.5rem;
		color: #999;

	}

	.title {
		word-break: break-all;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		font-weight: 700;
		padding: .25rem;
	}

	.icon_cart {
		color: #FF5722;
		float: right;
	}

	@media (max-width: 992px) {

		.goods {
			width: calc(33% - 1rem);
			;
		}

	}

	@media (max-width: 768px) {

		.goods {
			width: calc(50% - 1rem);
			;
		}

	}
	
.slide-transition {
  transition: transform 0.5s ease;
}
    .carousel {
        position: relative;
        width: 100%;
        height: 300px; /* 设置轮播图的高度 */
        overflow: hidden;
        }

.slider {
  display: flex;

}

.slide {
    flex-shrink: 0;
	width: calc(33.33% - 1rem);
   
}


.slide img{
    width: 300px;
    height: 200px ;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.prev,
.next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  font-size: 24px;
  background-color: #ccc;
  border-radius: 50%;
  border: none;
  color: #fff;
  opacity: 0.7;
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
}

.paginations {
    display: flex;
    /* padding-left: 0; */
    /* list-style: none; */
    width: 20%;
    left: 41%;
    justify-content: space-around;
    font-size: 25px;
    border: none;
}

button.active {
  background-color: rgb(221, 127, 4);
  color: white;
}
.tag{
	position: absolute;
	left: 10px;
	top: 10px;
	z-index: 2;
	padding: 5px 10px;
	font-size: 12px;
	color: #fff;
	background: #ff5055;
	border-radius: 4px;
}
</style>

