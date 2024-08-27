# ps5-irc-twitch
用于ps5接受b站弹幕，前提是ps5使用nginx-rtmp方式进行推流

### 方法1
B站接收弹幕用的是https://github.com/xfgryujk/blivedm (请使用最新blivedm的仓库)

本地运行twitch.py,监听6667端口，用于做消息中转

本地运行此项目中的sample.py，将用户的弹幕消息，通过新增的send方法，将弹幕转发到twitch.py的6667端口，ps5即可推流时收到弹幕

### 方法2
需要有开放平台的access_key,access_key_secret,项目id,具体方式看b站官方开放平台

本地运行twitch.py,监听6667端口，用于做消息中转

本地运行ws.py,可以获取到自己直播间的弹幕消息
