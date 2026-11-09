# 两类基础模板首次制作记录

日期：2026-11-09。模板：A=`base-a`（魔法师），B=`base-b`（弓箭手），名称为用户暂定，稳定 ID 不变。

## 输入和实际检查

用户目录：`D:/desktop-pet/素体参考图/`。魔法师 8 张、弓箭手 9 张，已逐张查看，原件均未修改。索引见 [reference-inventory.json](../assets/characters/base-templates/reference-inventory.json)。

魔法师 1–7 为含头发与内衣外观的游戏图，第 8 张为低像素侧向轮廓；弓箭手含头发、遮盖和弓箭，另有跳跃/翻转姿态。来源图仅 75–143 像素宽，不足以精查指趾、精确关节或隐藏身体结构。不能把姿态的透视投影当成不变的身体比例。

## 生成过程与边界

1. 计划用魔法师 1/3/5/8 为参考，生成不透明中性连体基础层版本，保留比例并去除原装饰/武器。完整提示词为 [A 初始尝试](../assets/characters/base-templates/base-a-mage/v01/prompt.txt)。
2. 内置 image_gen 在输入审核阶段拒绝该请求，类别 sexual，无图片输出。请求标识与记录见 [generation-attempts.json](../assets/characters/base-templates/generation-attempts.json)。没有继续请求去除幼态角色的遮盖，也没有将被拒绝的生成称为成功。
3. 改为两项独立的非人形面貌机械技术人台：不传入原参考图，使用较紧凑/较修长的文字方向，生成用于讨论结构的机械分段图。它们不是原参考的人体复原，也不是原请求中去掉遮盖的人体素体。
4. 两项最终位图均为内置 image_gen 输出，未经像素后处理，复制到项目后记录 SHA256；原生成文件保留。

## 交付

| 模板 | 草案 | 最终实际使用的完整提示词 |
|---|---|---|
| A 魔法师 | [机械结构草案 v01](../assets/characters/base-templates/base-a-mage/v01/base-a-mage-mannequin-v01.png) | [mannequin-prompt.txt](../assets/characters/base-templates/base-a-mage/v01/mannequin-prompt.txt) |
| B 弓箭手 | [机械结构草案 v01](../assets/characters/base-templates/base-b-archer/v01/base-b-archer-mannequin-v01.png) | [mannequin-prompt.txt](../assets/characters/base-templates/base-b-archer/v01/mannequin-prompt.txt) |

工作区说明及人工 QA：[README](../assets/characters/base-templates/README.md)。文件索引：[candidate-index.json](../assets/characters/base-templates/candidate-index.json)。文件检查：[file-check.json](../assets/characters/base-templates/file-check.json)。

## 未达到的目标与下一步

本轮没有完成从参考精确恢复人体素体，没有人体基底定稿、透明分层 PNG/PSD、CMO3/MOC3、可驱动参数或动画。A 草案头部偏大、四肢偏厚，B 草案较修长，两类差异可能过度，不冻结这些比例，不进入绑定，也不据此声称 G0 通过。

继续人体外观候选时，采用完整着装的中性站姿参考及不透明中性基础层，先人工确认轮廓和比例。隐藏结构只标推定，不将它称为精确提取。技术人台若不符合用户预期可弃用；它不替代已认可角色设计。

## 版本同步

上次本地提交 `dd2c113` 包含二维路线、双模板规范、接口和验收闸门，先前未推送成功。本轮新增原始参考、索引、提示词、失败记录、机械草案与 QA，并更新参考已提供的状态。将本轮提交与前一提交一并推送，实际结果以交付时 Git 输出为准，不预写“已同步”。
