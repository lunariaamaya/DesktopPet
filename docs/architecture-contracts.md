# 模块与数据接口契约

版本：0.3 · 日期：2026-11-07 · 状态：设计草案，未实现
上位需求：[PRD](./PRD.md)。接口使用 TypeScript 风格说明，与最终语言无关；WPF/C# 可等价映射。接口名不是已经可调用的 API。

## 1. 设计原则与依赖

单模块单功能，模块之间不直接访问对方数据表、窗口实例或内部类。优先模块化单体；只有系统执行、凭证访问与渲染等存在权限差异的部分划定进程边界。不要为未来模块提前搭建微服务。

```text
界面/输入 → ApplicationCoordinator（用例编排）
                 ├─ Interaction → Character / Scene
                 ├─ Conversation → ModelProvider + Memory（只读快照）
                 ├─ Task → Permission → OS Adapter
                 └─ Profile / Settings / Content / Locale
各模块 → Repository / EventPublisher（公共基础接口）
未来 Auth / Sync / Wardrobe / Story / Voice 通过同类端口接入
```

UI→宿主的 IPC 是类型化白名单；禁用任意方法调用、动态脚本求值与原始 shell。渲染器按不可信调用方验证。外链在系统浏览器打开；对话正文按文本或经过清洗的 Markdown 渲染，不执行 HTML/脚本。内容包不含脚本；首版不加载第三方二进制插件。

## 2. 模块边界、接口与数据所有权

| 模块 | 单一职责/归属 | 核心接口（逻辑名称） | MVP/未来 |
|---|---|---|---|
| DesktopHost | 窗口、桌面层、生命周期 | attach, detach, setInteractionMode, setPaused, getHostState | MVP |
| Character | 角色渲染及动作仲裁 | load, getCapabilities, playAction, setExpression, stop | MVP |
| Scene | 场景渲染、物件与场景状态 | load, getHotspots, applyAction, snapshot | MVP |
| Interaction | 将用户热点输入映射为语义意图 | dispatch, setEnabled | MVP |
| Conversation | 对话会话、消息与模型编排 | createSession, send, cancel, deleteSession | MVP |
| Memory | 个人记忆与版本 | propose, confirm, query, update, delete, clear, export | MVP |
| Task | 计划、执行与可核实结果 | prepare, execute, cancel, getStatus | MVP |
| Permission | 权限与批准记录 | evaluate, grant, revoke, validateBeforeExecute | MVP |
| Profile | 本地用户资料与关系身份 | getCurrent, updatePreferences | MVP，本地单资料 |
| Settings | 配置与凭证引用 | get, update, testConnection；getCredentialRef 不返回密钥 | MVP |
| Content | 内容包校验与选择 | inspect, load, getManifest, resolveAsset | MVP，仅打包内置资源 |
| Locale | 翻译与格式化 | resolve, formatDate, formatNumber, listAvailable | MVP |
| Storage | 数据库事务与版本迁移 | transaction, migrate, healthCheck | MVP，业务不绕过 Repository |
| Diagnostics | 脱敏事件和诊断 | record, exportRedacted, purge | MVP |
| Auth | 云端身份认证 | initiateLogin, handleCallback, getUser, logout | 未来端口 |
| Sync | 本地/云端副本同步 | previewLink, sync, resolveConflict, unlink | 未来端口 |
| Wardrobe | 服装兼容与装备 | validateEquip, equip, unequip | 未来端口 |
| Story | 剧本执行、分支与存档 | start, choose, pause, resume, stop | 未来端口 |
| Entitlement | 内容/服务使用权益 | check, refresh | 未来端口 |
| Voice | 语音输入输出 | startInput, stopInput, speak, cancel | 未来端口 |

例如换装：Wardrobe 校验 Character 的槽位与 Content 的服装包 → 提交装备配置 → 发出 wardrobe.equipped → Character 刷新外观。不需要修改 Conversation。更换角色与「新建关系」为不同操作，不能默认清空记忆。

## 3. 公共信封、错误和版本

