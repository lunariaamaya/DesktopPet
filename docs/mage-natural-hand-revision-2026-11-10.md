# 魔法师 A：自然小手重做 v08

日期：2026-11-10。用户明确否定 v07：手指不美观、手势不自然、有重影；要求纤细小巧、白嫩圆润，并有正常五指。v07 的指头可数不等于手型质量达标，旧检查不能替代用户验收。

## 方法改变与交付

回退到 v06 作为唯一整图编辑底图，不在被否定的 v07 手型上继续叠加。先用内置 image_gen 生成独立高分辨率手型参考，确认四指轻拢、拇指放松的方向，再以 v06＋该参考编辑整图。两个生成阶段均记录完整提示词，输出原文件保留。

- [v08 完整候选 PNG](../assets/characters/base-templates/base-a-mage/v08/base-a-mage-natural-five-finger-hands-front-v08.png)
- [新手型细节参考](../assets/characters/base-templates/base-a-mage/v08/natural-hand-guide-v08.png)
- [v07／v08 手部放大对比](../assets/characters/base-templates/base-a-mage/v08/hand-detail-review.png)
- [手型参考提示词](../assets/characters/base-templates/base-a-mage/v08/hand-guide-prompt.txt) · [整图编辑提示词](../assets/characters/base-templates/base-a-mage/v08/prompt.txt)
- [两阶段生成及输入摘要](../assets/characters/base-templates/base-a-mage/v08/generation.json) · [人工检查](../assets/characters/base-templates/base-a-mage/v08/hand-inspection.json)

整图为 1024×1536 的静态合成 PNG。两张生成图均原样复制，没有像素后处理。放大对比只裁剪原像素并作最近邻 4 倍放大，未补画细节，不是另一张生产模型图。

## 本轮检查标准

除双手各五指外，同时检查手指自然轻拢、拇指放松、腕掌连接平顺、关节弯曲不成生硬折线、指尖纤细圆润、皮肤连续且轮廓单一。不要为强行展示数量而把手张成扇形，也不能把正常指缝与旧线重影混为一谈。

本轮放大观察：五指仍可分辨；手指弯曲和轮廓较 v07 柔和、连贯，原拇指根部的尖锐白斑减弱，未见明显旧指形叠加。完整图中的脚部肤色和五趾继续保留。上述是人工观察，不是自然度、美观度或解剖正确的自动证明，最终仍待用户看图确认。

v07 已标为 `rejected` 并保留用户反馈，v08 标为 `not_reviewed`。源 v06、被否定 v07 和新手型参考均保留，不能再次把 v07 当认可基线。原分层、绑定和动画阶段仍未完成，G0 未自动通过。

生成式编辑不能保证手部外逐像素不变。本轮不声明全局精确保持，不因模型成功返回或指头数量正确就宣布问题全部解决。B 类和用户新增的弓箭手参考目录不在本轮处理范围。
