# Reason LLM Guard

Reason LLM Guard 是 CIPS（Counterfactual Intervention Prefix Selection）的研究代码库。项目研究一个核心问题：面对不同类型的输入，能否预测不同安全 Prefix 对安全性、任务效用和推理成本的影响，并选择满足安全约束的最小干预。

当前版本聚焦第一阶段的 Go/No-Go 验证：比较固定 Prefix 与逐样本 Oracle，检验 Prefix Effect Heterogeneity 是否真实存在。

## 快速开始

项目当前只依赖 Python 标准库，Python 3.10 及以上即可运行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .

cips demo --output artifacts/demo-results.jsonl --samples 150 --seed 42
cips analyze artifacts/demo-results.jsonl --bootstrap 2000 --seed 42
python -m unittest discover -s tests -v
```

`demo` 使用可复现的模拟结果验证整条分析链路，不代表真实模型表现。接入模型后，每个样本需分别运行 `no_prefix`、`P1`–`P4`，把结果写成相同的 JSONL 格式，再用 `cips analyze` 计算 Global Best、Oracle 与 Oracle Gap。

## 研究结构

```text
configs/                 Prefix 与实验配置
data/                    原始、处理后数据及格式说明
docs/                    研究计划与决策记录
src/reason_llm_guard/    Prefix、数据结构、分析和命令行工具
tests/                   核心指标测试
artifacts/               本地实验输出（不提交）
```

## 第一阶段验收标准

- 四个 Prefix 均能通过统一接口运行。
- 100–150 条 Pilot Prompt 覆盖 harmful、benign 与 mixed-intent。
- 每条 Prompt 完成五种干预的配对生成与独立评分。
- Oracle 相比 Global Best 的优势具有实际意义，且 Bootstrap 置信区间稳定。
- 若优势不成立，先调整 Prefix 的功能边界，再开发 Effect Estimator。

完整路线见 [七周研究计划](docs/research-plan.zh-CN.md)，数据协议见 [数据说明](data/README.md)。

