import datetime

from django.core import serializers
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

from api_manager.models import Message, Stock

REPLIES = {
    "hi": "hello",
    "hello": "hi",
    "when are you available": "Tomorrow at noon"
}
message_data = [
    {
        "message_text": "Hello",
        "sender": "Ramesh",
        "sent_date": "2021/11/19 11:21:32"
    },
]


def create_json_from_request_data(request):
    if "json" in request.headers.get("Content-Type"):
        return json.loads(request.body)
    else:
        return {}


@csrf_exempt
def stock_data(request):
    if request.method == "POST":
        json_data = create_json_from_request_data(request)
        Stock(
            product_name=json_data["name"], product_quantity=json_data["quantity"],
            product_cost_price=json_data["costPrice"], product_sell_price=json_data["sellPrice"],
            profit=json_data["profit"]
        ).save()

    return JsonResponse({
        "stock_data": (json.loads(serializers.serialize("json", Stock.objects.all())))
    })


@csrf_exempt
def messenger_bot(request):
    if request.method == "POST":
        json_data = create_json_from_request_data(request)
        message_data.append(json_data)
        message_text = json_data.get("message_text", "")

        if message_text in REPLIES:
            reply_msg = REPLIES[message_text]
        else:
            reply_msg = "Sorry, I am busy right now. I will call you later."

        message_data.append({
            "sender": "Bot Bahadur",
            "message_text": reply_msg,
            "sent_date": "2021/11/19 11:21:32"
        })

    return JsonResponse({"messages": json.loads(serializers.serialize("json", Message.objects.all()))})
