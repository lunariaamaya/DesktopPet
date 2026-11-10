# 魔法师 A：四肢肤色与色差修订 v09

日期：2026-11-10。用户确认 v08：“很不错，我很满意”，随后要求保持现有身材形状，将手臂与腿部恢复正常肤色，并改善色差。

## 基线与本轮范围

唯一底图为已获认可的 [v08](../assets/characters/base-templates/base-a-mage/v08/base-a-mage-natural-five-finger-hands-front-v08.png)，SHA256 `729bd3685bc9115713bbd56a9c452c7cdba47a9fccb2c77d1b396030ce6c7bf8`。已将其状态改为 `approved_reference`，保留用户原话；认可仅限当前正面静态参考，不扩大为多视图、分层或绑定验收。

本轮仅要求四肢颜色与肤色衔接：肩部至手腕、短腿基础服装下缘至脚踝改为与现有手脚接近的肤色。躯干与骨盆保留灰色不透明基础服装，新增简单内部袖窿/短裤边界以区分材质；不要求改变身体外轮廓。原纤细直腿、头身比、站姿、手势、五指与脚趾均为保持项，失败回退到 v08。

## 输出与生成方法

- [v09 完整候选 PNG](../assets/characters/base-templates/base-a-mage/v09/base-a-mage-skin-tone-limbs-front-v09.png)，1024×1536，SHA256 `4c740be63fe75c00ab0f093cfb76768b0c43bf09c1329a252f897199403bee4c`。
- [完整提示词](../assets/characters/base-templates/base-a-mage/v09/prompt.txt) · [生成与输入摘要](../assets/characters/base-templates/base-a-mage/v09/generation.json)。
- [手腕/脚踝放大对比](../assets/characters/base-templates/base-a-mage/v09/skin-transition-review.png) · [颜色取样与稀疏轮廓检查](../assets/characters/base-templates/base-a-mage/v09/color-inspection.json)。

使用内置 image_gen 编辑一次，输入仅为 v08；没有加入其他版本或角色参考。正式 PNG 从工具生成目录原样复制，未作脚本像素后处理。检查图仅裁剪原图、最近邻放大两倍并排列标注，不是生产素材，也未增加原图细节。

## 颜色与人工复核

以原手脚为配色方向，采用低饱和浅粉象牙白、正面柔光、连续同色系浅影。v09 受光区小范围 RGB 中位数如下；具体坐标及区间见检查 JSON，不将单点或中位数当成整块皮肤颜色。

| 参考区域 | v09 取样 |
|---|---|
| 左/右上臂（观者方向） | `#FEF1EE` / `#FEF0ED` |
| 左/右前臂 | `#FEF1EE` / `#FEEFEC` |
| 左/右手 | `#FEEEEB` / `#FEEDEA` |
| 左/右大腿 | `#FEF2EF` / `#FEF1EE` |
| 左/右小腿 | 均为 `#FEF0ED` |
| 左/右脚 | 均为 `#FEEFEC` |

放大观察可见原五指自然轻拢姿态与五趾仍保留，原手腕/脚踝的灰色边界已消除，新增皮肤与手脚之间未见明显硬色块断层。全图视觉对照中比例、纤细直腿与姿势保持接近。稀疏行的深色轮廓极值多数相同，但颜色/抗锯齿也影响阈值，不能将该代理检查当作全轮廓逐像素相同的证明。

生成器将标题版本号从 v08 更新为 v09，虽然提示词要求保留文字；其他位置也有像素差异。因此本轮不宣称选区外逐像素不变、完全无底噪或解剖结构已自动验证。v09 为 `not_reviewed` 候选，等待用户判断颜色是否合适；已认可的回退图仍为 v08。

当前仍是单张合成 PNG，没有图层、Cubism 工程、绑定或动画。完整 G0 和后续二维阶段未因本轮改色自动完成；B 类与新增弓箭手素材不在本轮范围。
