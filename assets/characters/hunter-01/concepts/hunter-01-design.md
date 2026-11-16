# 猎人 1 · 弓箭手全身设计稿

DesktopPet · B 类弓箭手 · 2026-11-14

[全身设计图 v01](hunter-01-design-v01.png)为首版候选，待用户确认。由内置 ImageGen 生成。

## 参考与补绘

- 查看了用户提供的 10 张像素参考图，位于 `角色素材/弓箭手/猎人/猎人1`。第 1、3、4、7 张另外以五倍最近邻放大观察。
- 参考图 3 用于近正面微侧身、双脚宽站、手臂位置及猎具从画面左上至右下的斜线。参考图 1 用于正面交领、袖缘红色断线与踝饰。参考图 4 用于发束和衣袖内衬。参考图 7 用于木色猎具尾部及琥珀色饰纹。
- [B 类弓箭手 v08](../../base-templates/base-b-archer/v08/base-b-archer-pale-skin-front-v08.png)用于约 6.5 头身的站立比例、纤细四肢、小手足和浅粉象牙肤色。底稿 SHA256 为 `e32c4cb1d93f2613b3b12d86d20f7a4b191d777d95b2a21930c006dcc316e6e9`。
- 原参考的虹膜、头顶尖饰和面料细节分辨率有限。本稿将其补绘为淡紫虹膜、贴近发顶的尖瓣饰、有透明层次的粉色裙片与细金踝环。

## 版本与检查

- v01 直接以参考图 3、1、4、7 和 B v08 为输入，没有上一版猎人设计稿。
- 人工核对了头到脚构图、近正面微侧身、双脚宽站、猎具完整剪影、袖缘与双踝的可见性。与参考图 3 相比，画面右脚略向外转，躯干略直。腰胯受衣物和道具遮挡，比例按可见关节及轮廓估核。
- PNG 原尺寸 1189 × 1323，项目副本与工具原图 SHA256 一致。SHA256 ab52bdd5f4f3f61f27db1e75ff94c13dd2603053a7a74e382fbe9638693534a3

## v01 完整生成提示词

```text
Use case: stylized-concept. Create one exquisite full-body 2D anime fantasy game character design illustration of the female Hunter (archer class) from these attached pixel references. Translate the sprite into a crisp, beautifully finished illustration with the same identity, palette, silhouette and stance.

Input image roles in order. (1) 猎人角色参考图3.png is the primary pose and viewing-angle reference; closely follow its composition, wide stance, hands and diagonal equipment. (2) 猎人角色参考图1.png clarifies front outfit, hair crown and feet. (3) 猎人角色参考图4.png clarifies the long lavender-and-pink hair, the sleeve lining and silhouette, and the equipment profile. (4) 猎人角色参考图7.png clarifies the look and colors of the stylized fantasy hunting prop and the moving garments; do not use its seated pose. (5) base-b-archer-pale-skin-front-v08.png is only the guide for underlying anatomy and complexion: approximately 6.5 anatomical heads in a standing position, slender shoulders, waist, hips and limbs, natural thigh-to-calf ratio, small hands and feet, and low-saturation very pale pink-ivory skin with soft shading. Do not reuse the mannequin pose, clothing, eye colors or graphics.

Lock the gesture to image 1. From the viewer's perspective, near frontal three-quarter, torso angled slightly toward viewer-right, head just right of center looking toward viewer-right with a slight head tilt; subtle forward lean. Both bare-looking feet are spread far apart, at the same ground level, viewer-left leg projecting clearly down-left and the partly hidden viewer-right leg projecting diagonally down-right, with natural soft knees. Her right sleeve (viewer-left) drops diagonally toward the upper thigh and its folded forearm brings the hand naturally inward to the upper-midsection of the equipment near her own chest/upper waist. The other oversized sleeve drapes down on the viewer-right side; the other hand may be naturally partly obscured. Keep the torso-to-leg balance and the asymmetry of the sprite. Trace the distinctive diagonal in front of the body: a broad warm-brown flared stock rises up behind the viewer-left shoulder with a tiny glowing amber four-point inlay, from there the long twin dark indigo steel rails slope prominently down across the front of her torso and skirt near the center, passing the knees to end a little below foot height in the image near viewer-right. The stock cap is near the height of the top of the hair. Her feet are on either side of the long diagonal. Preserve the stylized oversized fantasy hunting piece shown in the sprite with smoked violet metal, walnut brown, fine gold edge and small amber accents. Keep it pointed down at rest. Render the two dark parallel forms and their tips cleanly as one visually coherent fantasy prop. No shot, action effect, bow, arrow, or additional gear. Follow the given pose, rather than a standard upright pose, side walking profile or action lunge.

Faithfully retain the silhouette and color blocks. Pale silver-white face-framing bangs, softly side swept, and thick very long wavy hair with cool lavender middle masses and billowing rose-pink, pale peach lit ends sweeping out behind each sleeve around the hips to the knee area. Several coherent broad S-shaped locks and a few flyaways, not many thin ribbons. Two small pointy pale crown tufts or petal-like hair ornaments with pink-violet inner accents close to the head, matching the tiny sprite shapes, no added animal tail. Gentle mature anime face with clear muted violet eyes, natural eyebrows and subtle pink cheeks. Ivory wrap-front robe top with folded overlapping neckline, muted gray-green fitted waist wrap, and very distinctive oversized kimono-like draped pointed sleeves. Keep the sleeves off-white with subdued lavender-gray lining and fine broken crimson trim following the edges. A short layered soft rose pink wrap skirt with an overlapping front and a few translucent diagonal panels over the hips, remaining recognizably like the reference. Visible legs, delicate bare feet and fine warm gold ankle bands, as the pixels suggest. Add restrained stitch and fabric-fold detail within the original shapes. Do not add armor, bustle, stockings, boots, accessories or oversized head ornaments.

Single centered complete character, vertical or almost square composition to hold the wide feet and flow of hair. All tips, both feet, and all hair inside the margins. Clean pale warm-gray to near-white neutral studio ground, slight soft contact shadow. Elegant thin anime linework, clean cel shading with soft controlled gradients, legible folds and seams, subtle satin sheen on pale fabrics and crisp contrasting metal, clear color boundaries, high-production-value game concept art. Preserve very fair softly lit skin and quiet expressive face. No text, watermarks, decorative frames, panels or inset views.
```