```ts
type Locale = 'zh-CN' | 'en' | 'es' | 'ja';
type ErrorCode = 'INVALID_INPUT' | 'NOT_CONFIGURED' | 'PERMISSION_REQUIRED'
  | 'PERMISSION_DENIED' | 'UNSUPPORTED_CAPABILITY' | 'CANCELLED' | 'TIMEOUT'
  | 'PROVIDER_UNAVAILABLE' | 'RATE_LIMITED' | 'STORAGE_ERROR'
  | 'CONTENT_INVALID' | 'VERSION_INCOMPATIBLE' | 'STALE_CONTEXT' | 'INTERNAL';

interface RequestContext {
  contractVersion: 1;
  requestId: string;       // UUID，去重和关联日志
  profileId: string;       // 宿主从当前资料注入，不能信任渲染器自行传值
  relationshipId: string;
  locale: Locale;
  deadlineAt: string;      // UTC ISO-8601
}
type Result<T> =
  | { ok: true; data: T; requestId: string }
  | { ok: false; error: { code: ErrorCode; messageKey: string;
        params?: Record<string, string | number>; retryable: boolean };
      requestId: string };

interface DomainEvent<T> {
  schemaVersion: 1;
  eventId: string;
  eventType: string;
  occurredAt: string;
  sourceModule: string;
  correlationId: string;
  profileId: string;
  payload: T;
}
```

未知 errorCode 显示通用本地化错误；不得把原始异常、密钥、路径写进错误消息。新增可选字段兼容旧版；删除/改类型须升级主版本。数据库版本、内容版本和契约版本各自管理，不混用应用版本。

模块注册声明 id、version、requiredCapabilities、optionalCapabilities。宿主在启动前检查依赖；缺必需能力禁用对应功能并提示，不让全应用无故退出。

命令采用 request/response 或类型化流，写入完成后才返回成功。事件用于状态通知；进程内不保证持久交付，不能以 event「已发出」替代实际记忆提交或任务结果。未来同步事件须增加持久 outbox，订阅方按 eventId 去重。

## 4. 关键业务接口

### 4.1 角色、场景与内容能力

当前二维制作与验收以 [二维管线](character-2d-pipeline.md) 为准；旧三维文件保留历史，不作为首版运行时支持承诺。

```ts
interface CharacterCapabilities {
  renderer: 'sprite2d' | 'live2d';
  baseTemplateId: BaseTemplateId;
  templateRevision: string;
  rigProfileVersion: string;
  poseSetVersion: string;
  actionIds: string[];
  expressionIds: string[];
  hotspots: Array<{ id: string; polygon: number[][]; actionId: string }>;
  wardrobeSlots: string[]; // MVP 可为空，不能伪造换装支持
}
interface ActionRequest {
  actionId: string;
  source: 'user' | 'conversation' | 'task' | 'scene' | 'story';
  priority: number;       // 宿主按规则赋值，不接受模型任意优先级
  interruptible: boolean;
}
interface Hotspot { id: string; polygon: number[][]; actionId: string; labelKey: string }
interface SceneAction { actionId: string; targetId: string; value?: string | boolean }

type BaseTemplateId = 'base-a' | 'base-b'; // 恰好两类，不从外观名称推断
interface BodyLandmark {
  id: string;
  x: number; y: number; // 标准画布归一化坐标，非真实厘米尺寸
  evidence: 'visible' | 'inferred' | 'user_confirmed';
  sourceRefIds: string[];
}
interface BaseTemplateSpec {
  id: BaseTemplateId;
  revision: string;
  status: 'draft' | 'approved';
  designSize: { width: number; height: number };
  landmarks: BodyLandmark[];
  ratioMeasurements: Array<{ id: string; value?: number;
    evidence: 'visible' | 'inferred' | 'user_confirmed' }>;
  rigProfileVersion: string;
  poseSetVersion: string;
}
interface AppearanceCompatibility {
  baseTemplateId: BaseTemplateId;
  templateRevisions: string[];
  rigProfileVersion: string;
  poseSetVersion: string;
  slotId: string;
  supportedActionIds: string[];
  occlusionMaskAssetIds: string[];
}
type CreationStage = 'reference' | 'appearance' | 'layers' | 'rig_motion' | 'qa_preview';
interface CreationJob {
  id: string;
  baseTemplateId?: BaseTemplateId; // 无法判断时待确认，不自动分到 A
  stage: CreationStage;
  state: 'pending' | 'running' | 'needs_review' | 'failed' | 'complete';
  artifactIds: string[];
  unresolvedEvidenceIds: string[];
}
// 未来创作端接口；MVP 不部署用户上传/生成服务。
interface CharacterCreation {
  createJob(referenceAssetIds: string[]): Promise<Result<CreationJob>>;
  runStage(jobId: string, stage: CreationStage): Promise<Result<CreationJob>>;
  getPreview(jobId: string): Promise<Result<{ videoAssetId?: string;
    interactivePreviewId?: string; qaReportAssetId: string }>>;
  approveBaseline(jobId: string, artifactId: string): Promise<Result<CreationJob>>;
}
```

