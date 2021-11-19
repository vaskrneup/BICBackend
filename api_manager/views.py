import datetime

from django.core import serializers
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

from api_manager.models import Message, Stock

REPLIES = {
    "hi": "hello",
    "when are you available": "Tomorrow at noon"
}


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
        message_text = json_data.get("message_text", "")
        Message(
            sender=json_data.get("sender"), sent_date=json_data.get("sent_date"),
            message_text=message_text
        ).save()
        if message_text.startswith("#help"):
            if message_text := message_text.replace("#help", "").strip():
                if message_text in REPLIES:
                    Message(
                        sender=json_data.get("sender"), sent_date=json_data.get("sent_date"),
                        message_text=message_text
                    ).save()
                    reply_msg = REPLIES[message_text]
                else:
                    Message(
                        sender="Bot Bahadur", sent_date=datetime.datetime.now,
                        message_text=REPLIES[message_text]
                    ).save()
                    reply_msg = "Sorry, I am busy right now. I will call you later."

                Message(
                    sender="Bot Bahadur", sent_date=datetime.datetime.now,
                    message_text=reply_msg
                ).save()

    return JsonResponse({"messages": json.loads(serializers.serialize("json", Message.objects.all()))})
