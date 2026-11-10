# 魔法师 A：以角色设计图修订比例与脸型

日期：2026-11-10。用户反馈 v02 与参考不够相似，主要观感为“太高”，指定 [design-v01.png](../assets/characters/first-character/concepts/design-v01.png) 为本轮基准。

## 输入与变更范围

- 唯一编辑底图：[v02 全覆盖正面候选](../assets/characters/base-templates/base-a-mage/v02/base-a-mage-covered-front-v02.png)。保留不透明高领、长袖、长裤连脚的灰色基础层及正面 A-pose 用途。
- 比例基准：design-v01 左侧全身图；脸型/五官参考：右侧头像。头像局部不能用作身体缩放比例。
- 全覆盖基础层、无发型/佩戴配饰继续保留；不把设计图的白裙、头发、猫耳饰、项链、尾巴等复制到基底。
- 精灵耳属于本轮采用的基础脸部特征；恢复角色自身左红右蓝异瞳，即正面观者右红、左蓝。它们是本次脸部参考选择，不代表两类模板所有角色都必须使用同一耳型/眼色。

## 差异判断及修订

v02 显高并非单纯整张图尺寸大：头相对身体较小，颈肩连接和下肢轮廓更修长，面部及耳型也与设计图不同。本轮对头、颈肩、躯干和腿的相对关系作调整，保持四肢纤细，不以增加围度代替娇小感。

生成后的 v03 头部相对身体增大明显，颈部与下肢更紧凑，异瞳方向、精灵耳与小嘴形已靠近指定设计。它仍是新候选，不能自动替用户确认“比例已正确”。设计图的头发与长裙遮住部分头骨、腰胯和腿部，隐藏轮廓仍为推定，不能声称精确提取。

## 交付与检查

- [v03 正面候选 PNG](../assets/characters/base-templates/base-a-mage/v03/base-a-mage-design-proportion-front-v03.png)
- [完整提示词](../assets/characters/base-templates/base-a-mage/v03/prompt.txt)
- [生成记录与输入/输出摘要](../assets/characters/base-templates/base-a-mage/v03/generation.json)
- [候选与人工 QA](../assets/characters/base-templates/base-a-mage/v03/candidate.json)

方法为内置 image_gen 编辑，按上述两图角色输入；输出原样复制为 1024×1536 PNG，未做像素后处理。源设计图、v02 图片均保留不变，SHA256 记录于候选中。生成式编辑不保证非目标区域逐像素相同；本轮不作该承诺。

v02 已根据用户反馈标为 `revision_requested`，v03 标为 `not_reviewed`。B 类弓箭手不改，基础模板仍恰好两类。文件检查验证摘要、文件可读和引用，不证明自动还原度。

下一关口：用户看图确认头身关系、颈肩、四肢长度/粗细及脸型。头部相对放大的程度尤其需要确认。不直接进入分层或绑定，当前无透明分层、PSD、CMO3/MOC3 或动画；不替换已认可角色设计的原始图片。