热点使用内容 manifest 的 designWidth/designHeight 坐标；宿主维护唯一缩放变换，输入与渲染共用。Character 只执行自身动作；Scene 只修改物件状态。Interaction 中的语义映射如「头部点击→回应动作＋本地台词」不能包含系统工具执行。

二维大姿态切换需声明 entryPose、exitPose、接地/家具锚点、图层顺序及可打断规则；不能把不兼容动作强制混合。坐姿热点可随姿态切换，输入与显示共用当前变换。Wardrobe 按 AppearanceCompatibility 检查，不匹配返回不兼容结果并保留原装备；不得直接拉伸服装凑合适配。有限捏脸参数必须在模板允许范围内，范围外进入新修订审阅。模型参数名、编辑器命令和 MCP 细节封装在适配器，不暴露给 Conversation/Memory。

### 4.2 对话与模型

```ts
interface SendMessage {
  sessionId: string;
  text: string;
  context: RequestContext;
}
type ConversationEvent =
  | { type: 'delta'; turnId: string; text: string }
  | { type: 'expression'; turnId: string; expressionId: string }
  | { type: 'memory_proposal'; turnId: string; proposalId: string }
  | { type: 'task_proposal'; turnId: string; planId: string }
  | { type: 'completed'; turnId: string }
  | { type: 'cancelled'; turnId: string }
  | { type: 'error'; turnId: string; code: ErrorCode };

interface ModelProvider {
  readonly providerId: string;
  capabilities(): { stream: boolean; tools: boolean; cancel: boolean };
  testConnection(config: ModelConnection, signal: AbortSignal): Promise<Result<ConnectionStatus>>;
  listModels(config: ModelConnection, signal: AbortSignal): Promise<Result<ModelDescriptor[]>>;
  inspectModel(config: ModelConnection, modelId: string,
    signal: AbortSignal): Promise<Result<ModelDescriptor>>;
  generate(input: ModelInput, signal: AbortSignal): AsyncIterable<ModelOutput>;
}
// ModelInput 包含人格/策略、上下文、有效记忆快照、语言和白名单工具 schema；
// ModelOutput 是经适配器标准化的文本/表情/候选/工具提议，不能直接触发 OS。
```

调用链：用户消息→取 MemorySnapshot(revision)→组装有限上下文→模型→校验输出→对话显示/候选/任务计划。工具参数需 schema 验证；非法结构不执行。对话正常完成与电脑操作成功是不同事件。

首版允许非流式适配器，但有等待和取消状态。cancel 不保证供应商停止计费；取消后按 turnId 丢弃迟到结果，不再保存记忆候选或发出任务。

#### 本地大模型端口（MVP 预留，后续实现 Ollama）

```ts
interface ModelConnection {
  id: string;
  provider: 'cloud_api' | 'ollama' | 'openai_compatible';
  deployment: 'local' | 'remote'; // 与协议分开，兼容协议也可能部署在本地
  protocol: 'provider_native' | 'ollama_native' | 'openai_compatible';
  baseUrl: string;
  modelId: string;
  credentialRef?: string; // 本地默认无凭证，不在此保存密钥
  connectTimeoutMs: number;
  firstOutputTimeoutMs: number;
  totalTimeoutMs: number;
  contextBudget?: number;
}
interface ConnectionStatus {
  reachable: boolean;
  serviceVersion?: string;
  modelAvailable: boolean;
  executionLocation: 'local' | 'remote' | 'unknown';
}
interface ModelDescriptor {
  id: string;
  label: string;
  executionLocation: 'local' | 'remote' | 'unknown';
  contextWindow?: number;
  capabilities: {
    chat: boolean;
    stream: boolean;
    tools: boolean;
    structuredOutput: boolean;
    cancellation: 'transport_only' | 'confirmed_backend' | 'unsupported';
  };
}
```

