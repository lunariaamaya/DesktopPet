# 魔法师底稿确认与弓箭手正面候选

日期：2026-11-10。稳定模板仍为 A=`base-a`（魔法师）、B=`base-b`（弓箭手），不新增第三类。

后续更新：用户要求修手部重影与五指可读性，明确弓箭手角色自身左眼紫、右眼蓝，随后要求修复头部肤色块。[v06 修订](archer-hands-eyes-head-revision-2026-11-10.md) 现已获用户确认，作为后续弓箭手设计的身材比例、体型和肤色基准；与魔法师 v09 一同纳入 [skill 底稿规范](../skills/character-reference-to-turnaround/references/cases/desktop-pet-base-templates/reference-standard.md)。下文 v02 的普通双眼颜色是当时推定，已被用户新设定覆盖；原图/历史记录保留。

## 魔法师：确认并冻结 v09

用户明确要求：“很好，就以这张作为魔法师角色的底稿，后续的魔法师角色设计就参照这张的身材比例及体型和肤色。”

当前正式正面底稿为 [魔法师 v09](../assets/characters/base-templates/base-a-mage/v09/base-a-mage-skin-tone-limbs-front-v09.png)，SHA256 `4c740be63fe75c00ab0f093cfb76768b0c43bf09c1329a252f897199403bee4c`。原图未改动，已登记 `approved_reference`；规范与取样见 [baseline.json](../assets/characters/base-templates/base-a-mage/baseline.json)。后续魔法师设计沿用该图的头身关系、躯干/四肢相对长度、纤细体型、肩腰胯轮廓及浅粉象牙白肤色，除非用户明确提出新变更。发型、衣物与饰品设计应建立在这个基底上。

认可的是正面底稿及上述特征，不是精确恢复原始身体、真实厘米参数、侧背面结构或已绑定模型。v08 保留为历史认可参考，v09 为当前有效基线。

## 弓箭手：参考与输入分工

已查看 `素体参考图/弓箭手/新素体参考图/` 中 12 张新参考的联系表，单独查看原图 1、2、5、6。图片宽 115–145 像素，动态姿势、长发、弓箭和原服饰遮挡部分结构，无法由此精确恢复隐藏身体。

- [参考清单与 SHA256](../assets/characters/base-templates/base-b-archer/v02/reference-inventory.json) · [12 张参考联系表](../assets/characters/base-templates/base-b-archer/v02/reference-contact-sheet.png)。原文件保持不变并随本轮纳入版本管理。
- 生成实际输入：站立参考 1、2 主要提供比例/体型；侧面参考 5 辅助判断体型。其余图片用于联系表观察，没有全部送入生成器。
- 魔法师 v09 仅提供绘制完成度、浅肤色、灰色基础服装覆盖范围及手足标准。弓箭手不复制魔法师的大头比例、精灵耳或红蓝异瞳。

弓箭手候选采用相对更小的头部占比、修长躯干与较长腿部，统一为正面自然站姿。无发型、头饰、弓箭和其他配饰；躯干与骨盆使用不透明灰色高领无袖短连体基础服装。手臂、腿部和手足为连续的低饱和浅粉象牙白。

## 候选与生成记录

- [弓箭手正面底稿候选 v02](../assets/characters/base-templates/base-b-archer/v02/base-b-archer-covered-front-v02.png)，1024×1536，SHA256 `69e19e6018721583fe96aad3ee297e337cfffbf23a3aa594b9e67203d607632f`。
- [魔法师/弓箭手并排图](../assets/characters/base-templates/base-b-archer/v02/mage-archer-comparison.png) · [弓箭手手足放大](../assets/characters/base-templates/base-b-archer/v02/hand-foot-review.png)。两者显示缩放相同，不表示两类角色的真实身高已确定。
- [完整提示词](../assets/characters/base-templates/base-b-archer/v02/prompt.txt) · [输入角色、摘要和生成记录](../assets/characters/base-templates/base-b-archer/v02/generation.json) · [颜色取样与人工检查](../assets/characters/base-templates/base-b-archer/v02/visual-inspection.json)。

使用内置 image_gen，4 张输入、1 次生成。正式 PNG 原样复制到项目，不覆盖旧版，也未作脚本像素后处理。v01 为先前独立机械人台实验；本轮 v02 是弓箭手首张人形正面底稿候选，不在机械人台上直接改造。

## 检查与待确认

全图及放大观察中，两手各可辨一拇指加四长指，姿态为自然轻拢；两脚各五趾，内侧大脚趾，保持圆润的小手小脚方向。四肢与手足受光取样约 `#FEEEEB`–`#FEF2F0`，与魔法师同色系，未见明显手腕或脚踝硬色块衔接。取样坐标、像素数量及分位数在检查 JSON 中，不能据此宣称全局无底噪或解剖完美。

耳型和精确眼色无法从低清参考可靠确定。本轮暂用小型普通耳与双侧低饱和红棕色眼睛，明确属于推定候选，不是用户设定；比例、体型、耳型、眼色仍由用户看图判断。没有将魔法师专属异瞳默认继承给弓箭手。

B 的状态为 `not_reviewed`，不自动登记为认可底稿。A 已确认；两类均尚无分层 PNG/PSD、Cubism 工程、绑定或动画，完整 G0 与后续阶段没有自动通过。
