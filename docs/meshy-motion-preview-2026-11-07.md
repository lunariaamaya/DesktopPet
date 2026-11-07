# 角色试修动画预览

日期：2026-11-07。为方便直接观看，将现有 v04 动作 GLB 导入 Blender 渲染为 GIF 和 MP4。本轮没有继续修改模型，也未调用 Meshy 付费生成。

- [自动循环动图](../assets/characters/first-character/diagnostics/meshy-motion-preview-2026-11-07/motion-preview.gif)
- [MP4 视频](../assets/characters/first-character/diagnostics/meshy-motion-preview-2026-11-07/motion-preview.mp4)
- [原模型及源动画信息](../assets/characters/first-character/diagnostics/meshy-motion-preview-2026-11-07/preview-source.json)

左侧正面、右侧背面同步播放。演示抬手、转头、尾饰和发梢的控制动作。原 GLB 中动作长 3 秒；每隔两帧采样，以 8 fps 播放，预览约 5.75 秒，方便观察。动图自动循环，MP4 无音轨。

它是已有模型中检查动作的真实三维渲染，不是恢复原 Meshy 动作，也不是完整动作质量认证。当前仍有袖口/腋下拉伸；裙摆独立控制、坐姿修形、自然物理和碰撞尚未完成。详见 [试修记录](meshy-rig-repair-2026-11-04.md)。

复现脚本：[render-meshy-motion-preview.py](../scripts/render-meshy-motion-preview.py)。依次运行 render（隔离 bpy）、label（NumPy/Pillow 主 Python）、encode（隔离 bpy）三个阶段，生成的原始帧和字幕帧位于忽略的 tmp 目录，最终 GIF/MP4 纳入 Git。
