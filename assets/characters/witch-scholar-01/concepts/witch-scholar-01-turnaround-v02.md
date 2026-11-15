# 魔道学者「魔道1」三视图 v02

本版依据用户反馈修订 [三视图 v01](witch-scholar-01-turnaround-v01.png)。角色造型仍以已选定的 [修长身形 v01 去白边设计图](witch-scholar-01-design-v01-white-cat-print-clean-edge.png) 为依据。使用内置 ImageGen 编辑，另存为 [三视图 v02](witch-scholar-01-turnaround-v02.png)。

- v01 的中间视图朝画面左侧，实际显示角色左侧，兔饰却画在近侧。v02 改为角色右侧面，鼻尖和鞋尖朝画面右侧。兔饰位于右太阳穴，从侧面只见兔脸的一侧。
- 背面在画面右上方补齐同一兔饰的第二只耳朵。两只耳朵均从发顶露出，兔脸被头发遮挡。
- 放大检查了三栏兔饰耳数及左右位置，并目视核对鞋底线、裙摆和踝圈高度。正面保留原站姿、服装和白猫印花。生成式修订可在指定区域之外引入少量笔触差异。
- v02 为 1536 × 1024 PNG，SHA256 为 `bd2ef26256ed4c8767cf7501b63ca3bb35c1de303bd83808ed6aa586cb535f6c`。

## 生成提示词

第一轮以三视图 v01 为输入修正侧视方向和背面兔耳。

```text
Edit this exact three-view Witch Scholar sheet (landscape 1536×1024). Make two strictly scoped corrections.

1. MIDDLE PANEL ONLY: redraw the middle view as a true RIGHT PROFILE with the nose, front of chest, and shoe toes unmistakably pointing toward the RIGHT edge of the canvas, toward the back-view panel. Hair at the back of her head and body falls toward the LEFT of her profile. This is the character's own RIGHT side shown to camera, consistent with the rabbit clip on her own right temple (viewer left of the original front view). The ear of the human character and exactly one cyan eye on this right side are visible. The existing single white two-eared rabbit clip sits near the front of the visible right temple, with both ears in their same relationship, the body of the small accessory viewed at a realistic side projection, not its full face facing camera. Its face points in the same direction as the character, toward the right. Reconstruct the same exact outfit, hair colors and distinct long curl shapes, head, neutral upright pose, leg proportions and relaxed hand, now seen from the character's right. Preserve the middle panel's centered placement, crown height, eye/shoulder/waist/knee heights, skirt hem and ankle band, and precisely shared floor line. Black leather shoe's toe points RIGHT and displays the single small flat white cat-face print on the vamp, foreshortened as in a profile. Allow natural overlap of far limbs into this true side view. Do not change the approved front and back poses to accommodate the profile.

2. BACK PANEL ONLY, AT TOP OF HEAD: retain the existing single rabbit clip at its established position on the upper image-right edge of the character's head in the BACK view, to the right of the pink cowlick. At present only ONE light lavender rabbit ear projects beyond the pink hair. ADD the corresponding SECOND distinct elongated rabbit ear, visually linked to the same clip, adjacent to the first, matching the reference ear proportions and pale outer lavender-white material. On rear view the existing ear tilts outward to image-right, the additional inner ear is straighter and rises a little higher, as the frontal accessory mirrored by the opposite viewing angle. Both ear silhouettes are clearly visible simultaneously and have a little gap. Hide the clip's face behind the pink hair. No extra heads, decorations, or ears on the other side. Keep the cowlick and rest of the rear view completely intact.

Front panel on left is untouched. Preserve the canvas, soft very pale pink background, uniform orthographic scale, straight ground line, body proportions, clothing, color and fine crisp anime linework everywhere, with no added text, framing, other panels, or white halos. Keep generous horizontal spacing.
```

第二轮以第一轮图为输入清理右侧视兔饰多出的一条耳形，使其与正、背视图一致。

```text
Make exactly one tiny retouch on the supplied Witch Scholar orthographic three-view character sheet. In the CENTER panel only, the white rabbit-head hair clip has three apparent ear shapes. Remove the extra MIDDLE darker dull lavender upright blade-shaped sliver behind the other two ear lobes, immediately to the left of the tallest white upright ear and above the slanted left ear. Fill this triangle/sliver with the correct continuous pink hair and pale background following the original edge of the head. Keep the two distinct light rabbit ears in place: the left ear that leans left diagonally and the right, tallest ear that is almost vertical. The final single rabbit clip in center profile must have exactly TWO visible ears, with a clean open gap between them and no other lavender shape, and the rabbit's face still points to frame right. Preserve the white rabbit head, its facial features, pose, and position. The front panel and back panel rabbit clips are ALREADY CORRECT with two ears each; preserve those precisely. Preserve the back panel's two ears peeking above the pink hair at image-right. The center character, her nose and her shoe all continue to point RIGHT. Do not alter any other pixel intentionally, do not rescale or recompose, preserve the entire full-frame 1536×1024 landscape art.
```
