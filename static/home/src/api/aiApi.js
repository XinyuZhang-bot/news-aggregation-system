import aiRequestHelper from "@/utils/aiRequestHelper";
// 添加基地 put-post-delete
export function $aiPost(data, options) {
  return aiRequestHelper.post({
    data,
    options,
  });
}
