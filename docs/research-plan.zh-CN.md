# CIPS 七周研究计划

周期：2026-11-16 至 2027-01-03。

## 研究问题

CIPS 研究实例级 Prefix Effect Heterogeneity：不同 Prompt 是否需要不同的防御 Prefix，以及能否在安全约束下预测效果并选择最小干预。核心证据链是：

1. Oracle 明显优于 Global Best。
2. 配对反事实数据能稳定刻画安全、效用与成本。
3. Effect Estimator 能预测干预效果和相对排序。
4. 学习式选择优于 Risk-only 与 Failure-rule。
5. Prefix Library 与 Selector 能迁移到其他模型。

## 里程碑

| 周次 | 日期 | 目标 | 验收结果 |
| --- | --- | --- | --- |
| W1 | 11/16–11/22 | 创新验证与 100–150 条 Pilot | Go/No-Go 决策 |
| W2 | 11/23–11/29 | 500 条数据、标注规范、冻结 Prefix | 数据冻结 |
| W3 | 11/30–12/06 | 五种干预的反事实生成与评分 | Counterfactual Dataset v1 |
| W4 | 12/07–12/13 | Failure Attribution 与多任务 Effect Estimator | 核心模型完成 |
| W5 | 12/14–12/20 | 安全约束 Selector 与主实验 | CIPS v1.0 |
| W6 | 12/21–12/27 | 跨模型、消融、鲁棒性与 Pareto 分析 | 实验冻结 |
| W7 | 12/28–01/03 | 论文、图表、引用与代码一致性 | 英文论文初稿 |

## Prefix Library

- P1：Instruction Hierarchy Restoration。
- P2：Untrusted Context Isolation。
- P3：Malicious Intent Recognition。
- P4：Selective Task Completion。
- No Prefix：对照组。

## 数据与评价

目标数据约 500 条：harmful 200、benign 150、mixed-intent 150；按攻击家族、底层任务和模板分组划分为 300/100/100。失败标签包括 Instruction Confusion、Intent Misinterpretation、Unsafe Subtask Execution 与 Benign Task Suppression。

每条样本运行 No Prefix 和 P1–P4，独立保存 Safety、Utility、Latency 与 Token Cost。主模型预计至少得到 2500 个干预结果，20% 样本增加第二随机种子。执行顺序应随机化。

目标函数为：

```text
J(a) = alpha * unsafe(a) + beta * (1 - utility(a)) + gamma * cost(a)
```

越低越好。第一阶段比较固定的 Global Best 与逐样本 Oracle，报告配对 Bootstrap 置信区间和实际效果差异。

## 核心模型与对照

Effect Estimator 使用 Frozen Text Encoder、Multi-task MLP 和 Pairwise Ranking Head，预测 Safety、Utility、Cost 与不确定性。最终选择器在安全阈值下最小化效用损失和成本，并提供保守回退。

主要对照为 No Defense、Static Prefix、Risk-only、Failure-rule、Global Best、CIPS 和 Oracle。必须完成 Attribution、Estimator、Ranking、Utility Constraint、Uncertainty 和 Minimal Intervention 六组消融。

## 范围约束

第一版不进行从零训练大模型、大规模 Soft Prefix Tuning、强化学习、多轮或多模态 Jailbreak、大规模 Prefix 搜索。优先完成可复现的证据链，再扩展研究范围。

## Go/No-Go

若 Oracle 与 Global Best 几乎没有差别，停止复杂 Selector 开发并重新设计 Prefix 的功能边界。若差异稳定存在，再进入正式数据构建和 Effect Estimator 阶段。