类型为契约草案，名称尚未实现。ConnectionRegistry 属于 Settings：持久化连接配置和活动连接 ID；ProviderRegistry 按 provider/protocol 选择适配器，禁止按 URL 字符串猜供应商。ModelDescriptor 是所选模型的实际能力；原 capabilities() 只表示适配器能力上界，有效能力取两者交集。未知能力按不支持处理，不能凭模型名称推断工具可用。

Ollama 适配映射（2026-10-31 按官方仓库文档核对；实现时再确认兼容版本）：

| 公共方法 | 原生接口/行为 | 处理要求 |
|---|---|---|
| testConnection | 检查服务和已配置模型；服务版本为可选信息 | 服务可达与模型存在分开；探测不触发下载/昂贵推理 |
| listModels | GET /api/tags | 列出模型 ID；空列表有引导；不自动选择并拉取模型 |
| inspectModel | POST /api/show | 读取可用元信息和能力；能力信息不完整时保守降级 |
| generate | POST /api/chat | 标准化多轮 messages、流式分片与 tool_calls；流式 JSON 分片按协议解析，不能直接复用另一供应商解析器 |
| cancel | 终止本次 HTTP/流读取并忽略迟到数据 | 不把关闭客户端连接等同于后端已卸载模型或停止 GPU 工作 |

