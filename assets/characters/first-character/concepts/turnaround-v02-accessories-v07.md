# v02 局部修订 07 · 冷白肤色

日期：2026-11-02。工具：内置 image_gen，非 CLI。编辑底图 turnaround-v02-accessories-v06.png；design-v01.png 仅参考初版肤色。输出 turnaround-v02-accessories-v07.png，旧版保留。

用户要求皮肤尽量白，脸颊略白里透红，呈现冷白皮，去除全身偏红观感。此次统一裸露皮肤为低饱和浅白偏中性冷调，降低偏红轮廓及关节/指趾泛红，保留极淡脸颊粉色。其他材质、装饰位置与照明规则不主动修改。

检查：正侧面肤色、耳部、四肢、手足红调显著下降，淡粉面颊保留；白发、白衣、紫饰、宝石与异瞳颜色可辨。仍为生成式编辑候选，不保证区域外逐像素一致；没有制作三维材质或模型。

## 完整提示词

```text
SKIN COLOR ONLY correction. IMAGE1 current approved three-view sheet is the exact edit target. IMAGE2 initial concept is reference ONLY for delicate pale complexion, do NOT transfer its pose, proportions, dress, hairstyle, feet, expression or composition. In ALL three figures, change exposed SKIN from warm reddish/coral peach to very pale COOL FAIR porcelain/ivory complexion: extremely low saturation, high-value neutral-white base with a subtle cool undertone and soft light gray-pink form shadows. Remove excessive RED/ORANGE saturation on face, elf ears, neck, shoulders, arms, hands, lower legs and feet; also soften reddish skin contour lines to low-saturation taupe/rose-gray so limbs do not retain red outlines. Face cheeks may have ONLY a tiny faint diffuse translucent pink blush, white skin softly tinged pink, not red cheeks or makeup; body skin is evenly pale with no widespread redness at joints/fingers/toes. Keep enough gentle form shading so skin remains distinct from white background and white clothes; do not turn skin blue, corpse-gray, purple or flat featureless white. Each view still has its own soft camera-axis light. Preserve exact original eye colors (red and blue irises), green emerald, purple bows, white flowers, inner fabric of cat ears (accessory) and all non-skin materials. ALL GEOMETRY, hair colors/volume/position, line shapes, hands/finger order, feet, tail, ornaments, clothes and expression must stay as IMAGE1. No new details, no other fixes, no recoloring whole image, no labels/insets. Only epidermal complexion and overly red skin contour color, retaining tiny subtle cheek blush. Full same front/side/back sheet.
```
