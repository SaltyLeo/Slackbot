# coding: utf-8
#!/usr/bin/python3
import os
import time
import re
from slackclient import SlackClient
import urllib.request
import requests

slack_client = SlackClient('你的Slack-Token')

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "(.*)"
def parse_bot_commands(slack_events):

    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = parse_direct_mention(event["text"])
            return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):

    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1).strip()) if matches else ( None)

def handle_command(command, channel):

    headers = {'content-type': 'application/json'} 
    com1 = command.replace('[', '') #将收到的消息转到给茉莉机器人api
    response = requests.post("""http://i.itpk.cn/api.php?question="""+com1+"""&api_key=你的Api Key&api_secret=你的Api Secret""", headers=headers)
    default_response = response.text #用茉莉机器人返回的数据作为默认回复。
	
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text= response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

