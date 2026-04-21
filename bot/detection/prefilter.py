import re

MIN_LENGTH = 200
MIN_SIGNAL_HITS = 2

JOB_SEEKING = [
    r"\blooking for (?:\w+ ){0,2}(?:dev|developer|engineer|opportunit|work|job|role|gig|remote|position|client|team|collaborat)",
    r"\bopen to (?:\w+ ){0,2}(?:opportunit|work|job|role|project|collaborat|position|hire|gig)",
    r"\bavailable for (?:\w+ ){0,2}(?:work|hire|freelance|projects|opportunit|position|gig|role)",
    r"\bfeel free to (?:reach out|contact|dm|message|connect)",
    r"\breach out (?:to me|if|directly)",
    r"\bcontact me\b",
    r"\bdm me\b",
    r"\bhire me\b",
    r"\bmessage me\b",
    r"\blet'?s (?:talk|connect|chat)\b",
    r"\bif you'?re (?:looking|building|hiring|interested)",
    r"\bwriting (?:opportunit|position|role|gig|work)",
]

SELF_PROMO = [
    r"\bi(?:'m| am) an? (?:senior |junior |lead |principal |full[- ]stack |experienced |professional |freelance )?(?:software |web |ai |ml |backend |frontend |mobile |content |technical )?(?:developer|engineer|programmer|coder|designer|writer|consultant|freelancer|marketer|editor|creator|specialist|architect)",
    r"\bi(?:'ve been|'?ve been| have been) (?:writing|coding|developing|working|building|designing|consulting|engineering)(?:\s+\w+){0,5}\s+for (?:a couple of |several |many |over )?(?:year|\d)",
    r"\bresume\s*[-:—]",
    r"\bportfolio\s*[-:—]",
    r"\bcheck out my (?:blog|work|portfolio|github|latest|recent)",
    r"\bmy (?:tech |primary )?stack\b",
    r"\b(?:years?|yrs) of experience\b",
    r"\brich experience\b",
    r"\bhave experience (?:in|with|developing|building)",
    r"\bspecializ(?:e|ing|ed) in\b",
    r"\bexpertise in\b",
    r"\bi can (?:build|develop|create|help|deliver|fit in|write|design|handle)",
    r"\bi (?:help|work with) (?:founders|startups|businesses|teams|clients)",
    r"\bi(?:'ve| have) (?:built|developed|worked on|spent|written)",
    r"\bmost of my work\b",
    r"\bend[- ]to[- ]end\b",
    r"\bproduction[- ]ready\b",
    r"\bfit in (?:well|any) (?:in )?(?:position|role|team)",
]

TECH_NAMES = [
    "react", "next.js", "nextjs", "vue", "angular", "svelte",
    "node.js", "nodejs", "express", "python", "typescript", "javascript",
    "rust", "golang", "go", "java", "c#", "c++", "ruby", "php",
    "flutter", "react native", "swift", "kotlin",
    "django", "fastapi", "flask", "tailwind",
    "langchain", "openai", "anthropic", "gemini", "llm", "rag",
    "postgresql", "postgres", "mongodb", "redis", "mysql",
    "docker", "kubernetes", "aws", "gcp", "azure", "firebase",
    "tensorflow", "pytorch",
    "html", "html5", "css", "css3", "sass", "scss",
]


def looks_like_resume(content: str) -> bool:
    text = content.strip()
    if len(text) < MIN_LENGTH:
        return False
    lowered = text.lower()
    hits = _count_phrase_hits(lowered, JOB_SEEKING)
    hits += _count_phrase_hits(lowered, SELF_PROMO)
    hits += _count_tech_hits(lowered)
    return hits >= MIN_SIGNAL_HITS


def _count_phrase_hits(lowered: str, patterns: list[str]) -> int:
    return sum(1 for pat in patterns if re.search(pat, lowered))


def _count_tech_hits(lowered: str) -> int:
    matches = sum(1 for name in TECH_NAMES if _contains_word(lowered, name))
    if matches >= 4:
        return 2
    if matches >= 2:
        return 1
    return 0


def _contains_word(haystack: str, needle: str) -> bool:
    escaped = re.escape(needle)
    return re.search(rf"(?<![\w.]){escaped}(?![\w])", haystack) is not None
