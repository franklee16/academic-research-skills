# ProSlide Failure Recovery

遇到浏览器、图片、截图或导出问题时读取本文件。修复后必须重新回到用户确认节点。

## 浏览器打不开 HTML

- 若 `file://` 被阻止，启动本地只读 HTTP 服务，例如 `python3 -m http.server`。
- URL 中有中文或空格时，使用浏览器/库自动编码，避免手工拼错。
- 浏览器失败不代表可以跳过 HTML 预览确认。

## 图片或 logo 加载失败

- 确认图片路径相对 HTML 文件可访问。
- 若路径复杂、中文文件名或 HTTP 服务导致加载失败，可将图片复制到 HTML 同目录或转成 base64 data URI。
- 截图前必须等待 `document.images` 全部 `complete` 且 `naturalWidth > 0`。
- 发现破图时，禁止继续截图导出 PPTX。

## 字体或 CSS 未渲染完成

- 截图前等待 `document.fonts.ready`（若浏览器支持）。
- 再等待短暂稳定时间，例如 1000ms。
- 若字体缺失，使用系统中文字体栈：`Microsoft YaHei`, `PingFang SC`, `Noto Sans CJK SC`, Arial, sans-serif。

## 截图问题

- 禁止整页截图后裁切。
- 禁止用 CSS `transform: scale()` 或 `zoom` 放大页面后整页截图。
- 必须定位每一个 `.slide` 元素执行元素级截图。
- `viewport` 固定为 `1280×720`。
- `device_scale_factor` 最低 2，推荐 3。
- 每页截图像素不得低于 `2560×1440`，推荐 `3840×2160`。
- 如果出现重复拼接、页面串页、裁切或模糊，必须废弃截图并改用元素级截图重新导出。

## PPTX 导出问题

- PPTX 页数必须等于 `.slide` 元素数量。
- PPTX 页面比例必须为 16:9。
- 图片插入时必须同时设置 width 和 height 铺满整页，避免比例变形。
- 导出后用 `python-pptx` 或等价方式检查页数和页面尺寸。
- 必要时将 PPTX 转成图片或用 Quick Look 预览，检查视觉溢出和清晰度。

## 失败后的用户沟通

如果某一步失败，简短说明问题和修复动作，不要把失败的半成品当成确认稿：

```md
预览/导出时发现 [问题]，我已改用 [修复方式] 重新生成。
下面是新的预览，请重新确认是否继续。
```
