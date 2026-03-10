# WEEX Python Connectors

WEEX Python Connectors 提供现货、合约和共享运行时模块，便于通过 Python 接入 WEEX REST API、WebSocket API 与 WebSocket Streams。

## Prerequisites

在使用本仓之前，请确保本地具备：

- Python 3.9 或更高版本
- `pip`
- 可选：`venv` 或其它虚拟环境工具

## Available SDK

- [common](./common) - WEEX Python Connectors 共享运行时包，提供 `weex_common` 下的配置、签名、传输、错误与 WebSocket 基础能力。
- [clients/spot](./clients/spot) - WEEX Spot Connector，保留独立的 REST、Public WebSocket、Private WebSocket 能力与子 README。
- [clients/contract](./clients/contract) - WEEX Contract Connector，保留独立的 REST、Public WebSocket、Private WebSocket 能力与子 README。

## Documentation

详细使用方式请优先查看各子 Connector 的 README：

- [common/README.md](./common/README.md)
- [clients/spot/README.md](./clients/spot/README.md)
- [clients/contract/README.md](./clients/contract/README.md)

说明：

- 现货仍排除 `POST /api/v3/order/batch`。
- 合约仍排除 `POST /capi/v3/batchOrders`。
- 鉴权信息只通过环境变量传入，不写入源码、README 默认值或日志样例。

## Installation

本仓采用根级 `common/` + `clients/{spot,contract}` 的目录结构。安装任一子 Connector 前，都需要先安装共享 `common` 包：

```bash
pip install -e ./common
pip install -e ./clients/spot
pip install -e ./clients/contract
```

如果你只使用其中一个子 Connector，也仍然需要先安装 `./common`，然后再安装目标子包。

常用环境变量：

```bash
WEEX_API_KEY=your_api_key
WEEX_API_SECRET=your_secret_key
WEEX_API_PASSPHRASE=your_passphrase
WEEX_BASE_URL=https://stg-api-host
WEEX_WS_PRIVATE_URL=wss://stg-private-ws
WEEX_WS_PUBLIC_URL=wss://stg-public-ws
```

导入方式示例：

```python
from weex_spot_sdk import Spot
from weex_contract_sdk import Contract
```

## Contributing

修改时建议：

1. 涉及共享配置、签名、传输、错误或 WebSocket 基类时，优先修改 [`common`](./common)。
2. 业务特定改动放在对应子 Connector（`clients/spot` 或 `clients/contract`）内完成。
3. 同步更新对应子 README、示例和测试，并保持根 README 与子 README 的能力边界一致。

## Code Style

Python 代码延续现有子 SDK 的风格约定：

- 遵循 PEP 8
- 优先保持现有公开 API 不变
- 修改后至少运行对应子目录下的基础测试或构建检查

## License

仓库当前未附带独立开源许可证文件。如需对外发布，请先补充 LICENSE 并审查相关许可声明。
