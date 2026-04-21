from openai import AsyncOpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
HTTP_REFERER = "https://github.com/Bentlybro/discord-resume-filter"
APP_TITLE = "discord-resume-filter"

PROMPT = """You are a moderator for a Discord server's general chat. Your job is to detect messages that are self-introductions, resumes, portfolios, or job-seeking pitches — content that belongs in an #introduce-yourself channel instead of general chat.

Flag as YES if the message is:
- A developer/engineer/writer introducing themselves and offering services
- A job-seeking pitch listing skills, stacks, or years of experience
- A "looking for opportunities" / "available for hire" style post
- A portfolio/resume drop with contact info

Flag as NO if the message is:
- A technical question or discussion
- A casual greeting ("hi", "hello")
- A project update or product question
- Feedback or bug reports
- General conversation between community members

Respond with exactly one word: YES or NO.

Message:
---
{content}
---
"""


class OpenRouterClassifier:
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": HTTP_REFERER,
                "X-Title": APP_TITLE,
            },
        )
        self._model = model

    async def is_resume(self, content: str) -> bool:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": PROMPT.format(content=content)}],
            max_tokens=5,
            temperature=0.0,
        )
        text = (response.choices[0].message.content or "").strip().upper()
        return text.startswith("YES")
