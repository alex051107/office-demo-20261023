## 候选文件访问校验修订

本节为当前状态，后续旧章节仅作历史记录。金标新有效判定 0/5；旧暂定分 1.0，当前分 不可用；程序部分仍为1。总分样本标准差：不可计算（少于两次有效判定）。不足五次不宣称满足一致性要求。

已删除缺文件时负项按无违规处理的退路。内容裁判必须先用python3/openpyxl打开候选；每条理由必须引用候选工作表的具体单元格。程序成功打开候选后，若理由称候选缺失/不可读，或没有候选单元格引用，记verifier_error=1、judge:artifact_access_error，不纳入有效分数。来源文件缺失与候选文件无法访问分开处理，避免把正常来源扣分误作裁判错误。判据文字和权重不变。

本题实际尝试 0 次，终止时观测的累计账户用量差 0.000000 美元；逐次明细见轨迹报告的judge_costs.json。每次运行前后核对账户，费用超过2美元、账户达到1635美元或运行超过15分钟即停止后续运行；超时终止容器。停止原因：single_run_cost_exceeded_2_usd。模型原分/现分：{'claude-opus-4-8': 0.0, 'gpt-5.6-sol': 0.0, 'qwen3.8-max': 0.0} / {'claude-opus-4-8': 0.0, 'gpt-5.6-sol': 0.0, 'qwen3.8-max': 0.0}。指定模型新判定尚未取得；保留原记录，不声称已复判。

旧代表、旧五次重复及无效新尝试均保留在既有重判历史目录；无效尝试不记为答卷零分。instruction.md、test.sh、判据权重、金标工作簿及模型答案均未改动。

---

本次提交 1 道市政财务题（C 轨，合同与台账），三模型单次答卷均分 0.00%。

题包：ZCloud-市政财务-002-20261022.zip；轨迹报告：ZCloud-市政财务-002-20261022-轨迹报告.zip。提交时两个文件链接放在同一行。

数据量：1 道题，8 份输入文件（Agreement.pdf、Records.pdf、Records_Broker_payments.png、Records_Finance_forecast.png、Records_Other_payments.png、Records_Plans.png、Records_Sources.png、Records_Sponsorships.png）。
三个模型：GPT-5.6-SOL、Claude Opus 4.8、Qwen 3.8 Max。
三模型得分：GPT-5.6-SOL 0.0000，Claude Opus 4.8 0.0000，Qwen 3.8 Max 0.0000；均分 0.0000。参考答案分数：1.000（暂定历史判定重组值；本轮真实重判因费用超限停止，未完成）。

轨迹报告含三模型原始消息、工具调用、实际答卷 xlsx、每张工作表的渲染图及逐条裁判记录（Claude Opus 4.8 的 LLM 扣分项未评完，见说明与限制）。

求解 Agent 只能看到 instruction.md 与 environment/input_files/；答卷写入 /app/output/answer.xlsx。rubrics.json、solution/、tests/、metadata/ 和轨迹报告不挂载到求解上下文。

三个模型各在独立的 Docker 容器中运行：GPT-5.6-SOL 与 Qwen 3.8 Max 使用 Codex CLI，Claude Opus 4.8 使用 Claude Code。模型名称保留网关原始返回值；Qwen 运行中网关返回过 qwen/qwen3.8-max 与 qwen3.8-max-0902 两种写法，属同一基础型号。每个模型目录下的 container_boundary.json、gateway_config.json、execution_verification.json、trajectory/provider_requests.jsonl 由运行时回执导出，未补造任何请求。

**评分与证据**

- 评分标准共 20 条：程序判据 17 条（其中正项 6 条），LLM 扣分项 3 条；正项权重合计 51。权重只取 [-3, 7, 10] 中的值。
- 计分：正项按正确度计分，负项按违规程度扣分，负项不进入分母，总分截断到 [0, 1]。公式：`round(clip((sum(w_i*q_i for w_i>0)-sum(abs(w_j)*v_j for w_j<0))/s_max,0,1),6)`。通过阈值 0.7。
- 一致性：五份历史判定重组总分均为 1.0，各项及总分样本/总体标准差均为 0.0；本轮新真实裁判有效数为 0，新的 σ 不可计算，尚未通过第二轮一致性验收。
- 区分度：参考答案 1.000，三模型 0.0000、0.0000、0.0000。
- 部分正确样例：以参考答案为底改错部分结果项，离线程序评分为 0/6 项正确 0.000、1/6 项正确 0.196、2/6 项正确 0.392、3/6 项正确 0.588、4/6 项正确 0.725、5/6 项正确 0.863、6/6 项正确 1.000（仅程序子集，未推定 LLM 是否违规），见轨迹报告 discrimination_cases.json。
- 难度：每个模型各一次有效运行（pass@1），未做 8 次独立运行，所以没有 pass@8。
- 逐条结果见轨迹报告各模型目录下的 judge.json；汇总见 quality_report.json。

