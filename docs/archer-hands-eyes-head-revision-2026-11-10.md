# 弓箭手：五指、蓝紫异瞳与头部肤色连续化

日期：2026-11-10。后续用户已明确确认 **v06 为弓箭手底稿**，要求今后同类设计参照其身材比例、体型和肤色。见 [B 类基线规范](../assets/characters/base-templates/base-b-archer/baseline.json)；两张底稿已纳入 [skill 的 A/B 参考规范](../skills/character-reference-to-turnaround/references/cases/desktop-pet-base-templates/reference-standard.md)。下文“候选/待确认”均为生成当时状态，不覆盖本段认可。魔法师 v09 保持原图不变。

## 本轮用户要求与有效状态

用户先指出 v02 手部有重影、无法清楚分辨五指，要求只修双手及眼睛；明确弓箭手眼色以角色自身为准：左眼紫、右眼蓝。因此正视图是观者左蓝、右紫，不能沿用魔法师红蓝异瞳。

后续用户在 v04 生成后补充：“头部有很明显的色差块，需要修复一下。其他的保持不变。”本轮继续以 v04 为头部修色底图，保留该版新手型和蓝紫眼色，不回退到 v02 的旧手指与旧眼色。

- [当前 v06 完整 PNG](../assets/characters/base-templates/base-b-archer/v06/base-b-archer-continuous-head-skin-front-v06.png)，SHA256 `9956cf5dcf3437d38f64b8c0feac9401d0cc19ec603694d66f70d91b4782c21c`。
- [头部正常/低对比度放大对比](../assets/characters/base-templates/base-b-archer/v06/head-color-review.png) · [v02/v04 手部与眼色对比](../assets/characters/base-templates/base-b-archer/v04/hands-eyes-review.png)。
- [当前 B 类规格](../assets/characters/base-templates/base-b-archer/working-spec.json) · [头部处理记录](../assets/characters/base-templates/base-b-archer/v06/processing.json) · [像素与颜色检查](../assets/characters/base-templates/base-b-archer/v06/visual-inspection.json)。

## 方法与版本选择

| 版本 | 实际输入与方法 | 结果与选择 |
|---|---|---|
| v03 | 内置 image_gen；v02 整图＋既有自然手型参考，仅修手与虹膜 | 异瞳方向正确，但放大后指端与旧线仍不够清楚，内部未采用；不是用户明确否定 |
| v04 | 先生成清楚分离的五指参考，再用 v02＋该参考编辑手与眼色 | 四长指各有圆润指端，拇指单独可辨，左右各五指；作为后续修头底图，尚未用户最终认可 |
| v05 | 内置 image_gen 以 v04 请求只修头部颜色 | 出现头部外皮肤与轮廓偏红，内部未采用，原文件留档 |
| v06 | 回到 v04；使用用户此前允许的程序化颜色后处理，通过局部掩模连续化头部皮肤 | 当前候选；正式输出不是 v05，也不是原样复制的生成图 |

完整提示词均保留：[v03 编辑](../assets/characters/base-templates/base-b-archer/v03/prompt.txt)、[v04 手型参考](../assets/characters/base-templates/base-b-archer/v04/hand-guide-prompt.txt)、[v04 整图编辑](../assets/characters/base-templates/base-b-archer/v04/prompt.txt)、[v05 修头尝试](../assets/characters/base-templates/base-b-archer/v05/prompt.txt)。本轮共 4 次内置图像调用（v03 一次、v04 两阶段、v05 一次），v06 无新增生成调用。

v04 手型参考：[分离五指参考 PNG](../assets/characters/base-templates/base-b-archer/v04/separated-five-finger-guide.png)。手指以自然下垂、小幅分离为目标，不为显示数量而大幅张成扇形；保留 v02 体型、站姿、灰色基础服装、肤色与手足大小的方向。生成式手/眼编辑仍有选区外像素差异，不能声称 v04 相对 v02 全部逐像素一致。

## v06 局部颜色处理与精确保持

使用 [PowerShell/C# 处理脚本](../scripts/recolor-archer-head-v06.ps1)，原始输入为 [v04](../assets/characters/base-templates/base-b-archer/v04/base-b-archer-five-fingers-blue-purple-eyes-front-v04.png)，SHA256 `fd9074e12b38fd7e27ac579a5ce777c964955bc876d3159c5383cc4efcc1eb14`。正式 [灰度掩模](../assets/characters/base-templates/base-b-archer/v06/head-skin-edit-mask.png) 限制在头部，并羽化保护眉、眼、鼻、口和轮廓；眼色核查区完全不动。脚本默认拒绝覆盖已有结果。

头部皮肤改为连续、低饱和浅粉象牙白场，使用非常弱的正面柔光变化与轻微弥散腮红，避免再保留原头皮/额头的块状明暗。头皮取样中位数约 `#FEF1EE`–`#FEF1EF`；不是全头使用单一值，也不把取样当作所有屏幕上的固定色名。

已执行正常显示、对比度 0.65 的诊断显示及放大检查；对比度处理仅用于检查图，不修改正式输出。像素检查记录：

- 掩模非零区域为 13,207 像素；**掩模外变化像素 0**。
- **头部外变化像素 0**，身体、服装、背景、标题、手脚均与 v04 一致。
- 左蓝/右紫虹膜核查区、双手与身体/脚部核查区，变化像素分别均为 0。
- Alpha 与 v04 一致；没有重采样、移动角色或改动四肢轮廓。

文件检查会重新校验原图/掩模摘要、脚本的 LF 归一化摘要及选区外保持，不仅信任记录中的零值。局部取样的标准差下降只能证明这些区域更平稳，不能推广为全图零噪声或解剖完全正确。

为遵守保留其他部分，图内旧标题仍是 v02；当前文件、元数据与过程记录明确为 v06。v03–v05 留作过程，不覆盖旧图、不替用户宣布确认。当前仍为单张静态 PNG，未制作 PSD/独立部件、Cubism 绑定或动画。
