# 召唤师 · 三视图 v01

2026-11-15 · DesktopPet · A 类魔法师 · 待用户确认

- 底稿为用户指定的[全身设计稿 v01](summoner-01-design-v01.png)。SHA256 为 `c3f5407c127e4aa8d91b6ffe211121e0c2fc3c5f4563244e86f626c4f59a64cb`。
- 出图为[三视图 v01](summoner-01-turnaround-v01.png)，1536 × 1024 PNG。SHA256 为 `9195cda6313f58f652eaa12fd8e421413c550b10ebf3dcdedeb2d0f90fcc53f3`。归档文件为内置 ImageGen 的原尺寸输出。

## 参考与绘制

- 以全身设计稿 v01 为造型依据，保留发型、蓝红异瞳、白色泡袖长裙及镂空花纹、颈部绿宝石、紫结尾饰和白色脚环。[设计稿生成记录](summoner-01-design-v01.md)
- 同角色的[旧三视图版 12](../../first-character/concepts/turnaround-v02-accessories-v12.png)用于判断尾饰挂位、裙边延续及后视长发的遮挡。[A 类魔法师 v10](../../base-templates/base-a-mage/v10/base-a-mage-proportion-front-v10.png)用于复核体型、四肢比例和浅肤色。
- 从左到右为正面、角色自身右侧面、背面。正面中角色右眼（画面左）为蓝色，左眼为红色。右侧面的鼻尖和脚尖朝画面右侧，仅见蓝眼。背面露出双脚后跟。
- 三栏采用同尺度自然站姿、共用足底线，各视图均以镜头方向的柔光呈现。背面由长发自然覆盖后领和大部分后背。裙边沿用正面的花纹并绕至背后。脚环正面见花，侧面见花的侧缘，背面见素色环带。

## 核验与待确认项

初版把蓝眼画在了朝向错误的侧视上。用初版作编辑底图、全身设计稿 v01 作细节参考，重新绘制了中间一栏。成图已目视核对头部、肩腰、裙摆、脚环和足底线，以及项链和尾饰在三栏的投影。尾饰挂位仍由后发遮挡，侧视紫色尾结的折角为补绘，略接近正面展开效果。

## 首次生成提示词

