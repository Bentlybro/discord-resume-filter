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
| `DRY_RUN` | no | `true` to detect but not act |

## Bot permissions

The bot needs: `Read Messages`, `Send Messages`, `Manage Messages` (to delete), `Manage Webhooks`. Message Content Intent must be enabled in the developer portal.

## Tests

```bash
pip install pytest
pytest
```
