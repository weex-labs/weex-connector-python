# WEEX Python Spot SDK

WEEX Python Spot SDK 提供现货 REST、私有 WebSocket API 和公共 WebSocket Streams 接入能力：

- [REST API](./src/weex_spot_sdk/rest_api/rest_api.py)
- [WebSocket API](./src/weex_spot_sdk/websocket_api/websocket_api.py)
- [WebSocket Streams](./src/weex_spot_sdk/websocket_streams/websocket_streams.py)

## 目录

- [支持特性](#支持特性)
- [安装](#安装)
- [文档](#文档)
- [REST API](#rest-api)
- [WebSocket API](#websocket-api)
- [WebSocket Streams](#websocket-streams)
- [测试](#测试)
- [当前边界](#当前边界)
- [许可证](#许可证)

## 支持特性

- 覆盖现货 SDK 范围内的 REST 服务分组：`GeneralApi`、`MarketApi`、`TradeApi`、`AccountApi`、`RebateApi`。
- 提供私有 WebSocket API 与公共 WebSocket Streams 两套实时连接入口。
- 仓库内提供可直接运行的示例与 live 集成测试：
  - [REST 示例](./examples/rest_example.py)
  - [公共 WebSocket 示例](./examples/public_ws_example.py)
  - [私有 WebSocket 示例](./examples/private_ws_example.py)
  - [Live 集成测试](./tests/live_integration.py)

## 安装

建议使用 Python 3.9 或更高版本。

当前目录只包含 Spot 客户端源码；共享 `weex_common` 已经上提到 [`../../common`](../../common)。推荐从 `output/weex-connector-python` 根目录执行：

```powershell
pip install -e .\common
pip install -e .\clients\spot
```

常用环境变量：

- `WEEX_API_KEY`
- `WEEX_API_SECRET`
- `WEEX_API_PASSPHRASE`
- `WEEX_BASE_URL`
- `WEEX_WS_PRIVATE_URL`
- `WEEX_WS_PUBLIC_URL`

如果你要单独访问返佣/代理链路，可额外准备一组 partner 前缀凭证，并通过 `Spot.from_env(env_prefix="WEEX_PARTNER_")` 创建独立客户端：

- `WEEX_PARTNER_API_KEY`
- `WEEX_PARTNER_API_SECRET`
- `WEEX_PARTNER_API_PASSPHRASE`

## 文档

详细接口说明请参考以下文档：

- [中文源文档](../../../../resources/source_docs/zh-CN/)
- [英文源文档](../../../../resources/source_docs/en/)
- [OpenAPI 规格](../../../../specs/openapi.yaml)
- [spec 与实测差异](../../../../analysis/shared/spec_vs_actual.md)

## REST API

所有 REST 接口统一通过 [`rest_api`](./src/weex_spot_sdk/rest_api/rest_api.py) 入口访问。你可以使用分组方法，也可以在需要时通过 `execute_operation()` 按 `operationId` 直接调用。

```python
from weex_spot_sdk import Spot

client = Spot.from_env()
response = client.rest_api.market_api.get_depth(
    {"query": {"symbol": "BTCUSDT", "limit": 15}}
)
print(response.status_code)
print(response.data)
```

更多用法可参考 [REST 示例](./examples/rest_example.py)。

### 配置项

REST 侧对应 `ConfigurationRestAPI`，当前支持的主要配置项有：

- `base_path`：REST 基础地址，默认生产地址为 `https://api-spot.weex.com`
- `api_key` / `api_secret` / `passphrase`：签名鉴权凭证
- `timeout`：请求超时秒数，默认 `30.0`
- `max_retries`：重试次数，默认 `0`
- `base_headers`：追加请求头
- `user_agent`：自定义 User-Agent
- `session`：自定义 HTTP session

默认环境变量装配方式：

```python
from weex_spot_sdk import Spot

client = Spot.from_env()
partner_client = Spot.from_env(env_prefix="WEEX_PARTNER_")
```

### 错误处理

Python 版本提供细粒度异常类型，常见类型包括：

- `RequiredError`
- `ClientError`
- `SignatureError`
- `NetworkError`
- `BadRequestError`
- `UnauthorizedError`
- `ForbiddenError`
- `NotFoundError`
- `TooManyRequestsError`
- `ServerError`
- `ApiBusinessError`

### Staging

如果你要切换到 staging 环境，可设置：

```powershell
$env:WEEX_BASE_URL='https://stg-spotpro-openapi.weex.tech'
```

如果还需要覆盖 WebSocket 地址，可同时设置 `WEEX_WS_PRIVATE_URL` 与 `WEEX_WS_PUBLIC_URL`。

## WebSocket API

私有 WebSocket API 通过 [`websocket_api`](./src/weex_spot_sdk/websocket_api/websocket_api.py) 暴露，适合账户、订单等需要鉴权的订阅。

```python
from weex_spot_sdk import Spot

client = Spot.from_env()
ws_api = client.websocket_api
ws_api.connect()
ws_api.subscribe_orders()
print(ws_api.receive())
ws_api.close()
```

更多用法可参考 [私有 WebSocket 示例](./examples/private_ws_example.py)。

## WebSocket Streams

公共流式订阅通过 [`websocket_streams`](./src/weex_spot_sdk/websocket_streams/websocket_streams.py) 暴露，适合 ticker、depth、trade、kline 等实时行情。

```python
from weex_spot_sdk import Spot

client = Spot.from_env()
streams = client.websocket_streams
streams.connect()
streams.subscribe_ticker("BTCUSDT")
print(streams.receive())
streams.close()
```

更多用法可参考 [公共 WebSocket 示例](./examples/public_ws_example.py)。

## 测试

基础构建校验建议从 `output/weex-connector-python` 根目录执行：

```powershell
python -m compileall .\common\src
python -m compileall .\clients\spot\src
```

如果你已经准备好 full-live 所需的环境变量与测试条件，再执行：

```powershell
python .\clients\spot\tests\live_integration.py
```

说明：

- 现货 live 验证默认读取 `WEEX_API_*`。
- 返佣/代理链路验证会在存在 `WEEX_PARTNER_*` 时自动创建 partner client。

## 当前边界

- `POST /api/v3/order/batch` (`placeBatchOrders`) 已按用户要求排除，不生成对应 SDK 方法。
- `internalWithdrawal` 仍保留在 SDK 中，但本轮未纳入 required live。

## 许可证

仓库当前未单独附带许可证文件。如需对外发布，请按你的仓库规范补充许可证与版本发布信息。