**运行与验收**

以下变量由验收运行器注入 verifier 容器，不注入求解 Agent。

| 变量 | 必选 | 默认值 | 用途 |
|---|---|---|---|
| JUDGE_API_KEY | 是 | 无 | 裁判 API 凭据；未设置时读取 EVAL_API_KEY。真实凭据不随题包交付。 |
| JUDGE_BASE_URL | 是 | 无 | 裁判服务地址；未设置时读取 EVAL_API_BASE。 |
| JUDGE_MODEL | 否 | qwen3.7-plus | 裁判模型；通过 REWARDKIT_MODEL 传入评分器。 |
| JUDGE_PROVIDER | 否 | anthropic | Provider 接口声明；协议切换由 JUDGE_API_PROTOCOL 控制。 |
| JUDGE_API_PROTOCOL | 否 | anthropic | 默认使用 Claude Code Judge；openai 切换兼容 LLM Judge。 |
| EVAL_API_KEY | 否 | 空 | 旧配置兜底；有 JUDGE_API_KEY 时忽略。 |
| EVAL_API_BASE | 否 | 空 | 旧配置兜底；有 JUDGE_BASE_URL 时忽略。 |
| LITELLM_DROP_PARAMS | 否 | true | 网关参数兼容开关。 |

Oracle 入口为 `bash /solution/solve.sh`，验收入口为 `bash /tests/test.sh`，评分输出位于 `/logs/verifier/`。这些是容器内运行路径，不是交付附件路径；test.sh 只在验收容器内执行，不要在宿主机直接运行。verifier 总超时 18000 秒，由 task.toml 配置，不是求解 Agent 的轮次限制。

**说明与限制**

- 题面改编自公开材料；输入文件随包交付，没有外链。
- 每个模型只有一次运行，分数是单次结果，不代表 pass@8。
- environment_template 写为 environment/Dockerfile，表示包内自定义 Dockerfile；平台是否接受这种写法需要确认。
- 裁判的上游原始 HTTP 响应没有单独保存，judge_provider_response.json 写明了这一点；逐条裁判结果完整保留在 reward-details.json 与 judge.json。
- 模型运行时实际收到的题面原样放在轨迹报告各模型目录下的 solver_prompt.md。
- 题面差异：Results 表的小标题和表头说明句换了措辞，行顺序、单位和数值要求不变；末尾的运行说明把输入目录从 /app/input 改为题包镜像里的 /app/input_files/。数值、判据和输出格式要求相同。
- environment/Dockerfile 只用公开源构建（python:3.12-slim-bookworm、Debian、npm、PyPI）。模型运行时用的是开发环境镜像；用本 Dockerfile 在断网容器里重算程序判据，参考答案 1 分，三份模型答卷的程序分与本文成绩一致。
- Claude Opus 4.8 答卷的 LLM 裁判作业运行异常（请求次数远超正常作业），被人工停止，没有纳入一致性统计。
- Claude Opus 4.8 答卷只有程序判据结果：正项得分为 0，LLM 判据全部是扣分项，所以总分只能是 0，记 0。
- 开发阶段的另一套评分规则给三个模型各 0.07 分，全部来自格式项；本包规则下格式项只扣分不加分，记 0。

## 评分器 v2（2026-10-26）

此为固定版本标签；第二轮修订与验证执行于 2026-10-25。评分修复及离线验证完成；五次新金标裁判未完成，不能把历史重组值当作第二轮真实一致性验收。

