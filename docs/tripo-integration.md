# Tripo 接入核查与后续方案

核查日期：2026-11-03。结论：Tripo 支持通过 MCP 接入；当前会话没有暴露 Tripo 工具，尚未完成安装、登录或端到端任务验证。用户已有一个满意的外部生成模型，优先沿用该结果。

## 可用路线

| 路线 | 依赖与用途 | 本项目建议 |
|---|---|---|
| Tripo 3D Codex 插件 | 官方指引提供插件安装及浏览器授权；需要 Node.js 20+ | 首选，减少手工集成 |
| Tripo CLI 的 MCP 服务 | 已安装并登录的 CLI 执行 `tripo mcp`；文档同时列出扩展工具集 | 用户明确需要 MCP 时采用，不需要先写自建服务 |
| 较早的 `Tripo-Developer/tripo-mcp` | 官方仓库自述 alpha，依赖 Blender 与 Tripo AI Blender Addon | 仅需联动 Blender 时评估；不能等同于新 CLI MCP |
| Tripo Developer API | 适合产品自身批量提交、查询和下载任务 | 后续应用内集成使用；不因桌面助手接入而自动需要 |

插件说明来自 [Tripo 官方 Codex 指引](https://developers.tripo3d.ai/en/docs/codex-plugin)；CLI MCP 来自 [官方 CLI 文档](https://developers.tripo3d.ai/en/docs/cli)；旧 Blender 路线见 [官方 tripo-mcp 仓库](https://github.com/Tripo-Developer/tripo-mcp)。这些接口都调用 Tripo 服务，MCP 本身不执行三维推理。

## 当前本机检查

- Node.js：v24.19.0，满足官方文档的最低主版本要求。
- 当前可调用工具：没有 Tripo；PATH 中未找到 `tripo`。
- 插件目录搜索已尝试，但工具返回连接错误，无法据此判断账号是否能看到插件；更多插件可在 [插件目录](https://chatgpt.com/plugins) 查询。不能将该错误说成 Tripo 不受支持。
- 未安装任何 Tripo 插件/CLI，未修改全局 MCP 配置，未上传角色素材，未提交计费生成任务。

## 接入步骤与验证

1. 在 Codex 插件目录查找并启用 **Tripo 3D**；若账号目录没有显示，依据官方 CLI 文档采用 CLI 路线。
2. 先确认账号区域：国际站 `developers.tripo3d.ai` 为 `ov`，中国站 `developers.tripo3d.com` 为 `cn`。按对应区域完成浏览器设备授权，不在聊天、仓库或命令日志中明文粘贴 API Key。
3. 如果选择 MCP，在 CLI 安装并可启动后，核对实时 `tripo mcp --help`。可按 Codex 官方 STDIO 配置方式注册，例如 `codex mcp add tripo -- tripo mcp`。Windows 应使用实际可执行命令的绝对路径，并先确认该命令可由当前 Codex 进程启动，不能只验证交互 PowerShell 的别名。
4. 刷新连接后验证服务启动、工具发现和账号状态，再判断是否需要扩展工具集；不把配置存在或插件已安装称为已经端到端连通。
5. 如用户要求实际生成，再确定输入、模型版本和次数，先提交一个任务、记录 task_id、状态、额度与产物并查看结果。网络超时先查询已有 task_id，不盲目重复提交造成重复消费。

STDIO 注册方法见 [OpenAI 官方 MCP 配置说明](https://learn.chatgpt.com/docs/extend/mcp)。上面是准备好的操作方案，本轮未实际执行注册。Tripo 的浏览器账号授权和 MCP 客户端认证是不同层，不默认用 `codex mcp login` 代替 CLI 登录。

## 与本项目角色的衔接

官方 API 支持图像和多视图生成，见 [API 概览](https://developers.tripo3d.ai/en/docs/introduction)。若重新生成，先按对应接口要求分离视图、明确角色自身左右和统一尺度；不要把拼图的三个角色当作一个单视图对象。

现有网页生成的结果应优先导出 GLB 等可用模型文件再导入项目检查。网页任务能否由 API 读取、网页会员是否覆盖开发接口额度、相同模型版本和参数是否可用，需在用户账号及实际接口中验证，不作默认承诺。生成会使用 Tripo 额度，参见 [官方插件说明](https://developers.tripo3d.ai/en/docs/codex-plugin)。

对现有模型的验收依次为：正侧背与斜角相似度；贴图和颜色；手足和裙摆完整性；面数/材质/尺寸；是否已有骨架与可用表情；头发/尾饰/换装的可分离性。静态模型的质量好不自动证明具备这些后续能力。
