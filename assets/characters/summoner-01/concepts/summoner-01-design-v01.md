# 召唤师 · 全身角色设计 v01

2026-11-14 · DesktopPet · A 类魔法师 · 待用户确认

## 参考与设计

- [召唤师参考图目录](../../../../角色素材/魔法师/召唤师/召唤1/)中的 `召唤参考图1.png` 至 `召唤参考图16.png` 均已逐张查看。每张 PNG 的 SHA256 都与首位角色案例中同编号的 `角色N.png` 相符。另将第 1、3、4、8、9、10、12、13 张按编号从左至右、从上到下排成两行，最近邻放大 3 倍，作为生成输入 4。第 1、3、8 张用于观察衣饰和发型，第 4、9、10、12、13 张补充动作中的尾饰、裙摆和赤足。素材目录中的视频未用于本轮生成。
- 输入 1 为 [A 类魔法师 v10](../../base-templates/base-a-mage/v10/base-a-mage-proportion-front-v10.png)，用于纤细体型、约 6.6 头身、腿长分配和浅粉象牙肤色。底稿 SHA256 为 `663bafceed700b487285a1d22c8de6b8c06175388faa6bbbc6ce95c6b4ebd6ee`。
- 输入 2 为同角色已有的[三视图版 12](../../first-character/concepts/turnaround-v02-accessories-v12.png)，用于服装与配饰。白色泡袖露肩裙、花纹镂空裙边、绿宝石颈饰、猫耳发饰与精灵耳、紫结尾饰、白花脚环沿用[已确认的外观规格](../../../../docs/character-spec.md#1-已确认的外观基线)。角色自身右眼为蓝色、左眼为红色。
- 输入 3 为[早期候选设计](../../first-character/concepts/design-v01.png)，只参考白色卷发的绘制和五官。该图和三视图都只作为参考，本轮从头生成全身设计。
- 本轮采用近正面微转身、单手托掌的施法姿态，浅底柔光突出头发、裙褶及配饰。裙边花纹和布料细节按既有样式细化。

## 出图与核验

[全身设计图 v01](summoner-01-design-v01.png)为内置 ImageGen 生成的原始 PNG，尺寸 1024 × 1536。工作区副本与生成文件的 SHA256 一致，均为 `c3f5407c127e4aa8d91b6ffe211121e0c2fc3c5f4563244e86f626c4f59a64cb`。

目视核对了蓝红异瞳的方向、猫耳发饰和精灵耳的位置、绿宝石、尾结、裙边、花脚环和赤足。两手和两脚均完整入画，观者左侧的后跟随姿态微抬。头身与露出的肩颈、小腿和脚踝按 A 类 v10 目视对照，胯膝位置受长裙遮挡。

## 完整生成提示词

```text
Use case: stylized-concept. Generate a new, refined full-body 2D anime character design illustration of DesktopPet's white-haired Summoner mage. Render ONE figure, no inset. This is a fresh presentation pose for the established character, at the new A Mage v10 proportions, with crisp game concept art finish and completely readable outfit.

Input 1 is Mage A v10, the primary body and skin reference. Match only its anatomy, head size, slender narrow-shouldered frame, limb lengths, soft pale pink-ivory skin. Proportion targets under the costume: about 6.6 anatomical heads from bare scalp to soles, chin at about 15% of height, crotch near 46%, knees near 66%, ankles near 94%. Hair and cat-ear ornaments are excluded from these measurements. Keep delicate small hands and feet, subtly rounded tips, no extreme fashion lengthening or oversized head.

Input 2 is the verified costume reference, approved-in-direction three-view version 12, showing the same character as the sprites. Follow its costume and accessory construction, design and colors. Its older anatomy and A-pose do not govern this new drawing. Input 3 is the earlier hero concept for the well-defined luminous white hair and face identity only. Input 4 is the zoomed contact sheet from the provided raw sprites, additional evidence for hair movement, the white flowing long dress, blue-violet bow and bare feet. Ignore screenshot backgrounds, outlines and game UI.

Make both eyes visible: her anatomical right eye (viewer's left) clear sapphire blue and her anatomical left eye (viewer's right) deep warm red. Soft white wispy fringe, long voluminous snow-white waves down to her wrists when relaxed, cool pale neutral-lilac shadows, hair chiefly behind the shoulders. Show the real small pointed elf ears horizontally below the independent white cat-ear head ornaments with warm pink lining, small white flower clusters and muted deep violet satin bows at their bases. White scalloped neck ribbon with a single bright emerald green pendant in a very fine gold setting. Gentle, quietly focused expression with a very small smile.

Opaque snow-white off-shoulder bodice with ruffled neckline, modest coverage, puff sleeves that end just above the elbows in airy fabric cuffs, neat small white waist ribbon, graceful A-line mid-calf skirt with continuous even lower hem, subtle tonal floral cutwork with pale lavender depth, and a crisp lower white ruffle. Fine embroidery in the supported motifs, restrained and well resolved at full resolution. At the back hip a single slim white wearable tail curves outward to the viewer's left with a single deep muted violet satin bow near its white tip. Both ankles wear slim white floral bands and both feet are bare, natural and visible in full. Separate the pale skin, hair, lace, satin and opaque matte fabric with clean edges and gentle material-specific shading without darkening the character. Match the largely white palette with purple only in accessory bows and understated shadows.

Portrait illustration, from the tips of the head ornaments to the soles with comfortable margins, character filling the vertical canvas. Near-frontal eye-level three-quarter view with only a slight turn. Light, grounded contrapposto with two separate planted bare feet fully visible. One forearm gracefully opened low to the side, palm gently up in a subtle summoner gesture, and the other down and relaxed clear of the skirt. Hands clear with natural fingers. Dress folds fall under gravity, with a soft outward curve in the hair and tail, and only a very soft grounding shadow. Use a clean very pale neutral studio backdrop. No title, typography, border, watermark, props, staff, spell effects, or extra figures. High-end hand-painted anime rendering with deft fine linework, soft clean lighting, elegant fabric folds, distinct luminous white hair locks, carefully drawn face and fabric details.
```
