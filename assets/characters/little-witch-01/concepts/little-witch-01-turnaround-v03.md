# 小魔女1三视图 v03

以 [三视图 v02](little-witch-01-turnaround-v02.png) 为唯一编辑底图，沿用 [角色设计图 v01](little-witch-01-design-v01.png)。

- 修正 v01 和 v02 的侧面方向。中间图为角色自身右侧，鼻尖、前胸及鞋尖朝画面右方，后脑与长发朝左。角色右鬓的唯一白菊花位于近侧，与正面的画面左侧及背面的画面右侧对应。
- 背视图长发采用更疏松的波浪发束、交错的发梢和外缘留白，发束继续垂在肩背及腰后的衣片之外，原发尾高度约至膝。
- 内置 ImageGen 重绘右侧面及背面长发，随后回贴至 v02。重绘带来右侧轮廓及背面发束附近袖口遮挡的细微差异。局部平滑收拢侧视图腿肚后缘。第 727 行抽样宽度与 v02 同为 43 像素。
- 以左上角为原点，右、下边界不含，回贴范围为侧面 `(530,0)–(971,970)` 与背部 `(975,146)–(1508,664)`，区域内边采用 16 像素平滑过渡。正视图及背面小腿、鞋履位于区域外，保留 v02 像素。

| 文件 | 尺寸 | SHA256 |
| --- | --- | --- |
| [修订底图 v02](little-witch-01-turnaround-v02.png) | 1536 × 1024 | `71c3ae0182fd65f1c3a5ac34ff46133fd8b9235e4240d4b3a27a16eb3db41b55` |
| [修订版 v03](little-witch-01-turnaround-v03.png) | 1536 × 1024 | `615811f2d11f530b48685899ff8cbbb85bfd2d68f771b1566144084958edc00b` |

## 生成提示词

```text
Use case: precise-object-edit. Input sheet is the only edit target: exact 1536 x 1024 Little Witch three-view turnaround v02. Redraw only the central profile and the rear-view long hair. Keep the entire FRONT drawing on the left visually identical. Retain the composition, margins, aligned crown and soles, soft off-white background, overall sizes, original linework and labels FRONT, RIGHT PROFILE, BACK.

Critical correction in MIDDLE column: REVERSE THE DIRECTION OF THE PROFILE. Draw an actual right-facing silhouette. Her nose, lips, chin front, chest, knee fronts and the toes in white flip-flops all point toward the RIGHT EDGE OF THE PAGE (→), toward the rear-view figure, not toward the front-view figure. Her back, both heels, and the mass of her long hair lie toward the LEFT EDGE OF THE PAGE (←). This shows her own anatomical RIGHT half, the side with the one white chrysanthemum. The flower stays visibly attached at the near right temple, above and slightly in front of the near elongated flesh-colored pointed elf ear, next to the separate pale furry right deer-ear ornament. Match flower position/size and pink-lilac eye to the front view. Only one near eye, no far cheek, exact 90° view. Project the single throat brooch, two utility pockets on her right front hip, capelet, ruffled sleeve and near hand as appropriate for a true right-facing profile. Turn the full-body drawing, not just the head: show the original slender calf (rounded rear contour on the LEFT, straighter shin on the RIGHT), knee height, small ankle and white flat V-strap flip-flop, now pointing RIGHT. Retain exact proportions, neutral upright stance, floor and layout. Main hairstyle falls behind the back, hence in this view the hair fans out to the LEFT while face and toes point RIGHT. Keep the delicate neutral illustration and original physical design.

Right panel: retain the true rear head, the two stacked ear types, blue headband, glimpse of white chrysanthemum petals only on viewer's right, same shoulder, arms, hands, skirt ends, knees, SLIM calves, ankles and shoes. Redraw only the long silver-white hair BELOW the elf ears. Match the lifted, airy, loosely waving outer silhouette of the FRONT drawing: show a fuller shape fanning outward well beyond both elbows, fewer bigger sections, buoyant S-curved locks with staggered ends, loose outer curls that separate and leave small natural background gaps along their outside edge. Keep roughly the same overall hair width and lower tips around the knees as the front. It should look light, loose, and fluffy, not tightly packed, flattened, uniformly curled or dense. Softer shadows between grouped strands and broad gentle highlights. EVERY long lock remains behind the character and stays layered on the outside of the rear of the outfit, closer to the viewer in the rear view. Let the outer curls arc outward to either side in the same rear plane with transparent-looking open spaces around the silhouette, while preserving a coherent long fall over the rear torso and waist. Do not route any lock forward between the arms and body. Preserve skirt tails visible below the hair and original pose. No new ornaments, markings, or figure.
```
