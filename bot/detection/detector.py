from bot.detection.classifier import GeminiClassifier
from bot.detection.prefilter import looks_like_resume


class ResumeDetector:
    def __init__(self, classifier: GeminiClassifier):
        self._classifier = classifier

    async def is_resume(self, content: str) -> bool:
        if not looks_like_resume(content):
            return False
        return await self._classifier.is_resume(content)
