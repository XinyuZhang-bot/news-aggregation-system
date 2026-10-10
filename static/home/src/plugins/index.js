import sdk from './sdk.js';
import expand from './jquery_expand.js';
import Swiper from './swiper-bundle.esm.browser.min.js';
import component from './component.js';
import axios from "axios"
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import 'quill/dist/quill.core.css' // import styles
import 'quill/dist/quill.snow.css' // for snow theme
import 'quill/dist/quill.bubble.css' // for bubble theme
import VueQuillEditor from 'vue-quill-editor'

import {
	BootstrapVue,
	IconsPlugin
} from 'bootstrap-vue'


/**
 * 检测图片是否存在
 * @param url
 */
let imageIsExist = function (url) {
	return new Promise((resolve) => {
		var img = new Image();
		img.onload = function () {
			if (this.complete == true) {
				resolve(true);
				img = null;
			}
		}
		img.onerror = function () {
			resolve(false);
			img = null;
		}
		img.src = url;
	})
}

export default {
	install(Vue, options) {
		/**
		 * 指令名称为：default-img
		 * @param {Object} el
		 * @param {Object} binding
		 */
		Vue.directive('default-img', async function (el, binding) {
			let imgURL = binding.value; //获取图片地址
			if (imgURL) {
				let exist = await imageIsExist(imgURL);
				if (exist) {
					el.onerror = function () {
						el.setAttribute('src', imgURL);
					}
				}
			}
		});

		/**
		 * 通用拖拽指令 v-drag
		 * 使用方式：v-drag=" 'localStorageKey' " 或 v-drag="{ key: '...', ... }"
		 */
		Vue.directive('drag', {
			bind(el, binding) {
				el.style.position = 'fixed';
				el.style.zIndex = el.style.zIndex || '9999';
				
				let storageKey = null;
				if (typeof binding.value === 'string') {
					storageKey = binding.value;
				} else if (typeof binding.value === 'object' && binding.value.key) {
					storageKey = binding.value.key;
				}

				if (storageKey) {
					try {
						const saved = localStorage.getItem(storageKey);
						if (saved) {
							const pos = JSON.parse(saved);
							if (pos.left) el.style.left = pos.left;
							if (pos.top) el.style.top = pos.top;
							el.style.right = 'auto';
							el.style.bottom = 'auto';
						}
					} catch (e) {
						console.error('v-drag restore error:', e);
					}
				}

				el._dragMouseDown = function (e) {
					// 阻止默认行为，防止图片原生拖拽或文本选中干扰
					const target = e.target;
					const tagName = target.tagName.toLowerCase();
					// 如果不是输入类元素，则阻止默认行为
					if (tagName !== 'input' && tagName !== 'textarea' && tagName !== 'select' && !target.isContentEditable) {
						e.preventDefault();
					}

					const startX = e.clientX;
					const startY = e.clientY;
					
					const rect = el.getBoundingClientRect();
					const disX = startX - rect.left;
					const disY = startY - rect.top;
					
					let hasMoved = false;

					const onMouseMove = function (e) {
						const currentX = e.clientX;
						const currentY = e.clientY;
						
						if (Math.abs(currentX - startX) > 2 || Math.abs(currentY - startY) > 2) {
							hasMoved = true;
						}

						let left = currentX - disX;
						let top = currentY - disY;
						
						const clientW = document.documentElement.clientWidth;
						const clientH = document.documentElement.clientHeight;
						const elW = rect.width;
						const elH = rect.height;
						
						if (left < 0) left = 0;
						if (left > clientW - elW) left = clientW - elW;
						if (top < 0) top = 0;
						if (top > clientH - elH) top = clientH - elH;
						
						const bodyZoom = parseFloat(document.body.style.zoom) || 1;
						const elZoom = parseFloat(el.style.zoom) || 1;
						const finalZoom = bodyZoom * elZoom;
						
						el.style.left = (left / finalZoom) + 'px';
						el.style.top = (top / finalZoom) + 'px';
						el.style.right = 'auto';
						el.style.bottom = 'auto';
					};

					const onMouseUp = function () {
						document.removeEventListener('mousemove', onMouseMove);
						document.removeEventListener('mouseup', onMouseUp);
						
						if (storageKey) {
							const pos = {
								left: el.style.left,
								top: el.style.top
							};
							localStorage.setItem(storageKey, JSON.stringify(pos));
						}

						if (hasMoved) {
							const stopClick = (e) => {
								e.stopPropagation();
								e.preventDefault();
							};
							el.addEventListener('click', stopClick, true);
							setTimeout(() => {
								el.removeEventListener('click', stopClick, true);
							}, 50);
						}
					};

					document.addEventListener('mousemove', onMouseMove);
					document.addEventListener('mouseup', onMouseUp);
				};

				el.addEventListener('mousedown', el._dragMouseDown);
			},
			unbind(el) {
				if (el._dragMouseDown) {
					el.removeEventListener('mousedown', el._dragMouseDown);
				}
			}
		});

		Vue.use(BootstrapVue);
		Vue.use(IconsPlugin);
		Vue.prototype.$Swiper = Swiper
		Vue.prototype.$axios = axios
		Vue.use(component, options);
		Vue.use(VueQuillEditor, options)

	}
}

