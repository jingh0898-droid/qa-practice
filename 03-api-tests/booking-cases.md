# restful-booker 接口用例（第一组）

被测服务：https://restful-booker.herokuapp.com
接口文档：https://restful-booker.herokuapp.com/apidoc/index.html
执行工具：Postman 12.36.4
执行日期：2026-11-13

## 用例表

| 编号 | 用例标题 | 方法 | 接口地址 | 预期结果 | 实测结果 | 结论 |
|---|---|---|---|---|---|---|
| API-001 | 健康检查接口可访问 | GET | `/ping` | 状态码 201，响应体为 `Created` | 201，Body `Created` | 通过 |
| API-002 | 查询全部订单列表 | GET | `/booking` | 状态码 200，响应体为 JSON 数组，每个元素仅含 `bookingid` 且为**数字类型** | 200，数组元素形如 `{"bookingid": 2}` | 通过 |
| API-003 | 查询单条订单详情 | GET | `/booking/1` | 状态码 200，响应体为对象，含 `firstname`、`lastname`、`totalprice`、`depositpaid`、`bookingdates`（内部再嵌套 `checkin`、`checkout`）、`additionalneeds` | 200，字段与文档一致，`bookingdates` 为两层嵌套 | 通过 |
| API-004 | 查询不存在的订单（反向） | GET | `/booking/999999` | 状态码 404，不返回任何订单数据 | 404 | 通过 |

## 实测发现（可以写进测试报告的观察）

**1. `bookingid` 是数字类型，不是字符串。**
响应里是 `{"bookingid": 2}`，没有引号。**引号在 JSON 里就是类型的边界**：`2` 是数字，`"2"` 是字符串。这一点必须校验，因为后端返回 `"2"` 而前端按数字比较时，`"2" === 2` 在 JavaScript 里是 `false`，会导致列表点进详情、分页、去重等功能全部失效，而页面上看不出任何报错。**接口测试的价值一半在这里：类型错了，界面照样能显示。**

**2. `/ping` 返回 201 Created，状态码语义不匹配。**
健康检查接口的语义是「我还在，回你一声」，正常应为 `200 OK`。`201` 的含义是「服务端新建了资源」，而这里什么都没建。文档既然写 201，我们按 201 校验（当前实现与文档一致，不算 bug），但可作为「接口设计不规范」的观察记录。真实项目里遇到同类情况，可提为改进建议。

**3. 列表接口只返回 `bookingid`，不返回业务字段。**
这是**正常的设计**（列表轻量、详情按需拉取），不是缺陷。新手容易把它当 bug 提「为什么列表看不到姓名」，会显得没经验——**判断一个现象是 bug 还是设计，得先看文档怎么约定**。

**4. 反向用例的价值：查不到时必须报 404。**
`/booking/999999` 返回 404 而不是「200 + 空数组」或「200 + null」，说明错误的表达是明确的。如果它返回 200 配空对象，前端会把「不存在」当成「有一条空数据」，用户看到的是空白详情页而不是「订单不存在」——这类问题用户很难描述清楚，只有接口层能抓到。

## 待补充（下一组）

- `POST /booking` 创建订单（需 `Content-Type: application/json`）
- `POST /auth` 获取 token（体 `{"username":"admin","password":"password123"}`）
- 带 token 的 `PUT` / `DELETE`，以及**不带 token 时应当返回 403**
- 参数校验类：`POST /booking` 缺 `firstname`、`totalprice` 传字符串、`checkin` 格式非法，观察是否返回 400
