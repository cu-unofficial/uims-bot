# uims-bot

- A telegram bot for getting push notifications for announcements from https://cuims.in/
  on your smart phone.

- I can't say if this bot works or not at the moment since their website hardly opens
  as long as you are not on their local network. I haven't been able to test it lately.

## Changes in uims_bot.py for installation

- Change in browser.addheaders ```browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]```
- **Steps to find out user-agent of your system**

    (1) Open chrome browser.
    
    (2) search chrome://version in URL bar.
    
    (3) Copy user-agent and paste in script.
    
    for example: If your user-agent is abc. Then paste this abc like this
    
    ```browser.addheaders = [("User-agent","abc")]```
    
**NOTE- If you are using any other browser find the user-agent and paste it in the script**

## Installation and Usage

```
git clone https://github.com/ritiek/uims-bot
cd uims-bot
pip install -r requirements.txt
```

Create and add the bot to a channel and specify its token and channel name in the source
([here](https://github.com/ritiek/uims-bot/blob/0d16ff6505764650a24bd5557c7cd659b2073ce4/uims_bot.py#L9-L13)).

Start the bot using
```
python uims_bot.py
```

## Contributing

- Got any ideas? Open an issue or look for existing ones.

- Make a PR and remember, before pushing your code to GitHub, **make sure your
  credentials are not present!**

## License

`The MIT License`
