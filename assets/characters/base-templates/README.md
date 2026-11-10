# A/B 基础模板制作工作区

日期：2026-11-09。稳定模板 ID 与用户命名：A=`base-a`（魔法师），B=`base-b`（弓箭手）。名称可改，ID 不随展示名称变化。

**A 类魔法师底稿已确认：[v09](base-a-mage/v09/base-a-mage-skin-tone-limbs-front-v09.png)**。用户明确指定后续魔法师角色设计参照此图的身材比例、体型和肤色；规范与取样冻结在 [baseline.json](base-a-mage/baseline.json)。当前为正面静态底稿，后续外观服饰在此基础上设计，不擅自改变已认可的身体比例或肤色。见 [确认与弓箭手制作记录](../../../docs/archer-base-draft-2026-11-10.md)。

**B 类弓箭手底稿已确认：[v06](base-b-archer/v06/base-b-archer-continuous-head-skin-front-v06.png)**。用户明确指定后续弓箭手设计参照这张的身材比例、体型和肤色；规范与取样冻结在 [baseline.json](base-b-archer/baseline.json)。角色自身左紫、右蓝（正面看左蓝、右紫），手指及头部修色过程见 [制作记录](../../../docs/archer-hands-eyes-head-revision-2026-11-10.md) · [头部检查](base-b-archer/v06/head-color-review.png) · [B 类当前规格](base-b-archer/working-spec.json)。尚未分层或绑定。

**两类底稿的 skill 参考规范**：[A/B 规范与原尺寸图片](../../../skills/character-reference-to-turnaround/references/cases/desktop-pet-base-templates/reference-standard.md)。后续设计必须实际参照对应图的体型外形、头身关系、躯干/四肢比例和肤色，不仅匹配画风；服饰或发型设计不得擅自改变该基准。两张源 PNG 及 skill 内副本摘要一致。

B 类来源：[初始正面候选 v02](base-b-archer/v02/base-b-archer-covered-front-v02.png)、[12 张新参考索引](base-b-archer/v02/reference-inventory.json)。弓箭手自身修长比例保留，绘制/肤色标准参照魔法师 v09。v02 旧眼色推定已被用户明确的蓝紫异瞳覆盖；v03 手指分界改善不足、v05 整图修色导致头部外偏红，均记录为内部未采用结果，不作为当前底图。

历史认可参考：[自然小手 v08](base-a-mage/v08/base-a-mage-natural-five-finger-hands-front-v08.png)。后续四肢肤色 v09 已获确认并成为当前底稿，v08 保留作回退；两者均不等于多视图、分层或完整 G0 已完成。见 [重做说明及后续认可](../../../docs/mage-natural-hand-revision-2026-11-10.md) · [手型参考](base-a-mage/v08/natural-hand-guide-v08.png)。

v07 历史：[五指版（用户已否定）](base-a-mage/v07/base-a-mage-five-fingers-front-v07.png)。其计数检查不代表手势、肤色或轮廓质量达标，不作为后续默认底图。

v05–v06 历史：[脚部肤色与五趾候选](base-a-mage/v06/base-a-mage-detailed-toes-front-v06.png)。见 [脚部修订记录](../../../docs/mage-foot-revision-2026-11-10.md)。

v04 历史：[纤细直腿修订](base-a-mage/v04/base-a-mage-slim-straight-legs-front-v04.png)。按用户要求收细腿部并减弱外弓轮廓，详见 [腿部修订记录](../../../docs/mage-leg-revision-2026-11-10.md)。

v03 历史：[设计图比例修订](base-a-mage/v03/base-a-mage-design-proportion-front-v03.png)。此前用户反馈 v02 显高，指定 design-v01 为比例/脸型基准，已调整头身、颈肩、下肢及脸部特征。见 [比例修订说明](../../../docs/mage-proportion-revision-2026-11-10.md)。

2026-11-10：魔法师新增 7 张着装参考。前两次连接失败；用户检查网络后要求重试，第三次同方案成功，交付 [A 类全覆盖正面候选 v02](base-a-mage/v02/base-a-mage-covered-front-v02.png)。这是未确认的单张合成 PNG，比例与脸型待审阅，未分层、未绑定。见 [本轮记录](../../../docs/covered-mage-reference-attempt-2026-11-10.md)、[完整提示词](base-a-mage/v02/prompt.txt) 和 [调用历史](base-a-mage/v02/attempt.json)。旧参考由用户移至 `穿太少了/` 子目录，17 张摘要一致；历史索引的 `source` 保留原路径，`currentSource` 跟踪当前位置。以下 11 月 9 日机械人台记录保留，不覆盖当前 v02。

## 本轮实际结果

已逐张查看用户 `素体参考图/` 的 17 张图：魔法师 8 张、弓箭手 9 张。原件不覆盖，尺寸与 SHA256 见 [参考索引](reference-inventory.json)。画面尺寸仅 75–143 像素宽，动态姿态、头发与装备使部分轮廓不可见，不足以声称精确恢复原始身体。

最初尝试用魔法师参考生成不透明连体基础层版本；图像服务在输入审核阶段拒绝，未产生图片。没有继续请求去除这些角色的遮盖。失败提示词与服务返回原因见 [尝试记录](generation-attempts.json)。

随后改为**不使用参考图片输入**的新建非人形面貌、机械分段技术人台，用于讨论“较紧凑 A / 较修长 B”的方向。两张图均使用内置 image_gen 生成，图中文字已明确为结构草案：

| ID | 当前草案 | 完整提示词 | 状态 |
|---|---|---|---|
| base-a / 魔法师 | [结构草案 A](base-a-mage/v01/base-a-mage-mannequin-v01.png) | [人台提示词](base-a-mage/v01/mannequin-prompt.txt) | 未获用户认可，不能作为原参考精确重建 |
| base-b / 弓箭手 | [结构草案 B](base-b-archer/v01/base-b-archer-mannequin-v01.png) | [人台提示词](base-b-archer/v01/mannequin-prompt.txt) | 未获用户认可，不能作为原参考精确重建 |

两者均为白底、正/侧/背的 2D 合成位图，不是透明分层素材，也不是已绑定的 Cubism 工程或可播放模型。机械分段仅是绘图表现，不是实际可调用的骨骼。

## 人工检查与限制

- 当前图清除了发型、武器、饰品等角色外观元素，但采用了不同于人体底图的机械人台表达；不标注为“已完成去衣素体”。
- A 草案头部占比偏大、四肢仍偏厚，和参考的纤细程度有距离；B 草案明显修长。两者差异可能被生成放大，不能据此冻结实际比例。
- 三个视图有基本地面与头顶对齐，但没有逐关节精确配准，不保证手部、肩部和躯干在所有方向完全一致。
- 没有测得原始参考的精确头身比、身高厘米、骨盆/躯干隐藏结构。不能拿生成图的尺寸反推成原作者的真实参数。
- 没有分层、补全可动画面部、绑定、换装兼容或动作验收。不得将这些图直接登记为运行时 Character 内容包。

后续要继续制作更接近角色的覆盖式人体基底，应提供完整着装的中性站姿参考，并继续以不透明中性基础层呈现，不制作幼态角色的裸露版本。先确认轮廓与比例，再考虑图层和动作；本轮不进入二维绑定阶段。

## 版本与数据

[candidate-index.json](candidate-index.json) 记录图片摘要、方法和未完成项，是工作区索引，不是可加载的生产模型 manifest。

沿用 [二维管线](../../../docs/character-2d-pipeline.md) 的人工审阅关口。旧图、原始参考和失败提示词全部保留，不用新图覆盖已有已认可角色设计。
