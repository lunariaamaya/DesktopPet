# 元素师「元素1」三视图 v01

用户指定 [设计图 v03](elemental-mage-01-design-v03.png) 为本轮依据。三视图已生成，待用户确认。

## 参考与取舍

- 设计图 v03 是角色外观、配色、服饰和配饰的主要依据。SHA256 为 `5ec3dc07472385571fd844ac8812be09de29ce53eccad3925283d3f17df68eab`。
- [A 类 v09 底稿](../../base-templates/base-a-mage/v09/base-a-mage-skin-tone-limbs-front-v09.png) 是设计图 v03 所用的体型依据，本轮用来辅助核对站立后的头身关系、四肢和肤色。
- 第三张输入是用户提供的「元素参考图8.png」，仅用于观察背后发束的走向。背面发束的具体排布、裙边刺绣的环绕与服装被头发遮挡的部分按 v03 作延续性推定。
- 三个方向采用同一自然微 A 站姿和柔光。画面从左到右是正面、角色自身右侧面、背面。侧面鼻尖与鞋尖朝图面右方。

## 验收与输出

- 目测核对三个方向的头饰、肩、裙摆和足底高度。三张全身轮廓完整，平底鞋踩在同一地面线上。
- 正面双眼与侧面可见眼均为粉色。头饰缎带位于角色右侧，正面见于画面左侧，背面见于画面右侧。珍珠扣位于角色左前腰；右侧面和背面均由身体或衣装遮挡。
- 粉色兔兔拖鞋正面可见兔脸，侧面与背面可见平底及裸露后跟。长发自然遮挡背部衣身及腰线，衣背闭合结构仍待设定。
- 输出为 [三视图 v01](elemental-mage-01-turnaround-v01.png)，1536 × 1024 PNG。使用内置 ImageGen 生成并保存原尺寸。
- SHA256 为 `abf36a07e641a1355b62bdedeadba363b95a611363253cba8b0f466a55309079`。

## 完整生成提示词

```text
Use case: stylized-concept, production character turnaround/model sheet. Generate a single landscape high-resolution 2D anime reference sheet of the EXACT elemental mage in Image 1, arranged left to right FRONT / RIGHT SIDE / BACK. Image 1 is the approved v03 appearance, color and costume reference, including the exact eyes and slippers in its insets. Image 2 is the same type-A body reference v09 used for this very design: use its petite build, neck-shoulder relation, slim arms and legs, and soft pale pink-ivory skin as support for translating v03 into a neutral standing pose. Preserve v03's own head/face proportions, pink eyes, clothes and accessories. Image 3 is a tiny historical sprite and serves only as a clue for how her wavy hair hangs at the rear. Render everything in v03's refined anime drawing style, not pixel art.

Show EXACTLY three uncropped full-body figures, divided into equal columns with generous gutters. Label them simply FRONT, RIGHT SIDE, BACK in unobtrusive small gray sans-serif with no other text. Neutral plain warm white background. Same orthographic/long lens camera height and scale for all views. One faint straight shared ground line under all three. Align the tip of the ornament, skull, eye height, shoulders, elbow and wrist heights, waist, skirt hem, knee, ankle, and flat sole across all three columns. Center all feet on the same depth plane and parallel, shoulder/hips level, no head tilt. Neutral natural A-pose for all three, hands low and slightly away from hips, palms facing thighs, fingers relaxed and anatomically correct, five digits per hand including one thumb. Right side means view the character's anatomical right side with nose and toes pointing toward the RIGHT edge; draw a true 90-degree side profile with only the near eye visible, no three-quarter rotation or staggered legs. In rear view see her nape and the back of her body and feet, with correct near/far finger occlusion.

Copy v03's clean straight pale ivory-platinum bangs, delicate cheek curls and huge loosely curled ivory-blonde waves with soft lavender shadows. Hair flows down her back at rest, visible from all sides, longest tips slightly lower than the white petticoat edge near the knee; do not make it reach the ankles or bunch it up. In back view cascading separated curl masses flow naturally over the back of the blouse and upper skirt, letting sleeve ends and skirt edges remain readable. Pale elf ears on the sides of her head. Both eyes are exactly same rose-pink, never blue or fire red. Same one little lilac and white mascot hair ornament on crown with forehead diamond, pointed upper tuft, blue eyes and tiny pink/gold ribbon on its anatomical right (viewer LEFT in the front, viewer RIGHT from the back; visible on the near side in right profile). In profile show at most one of the mascot's eyes. From behind show the mascot back with lavender shading, no facial features. Preserve pearl fixing band at its base.

Match v03's white off-shoulder gathered top with light-lilac shading, puffed elbow sleeves and frilled cuffs, rose-pink waist sash, and pearl rosette with small drops on the character's anatomical LEFT front waist (viewer RIGHT in FRONT; on far side from the chosen RIGHT SIDE, hidden in BACK). Rose-pink pleated short bell skirt with the same fine white floral-vine embroidery band and continuous scalloped pink edge, layered white/lilac ruffled petticoat. Neutral skirt hem falls evenly in all directions. The back bodice/waist hidden by the hair can be a simple continuous matching garment with only original design elements showing where naturally visible. No added accessories.

Exact v03 pink plush bunny HOUSE SLIPPERS with two bunny ears on each toe, cute faces at the front, toe covers only, uncovered skin heels, thin perfectly flat continuous pink soles. Show the bunny faces and paired ears from the front. The true side profile carefully shows a flat sole, toe bunny and a visibly bare ankle and heel, with no heel counter even at the far foot. In the back view show exposed bare heels resting on flat sole, no vertical back walls, no rear-facing bunny faces. No high heel, ankle strap, ribbon tied to ankles, heel strap, or boots. Keep identical size and materials to v03. Draw all silhouettes from ornament to bottom of shoes with padding. Use soft uniform lighting for shape and matching material color. No action pose, costume variants, effects, decorative layout, extra studies, inset panels or superfluous art.
```
