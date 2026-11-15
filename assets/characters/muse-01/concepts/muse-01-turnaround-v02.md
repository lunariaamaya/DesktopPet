# 缪斯 · 三视图 v02

2026-11-15 · DesktopPet · B 类弓箭手 · 待用户确认

- 以 [三视图 v01](muse-01-turnaround-v01.png) 为唯一编辑底图。底图 SHA256 为 `5d3ce8781b59f4c68e5e8b9716cd96e597fbb4e51c251b0c79d5ee3ddd7d9b07`，对应的角色造型见[全身设计稿 v08](muse-01-design-v08.png)。
- [三视图 v02](muse-01-turnaround-v02.png) 为内置 ImageGen 的原尺寸 1536 × 1024 PNG，SHA256 为 `d15b714dcaccd58755a2f27c6dfc374ad081b65b8e880a9dad88695414f8015f`。

## 修订与核验

- 背视右肩外缘补出原辫子的辫股与辫尾，画面位于右侧。辫子由右侧后颈引出，绕肩向前。正视的辫子仍位于画面左侧，右视仍沿近侧肩胸垂下。
- 三栏收细大腿和小腿，让腿轴更顺直。正、背视减少小腿向外鼓出的弧线，右视让膝盖与踝部更接近同一承重线。保留现有身高、站距、赤足和金色脚环，足底线及裙摆高度与 v01 目视接近。
- 以画布 y=710 的小腿像素横截面作抽查，正视两腿由 56、56 px 减为 46、44 px，背视由 58、58 px 减为 46、45 px。数值按肤色阈值估算，用于比较同画幅的局部轮廓。
- 右视朝画面右方，三栏均为空手站姿。与底图目视对照，人物、衣装与画面布局延续 v01，部分小衣褶及笔触有细微生成式变化。

## 完整编辑提示词

```text
Use case: precise-object-edit. Edit the supplied 1536 × 1024 Muse turnaround sheet in just two ways: (1) make her existing right-shoulder braid readable in BACK, and (2) redraw all three views' leg silhouettes to look slimmer and straighter. Preserve the canvas and the exact character, layout, dynamic of the existing folds, clothing, colors, face, cosmetics, hands, feet, anklets, lighting, FRONT / RIGHT / BACK labels, and right-profile direction. Keep the figures at the current scale, their skirt hems and shared foot baseline unchanged, same upright rest pose. All three views remain empty-handed and carry no equipment.

1. The FRONT and RIGHT panels already show a single rose-pink braid hanging toward the front of the character's own right shoulder. They are read-only references for braid identity, scale, ties and length. Keep these two braids exactly as drawn. In the BACK panel (rightmost figure), show the SAME single braid from behind, on the character's own right (this is the viewer's RIGHT edge of the figure in the back). Its braided root visibly emerges at the right nape among the original wavy locks, and one or two recognizable plait segments turn over the outer shoulder toward the front. Allow the outer side of the braid and a little tied pink end to peek beyond the right shoulder and upper arm silhouette, or adjacent to the outer shoulder through clear space, corresponding to the front braid ending at upper bust height. The braid should clearly read as the same pink plait instead of a wispy loose curl, while the near torso and shoulder still occlude the part that is resting at the front. Keep the rest of the back hair shoulder-length and its natural layered shape. No additional braid, no central braid down the spine, no left braid, no changed shoulder pose, no broad plait over the bare back or sash. The braid is the only change above the skirt.

2. Correct the silhouette of both legs in all 3 panels. Match Muse's slender style by reducing the apparent transverse width of the upper and mid thighs by approximately 12 to 15 percent and the conspicuously bulbous calf mass by approximately 15 to 18 percent, smoothing the contours while keeping a gentle realistic calf and knee. In FRONT and BACK, remove the lateral bowing: use two near-vertical natural weight-bearing leg centerlines. For each leg independently, trace a gradual line from where the leg exits the skirt under the hip through the middle of the knee, the middle of the shin to the middle of its ankle, keeping knee and ankle centered and aligned over the foot, without outward bowed knees, bulging calf arcs, or collapsing knees inward. The legs taper gradually with a slim natural thigh-to-knee transition, then a discreet calf curve and a fine ankle. Keep a small readable space between legs, similar from knee to ankle with no inflated oval gap. Preserve natural adult anatomy and width of the feet. Do not make legs pencil-thin or mechanically straight-edged. Keep foot height and barefoot toe and heel shape, both gold anklets, and the current hem and kneecap height. In RIGHT profile (middle), preserve nose and toes pointing to viewer-right, draw slimmer thighs and calves with the hip under the same torso, knee more vertically aligned over ankle in a natural relaxed standing position. Gently straighten the excessive side-view knee bend, preserving a small realistic knee contour. Bare feet remain grounded in all three views. Keep highlights and shadows soft and continuous and preserve the same pale pink-ivory skin. These are edits to the leg contours, not to stance width, height or costume. Return the original wide full sheet with the two corrections, same panel framing and the same front/right/back views.
```
