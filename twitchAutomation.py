from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.object.eventsub import ChannelChatMessageEvent, ChannelSubscribeEvent, ChannelSubscriptionMessageEvent, ChannelCheerEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import os
import atexit
import requests


APP_ID = os.environ["TWITCH_APP_ID"]
APP_SECRET = os.environ["TWITCH_APP_SECRET"]
TARGET_SCOPES = [AuthScope.CHAT_READ, AuthScope.USER_READ_CHAT, AuthScope.BITS_READ, AuthScope.CHANNEL_READ_SUBSCRIPTIONS]
TARGET_CHANNEL = "feviknight"

AUTOMATIC_UPDATE_URL = f"http://localhost:{5050}/api/v1/manual"

CONVERSIONS = {
    "1000": "TwitchT1",
    "2000": "TwitchT2",
    "3000": "TwitchT3",
}


async def onReady(ready_event: EventData):
    print('Bot is ready for work, joining channels', TARGET_CHANNEL)
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


async def onSub(sub: ChatSub):
    print(f'??? just subscribed to {sub.room.name} with {sub.sub_plan}')
    requests.get(f"{AUTOMATIC_UPDATE_URL}?type={CONVERSIONS[sub.sub_plan]}&quantity={1}")


async def onChat(data: ChannelChatMessageEvent):
    print(f'{data.event.chatter_user_name} said: {data.event.message.text}')


async def onSubscribe(data: ChannelSubscribeEvent):
    print(f'{data.event.user_name} just subscribed to {data.event.broadcaster_user_name} with {data.event.tier} and {data.event.is_gift} (isGift)')
    requests.get(f"{AUTOMATIC_UPDATE_URL}?type={CONVERSIONS[data.event.tier]}&quantity={1}")


async def onSubscribeMessage(data: ChannelSubscriptionMessageEvent):
    print(f'{data.event.user_name} just resubscribed to {data.event.broadcaster_user_name} with {data.event.tier}')
    requests.get(f"{AUTOMATIC_UPDATE_URL}?type={CONVERSIONS[data.event.tier]}&quantity={1}")


async def onCheer(data: ChannelCheerEvent):
    print(f'{data.event.user_name} just cheered {data.event.bits} bits to {data.event.broadcaster_user_name}')
    requests.get(f"{AUTOMATIC_UPDATE_URL}?type=TwitchBits&quantity={data.event.bits}")


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, TARGET_SCOPES, force_verify=False)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, TARGET_SCOPES, refresh_token)

    targetUser = await first(twitch.get_users(logins=[TARGET_CHANNEL]))
    print(f"{targetUser.id=}")

    # create chat instance
    chat = await Chat(twitch)

    chat.register_event(ChatEvent.READY, onReady)
    chat.register_event(ChatEvent.SUB, onSub)

    chat.start()

    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()

    # try:
    #     await eventsub.listen_channel_subscribe(targetUser.id, onSubscribe)
    # except Exception as e:
    #     print("INSUFFICIENT PERMISSIONS for `listen_channel_subscribe`")
    #     print(f" - {e}")
    #
    # try:
    #     await eventsub.listen_channel_subscription_message(targetUser.id, onSubscribeMessage)
    # except Exception as e:
    #     print("INSUFFICIENT PERMISSIONS for `listen_channel_subscription_message`")
    #     print(f" - {e}")

    try:
        await eventsub.listen_channel_cheer(targetUser.id, onCheer)
    except Exception as e:
        print("INSUFFICIENT PERMISSIONS for `listen_channel_cheer`")
        print(f" - {e}")

    async def shutdown():
        chat.stop()
        await eventsub.stop()
        await twitch.close()

    atexit.register(shutdown)


if __name__ == "__main__":
    asyncio.run(run())