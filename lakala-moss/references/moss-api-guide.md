# 拉卡拉MOSS支付API指南

## API概览

- **接口地址**: `https://moss.lakala.com/ord-api/unified/v3`
- **请求方式**: POST
- **Content-Type**: application/json

## 请求结构

### head 字段

| 字段 | 必填 | 说明 |
|------|------|------|
| versionId | 是 | 版本号 "1.0" |
| serviceId | 是 | 服务ID "lfops.moss.order.pay" |
| serviceSn | 是 | 服务流水号（UUID） |
| systemCode | 是 | 系统编码 "MOSS" |
| channelId | 是 | 渠道ID "API" |
| businessChannel | 是 | 业务渠道 "C00000404" |

### request 字段

| 字段 | 必填 | 说明 |
|------|------|------|
| mer_no | 是 | 商户号 "M00002042" |
| order_no | 是 | 商户订单号（唯一） |
| total_amount | 是 | 支付金额（单位：分，字符串） |
| pay_scene | 是 | 支付场景 "0" |
| account_type | 是 | 支付方式 |
| order_eff_time | 是 | 订单有效时间（分钟） |
| subject | 否 | 订单标题 |
| remark | 否 | 交易备注 |
| callback_url | 否 | 回调地址 |

### 支付方式

- `ALIPAY`: 支付宝
- `WECHAT`: 微信支付
- `UQRCODEPAY`: 银联二维码
- 多种方式用逗号分隔：`ALIPAY,WECHAT,UQRCODEPAY`

## 响应格式

### 成功响应
```json
{
  "head": {
    "code": "000000",
    "desc": "成功",
    "serviceSn": "...",
    "serviceTime": "20260413145512"
  },
  "response": {
    "order_no": "TEST001",
    "counter_url": "https://moss.lakala.com/counter/#/r/0000?..."
  }
}
```

### 失败响应
```json
{
  "head": {
    "code": "E10001",
    "desc": "订单号重复"
  }
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 000000 | 成功 |
| E10001 | 订单号重复 |
| E10002 | 参数校验失败 |
| E10003 | 商户不存在 |
| E20001 | 系统异常 |
