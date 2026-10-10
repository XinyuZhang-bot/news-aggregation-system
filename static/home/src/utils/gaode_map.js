import AMapLoader from '@amap/amap-jsapi-loader';
import axios from 'axios';

// 用户提供的 Key 和 密钥
// const AMAP_KEY = 'c6bd63c9737176f87e50162865d81db3';
// const AMAP_SECURITY_CODE = '3d7072bf5ae2f2da1acfc01cc50b84d0';

const AMAP_KEY = '7a197d3785dc29b7e53d2d9c27f4f76e';
const AMAP_WEB_KEY = 'bcafb11917e1c0c24268fa0e3c69aa5b';
const AMAP_SECURITY_CODE = '1d361eb52f5895510a1636216b209f3a';

// 初始化安全密钥（必须在加载 JSAPI 之前设置）
if (typeof window !== 'undefined') {
  window._AMapSecurityConfig = {
    securityJsCode: AMAP_SECURITY_CODE,
  };
}

/**
 * POI搜索
 * @param {string} keyword 搜索关键字
 * @param {string} city 城市（可选）
 * @returns {Promise<Array>} 返回POI列表
 */
export const searchPoi = async (keyword, city = '全国') => {
  if (!keyword) return Promise.resolve([]);
  try {
    const AMap = await loadAMap(['AMap.PlaceSearch']);
    const placeSearch = new AMap.PlaceSearch({
      city: city,
      pageSize: 10,
      pageIndex: 1,
      extensions: 'all',
    });

    return new Promise((resolve, reject) => {
      placeSearch.search(keyword, (status, result) => {
        if (status === 'complete' && result.poiList) {
          const pois = (result.poiList.pois || []).map(item => {
            const name = item.name || '';
            const cityname = item.cityname || '';
            const adname = item.adname || '';
            const address = item.address || '';
            let fullAddress = `${cityname}${adname}${name}`;
            if (!fullAddress) {
              fullAddress = name + (address ? `(${address})` : '');
            }
            return {
              ...item,
              fullAddress
            };
          });
          resolve(pois);
        } else if (status === 'no_data') {
          resolve([]);
        } else {
          reject('搜索失败: ' + status);
        }
      });
    });
  } catch (error) {
    return Promise.reject(error);
  }
};

/**
 * 加载高德地图
 * @param {Array} plugins 插件列表，例如 ['AMap.Driving', 'AMap.Geocoder']
 * @param {string} version 版本号，默认 '2.0'
 * @returns {Promise} 返回 AMap 对象
 */
export const loadAMap = (plugins = [], version = '2.0') => {
  return AMapLoader.load({
    key: AMAP_KEY,
    version: version,
    plugins: plugins,
  });
};

/**
 * 地址转经纬度 (地理编码)
 * @param {string} address 详细地址
 * @returns {Promise<{lng: number, lat: number}>} 返回经纬度对象
 */
export const getCoordinates = async (address) => {
  if (!address) {
    return Promise.reject('地址为空');
  }
  try {
    const AMap = await loadAMap(['AMap.Geocoder']);
    const geocoder = new AMap.Geocoder({ city: '全国' });
    
    return new Promise((resolve, reject) => {
      geocoder.getLocation(address, (status, result) => {
        if (status === 'complete' && result.geocodes.length) {
          const loc = result.geocodes[0].location;
          resolve({ lng: loc.lng, lat: loc.lat });
        } else {
          reject('地理编码失败或未找到该地址');
        }
      });
    });
  } catch (error) {
    return Promise.reject(error);
  }
};

/**
 * 使用高德 Web 服务 place/text 接口进行 POI 搜索
 * 文档：https://restapi.amap.com/v3/place/text
 * @param {string} keyword 搜索关键字，例如“北京大学”
 * @param {string} city 城市（可选），如“北京”或城市编码
 * @returns {Promise<Array>} 返回 POI 列表，每项含 fullAddress 等字段
 */
export const searchPoiByApi = async (keyword, city = '全国') => {
  if (!keyword) return Promise.resolve([]);
  try {
    const response = await axios.get('https://restapi.amap.com/v3/place/text', {
      params: {
        key: AMAP_WEB_KEY,
        keywords: keyword,
        city,
        offset: 20,
        page: 1,
        extensions: 'all',
        output: 'JSON'
      },
      timeout: 5000
    });

    const data = response.data || {};
    if (data.status === '1' && Array.isArray(data.pois)) {
      const pois = data.pois.map(item => {
        const name = item.name || '';
        const cityname = item.cityname || '';
        const adname = item.adname || '';
        const address = item.address || '';
        let fullAddress = `${cityname}${adname}${name}`;
        if (!fullAddress) {
          fullAddress = name + (address ? `(${address})` : '');
        }
        return {
          ...item,
          fullAddress
        };
      });
      return pois;
    }

    return [];
  } catch (error) {
    return Promise.reject(error);
  }
};

