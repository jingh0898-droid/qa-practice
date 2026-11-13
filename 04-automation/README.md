# UI 自动化（Playwright + pytest）

把 `01-test-cases/` 里的手工登录用例，变成可以一键执行、自动判断的脚本。

## 环境准备

```bash
pip install playwright pytest
```

本脚本复用本机已安装的 **Microsoft Edge**（`channel="msedge"`），**不需要**再执行 `playwright install` 下载浏览器。
若要用 Chrome，把 `tests/conftest.py` 里的 `channel="msedge"` 改成 `channel="chrome"`。

## 运行

```bash
cd 04-automation
python -m pytest tests -v
```

## 用例与结果（2026-11-13 实测）

| 用例 | 检查点 | 结果 |
|---|---|---|
| TC-LOGIN-001 | 正确账号登录 → 跳转 /secure + 成功提示 + 显示登录用户名 | 通过 |
| TC-LOGIN-002 | 密码错误 → 停留 /login + `Your password is invalid!` | 通过 |
| TC-LOGIN-003 | 失败后用户名/密码输入框被清空 | 通过 |
| TC-LOGIN-004 | 用户名前导空格应被忽略（` tomsmith` 等同 `tomsmith`） | **预期失败（XFAIL）**：未做 trim |
| TC-LOGIN-005 | 连续失败 5 次后第 6 次不应直接放行 | **预期失败（XFAIL）**：次数无限制，对应 BUG-001 |
| TC-LOGIN-006 | 退出后回 /login，手动访问 /secure 被拦截 | 通过 |

**执行汇总**：`4 passed, 2 xfailed in 62.99s`

## 为什么用 xfail 而不是让它直接红

`@pytest.mark.xfail(strict=True)` 的含义是：「这条用例按正确行为写了断言，但我确定当前实现做不到」。

- 缺陷还在 → 显示 **XFAIL**，CI 不会因此中断，报告里一看就知道是已知问题；
- 缺陷修好了 → 断言意外通过，pytest 显示 **XPASS**，在 `strict=True` 下会**主动报错**，提醒你把标记删掉、更新缺陷状态。

这比“故意写错断言让它一直红”更严谨：**红是噪音，XFAIL 是有据可查的已知问题。**

## 脚本要点（面试常被追问）

1. **不用 `sleep` 等页面**：靠 `wait_for_load_state` 和 Playwright 自带的元素等待，减少不稳定；
2. **断言可验证**：每条都断言具体文字或具体 URL，不写 `assert flash == ""` 这种无法定位的表达；
3. **夹具复用浏览器**：`browser` 是 session 级夹具，6 条用例只启动一次 Edge，每条用例新建独立 context，互不污染；
4. **失败信息带实测值**：`assert ..., f"实际 URL={page.url}"`，失败时日志里直接看到现场，不用重现一遍。

## 已知局限

- 依赖公网练习站，网络抖动会导致偶发失败；真实项目应配置重试策略并区分「用例失败」与「环境不可用」
- 每条用例都真实跑一次浏览器，耗时约 10 秒/条；规模变大后需要并行执行（`pytest-xdist`）
- 尚未接入失败截图留证与 HTML 报告（下一步可加 `--screenshot`、`pytest-html`）
