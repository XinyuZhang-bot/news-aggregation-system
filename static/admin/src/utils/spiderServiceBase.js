/**
 * 爬虫 Flask 服务根地址（手动爬取、定时任务、/extract 拉正文）。
 * 优先级：localStorage「spiderServiceBase」> 环境变量 VUE_APP_SPIDER_BASE > 当前页面 hostname:5001 > 127.0.0.1:5001
 */
export function resolveSpiderServiceBase() {
  try {
    const u = localStorage.getItem("spiderServiceBase");
    if (u && /^https?:\/\//i.test(String(u).trim())) {
      return String(u).trim().replace(/\/$/, "");
    }
  } catch (e) {
    /* ignore */
  }
  if (typeof process !== "undefined" && process.env && process.env.VUE_APP_SPIDER_BASE) {
    return String(process.env.VUE_APP_SPIDER_BASE).trim().replace(/\/$/, "");
  }
  if (typeof window !== "undefined" && window.location && window.location.hostname) {
    const host = window.location.hostname;
    if (!host || host === "file") {
      return "http://127.0.0.1:5001";
    }
    const proto = window.location.protocol || "http:";
    return `${proto}//${host}:5001`;
  }
  return "http://127.0.0.1:5001";
}

/** 依次尝试：解析结果、本机 127.0.0.1、localhost（缓解仅 hostname 不通或混用环境） */
export function collectSpiderServiceBaseCandidates() {
  const out = [];
  const add = (u) => {
    const v = (u || "").trim().replace(/\/$/, "");
    if (v && !out.includes(v)) out.push(v);
  };
  add(resolveSpiderServiceBase());
  add("http://127.0.0.1:5001");
  add("http://localhost:5001");
  return out;
}
