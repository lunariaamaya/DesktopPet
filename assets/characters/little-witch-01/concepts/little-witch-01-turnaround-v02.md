# 小魔女1三视图 v02

以 [三视图 v01](little-witch-01-turnaround-v01.png) 为唯一编辑底图，沿用 [角色设计图 v01](little-witch-01-design-v01.png)。按用户反馈修订长发遮挡和小腿围度。

- 背视图长发从后颈连续垂至膝附近，叠在后披肩、腰带和裙片外侧。正面和右侧面的发型沿用底图。
- 收细正、右侧、背面的腿肚，保留脚踝以下和白色人字拖。以原尺寸图的第 727 行抽样估计五条可见腿肚的轮廓跨度，按画面从左到右分别由 46、45、50、46、46 像素缩至 40、40、43、40、40 像素。
- 调用内置 ImageGen 绘制修订，再将四处区域贴回底图。以左上角为原点，右、下边界不含，背发区域为 `(976,146)–(1506,670)`，正面小腿为 `(224,638)–(374,882)`，右侧面小腿为 `(696,633)–(786,882)`，背面小腿为 `(1158,636)–(1318,882)`。区域内边使用 18 像素平滑过渡。目视核对遮挡、腿型和接缝，并逐像素验证四处区域外的变动数为 0。

| 文件 | 尺寸 | SHA256 |
| --- | --- | --- |
| [修订底图 v01](little-witch-01-turnaround-v01.png) | 1536 × 1024 | `47c71d79725043c0ff24b4926e2e8fe7a70a29bdb274a5f2ca06ed6204b5f58a` |
| [修订版 v02](little-witch-01-turnaround-v02.png) | 1536 × 1024 | `71c3ae0182fd65f1c3a5ac34ff46133fd8b9235e4240d4b3a27a16eb3db41b55` |

## 生成提示词

```text
Use case: precise-object-edit. The supplied 1536×1024 Little Witch turnaround is the sole edit target. Preserve the exact three column layout, dimensions, labels, front and right profile orientation, rear head and all four ears, chrysanthemum positions, eye color, faces, clothing design, body height, torso, thighs, ankle and foot positions, floor line and white flip-flops. Make only these two changes in place:

1. REAR VIEW HAIR ONLY, right column. Fix the contradictory front/back overlap. Every long lock falls entirely behind the character from the shoulders downward. In this BACK VIEW the long hair is on the camera-near surface of her back and must visibly OVERLAY the capelet center, back bodice, rear waist belt and central upper back of the skirt. It is a single cohesive broad curtain, solid overlapping continuous locks from the nape down to around the knees, with no open holes down its central body area. Keep several graceful sculpted waves and natural curling tips, silver-white with lavender-gray undersides. Keep the original hair length and gently flowing volume. All outer long locks that previously loop around the upper arms, weave under sleeves, or appear to swing forward around the hips should join the same posterior fall, inside the rear silhouette of the shoulders, elbows and hands or immediately alongside as physically appropriate. No long locks show through the gaps in front of arms or emerge from under the frontward edges of sleeves or skirt. Keep the contours of both sleeves and hands, the same rear garment drapes visible below and alongside the hair. No rear bow, braid, or new accessories. Preserve the front and profile hair drawings exactly. Begin the changed back-hair arrangement below the elf ears so that both deer ear ornaments, both pointed elf ears, crown, headband and tiny visible petals on the character's right stay intact.

2. SLIM THE BULGING PART OF THE CALVES in ALL THREE views. Make the legs visibly more slender between knee and ankle, by reducing the widest mid-upper calf (gastrocnemius bulge) about 18–22 percent relative to the exact input. Front and back, tuck in both the inner and outer calf contours gently without moving the axes of either lower leg. In the right-side profile reduce the rounded bulge on the back of the visible calf, on the right edge of that leg. Preserve the front shin edge, skeletal alignment and neutral upright stance. Use a subtle anatomical transition from the knee through a slim smooth taper toward the same ankle joint, rather than a hollow or angular indentation. Do not change the length of the lower legs, the height or width of the knee, the ankle or the bare feet and white lightweight flip-flops. Smooth matching ink line and pale pink-ivory skin, no added muscle outlines or heavy contour shading.

Maintain exact original position and scale of drawings, unchanged background and labels FRONT, RIGHT PROFILE, BACK. The finished image must look like this same polished artwork with just the rear long-hair layering corrected and all calf bellies narrowed. No added views or decoration.
```
