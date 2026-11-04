# 害羞姿态全身设计候选 v01

日期：2026-11-04。状态：新设计候选，待用户复核；不替换既有暂定最终三视图或原始设计图。

## 本轮请求与方法

用户提供 `C:/Users/HP/Desktop/角色图.png`，要求参考左侧全身设计，将右侧方框内人物补全，去掉方框，以整体动作表达害羞、娇柔可爱和惹人怜爱的感觉。

本轮使用内置 image_gen 进行身份保持与全身补绘：右侧头像作为身份和面部画风依据，左侧人物作为服装、身体比例与装饰参考。输出为一位独立完整人物，白色背景，取消原双栏及头像框布局；采用微微歪头、双手轻拢、含蓄微笑的姿态。

图片：[design-shy-fullbody-v01.png](design-shy-fullbody-v01.png)。生成式重绘不是逐像素扩边，面部、身体比例及服装细节需要用户看图确认，不宣称原区域完全不变。本轮未作额外程序化图像后处理。

输入 SHA256：`5516d6c7e4ef47e73b5ff4597d8aa9ee763a053f29b51a91b2b71e36c7802fa6`。
输出 SHA256：`70c5b0086543210712760f659f860eb218e02f355535ad80733644168092d127`。

## 目视检查

- 输出包含头部至双脚，原头像矩形框已去除，没有重复人物或文字。
- 正面观者左侧蓝瞳、右侧红瞳，对应角色自身右蓝左红。
- 白色长卷发、精灵耳、猫耳发饰及花饰、紫色蝴蝶结、绿宝石颈饰、白裙、尾饰及脚环均有体现。
- 姿态以双手轻拢、头部轻倾、浅微笑和轻腮红表达害羞，尚未获用户认可。
- 头饰接近画面上缘，裙摆及局部装饰并非建模对照稿；这是一张表情与姿态插画候选。

## 完整提示词

```text
Use case: identity-preserve, character illustration outpainting.
Edit the attached character-design image. The right-hand framed portrait is the PRIMARY identity and facial rendering target; the left-hand full-body figure is ONLY the reference for the same character's body proportions, clothing, accessories, hair and tail. Complete the right-hand portrait downward into a fully finished, standalone HEAD-TO-TOE character illustration. Deliver ONE character centered on a clean white portrait canvas, no box, no border, no inset, no extra duplicate figure. Do not deliver the original two-panel sheet.

Preserve the right portrait's recognizable face, huge delicate heterochromatic eyes, fine lashes, small nose and tiny mouth, fine linework, and softly shaded anime illustration style. Anatomical LEFT eye is red (viewer right in front view), anatomical RIGHT eye blue (viewer left). White fluffy flowing wavy hair with the same fringe and wispy curls, elf ears, separately worn white cat-ear accessories with pink interiors, lavender-purple ribbon bows and white flowers at cat ears. Retain the emerald-green pendant and white ruffled neck ornament. Keep the original petite proportions, slender limbs, small rounded fingers and toes, and pale porcelain ivory skin with a faint peach-pink undertone; only a subtle blush on cheeks. Rounded extremities must NOT mean thick or chubby arms, fingers, legs or feet.

Complete the outfit directly from the LEFT full-body reference: opaque white off-shoulder ruffled dress, airy short puff sleeves, fitted but modest bodice, white waist bow, full calf-length skirt with layered ruffles and the same delicate floral cutout/lace band around the hem. The skirt covers the thighs and most of the calves, revealing ankles with their white floral ankle bands and small bare feet. Reproduce the white fluffy wearable tail with the purple bow, emerging from behind the upper hip, with its curve readable to the side. Preserve the original costume design, colors, and ornament identity.

New overall pose and expression: bashful, tender, sweet, endearing and completely innocent. A very slight head tilt and lowered chin, gentle shy eye contact, relaxed eyebrows, a tiny soft closed-mouth smile, not crying or distressed, not a large grin. Shoulders relaxed and arms drawn gently inward. Both small hands loosely clasped in front of the upper torso in a natural shy fidget, fingers rounded and anatomically readable. A relaxed upright stance with feet close and one slightly offset, maintaining slender proportions and natural balance. Let the hair and dress drape gracefully with a little soft movement. Keep the whole pose age-appropriate and non-suggestive.

Composition: one polished full-body illustration with ample room around cat-ear tips, long hair, tail, hem and feet; every extremity in frame. High quality clean crisp linework, fine smooth color transitions, luminous WHITE hair and WHITE fabric with controlled pale lavender-grey shadows, no dirty grey wash, no gradient hair dye, no noisy texture or patchy skin. Soft neutral frontal light, clean white background with only a subtle grounding shadow. No text, labels, frames, watermarks, extra people or scenery.
```
