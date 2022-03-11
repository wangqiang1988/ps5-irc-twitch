# -*- coding: utf-8 -*-
import asyncio
import random
import blivedm
import socket

def send(bmsg):
# 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
    s.connect(('10.255.1.101', 6667))
    s.send(bmsg.encode('utf-8'))
    s.close()

# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    22509403,
#    2208319,
]


async def main():
    await run_single_client()
    await run_multi_client()


async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = random.choice(TEST_ROOM_IDS)
    # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
    client = blivedm.BLiveClient(room_id, ssl=True)
    handler = MyHandler()
    client.add_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()


async def run_multi_client():
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id) for room_id in TEST_ROOM_IDS]
    handler = MyHandler()
    for client in clients:
        client.add_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))


class MyHandler(blivedm.BaseHandler):
    # # 演示如何添加自定义回调
    # _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    # async def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa

    async def _on_heartbeat(self, client: blivedm.BLiveClient, message: blivedm.HeartbeatMessage):
#        wang = "willwillwang"
        print(f'[{client.room_id}] 当前人气值：{message.popularity}')
#        send(":" + wang +"!" + wang + "@" + wang  + ".tmi.twitch.tv PRIVMSG " + "#willwillwang :" + "hot" + str(message.popularity))
    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        print(f'[{client.room_id}] 弹幕:{message.uname}：{message.msg}')
#        send(f'{message.uname}: {message.msg}')
        send(":" + message.uname +"!" + message.uname + "@" + message.uname + ".tmi.twitch.tv PRIVMSG  " + "#willwillwang :"+ message.msg + "\r\n")
    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')
        send(":" + message.uname +"!" + message.uname + "@" + message.uname + ".tmi.twitch.tv PRIVMSG  " + "#willwillwang :"+ "give " + message.gift_name + "x" + message.num)
    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')
        send(":" + message.uname +"!" + message.uname + "@" + message.uname + ".tmi.twitch.tv PRIVMSG  " + "#willwillwang :"+ "buy" + message.gift_name)
    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