/**
 * 使用高德 Web 服务地理编码 API 将地址转换为经纬度
 * 文档：https://restapi.amap.com/v3/geocode/geo
 * @param {string} address 详细地址
 * @param {string} city 城市（可选），如“北京市”或城市编码
 * @returns {Promise<{lng: number, lat: number}>}
 */
export const getCoordinatesByApi = async (address, city = '') => {
  if (!address) {
    return Promise.reject('地址为空');
  }
  try {
    const response = await axios.get('https://restapi.amap.com/v3/geocode/geo', {
      params: {
        key: AMAP_WEB_KEY,
        address,
        city,
        output: 'JSON',
      },
      timeout: 5000,
    });

    const data = response.data || {};
    if (data.status === '1' && Array.isArray(data.geocodes) && data.geocodes.length > 0) {
      const loc = data.geocodes[0].location;
      if (!loc) {
        return Promise.reject('未返回坐标信息');
      }
      const [lngStr, latStr] = loc.split(',');
      const lng = Number(lngStr);
      const lat = Number(latStr);
      if (Number.isNaN(lng) || Number.isNaN(lat)) {
        return Promise.reject('坐标解析失败');
      }
      return { lng, lat };
    }

    const info = data.info || '地理编码失败';
    return Promise.reject(info);
  } catch (error) {
    return Promise.reject(error);
  }
};

/**
 * 使用高德 Web 服务 direction/driving 接口进行驾车路线规划
 * 文档：https://restapi.amap.com/v5/direction/driving
 * @param {{lng:number,lat:number}} start 起点坐标
 * @param {{lng:number,lat:number}} end 终点坐标
 * @returns {Promise<{distance:number,time:number,points:Array<{lng:number,lat:number}>,raw:any}>}
 */
export const getDrivingRouteByApi = async (start, end) => {
  if (!start || !end) {
    return Promise.reject('起点或终点坐标为空');
  }
  try {
    const response = await axios.get('https://restapi.amap.com/v5/direction/driving', {
      params: {
        key: AMAP_WEB_KEY,
        origin: `${start.lng},${start.lat}`,
        destination: `${end.lng},${end.lat}`,
        output: 'JSON',
        show_fields: 'polyline,cost'
      },
      timeout: 8000
    });

    const data = response.data || {};
    const route = data.route;
    const paths = route && Array.isArray(route.paths) ? route.paths : [];
    if (data.status !== '1' || !paths.length) {
      return Promise.reject(data.info || '驾车路径规划失败');
    }

    const firstPath = paths[0];
    const distance = Number(firstPath.distance || 0);
    const time = Number(firstPath.duration || 0);
    const steps = Array.isArray(firstPath.steps) ? firstPath.steps : [];

    const points = [];
    steps.forEach(step => {
      if (!step.polyline) return;
      step.polyline.split(';').forEach(str => {
        const [lngStr, latStr] = str.split(',');
        const lng = Number(lngStr);
        const lat = Number(latStr);
        if (!Number.isNaN(lng) && !Number.isNaN(lat)) {
          points.push({ lng, lat });
        }
      });
    });

    return {
      distance,
      time,
      points,
      raw: firstPath
    };
  } catch (error) {
    return Promise.reject(error);
  }
};

/**
 * 计算两点间的驾车路线
 * @param {Object} start {lng, lat} 起点
 * @param {Object} end {lng, lat} 终点
 * @param {Object} mapInstance AMap.Map 实例（可选，如果传入则会在地图上绘制路线）
 * @returns {Promise<{distance: number, time: number, route: Object}>} distance单位米，time单位秒
 */
export const getDrivingRoute = async (start, end, mapInstance = null) => {
  try {
    const AMap = await loadAMap(['AMap.Driving']);
    const drivingOptions = {
      hideMarkers: true, // 隐藏默认的起点终点标记（通常我们自己画）
      showTraffic: false,
    };
    
    if (mapInstance) {
      drivingOptions.map = mapInstance;
    }

    const driving = new AMap.Driving(drivingOptions);

    return new Promise((resolve, reject) => {
      driving.search(
        new AMap.LngLat(start.lng, start.lat),
        new AMap.LngLat(end.lng, end.lat),
        (status, result) => {
          if (status === 'complete') {
            if (result.routes && result.routes.length) {
              const route = result.routes[0];
              resolve({
                distance: route.distance, // 米
                time: route.time,         // 秒
                route: route
              });
            } else {
              reject('未找到有效路线');
            }
          } else {
            reject('驾车路线规划失败: ' + result);
          }
        }
      );
    });
  } catch (error) {
    return Promise.reject(error);
  }
};
