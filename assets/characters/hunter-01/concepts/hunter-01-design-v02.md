# 猎人 1 · v02 身高微调

[v02 全身设计图](hunter-01-design-v02.png)为待确认候选。唯一编辑输入为 [v01](hunter-01-design-v01.png)，以 v01 的宽站姿和斜持猎具为参照。使用内置 ImageGen 对原图做生成式编辑。

- 目标为同画幅内的角色高度调低约 5%，主要微收大腿和小腿长度，延续 v01 的头部大小和宽站脚位。
- 对比同尺寸图，角色头部与顶饰向下约 60 像素，脚底地面线基本对齐，画面内的头顶至脚底高度缩短约 5%。此数值按当前动作的画面地标估测。
- 复核了头脸尺度、宽站姿、双踝与猎具斜线。为了配合上身下移，猎具上端和握持点也向下微移。袖口、发梢和裙片的细部随生成略有重绘。
- PNG 原尺寸 1189 × 1323。
- v01 SHA256 "ab52bdd5f4f3f61f27db1e75ff94c13dd2603053a7a74e382fbe9638693534a3"。v02 SHA256 "9d64922243a4dddfd783782c73bd7bb4ed86cdbadd76c63f508f5d03b024b84e"。

## v02 完整生成提示词

```text
Use case: identity-preserve, precise edit of the existing Hunter character illustration. The only edit target is the attached v01 illustration. Return a single full-body illustration in the same portrait framing.

Make this exact adult character look a little shorter at the same image scale. Keep her feet on their current ground level and at the same wide side-to-side placement. Reduce the vertical head-to-sole extent by about 5% (in the 1189x1323 original, approximately 55 to 60 pixels), while keeping the original scale and proportions of her face, head, neck, shoulders and upper body. Move the intact upper body slightly down toward the feet. Absorb the difference mainly by slightly shortening both thighs and both calves in a balanced way; keep the legs slim, maintain natural knee and ankle articulation, the leftward slant of the leg at viewer-left and the rightward slant of the leg at viewer-right. Keep the actual feet, toe orientation, fine gold anklets, both knee bends, and the distinctive broad grounded stance. This should look like a subtle change to her anatomical height, not a camera zoom, a global stretch, squat, childlike change, or enlarged head.

Preserve the illustration as closely as possible. Keep the same face, eyes and expression, pale ivory skin, two small petal-like headpieces, identical white-lavender-pink wavy hair with the same locks and finish, wrap neckline, gray waist wrap, two very long ivory sleeves with red running trim, pink overlapping skirt and translucent layers, both original hand poses and placements relative to the costume and the prop, linework and pastel lighting. Preserve the existing fantasy prop as drawn, its wood-and-indigo palette, gold edging, twin rail silhouette and amber inlay, its diagonal in front of her and resting end near the ground. Allow the minimal positional adjustment at the grip and the stock required by the slight downward shift of her upper body. Keep the canvas composition, simple near-white lavender-gray background and shadows. All of her and the prop remain inside the frame. No new detail, no redesign, no text or framing.
```
