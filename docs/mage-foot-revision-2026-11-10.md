# 魔法师 A：脚部肤色与脚趾细节 v05–v06

日期：2026-11-10。沿用 v04 的纤细腿型及头身/面部设计。用户先要求脚部恢复肤色，随后补充要求还原精致脚趾，两项需求在同轮继续完成。

后续：用户反馈手部看似四指，以 v06 为底图补齐双手五指，交付 [v07 手部候选](mage-hand-revision-2026-11-10.md)。脚趾设计继续保留，本记录不代表整体模板已定稿。

## 版本与交付

| 版本 | 本轮实际变化 | 图片 | 完整提示词与生成记录 |
|---|---|---|---|
| v05 | 脚踝以下改为与面部、手部协调的浅肤色，保留灰色裤腿 | [肤色候选](../assets/characters/base-templates/base-a-mage/v05/base-a-mage-skin-tone-feet-front-v05.png) | [提示词](../assets/characters/base-templates/base-a-mage/v05/prompt.txt) · [记录](../assets/characters/base-templates/base-a-mage/v05/generation.json) |
| v06 | 在肤色版上补足五趾结构、趾缝及少量甲面提示 | [脚趾候选](../assets/characters/base-templates/base-a-mage/v06/base-a-mage-detailed-toes-front-v06.png) | [提示词](../assets/characters/base-templates/base-a-mage/v06/prompt.txt) · [记录](../assets/characters/base-templates/base-a-mage/v06/generation.json) |

v05 以 v04 为唯一编辑底图；v06 以 v05 为唯一底图，并仅参考 design-v01 左侧全身图底部的脚趾画法，不复制其服装/发型/配饰或姿态。两次均使用内置 image_gen 编辑，生成原文件保留，输出原样复制入项目，不做像素后处理。

## 检查

人工看图：v06 两脚各五趾可辨，大脚趾在各自内侧，其余向外逐渐变小，末端圆润、间距较小；有细短趾缝与小甲面提示。脚部维持小脚轮廓，皮肤色延续浅粉象牙白观感，脚踝以上仍为不透明灰色基础层。

[只读 QA](../assets/characters/base-templates/base-a-mage/v06/comparison-qa.json) 保留 v04/v06 摘要和取样坐标。两个指定脚部内部小区域中间色均约为 `#FEF2EE`；此值来自当前候选图采样，不是全脚统一颜色或通用肤色标准。

头身、面部和腿型在视觉上沿用 v04，但非目标区域存在生成式像素变化，不承诺逐像素锁定。是否足够精致、比例是否符合预期仍由用户看图确认。

v04 和 v05 标为需修订，v06 待用户确认；不将其中任何一版当作已批准模板。它仍是单张静态合成 PNG，没有透明图层、PSD、CMO3/MOC3、绑定或动画。B 类弓箭手不变。旧版图像及原设计文件不覆盖。

本轮版本管理同时保留尚待推送的 v03/v04 提交；最终同步结果以实际 Git 输出为准。
