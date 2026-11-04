# 坐地抱腿设计候选 v01

日期：2026-11-04。状态：候选，待用户看图确认。

用户要求保留上一版的面部表情，将身体姿势调整为坐在地上、双手环抱双腿。本轮唯一底图为 [害羞全身版01](design-shy-fullbody-v01.png)，SHA256：`70c5b0086543210712760f659f860eb218e02f355535ad80733644168092d127`。

方法：内置 image_gen 身份保持编辑，无程序化后处理。输出为 [design-shy-seated-v01.png](design-shy-seated-v01.png)，不覆盖原图或三视图。

目视检查：人物坐地、双膝收拢、双臂环抱膝腿；裙装覆盖膝部与腿部，衣摆与长发自然铺地；沿用浅微笑、异瞳与腮红，猫耳饰、精灵耳、绿宝石、尾饰与脚环均可见。生成式重绘不能保证面部或其他区域逐像素不变，表情及细节仍以用户验收为准。

## 完整提示词

```text
Use case: identity-preserve. Edit the attached illustration, using this ONE image as the sole base.
Change ONLY the character's body pose from standing to sitting on the floor, hugging both bent legs with both arms.

MOST IMPORTANT: preserve the existing facial expression exactly as closely as possible: same tiny closed-mouth soft smile, same mouth size and curve, same eye shapes and gaze, same relaxed eyebrows, same faint cheek blush and head tilt. Do not invent a new smile, pout, crying face, open mouth, wink or changed expression. Keep the face recognizable and retain its rendering, proportions and delicate lines.

Pose: the character is seated naturally on the ground, hips clearly supported by the floor, both knees bent and drawn gently toward her torso, knees close together. Both forearms wrap around the FRONT and sides of both knees/upper shins, hands gently resting on the opposite shin or forearm, relaxed rounded fingers; she is visibly embracing BOTH legs, not clasping hands at the chest. Her torso is comfortably upright with a slight natural forward inclination. Small feet rest naturally near her body on the floor. Natural anatomy and balance, no extra fingers or limbs. The opaque long dress covers her lap, thighs and knees completely and drapes around the bent legs with believable folds, spreading lightly onto the floor. Preserve the original dress length and design; let ankle ornaments and feet appear naturally below the hem without turning them into the focal point. Fully clothed, innocent and age-appropriate.

Preserve all other character design features: petite slender proportions; fluffy long PURE WHITE curly hair and the same fringe, hair fanning naturally onto the floor behind and beside her; anatomical LEFT eye red (viewer right) and RIGHT eye blue (viewer left); elf ears; worn cat-ear head accessories with pink interiors, white flowers and lavender bows; emerald-green necklace and white ruffled collar; opaque white off-shoulder ruffled dress, puff sleeves, waist bow, lace floral-cutout hem and layered ruffles; white fluffy decorative tail with the same purple bow lying gently to the side; white floral ankle bands. Keep the same skin tone, clean luminous whites, pale lavender-grey shading and smooth anime illustration finish.

Composition: ONE complete seated character including ears, hair, tail, clothing and feet, centered with comfortable white margins on a clean white square canvas; natural frontal/slightly three-quarter eye-level view, no low-angle perspective. Small soft floor contact shadow to show she is seated. No frame, inset, text, watermarks, props or additional people. Do not redesign face, costume, palette or ornaments.
```
