#!/usr/bin/env python3
"""
拉卡拉MOSS支付下单脚本
"""

import argparse
import json
import uuid
import sys
import requests


def generate_service_sn():
    """生成服务流水号"""
    return str(uuid.uuid4()).replace('-', '')


def create_order(order_no, total_amount, subject="订单标题测试",
                 remark="交易备注信息测试", callback_url="lakala.com"):
    """
    发起支付下单请求

    Args:
        order_no: 商户订单号（唯一）
        total_amount: 支付金额（单位：分）
        subject: 订单标题
        remark: 交易备注
        callback_url: 回调地址

    Returns:
        dict: 包含支付链接或错误信息
    """
    url = "https://moss.lakala.com/ord-api/unified/v3"

    request_data = {
        "head": {
            "versionId": "1.0",
            "serviceId": "lfops.moss.order.pay",
            "serviceSn": generate_service_sn(),
            "systemCode": "MOSS",
            "channelId": "API",
            "businessChannel": "C00000404"
        },
        "request": {
            "order_no": order_no,
            "total_amount": str(total_amount),
            "mer_no": "M00002042",
            "pay_scene": "0",
            "account_type": "ALIPAY,WECHAT,UQRCODEPAY",
            "order_eff_time": "30",
            "subject": subject,
            "remark": remark,
            "callback_url": callback_url
        }
    }

    try:
        response = requests.post(url, json=request_data, headers={"Content-Type": "application/json"}, timeout=30)

        if response.status_code >= 400:
            return {"success": False, "error": f"HTTP错误: {response.status_code}"}

        response_data = response.json()
        head = response_data.get("head", {})
        resp_code = head.get("code") or head.get("respCode")
        resp_msg = head.get("desc") or head.get("respMsg")

        if resp_code != "000000":
            return {"success": False, "error": f"业务失败: {resp_msg}", "code": resp_code, "desc": resp_msg}

        result = response_data.get("response", {})
        pay_url = result.get("counter_url")

        if not pay_url:
            return {"success": False, "error": "响应中未包含支付链接"}

        return {
            "success": True,
            "pay_url": pay_url,
            "order_no": order_no,
            "total_amount": total_amount,
            "service_sn": head.get("serviceSn"),
            "service_time": head.get("serviceTime")
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="拉卡拉MOSS支付下单")
    parser.add_argument("--order-no", required=True, help="商户订单号（必须唯一）")
    parser.add_argument("--total-amount", required=True, help="支付金额（单位：分）")
    parser.add_argument("--subject", default="订单标题测试")
    parser.add_argument("--remark", default="交易备注信息测试")
    parser.add_argument("--callback-url", default="lakala.com")
    args = parser.parse_args()

    try:
        amount_int = int(args.total_amount)
        if amount_int <= 0:
            print("错误：金额必须大于0", file=sys.stderr)
            sys.exit(1)
    except ValueError:
        print("错误：金额必须是数字", file=sys.stderr)
        sys.exit(1)

    result = create_order(args.order_no, args.total_amount, args.subject, args.remark, args.callback_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
