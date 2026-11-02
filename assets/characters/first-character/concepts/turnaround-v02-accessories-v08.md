# v02 局部修订 08 · 参考小腿的浅桃粉象牙白肤色

日期：2026-11-02。工具：内置 image_gen，非 CLI。底图 turnaround-v02-accessories-v07.png；用户提供桌面「角色图.png」仅作小腿肤色参考，未复制其结构。输出 turnaround-v02-accessories-v08.png。

参考图片 1226×1283，在小腿受光区只读取样：(480,1030) #FEEFE9；(480,1050) #FFF1EA；(477,1070) #FEF0E9；(353,1045) #FFEFE9。色值为图像像素值，不是去除光照后的真实材质反照率，也不是对生成图精准配色的保证。

便于沟通的描述名：**低饱和浅桃粉象牙白**，或「带极淡桃粉底调的瓷白肤色」。英文描述 very pale peach-pink ivory。不是唯一标准色名；相较前版灰冷白，加入少量桃粉血色，但避免饱和珊瑚红与橙黄。建议受光基准约 #FFF0E9，脸颊微粉、阴影低对比，不能用一个色号填平所有明暗。

用户下一次可用描述：「肤色用低饱和浅桃粉象牙白，受光面参考 #FFF0E9；白里透淡桃粉，不偏灰蓝、不泛红橙。参考原图小腿，保留柔和明暗，脸颊只有极淡粉色。」

检查：肤色较版07回暖，皮肤保持浅色，未主动调整几何或装饰。生成式编辑不能保证局部外逐像素不变，仍待用户复核；没有生成三维模型或实际材质。

## 完整提示词

```text
SKIN TONE MATCH ONLY. Image1 is the current approved three-view sheet, exact editing target; preserve ALL its structure, silhouette, hand/finger arrangement, poses, hair colors/volume, costume/accessory layout, expressions, feet, tail and camera-axis soft lighting. Image2 is a reference ONLY for the exposed CALF SKIN COLOR, NOT its face blush or any design. Match the light central illuminated calf skin in image2: sampled sRGB #FEEFE9, #FFF1EA, #FEF0E9, #FFEFE9. Target base about #FFF0E9: very pale LOW-SATURATION PEACH-PINK IVORY / fair porcelain with tiny warm peach undertone, not the grayish cold white currently on image1, and NOT saturated red/coral/orange. Apply consistent material base across face/ears/neck/shoulders/arms/hands/lower legs/feet of ALL three views. Keep gentle soft low-contrast shadows, slightly rosy reflected skin depth without red outlines or widespread joint redness. Tiny subdued cheek blush only. This should retain reference calf's natural creamy pale translucent skin appearance, not pure white, blue-gray, lavender or red. Treat HEX values as local illuminated midtone anchors, not flat-fill all shadows. Keep white dress and hair, green gem, red-blue eyes and purple ribbons UNCHANGED. No recolor outside skin, no geometry changes, no beautification, no extra accessories, no smile changes, no text/insets. Return same full front/side/back sheet on white background. Opaque modest fantasy clothing unchanged.
```
