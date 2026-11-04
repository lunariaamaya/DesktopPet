# v02 局部修订 06 · 同材质连续色与机位正面柔光

日期：2026-11-02。工具：内置 image_gen，非 CLI。输入 turnaround-v02-accessories-v05.png；输出 turnaround-v02-accessories-v06.png。用户认可最新版装饰位置，本轮只处理色彩连续和明暗，原版保留。

同材质采用连续底色：白发、白色衣料、肤色分别统一，不把紫灰色块作为材质花纹；阴影为平滑低对比中性明暗，保持头发蓬松和衣褶体积。紫色蝴蝶结、绿宝石、异瞳等真实配色保留。

照明约定：三幅视图各自有独立镜头轴向正面柔光；正视从角色正前、侧视从角色对应侧面、后视从角色正后照亮朝向镜头的表面。不是三视图共享同一世界坐标方向灯。不使用强烈偏色补光或斑驳阴影。

检查：白发和衣料上的紫灰色斑块明显减弱，过渡更连续；配饰本色保留。没有主动更改结构/装饰位置。生成式编辑不保证结构像素完全不变；绘制的照明也不等于经过三维光照或定量色差检验，待用户复核。

## 完整提示词

```text
MATERIAL COLOR CONTINUITY AND LIGHTING CORRECTION ONLY on this exact approved character three-view sheet. All geometry, line contours, hair lock placement/volume, anatomy, poses, fingers, face expression, clothing shapes, decoration positions, jewelry, tail/bow, ankle flowers, proportions, layout and white background MUST remain as supplied. Do NOT redesign or improve anatomy. Remove blotchy patchwork discoloration on SAME MATERIAL: white hair has one consistent clean WHITE base root to tip, white dress fabric has continuous WHITE base across its panels/sleeves/hem, skin has one continuous light peach base. Purple bows remain purple, emerald remains green, anatomical left eye red and right eye blue remain, inner-ear pink remains intentional. Do not bleach colored accessories. Hair and skirt should not have alternating lavender/gray/white painted PATCHES or high-contrast random islands; maintain airy fluffy hair and full soft folds using smoothly graduated LOW-CONTRAST neutral-gray shading following continuous surfaces, no stains, harsh cel patches, ombre, chunky zigzags, dirty cloudy mottling or plastic mirror highlights. Lighting rule: EACH VIEW has its OWN large soft neutral light centered ON ITS CAMERA AXIS. Front figure lit from directly in FRONT of its face/body; side figure lit from its CAMERA-FACING SIDE; back figure lit from directly BEHIND body facing back of head/dress. Thus every image's camera-facing surfaces are broadly and evenly illuminated, soft symmetric form falloff and subtle occlusion only in real curl/fold recesses. No common world-space side lamp, no strong lateral cast shadows, no purple colored fill, no hard rimlight. Preserve depth and curls, not flat white silhouette. Shade same continuous material with continuous smooth transitions, consistent exposure and white balance across all three views. Keep extremely fine existing decorative detail and exact hand/tail/accessory silhouettes. Full original three-view sheet, no labels/insets, no added elements, no cropping. Modest opaque fantasy costume unchanged.
```
