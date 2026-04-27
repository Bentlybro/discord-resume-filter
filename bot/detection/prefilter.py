import re

MIN_LENGTH = 200
MIN_SIGNAL_HITS = 2

STRONG_SIGNALS = [
    r"\bi(?:'?m| am) (?:currently |actively )?(?:looking for|seeking) (?:a |an |new |some |any )?(?:job|work|gig|role|position|opportunit)",
    r"\blooking for (?:a |new |any |some )?(?:job|gig)\b",
    r"\bavailable for hire\b",
    r"\bhire me\b",
    r"\bdm (?:me )?if (?:\w+ ){0,2}(?:looking for|seeking|interested in|need)",
    r"\bif you need (?:senior|expert|experienced|help with|someone|a developer|a dev|talent|execution)",
    r"\bmessage me with (?:your|the|a|any) (?:project|scope|details|brief|requirements|idea)",
    r"\bi(?:'?m| am) (?:currently |actively )?(?:open to|available for) (?:new |freelance |remote |contract |full[- ]?time |part[- ]?time )?(?:job|work|gig|role|position|opportunit|hire|client|project)",
]

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
    r"\bover the (?:past|last) (?:\d+\s*year|decade|few year|several year)",
    r"\bi(?:'ve| have) led (?:the |a |our |my )?(?:design|deployment|development|architecture|team|engineering|project|building|delivery)",
    r"\bi built (?:a|an|my|the|our)(?:[\w ]+ )?(?:framework|system|platform|product|tool|pipeline|infrastructure|app|api|bot|library|service)",
    r"\bmy experience (?:includes|spans|covers|is in)",
    r"\bi focus on (?:building|delivering|creating|developing|designing|making)",
    r"\bsenior[- ]level\b",
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
    "gpt", "llama", "claude", "mlops", "etl",
    "postgresql", "postgres", "mongodb", "redis", "mysql",
    "docker", "kubernetes", "aws", "gcp", "azure", "firebase", "supabase",
    "tensorflow", "pytorch",
    "html", "html5", "css", "css3", "sass", "scss",
]


def looks_like_resume(content: str) -> bool:
    text = content.strip()
    lowered = text.lower()
    if _has_strong_signal(lowered):
        return True
    if len(text) < MIN_LENGTH:
        return False
    hits = _count_phrase_hits(lowered, JOB_SEEKING)
    hits += _count_phrase_hits(lowered, SELF_PROMO)
    hits += _count_tech_hits(lowered)
    return hits >= MIN_SIGNAL_HITS


def _has_strong_signal(lowered: str) -> bool:
    return any(re.search(pat, lowered) for pat in STRONG_SIGNALS)


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
