# Free Games Notifier

Get a Telegram message whenever a new free game appears on **Epic Games** or **Steam**.

A small Python script checks both stores every 6 hours using GitHub Actions, so it runs for free and your computer doesn't need to be on.

## How it works

- **Epic Games:** reads Epic's public free games promotions.
- **Steam:** reads the GamerPower giveaways API (Steam has no official free games API).
- **Notifications:** sends a Telegram message for each new game.
- **No duplicates:** `seen.json` remembers games already sent.

## Setup

1. **Fork** this repository (button at the top right).
2. In Telegram, message **@BotFather**, send `/newbot`, and copy the token.
3. Send any message to your new bot, then open
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   and find your chat ID (`"chat":{"id": ...}`).
4. In your fork, go to **Settings → Secrets and variables → Actions** and add two secrets:
   - `TG_TOKEN`: your bot token
   - `TG_CHAT_ID`: your chat ID
5. Go to the **Actions** tab and enable workflows.
6. Select **Free games** and click **Run workflow** to test it.

After that, it runs automatically every 6 hours.

## Run it on your own computer

```
pip install requests
```

Windows (PowerShell):
```
$env:TG_TOKEN="your_token"
$env:TG_CHAT_ID="your_chat_id"
python freegames.py
```

Mac/Linux:
```
TG_TOKEN=your_token TG_CHAT_ID=your_chat_id python freegames.py
```

## Notes

- Never write your bot token in the code. Always use secrets or environment variables.
- Epic's free games usually change on Thursdays.
- Some Steam items are free keys that can run out, so open the link quickly.
- Want another notification method (Discord, email, ntfy)? Only the `notify()` function needs to change.
