# discord-resume-filter

Discord bot that catches resume/job-pitch posts in general chat and redirects them to an introductions channel.

## How it works

1. A cheap regex/keyword prefilter runs on every message in watched channels.
2. If the prefilter fires, an LLM classifier (via OpenRouter — default `google/gemini-2.5-flash`) confirms it's a resume/pitch.
3. If confirmed: the original message is deleted, reposted to the intro channel via a webhook using the user's name + avatar (so it looks like they sent it there), and the user is DM'd a friendly "we moved this for you" note.

The two-stage filter means the LLM is only called on messages that already look suspicious, keeping API costs near-zero. Using OpenRouter gives you clean per-request analytics and lets you swap the model with a single env var.

## Setup

### Windows (cmd)

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m bot
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m bot
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m bot
```

Fill in the values in `.env` between `copy` and `python -m bot`.

## Env vars

| Name | Required | Notes |
|------|----------|-------|
| `DISCORD_TOKEN` | yes | Bot token |
| `OPENROUTER_API_KEY` | yes | [openrouter.ai](https://openrouter.ai) key |
| `OPENROUTER_MODEL` | no | Default `google/gemini-2.5-flash`. Any OpenRouter model ID works. |
| `INTRO_CHANNEL_ID` | yes | Channel to repost into |
| `WATCHED_CHANNEL_IDS` | yes | Comma-separated channel IDs to monitor |
| `LOG_CHANNEL_ID` | no | Channel to log moderation actions to |
| `SYNC_GUILD_ID` | no | Guild ID for instant slash-command sync. Leave empty for global sync. |
| `MAX_MOVES_PER_WINDOW` | no | Default `1`. Per-user auto-move quota. |
| `MOVE_WINDOW_SECONDS` | no | Default `300`. Rolling window the quota applies over. |
| `DRY_RUN` | no | `true` to detect but not act |

## Spam protection

If a single user gets a flagged message moved, any further flagged messages from them within `MOVE_WINDOW_SECONDS` are **deleted only** — no repost, no DM. Stops a spambot pasting the same pitch across N watched channels from creating N copies in the intro channel. Manual `/move` and the context menu always bypass the rate limit.

## Manual moderation commands

Mods (`Manage Messages` permission) get two ways to manually move a post:

1. **Right-click the message → Apps → "Move to intro"** — fastest, works on any message
2. **`/move <url-or-id>`** — pass a Discord message URL, or a message ID from the current channel

Both run the same flow as automatic detection: webhook repost (with the user's name + avatar) into the intro channel, original deleted, DM sent.

## Bot permissions

The bot needs: `Read Messages`, `Send Messages`, `Manage Messages`, `Manage Webhooks`, and the `applications.commands` OAuth scope (so slash/context-menu commands appear). Message Content Intent + Server Members Intent must be enabled in the developer portal.

## Tests

```bash
pip install pytest
pytest
```
