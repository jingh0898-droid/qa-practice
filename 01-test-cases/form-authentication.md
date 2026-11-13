# Form Authentication 登录模块测试用例

被测页面：https://the-internet.herokuapp.com/login
有效账号：`tomsmith` / `SuperSecretPassword!`
编写日期：2026-11-13

> 说明：预期结果按“通用登录规范”编写，执行时以页面实际提示为准。若实际与预期不符，按 `02-bug-reports` 的格式记录一条缺陷。

| 用例编号 | 用例标题 | 前置条件 | 操作步骤 | 预期结果 | 优先级 | 执行结果 |
|---|---|---|---|---|---|---|
| TC-FA-001 | 正确账号密码登录成功 | 已打开 /login 页面 | 1. 用户名输入 `tomsmith`<br>2. 密码输入 `SuperSecretPassword!`<br>3. 点击 Login | 跳转至 /secure 页面；页面出现登录成功提示；地址栏 URL 变为 `/secure` | P0 | 未执行 |
| TC-FA-002 | 密码错误时拒绝登录 | 已打开 /login 页面 | 1. 用户名输入 `tomsmith`<br>2. 密码输入 `wrongPassword`<br>3. 点击 Login | 停留在 /login 页面；出现“密码错误”类提示；不跳转 /secure | P1 | 未执行 |
| TC-FA-003 | 用户名为空时提交 | 已打开 /login 页面 | 1. 用户名留空<br>2. 密码输入 `SuperSecretPassword!`<br>3. 点击 Login | 停留在 /login 页面；出现“用户名无效”类提示；不发起登录成功跳转 | P2 | 未执行 |
| TC-FA-004 | 密码大小写敏感校验 | 已打开 /login 页面 | 1. 用户名输入 `tomsmith`<br>2. 密码输入 `supersecretpassword!`（全小写）<br>3. 点击 Login | 登录失败，停留在 /login 页面；证明密码校验区分大小写 | P2 | 未执行 |
| TC-FA-005 | 登录成功后会话保持 | 已完成 TC-FA-001 登录 | 1. 在 /secure 页面刷新浏览器（F5）<br>2. 直接访问 URL `/secure` | 仍停留在 /secure，未要求重新登录；说明会话 Cookie 生效 | P1 | 未执行 |

## 待补充

- [ ] 用户名不存在时的提示
- [ ] 用户名前后带空格（` tomsmith`）是否被 trim
- [ ] 超长输入（如 200 字符）是否被截断或报错
- [ ] 连续多次登录失败是否有锁定或限流
- [ ] 退出登录（Logout）后再次访问 /secure 是否被拦截
