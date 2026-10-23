本次提交 1 道电力监管题（A 轨，专业计算），三模型单次答卷均分 0.00%。

题包：ZCloud-电力监管-001-20261020.zip；轨迹报告：ZCloud-电力监管-001-20261020-轨迹报告.zip。提交时两个文件链接放在同一行。

数据量：1 道题，2 份输入文件（Distribution_handbook.pdf、Powercor_RFM_inputs.xlsx）。
三个模型：GPT-5.6-SOL、Claude Opus 4.8、Qwen 3.8 Max。
三模型得分：GPT-5.6-SOL 0.0000，Claude Opus 4.8 0.0000，Qwen 3.8 Max 0.0000；均分 0.0000。参考答案分数：1.000（同一答卷重复评分 5 次，标准差 0.0）。

轨迹报告含三模型原始消息、工具调用、实际答卷 xlsx、每张工作表的渲染图及逐条裁判记录。

求解 Agent 只能看到 instruction.md 与 environment/input_files/；答卷写入 /app/output/answer.xlsx。rubrics.json、solution/、tests/、metadata/ 和轨迹报告不挂载到求解上下文。

三个模型各在独立的 Docker 容器中运行：GPT-5.6-SOL 与 Qwen 3.8 Max 使用 Codex CLI，Claude Opus 4.8 使用 Claude Code。模型名称保留网关原始返回值；Qwen 运行中网关返回过 qwen/qwen3.8-max 与 qwen3.8-max-0902 两种写法，属同一基础型号。每个模型目录下的 container_boundary.json、gateway_config.json、execution_verification.json、trajectory/provider_requests.jsonl 由运行时回执导出，未补造任何请求。

**评分与证据**

- 评分标准共 9 条：程序判据 6 条（其中正项 3 条），LLM 扣分项 3 条；正项权重合计 30。权重只取 [-3, 10] 中的值。
- 计分：正项按正确度计分，负项按违规程度扣分，负项不进入分母，总分截断到 [0, 1]。公式：`round(clip((sum(w_i*q_i for w_i>0)-sum(abs(w_j)*v_j for w_j<0))/s_max,0,1),6)`。通过阈值 0.7。
- 一致性：参考答案重复评分 5 次，总分 [1.0, 1.0, 1.0, 1.0, 1.0]，总分样本标准差 0.0，单条判据样本标准差最大 0.0（要求都 < 0.05）。
- 区分度：参考答案 1.000，三模型 0.0000、0.0000、0.0000。
- 部分正确样例：以参考答案为底改错部分结果项，离线程序评分为 0/3 项正确 0.000、1/3 项正确 0.333、2/3 项正确 0.667、3/3 项正确 1.000（LLM 扣分项按未违规处理），见轨迹报告 discrimination_cases.json。
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
- 题面差异：题面开头补了一句角色说明；Results 表的小标题和表头说明句换了措辞，行顺序、单位和数值要求不变；末尾的运行说明把输入目录从 /app/input 改为题包镜像里的 /app/input_files/。数值、判据和输出格式要求相同。
- environment/Dockerfile 只用公开源构建（python:3.12-slim-bookworm、Debian、npm、PyPI）。模型运行时用的是开发环境镜像；用本 Dockerfile 在断网容器里重算程序判据，参考答案 1 分，三份模型答卷的程序分与本文成绩一致。
- 6 次裁判作业因网关超时或连接中断没有完成，没有纳入成绩和一致性统计，也没有按 0 分计。
- Qwen 3.8 Max 答卷的三条 LLM 扣分项被判为违规，裁判给出的理由却写未发现虚构；该答卷正项得分为 0，总分不受影响，原始判定原样保留。
- 开发阶段的另一套评分规则会先重算公式，给 Qwen 3.8 Max 0.02 分；本包统一使用 Office 裁判分。