```text
Use case: stylized-concept. Create a finished professional 2D anime CHARACTER TURNAROUND of the Summoner in reference image 1. One wide landscape sheet with exactly three equally scaled, full-length, nearly orthographic drawings: facing viewer straight on at left, exact 90 degree anatomical RIGHT profile in center (nose and toes point to page LEFT, only her blue eye visible), and directly from behind at right. Under each view place one small quiet gray typeset label, exactly "FRONT", "RIGHT PROFILE", "BACK". Uniform near-white background. No other lettering, frames, graphics, cast shadows or effects. Draw all full silhouettes with space above, below and between figures. One common straight baseline under the soles. Align crown, the tips of the paired cat-ear ornaments, shoulders, natural waist, hem, ankle bands and soles across all views. Use the same relaxed standing pose: head level, balanced on both bare feet, toes forward, both arms only slightly away from body and lowered, forearms straight and relaxed, natural small hands. This is repeatable construction art, so a quiet pose supersedes the casting pose in the hero design.

Input 1, "Summoner full-body design v01", is the primary design and visual finish authority: same face, hair, costume structure, accessory sizes and colors, anatomy and slender silhouette. Render this design faithfully rotated into each direction. Preserve the detailed high-key anime rendering of input 1, luminous snow-white hair, rich but controlled shadows, subtle lavender shading and carefully finished folds. Input 2 is the same character's earlier turnaround: secondary reference only for the direction convention, occlusions and projection of the tail, rear hair mass and continuous skirt hem. Use the updated proportions and detailing from the new design, not the old image's proportions or styling. Input 3, A Mage v10, is supplementary for slender anatomy, pale pink-ivory skin and compact hands and feet, around 6.6 anatomical heads excluding coiffure and ornaments. Keep the full skirt and sleeves of input 1. No literal grey bodysuit.

Preserve the blue right eye and red left eye (frontal viewer sees blue on their left and red on their right); right profile shows only one blue eye, rear shows no eyes. Natural pointed elf ears below separate furry cat-ear head ornaments. Each cat ear has pink inner fur, a single muted violet satin bow and small white flowers at the base, with the contours foreshortened on the profile. The snowy long wavy hair falls mostly behind the shoulders, tips near relaxed wrists in all directions. In back, white waves veil most of bodice back and part of forearms with hands still readable. Side silhouette shows the nose, near cheek and elf ear in profile, far arm and foot hide behind the near ones. Hair remains white with lavender-gray shadows, not a gradient dye.

Replicate the scalloped white neck ribbon, small emerald pendant in thin gold setting, opaque white off-shoulder ruffled bodice and puff sleeves, proportional white waist ribbon bow at the front, and calf-length skirt. The modestly flared lower skirt has one consistent band of the same five-petal pale-lilac cutwork flowers and the same white gathered under-ruffle all the way around, no variation in hem height between views. Back of dress sits naturally under the hair, no added bow on the back waist. Emerald pendant faces forward and is seen edge-on at most in profile, invisible in rear. Keep two slim white ankle bands with small white flowers facing forward, white bands without flowers on the back. Bare feet small, flat on the same ground, subtle heels and rounded anatomically ordered toes, rear shows heels.

One continuous white costume tail is fixed on the rear midline at high hips, with one muted violet bow near the fluffy white tip. Tail hangs outward toward the character's anatomical right in all views, clearly visible to viewer's LEFT of the skirt in front, to viewer's RIGHT in back, and projects toward the rear (page RIGHT) in true right profile. Keep tail root partly hidden by hair and only show visible segments consistent with those occlusions, with the tail bow at a consistent lower-skirt height and viewed edge-on or at a narrower angle in profile. Three drawings must read as the same figure and same costume seen by a camera moving around them, without cropped figures, other insets, extra accessories or duplicated body parts. Clean soft front lighting in each panel with readable material separation.
```

## 右侧视图修订提示词

```text
Use case: precise-object-edit. Image 1 is the turnaround sheet to correct; Image 2 is the original full-body design v01, used only to confirm the face and accessory design. Correct the direction of ONLY the middle figure in Image 1. The final figure in the middle must be the anatomical RIGHT side, with the tip of her nose, chin and bare toes pointing to the RIGHT EDGE of the page, and the back of her head, the white tail and plum-purple tail bow on the LEFT side of that middle figure. The single visible eye is BLUE. The middle caption stays "RIGHT PROFILE".

Redraw the profile as a strict orthographic view in that direction, preserving the same apparent height, pose and soft rendered finish from Image 1. Keep the near blue eye and pointed right elf ear, puff sleeve, curled snow-white hair and whole bare foot. Keep her choker's emerald pendant just visible edge-on on the front edge of the body (page right), and show the front-facing white flower of the white ankle band only where it projects on the front edge (page right), with the band visible across the side. Keep the tail project behind her (page left), emerging from the rear high hip from under the hair, and keep the exact same white tail and plum bow design. Keep the scalloped floral cutwork and white gathered under-ruffle at the same same height. Overlap the far eye, arm and foot naturally behind the near ones. The entire middle silhouette must fit safely into its own middle cell with clean white gutters on both sides and enough space for the bow.

Preserve the existing FRONT and BACK figures at their exact locations and sizes as closely as possible, including their opposite tail projections, colors, anatomy, dress, white flower ankle bands from front and plain bands from back, the blue-left and red-right irises in FRONT, and full unobstructed crown and soles. Preserve the landscape image size, white background, shared thin baseline, character heights, heading positions and all three exact captions "FRONT", "RIGHT PROFILE", "BACK". No other modifications.
```
