# 登录模块 · 用例（含实测结果）

被测页面：https://the-internet.herokuapp.com/login
有效账号：`tomsmith` / `SuperSecretPassword!`
编写：2026-11-13　执行：2026-11-13（Chrome，实测）

| 用例编号 | 用例标题 | 前置条件 | 操作步骤 | 预期结果（实测） | 优先级 |
|---|---|---|---|---|---|
| TC-FA-006 | 用户名前后带空格 | 已打开 /login | 1. 用户名输入 ` tomsmith`（前导一个空格）<br>2. 密码 `SuperSecretPassword!`<br>3. 点 Login | 页面停留在 /login（URL 不变）；顶部出现红色提示条 `Your username is invalid!`，右侧带 `×` 关闭按钮；用户名与密码输入框均被清空 | P2 |
| TC-FA-007 | 用户名不存在 | 已打开 /login | 1. 用户名 `notauser`<br>2. 密码 `SuperSecretPassword!`<br>3. 点 Login | 页面停留在 /login；提示条 `Your username is invalid!`；输入框被清空；提示内容与 TC-FA-006 完全一致 | P1 |
| TC-FA-008 | 连续输错 5 次密码后正确登录 | 已打开 /login，未登录 | 1. 用户名 `tomsmith`、密码 `wrong`，点 Login<br>2. 重复上一步，共 5 次<br>3. 第 6 次改用 `SuperSecretPassword!` 登录 | 第 1–5 次均停留在 /login，提示 `Your password is invalid!`，无任何限流、验证码或账号锁定提示；第 6 次登录成功，跳转 /secure，提示条 `You logged into a secure area!`，正文显示 `Logged in as tomsmith` | P2 |
| TC-FA-009 | 用户名超长输入 | 已打开 /login | 1. 用户名粘贴 200 个 `a`<br>2. 密码 `SuperSecretPassword!`<br>3. 点 Login | 页面停留在 /login；提示 `Your username is invalid!`；输入框被清空；未出现长度限制提示，也无截断提示 | P2 |
| TC-FA-010 | 退出登录后会话销毁 | 已用正确账号登录，停留在 /secure | 1. 点页面上的 Logout<br>2. 观察地址栏<br>3. 手动输入 `/secure` 并回车 | 点 Logout 后跳转 /login，提示条 `You logged out of the secure area!`；手动访问 /secure 被重定向回 /login，提示条 `You must login to view the secure area!`，原会话已失效 | P1 |

---

## 实测结论（可以写进测试报告的部分）

**1. 用户名未做 trim 处理。**
TC-FA-006（` tomsmith` 前导空格）与 TC-FA-007（`notauser` 不存在）返回完全相同的提示 `Your username is invalid!`，说明空格未被忽略，且系统无法区分“用户不存在”和“输入格式问题”。
影响：用户从输入法或复制粘贴带入空格时无法登录，且提示信息无法辅助定位原因。

**2. 登录失败无任何限流或锁定机制。**
连续 5 次错误密码后，第 6 次用正确密码仍然直接登录成功，全程无限流、无验证码、无延迟增长。
影响：存在暴力破解风险，属于安全测试范畴的问题，严重程度可评为「严重」。

**3. 未登录访问受保护页面时，会话控制正确。**
退出后直接访问 /secure 被重定向到 /login，并给出明确提示 `You must login to view the secure area!`，没有出现“页面空白但实质已登录”的越权问题。这条是**通过项**，测试报告里同样要写——不只记录问题。

---

## 自查清单（第二版已过）

- [x] 预期结果里没有“正常”“正确”“符合预期”这类没法验证的词
- [x] 提示文字原样抄写，用反引号标出
- [x] 每条都写了“页面去哪”+“看到什么”+“变化”
- [x] 步骤里带具体输入值，别人能照着复现