- 先按原有 signed-weight 公式池化，分母仍为 51，再应用三个独立、命名、二元规则：`required_sheet_gate` 在必需表缺失或错名时令全题为 0；`required_header_cap` 在必需前置表头不符时封顶 0.69；`must_clause_cap` 在必需来源为空或纯数值、单位非 USD、非规定业务标签携带业务值（含零金额）时封顶 0.69。规则及原因和规则前后分数写入 `reward-details.json`，不增加权重或分母。
- 表头去首尾空格后精确匹配，大小写敏感。instruction.md 第 16、21 行指定 Results 的 A1:D1，第 31 行指定 Detail 的 A1:C1；没有 exactly/only 总列数限制，两表均允许在必需列之后附加列，允许额外支持表和空白有样式列。
- 行序与显示精度保留普通扣分。重复规定记录按既有 S05/P02 扣分；不是靠提高权重模拟封顶。Results 增加 Plan D 为 0.690000；规定行反序为 0.941176；Detail 列反序为 0.235294（已触发表头封顶，但数值错位使池化分更低）。
- p 位精度满足条件为：数字格式显示 p 位，或存值等于 round(value,p)；“至少 p 位”另接受存值小数位数不少于 p。General 格式的整数、等价存值不扣分。数值容差与显示精度分开，本题六个金额项都采用 0.005 USD；输入是整数金额与精确 10% 比率，合理舍入顺序不产生超过半分的差异，不需额外放宽。边界 0.0049、0.005 接受，0.0051 拒绝。
- 共 20 条加权判据：17 条程序项、3 条 LLM 负项；全部权重及 LLM 正文不变。职责归属见题包 `validation/llm_criterion_ownership.md`：来源是否真实存在归 L01，来源为空或纯数值归程序；无证据完成性声明归 L02；新增经营事实归 L03，数值误算与额外记录不重扣。
- 45 份回归控制卷及真实 finalize 汇总入口检查全部通过：34 个负例（5 个零分门槛、19 个封顶、10 个普通失分），11 个正控制全为 1.0。正控制包含附加支持表、表头尾空格、空白有样式列、等价存值、两个表允许的附加列。另有 5 个金额边界/缺文件检查及 4 个“至少 p 位”断言通过；本地无违规 LLM 占位明细仅用于验证汇总，不能代替真实裁判。
- 金标 5 份 xlsx 副本与首轮逐字节相同；保留两位小数、完整来源与文字计算。两张表重新导出 PDF/PNG 并目视检查，金额、日期和来源未改。原始 `.v1.json` / `.v1.jsonl` 未覆盖，首轮当前评分另存 `.round1.json` / `.round1.jsonl`。

| 答卷 | 原交付分 | 首轮分 | 第二轮程序分 | 第二轮重组分及依据 |
|---|---:|---:|---:|---|
| 金标 | 1.000000 | 1.000000 | 1.000000 | 1.000000，暂定，仅复用历史 LLM 判定 |
| GPT-5.6-SOL | 0.000000 | 0.000000 | 0.000000 | 0.000000，模型保存判定原样复用 |
| Claude Opus 4.8 | 0.000000 | 0.000000 | 0.000000 | 0.000000，程序分上界，LLM 仍未完成 |
| Qwen 3.8 Max | 0.000000 | 0.000000 | 0.000000 | 0.000000，模型保存判定原样复用 |

### 新金标裁判的实际状态

本轮只发起 1 次真实金标裁判，0 次有效完成。该次运行反复输出文本式 function_call/code_interpreter，随后收到要求 StructuredOutput 的停止钩子反馈，没有产生合格的结构化裁判结果。运行器结果为 verifier_error=1、criteria_counted=0；停止后的返回码为 137。这是裁判失败，不是金标得 0 分。

该尝试期间账户用量增量为 8.650104 USD；这是账户增量，不是单次请求的独立账单。费用上限存在 0.5/1 USD 两处表述，本轮按更严格的 0.5 USD 执行停止条件；发现时已超限，随即停止本任务容器，不再重试，也未启动 r2–r5。不能声称费用一直被控制在上限以内。脱敏回执见轨迹报告 `judge_runs/round2_attempts/golden_r1/`，汇总见 `judge_runs/golden_round2_status.json`。

第二轮新裁判的逐项与总分 σ 均为“不可计算”，不是 0。`consistency.json` 中五份历史判定重组的总分及 20 个判据样本/总体 σ 仍为 0，仅作历史重组检查，不满足本轮要求的新五次实验。现有 golden_r1..r5 保留历史来源标识，没有用失败运行或本地占位结果替换。

剩余项：修复真实裁判结构化输出兼容性并获准恢复费用后，补足五次有效金标裁判，再更新金标总分与一致性；本轮按费用停止规则不继续付费。instruction.md、8 份输入、3 个模型答卷及其保存的 LLM 判定不变；Sol 保存理由的“未找到交付文件”差异与 Opus 未完成状态均保留。第 1、2、4 类事项仍暂缓。

- 2026-10-26 重判：`rejudge_v4_20261026/previous/`保留替换前记录；轨迹报告同组`invalid_attempts/`保留无效尝试；有效金标4/5，无效尝试2次，不计分；费用12.692242美元。
