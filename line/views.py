from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn,TextSendMessage
)

LINE_CHANNEL_ACCESS_TOKEN = 'Li0swYw0GWbk1o7XzBF1KJLJ2/BV9n9nttEbuDsQdQi7AggHSmYL5w3Tsc+IUJ6fLHMa2DMj95oRww0W+DKJiBk978G2btHgqUO8wjs8dtJZJCjQjDks7sAsjK9rujXVvkBPmk77rtHjSLKfbWAi5QdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '18657efd765b4ed4cbb7cc2cfe3612fe'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                line_bot_api.reply_message(
                    event.reply_token,
                   [TextSendMessage(text=event.message.text),TextSendMessage(text=event.message.text)]
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()