from google import genai
from google.genai import types

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


class GeminiClassifier:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self._client = genai.Client(api_key=api_key)
        self._model = model

    async def is_resume(self, content: str) -> bool:
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=PROMPT.format(content=content),
            config=types.GenerateContentConfig(
                max_output_tokens=5,
                temperature=0.0,
            ),
        )
        text = (response.text or "").strip().upper()
        return text.startswith("YES")