官方依据：[Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)、[工具调用](https://github.com/ollama/ollama/blob/main/docs/capabilities/tool-calling.mdx)、[认证](https://github.com/ollama/ollama/blob/main/docs/api/authentication.mdx)。本地 API 默认不要求认证，因此默认只连回环地址，不能在产品中自动开放局域网访问。

本地服务未运行/模型不存在/能力不支持/冷启动超时分别映射为可本地化错误或状态，不混成“密钥错误”。发现与探测函数不支持时返回 UNSUPPORTED_CAPABILITY，云端可允许手动指定模型，不要求所有供应商提供模型列表。

首版预留这些端口与可序列化配置，不安装 Ollama 或打包模型权重。后续接入必须允许无云凭证启动本地聊天、使用同一 Memory 和 Task 边界；工具能力不足时保留聊天和用户手动工具入口，不从普通文本提取命令绕过策略。

模型切换在应用层执行：取消旧 turn→递增连接代次→重新计算上下文预算→使用新连接；历史消息及已确认记忆不改写。连接代次不同的迟到响应不得追加。冷启动等待时间按连接设置，不能沿用云端超时却无提示失败；本地推理与壁纸争用 GPU 的测试列入后续验收。

离线验收必须选择真正本地模型并禁止云端回退；回环地址可能连接到云端代理，executionLocation 为 unknown/remote 时不显示“完全离线”。本地服务安装、模型下载/升级、硬件适配与许可证是后续功能依赖，不因接口预留就视作完成。

### 4.3 记忆

```ts
interface MemoryProposal {
  id: string; relationshipId: string;
  category: 'name' | 'preference' | 'communication_style';
  text: string;
  sourceMessageId?: string;
  sourceType: 'explicit_user' | 'manual';
  status: 'pending' | 'confirmed' | 'rejected' | 'expired';
  expiresAt: string;
}
interface MemorySnapshot {
  revision: number;
  items: Array<{ id: string; text: string; updatedAt: string }>;
}
// confirm(proposalId, expectedRevision)、update(id, patch, expectedRevision)、
// delete(id, expectedRevision) 为事务命令，冲突返回 STALE_CONTEXT。
```

首版优先简单类别/关键词筛选，不要求向量库。确认后才进入 query；每次返回上限十条。关系级记忆与资料级偏好分开。手动纠正优先于旧记录，不靠模型选择哪个事实有效。删除后检索缓存和在途上下文同时失效；重新安装/登录/故事加载不能隐式恢复已删记录。

### 4.4 任务、权限与 OS 适配器

```ts
type ToolCall =
  | { toolId: 'app.open'; args: { appId: string } }
  | { toolId: 'web.open'; args: { url: string } }
  | { toolId: 'file.find'; args: {
      rootId: string; query: string; extension?: string; recursive?: boolean } };
interface TaskPlan {
  id: string; requestId: string; userMessageId: string;
  origin: 'explicit_user_request';
  steps: ToolCall[];       // 1–3 步
  argsDigest: string;
}
type TaskState = 'proposed' | 'awaiting_permission' | 'running'
  | 'succeeded' | 'partial' | 'failed' | 'cancelled';
interface PermissionGrant {
  id: string; profileId: string; toolId: ToolCall['toolId'];
  scope: { kind: 'app' | 'domain' | 'root'; resourceId: string };
  lifetime: 'once' | 'persistent';
  requestId?: string; argsDigest?: string;
  createdAt: string; revokedAt?: string;
}
interface ToolResult {
  taskId: string; stepIndex: number;
  status: 'succeeded' | 'partial' | 'failed' | 'cancelled';
  effect: 'process_started' | 'browser_dispatched' | 'files_found' | 'none';
  localDataRef?: string;  // 本地 UI 读取完整结果，不是可发给模型的内容
  modelSummary: { code: string; count?: number; truncated?: boolean };
  errorCode?: ErrorCode;
}
```

信任边界：模型提议→Task.prepare 校验→Permission.evaluate→必要时用户决定→执行前重新验证→OS 适配器→Task 提交结果→角色表现/对话描述结果。

授权校验先标准化再算参数摘要；URL 用解析器比对精确主机和允许协议，不使用字符串前缀放行；文件使用授权 rootId 对应的规范化绝对路径，禁止目录穿越、越根和重解析点绕过；应用只从本地登记表查 appId。凭证、原始路径不交给模型决定。

requestId 同时用于计划与执行去重；任务状态在执行前落库，外部副作用不可与数据库原子提交。异常重启时 running 状态标为 failed/结果未知，禁止自动重放打开类操作；提示用户核实后手动再试。停止后已经发出的启动请求不可撤销。

### 4.5 国际化

```ts
interface LocaleService {
  resolve(key: string, params?: Record<string, string | number>, locale?: Locale): string;
  listAvailable(): Array<{ locale: Locale; translated: boolean }>;
}
// 示例：task.file_found = "找到 {count} 个文件"，后续使用支持复数的消息格式。
// 资源目录建议 locales/zh-CN、locales/en、locales/es、locales/ja。
```

界面资源与内容台词分开，但同用 locale 标识；内容 manifest 提供自身默认语言。中文资源完整性和伪本地化均纳入检查；其他语言只有实际翻译通过后才出现在选择器。

## 5. 内容包契约与素材交付

```json
{
  "schemaVersion": 1,
  "id": "builtin.room01",
  "version": "0.1.0",
  "kind": "scene",
  "minHostVersion": "0.1.0",
  "defaultLocale": "zh-CN",
  "locales": ["zh-CN"],
  "renderer": "sprite2d",
  "designSize": {"width": 1920, "height": 1080},
  "entry": "scene.json",
  "requiredCapabilities": ["scene.hotspot.v1"],
  "assets": [{"path": "background.png", "sha256": "<构建时填写真实摘要>"}],
  "licenseRef": "licenses/content.txt"
}
```

示例为结构说明，摘要占位不能进入发布包。kind 可为 character/scene/wardrobe/story；MVP 只允许前两种。加载检查 schema、能力、版本、路径在包内、文件大小和资源摘要；拒绝远程脚本、路径逃逸和未知必需能力。损坏必需素材明确报错，可选动作缺失回退待机。

首版资源直接随程序发布，不做用户下载导入；未来下载器增加签名、解压配额、断点与权益校验，不复用“任意路径加载”。

素材 inventory：

| 资产 | 输入/交付 | 负责人 | 验收 |
|---|---|---|---|
| 角色参考 | 用户上传图片、来源和使用范围 | 用户 | 可用于衍生及公开分发 |
| 场景参考 | 用户上传图片、目标氛围 | 用户 | 明确前景/背景及热点位置 |
| 角色资源 | 透明底角色；待机/互动/思考/说话/成功/失败状态，必要时可复用表情 | 设计/开发 | 边缘干净、比例一致、无明显跳变；动作列表准确 |
| 场景资源 | 背景＋动态层＋两项互动状态 | 设计/开发 | 热点对齐；缩放不误点；无阻断遮挡 |
| 文本 | 固定人格、台词、错误资源键 | 产品/文案 | 中文完整，不硬编码到动画 |
| 许可与清单 | 每包来源、作者、版本、授权与摘要 | 开发/产品 | 发布包完整携带 |

用户上传参考图后另行进行图像生成/编辑；本次 PRD 不产生或假装已取得角色图。AI 生成的平面图不等于绑定完成的模型。

## 6. 数据模型与迁移

MVP 建议 SQLite（具体选型在技术验证确定），UTC 时间、稳定 UUID、事务写入。JSON 字段也需校验 schema。下列为逻辑表；future 表只定义、不要求首版创建。

| 实体 | 核心字段 | 归属/生命周期 |
|---|---|---|
| local_profiles | id, display_name, preferred_locale, created_at | Profile；不拿邮箱充当本地主键 |
| relationships | id, profile_id, character_identity_id, created_at | Profile；角色身份与外观包分离 |
| conversations | id, relationship_id, created_at | Conversation |
| messages | id, conversation_id, role, text, state, turn_id, created_at | Conversation；state 完成/中断/失败 |
| memory_proposals | id, relationship_id, category, text, source_message_id?, status, expires_at | Memory；七天到期，删除来源时取消关联 |
| memories | id, relationship_id, category, text, source_type, source_message_id?, revision, created_at, updated_at | Memory；确认后保存，来源关联可为空 |
| memory_revisions | relationship_id, revision | Memory；每次修改递增 |
| settings | profile_id, key, value, schema_version | Settings；仅凭证引用，不存明文密钥 |
| scene_states | profile_id, scene_id, content_version, state_json | Scene；状态 ID 不能绑定文案 |
| permission_grants | id, profile_id, tool_id, scope_json, lifetime, request_id?, args_digest?, revoked_at? | Permission |
| app_registry / search_roots | id, profile_id, local_path, display_name | Permission；本地敏感数据 |
| task_runs | id, request_id(unique), profile_id, state, step_states, timestamps | Task；完整路径不进入诊断副本 |
| content_selection | profile_id, character_pack_id, scene_pack_id, versions | Content；固定内容也记录 ID |
| diagnostic_events | id, type, enum_payload, occurred_at | Diagnostics；默认七天清理 |
| users（future） | id, name, email?, avatar?, created_at, updated_at | Auth；远端 userId 不替换 localProfileId |
| auth_identities（future） | user_id, provider, provider_user_id | Auth；支持多登录方式 |
| sessions（future） | id, user_id, token_hash, expires_at, revoked_at | Auth；服务器保存摘要 |
| memberships（future） | user_id, tier, status, expires_at, verified_source | Entitlement；服务端核实 |
| profile_links（future） | local_profile_id, cloud_user_id, linked_at | Sync；映射可撤销 |
| wardrobe_equips（future） | relationship_id, slot_id, content_id, version | Wardrobe |
| story_saves（future） | id, profile_id, relationship_id, story_id, story_version, node_id, flags | Story |

默认保留：messages 30 天；task_runs 七天（不保留原始用户指令副本）；diagnostic_events 七天；pending proposals 七天；确认记忆与配置直到用户清除。清除全部个人数据取消运行任务并删除相关本地记录；正常会话删除后独立已确认记忆保留但取消来源关联。

迁移要求：启动前检查版本；迁移在事务中完成，失败保留旧库并显示恢复入口，不覆盖数据。MVP 不长期保留含个人数据的隐式备份；未来备份加入备份清单与全清除路径。导出 JSON 包含 exportSchemaVersion、时间、profileId 和用户所选数据，不含凭证/授权/系统路径。首版不导入。

### 登录与同步预留

AuthProvider 定义 initiateLogin(provider)、handleCallback(callback)、getUser()、logout()。未来桌面登录走系统浏览器，采用适合公共客户端的授权码＋PKCE；桌面程序不内置 OAuth client secret，服务器秘密仅在服务端。

未来逻辑路由：auth.login、auth.callback、auth.me、auth.logout。若使用云 HTTP 服务映射为 /api/auth/login、/api/auth/callback/:provider、/api/auth/me、/api/auth/logout；首版不创建这些网络端点。

登录不自动上传本地记忆。Sync.previewLink 显示本地与云端资料，用户明确选择新建、合并或仅本地。合并按 UUID/revision 和字段冲突提示处理，不仅凭更新时间覆盖；时钟可能不准确。未来删除采用 tombstone＋同步确认，避免旧设备恢复已删数据。同步故障不能阻断本地互动和已有记忆。

登录功能开工前才要求：生产服务域名、回调地址、provider 注册、clientId、服务器 session secret、会话期限与退出语义。支付/同步需要另行补充真实依赖，不将缺这些配置当成本次 PRD 或无登录 MVP 的阻断。

## 7. 剧情与定制扩展约束

- 剧本是声明式节点：say、choice、character.action、scene.action、setFlag、wait、end；首版仅预留。节点 ID 与翻译无关，图加载检查孤立节点、无出口循环和不支持动作。
- StoryRunner 只获得角色、场景、对话呈现等 capability；没有 Task.execute/Permission.grant。剧情「我删除了文件」不改变真实文件。
- 剧情变量独立于个人记忆。故事推断、虚拟经历、角色设定不写入真人事实；跨入长期记忆须用户单独确认。
- 定制模块使用 characterIdentityId（关系身份）、characterPackId（视觉）、slotId（服装槽位）和 skeleton/rigVersion（适配）分离；同一身份换外观不重置关系，创建新身份需明确选择。
- 服装不匹配时返回 UNSUPPORTED_CAPABILITY，而非运行时穿模后仍显示成功。MVP 不要求任何服装包实现。
- 剧情退出/取消保留明确存档点，未来升级脚本需兼容或提供恢复节点；这些要求不能仅靠一条“支持插件”代替。

## 8. 关键事件与示例联动

| 事件 | 发布者 | 订阅者 | 约束 |
|---|---|---|---|
| interaction.triggered | Interaction | Coordinator | 输入须用户真实触发；仅驱动本地表现 |
| scene.state_changed | Scene | Character/Storage adapter | 持久化已提交后发布 |
| conversation.state_changed | Conversation | UI/Character | 包含 turnId，迟到事件忽略 |
| memory.changed | Memory | Conversation/cache/UI | 包含 revision，不广播正文 |
| task.state_changed | Task | UI/Character/Conversation | 仅据执行器真实状态描述 |
| content.loaded | Content | Scene/Character | 版本与能力检查通过后 |
| locale.changed | Locale/Settings | UI/content presentation | 不改写用户输入与主键 |

完整用例：「请记住我喜欢雨天」→对话返回候选→UI 确认→Memory 提交→memory.changed→面板刷新；用户点击窗外热点→Scene 切换下雨→Character 播放回应。记忆的存在不自动切天气；未来偏好驱动场景需新增明确规则与开关。

完整用例：「打开记事本」→工具提议 app.open(appId)→校验用户明确意图→权限决定→执行器启动→返回 process_started→角色回应「已经启动记事本」。不以动画播放成功作为应用打开成功的证据。

## 9. 接口验证清单

- 每个写命令有成功、非法输入、拒绝、超时/取消、重复 requestId 用例；未使用字段不能无限制透传到 OS。
- 替换一个假 ModelProvider 不修改角色/场景；替换固定内容包不修改对话/记忆。
- en/es/ja 的伪资源不影响数据 ID；缺动作回退；缺必需 manifest 能力明确失败。
- Memory 删除使旧上下文失效；任务重启后不自动重放；撤销权限后下一执行立即拒绝。
- 未来 Story 不具备真实 OS 操作能力，Auth 不成为本地陪伴强依赖。

[NEEDS_REVIEW]
