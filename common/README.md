# WEEX Python Common

`common/` 提供 Python 版 Spot 和 Contract SDK 共用的 `weex_common` 运行时依赖。

## 包含内容

- 配置与签名：`configuration.py`、`signature.py`
- 传输与响应模型：`transport.py`、`models.py`
- 公共错误与实时能力：`errors.py`、`websocket.py`

## 安装

推荐在 `output/weex-connector-python` 根目录执行：

```bash
pip install -e ./common
```

如果你接下来要使用 Spot 或 Contract Connector，再继续安装对应子包：

```bash
pip install -e ./common
pip install -e ./clients/spot
pip install -e ./clients/contract
```

## 说明

- `common/` 本身不暴露 Spot 或 Contract 业务入口。
- Spot 入口仍由 `weex_spot_sdk` 提供，Contract 入口仍由 `weex_contract_sdk` 提供。
