# qa-practice

软件测试实习准备期的练习仓库。所有用例、缺陷报告、接口测试与自动化脚本都放在这里。

## 目录结构

```
qa-practice/
├── 01-test-cases/       # 手工测试用例（Markdown 表格）
├── 02-bug-reports/      # 缺陷报告
├── 03-api-tests/        # 接口测试（Postman 集合、报告）
├── 04-automation/       # pytest / Playwright 自动化
└── README.md
```

## 练习对象

- Web 功能测试：https://the-internet.herokuapp.com/
- 控件级用例：https://github.com/cypress-io/cypress-example-kitchensink
- 接口测试：https://restful-booker.herokuapp.com/ 、https://httpbin.org/

## 进度

- [ ] 阶段 1：用例设计（100 条）
- [ ] 阶段 1：缺陷报告（5 条）
- [ ] 阶段 2：接口测试（Postman 集合 + 报告）
- [ ] 阶段 3：pytest 接口自动化 + CI
- [ ] 阶段 4：Playwright UI 自动化
- [ ] 阶段 6：真实项目测试报告（RuoYi-Vue / mall）

## 用例字段约定

| 字段 | 说明 |
|---|---|
| 用例编号 | TC-模块缩写-序号，如 TC-FA-001 |
| 模块 | 对应页面或功能模块 |
| 用例标题 | 一句话说清测什么 |
| 前置条件 | 执行前必须满足的状态 |
| 操作步骤 | 编号步骤，一步一个动作 |
| 预期结果 | 可验证的结果，不写“正常显示”这类空话 |
| 优先级 | P0 核心流程 / P1 主要功能 / P2 边界异常 / P3 次要 |
| 执行结果 | 通过 / 失败 / 阻塞 / 未执行 |
