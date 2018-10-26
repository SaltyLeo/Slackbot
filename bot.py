# coding: utf-8
from slackclient import SlackClient
import re
import time

slack_client = SlackClient('你的Token') # 在Slack API页面内获取

# 常量
RTM_READ_DELAY = 1 # 从RTM读取之间延迟1秒
EXANPLE_COMMAND = "我是不是很帅" # 这里就是关键词，bot从Slack RTM 接收信息，并匹配，匹配成功就执行相应的if。
MENTION_REGEX = "(.*)" #这是匹配全部命令的意思，会回复所有从RTM收到的消息。
def parse_bot_commands(slack_events):
    """
        解析来自Slack RTM API的事件列表，以查找bot命令。
        如果找到bot命令，则此函数返回命令和通道的元组。
        如果未找到，则此函数返回None，None。
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = parse_direct_mention(event["text"])
            return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        在消息文本中找到直接提及（在开头提及）
        并返回提到的用户ID。 如果没有直接提及，则返回None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # 第一组包含用户名，第二组包含剩余消息 这里我删除了第二组以获取全部数据。
    return (matches.group(1).strip()) if matches else (None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # 默认回复
    default_response = "啊~  没有找到相应的指令呢 ⊂((・x・))⊃ " 
	
    # 查找并执行给定的命令，填写响应
    response = None
    # 这里是填写更多命令的地方
    if command.startswith(EXANPLE_COMMAND): # 这一块就是命令执行部分。
        response = """是的，是的。"""
    # 将响应发送回通道
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response  or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # 通过调用Web API方法`auth.test`来读取bot的用户ID
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

