import discord
import openai
import re

# 设置 Discord API 密钥和 ChatGPT API 密钥
discord_token = 'YOUR_DISCORD_BOT_TOKEN_HERE'
openai.api_key = 'YOUR_OPENAI_API_KEY_HERE'

intents = discord.Intents.default()
intents.message_content = True

# 创建一个 Discord 客户端
client = discord.Client(intents=intents)


async def get_all_messages(thread):
    msgs = []
    async for msg in thread.history(limit=None):
        msgs.append(msg)
    return msgs

# 当机器人已经启动时运行
@client.event
async def on_ready():
    print('Bot is ready.')

# 当机器人收到新消息时运行
@client.event
async def on_message(message):
    print(message.content)

    if message.author.name == 'Etymology':
      return

    msgs = []
    msgs.append({
      'role': 'user',
      'content': message.content + '的含义的演变史是什么，请用中文回答'
    })


    # 使用 ChatGPT 生成词源
    response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=msgs
    )
    content = response.choices[0].message.content.strip()
    content = f"**{message.content}**\n{content}"

    print(content)
    # 发送总结到 Thread 频道
    await message.channel.send(content=content)

# 运行机器人
client.run(discord_token)
