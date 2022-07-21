# Clonechat

Clone all posts from the history of a Telegram Channel/Group to another Channel/Group.

Secure backup. Saves and protects the posts in the destination chat from possible deletion of posts from the source chat.

>> [Versão em Português](README_ptbr.md)

## Settings
- Run `update_libs.bat` file to update dependencies
- Register your telegram API access credentials in the `credentials.py` file

## USE

### via command line

Command: python clonechat.py --orig={chat_id of source channel/group} --dest=-{chat_id of destination channel/group}

Example: python clonechat.py --orig=-100222222 --dest=-10011111111

### Via menu in terminal

- Run the `exec_clonechat.bat` file
- Enter the chat_id of the originating channel/group
- Confirm with [ENTER]
- Enter the chat_id of the target channel/group
- Confirm with [ENTER]

### Finalization

- Delete the `posted.json` file when done cloning.

Note: If this file is not deleted, the next time you run the script the cloning will continue where it left off.

## FAQ

### How to get the chat_id of a channel or group

There are several ways to get the chat_id of a channel. We will show two of them:
- Using telegram client [Kotatogram](https://kotatogram.github.io/download/):
  - Access the channel description screen
  - Copy the `chat_id` that appears below the channel name
- Using Find_TGIDbot bot:
  - Access the bot window [@Find_TGIDbot](http://t.me/Find_TGIDbot) and launch it
  - Forward any channel post to this bot
  - The bot will reply with the message sender ID. In this case, the channel ID.
- Copy the `chat_id` (including the minus sign). It is worth mentioning that channels start with the number '-100'.

### How to generate telegram API access credentials?

- View this video: https://www.youtube.com/watch?v=8naENmP3rg4