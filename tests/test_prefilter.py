from bot.detection.prefilter import looks_like_resume


def test_short_message_rejected():
    assert not looks_like_resume("hi")


def test_casual_question_rejected():
    msg = (
        "Does anyone know how to fix the autogpt api timeout? I've been "
        "trying for hours and can't figure out what's wrong with my setup. "
        "Getting connection errors every time I try to run a workflow."
    )
    assert not looks_like_resume(msg)


def test_project_share_rejected():
    msg = (
        "AutoGPT made this entire multiplayer game for me — I can't believe "
        "what it's capable of now. You've all worked so hard and produced "
        "such an incredible piece of software. Really impressive stuff, "
        "keep it up team!"
    )
    assert not looks_like_resume(msg)


def test_senior_dev_pitch_detected():
    msg = (
        "is there anyone looking for devs here? i am an senior full stack AI "
        "developer and have rich experience in LLM/SaaS projects i can build "
        "chatbots, AI agents, automation workflows, image and video generation "
        "tools, mobile and desktop apps, Computer Vision, AR/VR, API integrations "
        "and custom AI tools using OpenAI, LangChain, Python, JS and so on. "
        "please feel free to reach out to me if you are looking for a developer "
        "now. Thanks"
    )
    assert looks_like_resume(msg)


def test_remote_opportunity_pitch_detected():
    msg = (
        "Hey everyone — I'm currently open to remote opportunities and wanted "
        "to introduce myself here. I'm an AI systems / backend engineer with "
        "experience building production-ready LLM products, backend "
        "infrastructure, and scalable automation systems. Most of my work has "
        "been focused on practical AI use cases like AI customer support systems, "
        "booking/workflow agents, RAG pipelines, API integrations, backend "
        "systems built for scale. I've worked with Python, FastAPI, TypeScript, "
        "PostgreSQL, Redis, OpenAI / Anthropic APIs, Docker, and distributed "
        "systems. If anyone here is building something interesting and needs "
        "someone technical who can execute fast, feel free to message me."
    )
    assert looks_like_resume(msg)


def test_full_stack_engineer_pitch_detected():
    msg = (
        "Hey everyone, I'm a full-stack AI/ML engineer specializing in building "
        "intelligent, production-ready digital products from the ground up. I "
        "help founders, startups, and businesses transform ideas into scalable "
        "applications, combining strong software engineering with modern AI "
        "capabilities. My work covers the full product stack, from frontend "
        "and backend development to AI integration, automation, data pipelines, "
        "and deployment. I work with a broad modern stack, including React, "
        "Next.js, Node.js, Python, FastAPI, Django, PostgreSQL, MongoDB, Redis, "
        "Docker, Kubernetes, AWS, and Firebase. If you're working on an idea "
        "and want a developer who understands both AI and full-stack product "
        "development end to end, feel free to contact me."
    )
    assert looks_like_resume(msg)


def test_writer_pitch_detected():
    msg = (
        "Hi everyone! I thought to put this up here that I'm a writer and "
        "I am currently open to writing opportunities and positions. I've "
        "been writing for a couple of years, and you can check out my "
        "latest pieces on my new blog:\n\n"
        "Blog - https://example.com/\n"
        "Resume - https://example.com/resume\n\n"
        "I'm also a very IT-inclined person owing to years of using the "
        "computer, so I can fit in well in any position that needs good "
        "writing skills with a background in IT."
    )
    assert looks_like_resume(msg)


def test_short_looking_for_dev_rejected():
    assert not looks_like_resume("is there anyone looking for a dev?")


def test_general_discussion_rejected():
    msg = (
        "Would a hybrid system using Tesseract + a vision encoder (e.g., CLIP, "
        "BLIP, LLaVA, or similar VLMs) be more appropriate for lore extraction "
        "and worldbuilding asset indexing? I've been experimenting with a few "
        "pipelines and wanted to get other people's thoughts before committing."
    )
    assert not looks_like_resume(msg)


def test_product_feedback_rejected():
    msg = (
        "Apologies if this is the wrong place to say this, but small piece of "
        "feedback on the beta signup process: I'm the sort of person who would "
        "enjoy playing around with the cloud-hosted version, and would share "
        "any useful feedback I had, so was willing to enter my email address; "
        "but I'm not willing to waste time filling out a form telling you "
        "about my business needs as requested in the email you sent."
    )
    assert not looks_like_resume(msg)
