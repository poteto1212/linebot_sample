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
                notes = [CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle02.jpg",
                            title="【ReleaseNote】トークルームを実装しました。",
                            text="creation(創作中・考え中の何かしらのモノ・コト)に関して、意見を聞けるようにトークルーム機能を追加しました。",
                            actions=[{"type": "message","label": "サイトURL","text": "https://renttle.jp/notes/kota/7"}]),

             CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle03.jpg",
                            title="ReleaseNote】創作中の活動を報告する機能を追加しました。",
                            text="創作中や考え中の時点の活動を共有できる機能を追加しました。",
                            actions=[
                                {"type": "message", "label": "サイトURL", "text": "https://renttle.jp/notes/kota/6"}]),

             CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle04.jpg",
                            title="【ReleaseNote】タグ機能を追加しました。",
                            text="「イベントを作成」「記事を投稿」「本を登録」にタグ機能を追加しました。",
                            actions=[
                                {"type": "message", "label": "サイトURL", "text": "https://renttle.jp/notes/kota/5"}])]

                messages = TemplateSendMessage(
                    alt_text='template',
                    template=CarouselTemplate(columns=notes),
                )
                if event.message.text== "おはよう":
                    replymessage="いい天気だね"
                elif event.message.text=="こんにちは":
                    replymessage="正午の鐘が鳴る"
                
                else:
                    replymessage=event.message.text

                line_bot_api.reply_message(
                    event.reply_token,
                   [TextSendMessage(text=event.message.text)
                   ,TextSendMessage(text=replymessage),
                   messages]
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()