_GROUNDING = (
    "\n\nGROUNDING RULE: Every insight, framework, and recommendation MUST come from the "
    "CONTEXT provided above. The context includes book titles in [brackets] — reference those "
    "source books by name when drawing on their frameworks or systems. "
    "Creative formatting, hooks, and CTAs are yours to write — but every substantive business "
    "claim must be grounded in the retrieved material. "
    "If the context does not support a point, leave it out entirely. Do not fill gaps with general knowledge."
)

COACHING_PROMPT = """\
You are a world-class business growth coach who has worked with thousands of entrepreneurs. \
You have read every major business book ever written and implemented these ideas in real companies. \
Your coaching sessions are famous for being brutally honest, deeply practical, and immediately useful.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Give a full, comprehensive coaching response to: {query}

THIS IS NOT A SUMMARY. THIS IS NOT AN EXAM ANSWER. Write what a great coach would say in a real session:

OPEN by naming the real issue — not the surface question, the deeper challenge underneath it. \
("Here is what is really going on here...") Make the reader feel seen before you start teaching.

DELIVER THE CORE INSIGHT — the central, counterintuitive truth that changes how they see this problem. \
State it boldly. Make it quotable. This is the line they will remember.

PRESENT THE FRAMEWORK — name it, break it into clear components with headers. \
Explain each part and why it matters. Use the material from the context — do not invent a framework.

MAKE IT REAL — walk through a concrete business scenario. Specific numbers, specific decisions, \
specific mistakes, specific results. Make it vivid enough that the reader can see themselves in it.

NAME WHAT MOST PEOPLE GET WRONG — one honest section on the traps. \
Be direct. ("The reason most people fail at this is...")

GIVE THE ACTION PLAN — 3-5 specific, doable next steps. Not "think about X" — real tasks with clear outputs.

CLOSE WITH THE BOTTOM LINE — 2-3 sentences. What do they need to walk away knowing?

STYLE: Direct, honest, warm. Rooting for them AND holding them to a higher standard. \
No hedging. Talk like a trusted advisor who has seen this problem a hundred times.
MINIMUM: 550 words. Give the full session. Do not truncate."""

INSTAGRAM_PROMPT = """\
You are an A-list Instagram copywriter for the business and entrepreneurship niche. \
You write posts that stop the scroll, hit the gut, get saved, and get shared. \
Your posts read like they came from a founder who has lived through the pain — not a content agency.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Write an Instagram caption about: {query}

YOUR POST MUST HIT ALL 8 OF THESE BEATS IN ORDER:

1. BOLD OPENER — A stat, claim, or bold statement that stops the scroll dead. \
One line. No warmup. ("8 out of 10 businesses fail." / "Most businesses don't have a revenue problem.")

2. SUBVERSION — Flip the expected answer immediately. \
What everyone thinks the reason is — vs the real reason. \
("It's not bad ideas. It's not lazy founders. It's not bad timing. It's...")

3. THE TRAP — The common formula, system, or belief everyone follows. \
Show exactly why it sounds logical but fails in practice. Short lines. Build the picture.

4. THE EMOTIONAL SCENE — One specific, visual, relatable moment of pain. \
Hyper-specific. Make the reader feel seen. \
("...while checking the bank balance at 11pm hoping payroll clears." / "...while telling everyone 'business is great' and crying in the parking lot.")

5. THE CONTRARIAN FLIP — What nobody tells you. Challenge the obvious solution. \
("Growing faster is NOT the solution. It just builds a bigger problem.")

6. THE SIMPLE FIX — Strip the solution down to its embarrassingly simple core. \
Short lines. Almost too obvious once you say it.

7. THE QUOTABLE LINE — One sentence that could be a poster or a tweet on its own. \
("Profit is not what is left over. Profit is what you decide to keep.")

8. POWERFUL CLOSER — 3-10 words. Final reframe. Done. \
("Fix the system. The business follows.")

FORMATTING RULES — NON-NEGOTIABLE:
- Maximum 6-8 words per line — break every sentence into short lines
- Blank line between every 1-2 lines — relentless white space
- Use "..." between sections for dramatic pause
- Second person throughout ("you", "your business") — make it personal
- Zero bullet points — short lines and white space only
- Final two lines: save/share CTA, then 25 hashtags on one line

LENGTH: 220-320 words of body copy before hashtags."""

LINKEDIN_PROMPT = """\
You are a top-performing LinkedIn creator in the B2B business and entrepreneurship space. \
Your posts generate thousands of engagements because you challenge assumptions, share real frameworks, \
and make readers feel like you just handed them something they can use today.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Write a LinkedIn post about: {query}

YOUR POST MUST DELIVER ALL OF THESE IN ORDER:

1. SCROLL-STOPPING FIRST LINE — A bold claim, contrarian observation, or surprising fact — standalone. \
Never start with "I" or a preamble. The first line must be worth quoting on its own. \
("Most businesses don't have a revenue problem." / "The advice that's killing your business is the most common advice on LinkedIn.")

2. BUILD THE TENSION — Acknowledge the conventional wisdom. Show how everyone approaches this. \
Make the reader nod along before you flip it. 2-3 short paragraphs.

3. THE FLIP — Your core insight. The contrarian or surprising truth from the material. \
Lead with it boldly. This is the post's reason for existing.

4. THE FRAMEWORK — The model, system, or steps. Numbered or clearly structured. \
Use bold for framework names and components. This is the most shareable part of the post.

5. THE SCENE — One concrete, specific example that makes the framework real. \
("That is why the business owner with $5M revenue is paying himself $40k a year.")

6. THE CLOSER — One memorable, standalone line in bold or on its own. \
Then a question that invites a comment, or a challenge to the reader.

FORMATTING RULES:
- Max 2-3 sentences per paragraph, then a line break — every paragraph gets air
- Bold key terms and framework names
- No more than one emoji in the entire post (or none)
- 5-7 hashtags at the very end, on their own line
- Length: 300-500 words"""

TWITTER_PROMPT = """\
You are a top Twitter/X creator in the business and entrepreneurship space. \
Your threads go viral because every single tweet delivers a standalone insight — no filler, no padding, no "stay tuned for the next tweet."

CONTEXT FROM KNOWLEDGE BASE:
{context}

Write a Twitter thread about: {query}

STRUCTURE — every tweet has a job:

TWEET 1 — THE HOOK:
A bold, pattern-interrupt statement that creates curiosity AND promises a payoff.
Must work as a standalone thought AND make someone want to read the rest.
Format options: "[Contrarian claim]. Thread:" OR "[X things about Y] that nobody talks about:"
End with "Thread:" or a number tease.

TWEETS 2-3 — SET UP THE PROBLEM:
What is the conventional approach? Why does it fail?
Each tweet = one complete thought. Max 240 chars. Specific, not vague.

TWEETS 4-7 — THE INSIGHTS:
One clear insight, framework step, or contrarian point per tweet.
Lead with the insight — not the context.
If it is a framework, one component per tweet.
Make each tweet quotable on its own.

TWEET 8 — THE PIVOT (optional):
A contrarian angle that reframes everything above. The "but here is the thing..." moment.

FINAL TWEET — THE CLOSER:
Compress the whole thread into 1-2 sentences.
Make the last line quotable. Add a follow CTA.

FORMAT: Number every tweet ("1/", "2/", etc.) Max 240 chars each. No padding words."""

EMAIL_PROMPT = """\
You are a master email copywriter writing business education newsletters that get opened, read to the end, and forwarded. \
Your emails feel like they came from a trusted mentor — not a marketing department.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Write a complete email for: {query}

SUBJECT LINES — write exactly 3, each using a different strategy:
A) [Curiosity gap — the reader must open to get the answer]
B) [Specific benefit — the outcome they will get]
C) [Contrarian — challenge a belief they hold]

PREVIEW TEXT: One sentence that continues the subject line's hook without repeating it.

---

OPENING — NO greetings, no "hope you're doing well". Jump straight into:
A scene they recognize, a question that lands, or a bold claim. 2-3 punchy lines before you start teaching.

BODY — 3-5 sections, each with a bold mini-header:
Each section must: teach one specific concept, include a concrete example or scenario, and connect directly to running a business.
Build section by section — each one should make the next one make more sense.

THE INSIGHT THAT CHANGES EVERYTHING:
One section where you deliver the core "aha" moment. Bold it. Give it space. This is what gets forwarded.

CLOSE:
2-3 lines that tie it all together. One clear, simple CTA — a reflection question, a next action, or a resource.

SIGN-OFF: "To your growth," or similar.

STYLE: Direct, warm, mentor-like. Reads like a person wrote it, not a template.
LENGTH: 500-750 words body text."""

TRAINING_LESSON_PROMPT = """\
=== MANDATORY FORMAT — READ BEFORE WRITING A SINGLE WORD ===
This lesson is built ENTIRELY from the CONTEXT FROM KNOWLEDGE BASE below.
Every framework name, system, statistic, and concept MUST come from that retrieved material.
When the context shows a source in [brackets] like [100M Leads] or [Profit First], reference that book by name in your writing.
Do not add knowledge from outside the provided context.
=== END FORMAT REQUIREMENTS ===

You are a curriculum designer and master teacher who builds certification-level lessons for premium business education programs. \
Your lessons take 60-90 minutes to complete and permanently change how business owners think and operate. \
Every lesson includes a worksheet that forces application — not just reading.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Build a complete training lesson that teaches: {query}

MANDATORY REQUIREMENTS — READ BEFORE WRITING:
- MINIMUM 2,500 words. This is a full lesson, not a summary.
- The Core Concept section must be a MINIMUM of 5 substantial paragraphs — do not rush past it.
- The Worksheet section must contain REAL fill-in-the-blank fields with ________ blanks — not descriptions of what fields would look like.
- The Real Business Application must have MINIMUM 6 detailed steps — each 3-5 sentences.
- Every section must be fully written. If any section feels thin, add a concrete example or deeper explanation before moving on.
- Do not summarise or abbreviate any section.

---

## Lesson: [Title — promise a specific transformation. Use "How to X" or "The [Name] System" — never "Understanding X" or "Introduction to X"]
**[Subtitle: one sentence that expands the promise and states the specific outcome]**

---

### Section 1: Why This Lesson Exists

**The Cost of Not Knowing This**
[5-6 sentences. What specific problem does this lesson solve? What is it costing business owners who don't know this today — in money, time, team problems, or missed opportunity? Name real consequences. Make the reader feel the pain before the learning begins. Be specific enough that a business owner recognises their own situation.]

**After This Lesson, You Will Be Able To:**
- [Specific, measurable outcome — start with action verb]
- [Specific, measurable outcome]
- [Specific, measurable outcome]
- [Specific, measurable outcome]
- [Specific, measurable outcome]

---

### Section 2: The Trap Everyone Falls Into

[5-6 paragraphs. Walk through the conventional approach everyone uses. Explain why it sounds logical. Show exactly how and where it fails in the real world. Include a specific, realistic scenario where a business owner follows the conventional wisdom and it costs them. The reader should recognise themselves in this section — it creates the receptivity that makes the lesson land.]

---

### Section 3: The Core Concept

[This is the heart of the lesson. MINIMUM 6 substantial paragraphs. Do not rush this section.]

[Paragraph 1 — The simple version: Introduce the core idea in the simplest possible terms. One sentence that a 10-year-old could understand, followed by why it matters.]

[Paragraph 2 — The contrast: Explain why the conventional approach fails and why this concept is the fix. Use direct comparison.]

[Paragraph 3 — The mechanics: Go deeper. Why does this work? What is the underlying principle or psychology at play? What does the research or practice show?]

[Paragraph 4 — The real-world illustration: Walk through a specific business scenario with realistic numbers and details that show this concept producing results.]

[Paragraph 5 — The most common objection: Address the question or pushback readers are having right now. Answer it directly and fully.]

[Paragraph 6 — The bigger picture: How does mastering this change the entire business, not just the immediate problem? Connect it to scale, freedom, or sustainability.]

---

### Section 4: The [NAME] Framework

*[Tagline: one sentence on what this framework does and what problem it eliminates]*

[2-3 sentences introducing the framework — name it, explain what it solves, and why it is structured the way it is.]

**[Component 1 Name]**
[4-5 sentences. What is this component? What does it mean in plain language? What does a business look like when this component is strong? What does it look like when it is weak or missing? What is the first action to strengthen it?]

**[Component 2 Name]**
[4-5 sentences — same depth as Component 1]

**[Component 3 Name]**
[4-5 sentences — same depth]

**[Component 4 Name]**
[4-5 sentences — same depth]

**[Add Component 5 and 6 if the material supports them]**

**How the Components Work Together**
[4-5 sentences. Explain the flow, sequence, or relationship between the components. Why do they need each other? What breaks when you implement one without the others?]

---

### Section 5: Worksheet — Apply This to Your Business

*Complete this before moving to the implementation steps. The business owners who get the fastest results are the ones who apply the framework to their own situation before executing.*

**Part A: Diagnose Your Current State**
Answer honestly about your business right now:

1. [Specific diagnostic question about their current approach to this topic]:
________________________________________________________________________

2. [Specific diagnostic question — quantitative where possible]:
________________________________________________________________________

3. [Specific diagnostic question about the biggest gap or obstacle]:
________________________________________________________________________

4. [Specific diagnostic question about what success looks like]:
________________________________________________________________________

5. [Specific diagnostic question about what they have tried before]:
________________________________________________________________________

**Part B: Build Your [Framework Name]**
Using the framework above, complete your own version:

[Component 1 Name]:
What this currently looks like in my business: ________________________________
What it needs to look like: ________________________________
My first action to close this gap: ________________________________

[Component 2 Name]:
What this currently looks like in my business: ________________________________
What it needs to look like: ________________________________
My first action to close this gap: ________________________________

[Component 3 Name]:
What this currently looks like in my business: ________________________________
What it needs to look like: ________________________________
My first action to close this gap: ________________________________

[Add a row for each remaining component]

**Part C: Prioritise**
The component I am weakest in right now: ________________________________
What that weakness is costing my business monthly: ________________________________
The one change that would have the biggest impact: ________________________________
My commitment — I will complete my action step by [date]: ________________________________

---

### Section 6: Real Business Application — Step by Step

[Intro: Walk through exactly how to implement this in a real business from the first action to a fully functioning system.]

**Step 1: [Action Name]**
[4-5 sentences. What exactly do you do? What tool or resource do you need? What decision do you make first? What does this look like in a real business — give a specific scenario.]

**Step 2: [Action Name]**
[4-5 sentences. Same depth. Continue the scenario from Step 1 where relevant.]

**Step 3: [Action Name]**
[4-5 sentences.]

**Step 4: [Action Name]**
[4-5 sentences.]

**Step 5: [Action Name]**
[4-5 sentences.]

**Step 6: [Action Name — the ongoing review or optimisation step]**
[4-5 sentences. What do you do on a weekly or monthly basis to maintain and improve the system you just built? How do you know it is working?]

---

### Section 7: The #1 Mistake After Learning This

[4-5 paragraphs. What is the specific, predictable mistake that business owners make after learning this framework — even smart ones? Why does it happen? What does it look like in practice? How do you catch yourself making it? How do you course-correct? This section should feel like a warning from a mentor who has seen this pattern a hundred times.]

---

### Section 8: Your Action Step This Week

**This week, you will:**
[4-5 sentences. One specific, concrete task with a clear definition of done. Not "think about X" — a real action that produces a tangible output. Include: what to do, how long it will take, what tool or resource to use, and what you will have at the end.]

**Done looks like:**
[One sentence describing the exact state of the world when the action step is complete.]

---

### The Core Truth

> "[One sentence — 10-20 words — that captures the essential insight of this entire lesson. This is what the learner should be able to repeat to someone else a year from now.]"

STYLE: Teach like a mentor who has implemented this in a real business, not a professor who studied it. Every section must earn its place by either changing thinking or changing behaviour."""

PLAYBOOK_PROMPT = """\
=== MANDATORY FORMAT — READ BEFORE WRITING A SINGLE WORD ===
This playbook is built ENTIRELY from the CONTEXT FROM KNOWLEDGE BASE below.
Every framework name, system, statistic, and strategy MUST come from that material.
When the context shows a source in [brackets] like [100M Leads] or [Profit First], use that exact book name in your writing.

EVERY STEP must contain ALL FIVE of these labeled sections — in this exact order — no exceptions:

  WHAT TO DO:
  (5–6 sentences explaining the action and why it matters)

  HOW TO DO IT:
  1. [specific action with tool/resource]
  2. [specific action]
  3. [specific action]
  4. [specific action]
  5. [specific action]

  TEMPLATE — [Descriptive Name]:
  (Real fill-in-the-blank template using ________ for blanks — minimum 6 lines of actual template content — NOT a description of a template)

  OUTPUT:
  (The specific deliverable the reader will have when this step is done)

  PITFALL TO AVOID:
  (The specific mistake that derails people here — 3–4 sentences)

Missing ANY of these five labeled sections from ANY step = incomplete playbook. Do not merge, skip, or rename them.
=== END FORMAT REQUIREMENTS ===

You are a business systems architect who builds execution playbooks used inside premium business education programs. \
Your playbooks are why members stay: they turn complex tactics into something any business owner can follow and execute today. \
A playbook is NOT an article. It is NOT an explanation. It is an operating manual.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Build a complete execution playbook for: {query}

MANDATORY REQUIREMENTS:
- MINIMUM 2,000 words. Count as you write. If you finish under 2,000 words, you have not written a complete playbook.
- Every Phase must be FULLY written — do not abbreviate, skip, or summarise any phase.
- Every TEMPLATE field must contain REAL fill-in-the-blank content with ________ blanks — not descriptions of what a template would look like.
- Each HOW TO DO IT section must have at minimum 4 numbered sub-points.
- Reference the source book by name wherever the context attributes content to a specific title.
- Do not write "See Step X" or "Similar to above" — every step is complete and standalone.

---

## Playbook: [Title using format "The [Specific Name] System for [Specific Measurable Result]"]

**What This Playbook Delivers**
[5-6 sentences. Describe the specific, measurable outcome the business owner will achieve. What will they have built? What problem does this permanently solve? What does their business look like after completing this? Be concrete — name systems, timelines, or metrics they can expect.]

**Time Required:**
- Phase 1: [X hours or days]
- Phase 2: [X hours or days]
- Phase 3: [X hours or days]

**Difficulty:** [Beginner / Intermediate / Advanced] — [one sentence explaining why]

**Before You Start, You Need:**
1. [Specific prerequisite — tool, decision, or information needed]
2. [Specific prerequisite]
3. [Specific prerequisite]
4. [Add more if the material calls for it]

---

### PHASE 1: [Phase Name — Foundation]
*Goal of this phase: [One sentence on what Phase 1 accomplishes and why it must come first before anything else.]*

**Step 1: [Action Verb + Specific Task Name]**

WHAT TO DO:
[5-6 sentences. What exactly is this action? Why does it come first? What goes wrong if you skip it? Make the scope of this step completely clear to someone doing this for the first time.]

HOW TO DO IT:
1. [First specific action — include tool, platform, or resource]
2. [Second specific action with enough detail to execute]
3. [Third specific action]
4. [Fourth specific action]
5. [Fifth specific action]

TEMPLATE — [Template Name]:
[Write the REAL template here. Use fill-in-the-blank format with ________ for blanks, [BRACKETS] for variable fields, or a structured form. Minimum 6-8 lines of actual template content. This must be something the reader can copy and fill in immediately.]

OUTPUT:
[The specific, tangible deliverable they will have when this step is complete. Name it precisely.]

PITFALL TO AVOID:
[The specific mistake that derails people here. Why does it happen? What does it look like when someone makes this mistake? How do you catch it early? 3-4 sentences.]

---

**Step 2: [Action Verb + Specific Task Name]**

WHAT TO DO:
[5-6 sentences — fully written, not abbreviated]

HOW TO DO IT:
1. [Sub-point 1]
2. [Sub-point 2]
3. [Sub-point 3]
4. [Sub-point 4]
5. [Sub-point 5 if needed]

TEMPLATE — [Template Name]:
[Real, usable fill-in-the-blank template — minimum 6 lines]

OUTPUT:
[Specific deliverable]

PITFALL TO AVOID:
[3-4 sentences — specific, not generic]

---

**Step 3: [Action Verb + Specific Task Name]**
[Same complete structure as Steps 1-2]

**Step 4: [Action Verb + Specific Task Name]**
[Same complete structure]

---

### PHASE 2: [Phase Name — Core Execution]
*Goal of this phase: [One sentence on what Phase 2 accomplishes, picking up directly from Phase 1.]*

**Step 5: [Action Verb + Specific Task Name]**
[All 5 fields — fully written]

**Step 6: [Action Verb + Specific Task Name]**
[All 5 fields — fully written]

**Step 7: [Action Verb + Specific Task Name]**
[All 5 fields — fully written]

**Step 8: [Action Verb + Specific Task Name]**
[All 5 fields — fully written]

---

### PHASE 3: [Phase Name — Review and Scale]
*Goal of this phase: [One sentence on what Phase 3 accomplishes.]*

**Step 9: [Action Verb + Specific Task Name]**
[All 5 fields — fully written]

**Step 10: [Action Verb + Specific Task Name]**
[All 5 fields — fully written]

**Step 11: [Action Verb + Specific Task Name — weekly or monthly review cadence]**
[All 5 fields — fully written]

---

**Success Metrics Dashboard**

| Metric | What It Measures | Healthy Target | Warning Signal |
|--------|-----------------|----------------|----------------|
| [Metric 1] | [What it tells you] | [Specific number or range] | [Specific signal to act] |
| [Metric 2] | [What it tells you] | [Specific number or range] | [Specific signal to act] |
| [Metric 3] | [What it tells you] | [Specific number or range] | [Specific signal to act] |
| [Metric 4] | [What it tells you] | [Specific number or range] | [Specific signal to act] |
| [Metric 5] | [What it tells you] | [Specific number or range] | [Specific signal to act] |

**Troubleshooting Guide**

If [specific symptom that indicates something is wrong]:
Likely cause: [diagnosis]
Fix: [specific action to take immediately]

If [specific symptom]:
Likely cause: [diagnosis]
Fix: [specific action]

If [specific symptom]:
Likely cause: [diagnosis]
Fix: [specific action]

If [specific symptom]:
Likely cause: [diagnosis]
Fix: [specific action]

**The Core Principle**
> "[One sentence — 10-20 words — that captures the essential philosophy behind this entire playbook. Make it memorable enough to repeat to someone else.]"

STYLE: Every line is an action, a template, or a decision. No theory for its own sake. Write like someone who has executed this exact system multiple times."""

FRAMEWORK_PROMPT = """\
You are a business framework designer who extracts and visualizes mental models from the world's best business books. \
Your frameworks are used by thousands of business owners as daily reference cards and strategy tools.

CONTEXT FROM KNOWLEDGE BASE:
{context}

Extract and present the core framework from the material above that addresses: {query}

## The [MEMORABLE NAME] Framework
*[One-line tagline that captures why this framework exists and what problem it solves]*

---

**The Problem This Solves**
[2-3 sentences naming the specific business pain this framework addresses. Make the reader feel the problem before seeing the solution.]

---

**The Framework**

[Choose the visual structure that fits — use markdown to make it clear:
- For a sequence: numbered steps with sub-items
- For a formula: write it on its own line like: Revenue − Profit = Expenses
- For components: bold name + colon + description for each
- For a table: use markdown table format]

[For each component deliver:]
**[Name]:** [What it means in plain English] → [What to do with it] → [What it produces]

---

**Why It Works**
[4-6 sentences on the logic. Why does this approach produce better results than the obvious one? What insight is baked into the structure of this framework?]

---

**How to Implement It — 4 Steps**
1. [Specific first action — do this today]
2. [Second step — concrete and doable]
3. [Third step]
4. [Ongoing practice or review cadence]

---

**What Breaks This Framework**
- [Mistake 1 — specific, with why it matters]
- [Mistake 2]
- [Mistake 3]

---

**The One-Line Version**
> "[The entire framework captured in one memorable sentence that stands alone]"

STYLE: Structured, precise, immediately usable as a standalone reference card."""

PROMPT_MAP: dict[str, str] = {
    "coaching": COACHING_PROMPT,
    "linkedin": LINKEDIN_PROMPT,
    "instagram": INSTAGRAM_PROMPT,
    "twitter": TWITTER_PROMPT,
    "email": EMAIL_PROMPT,
    "training_lesson": TRAINING_LESSON_PROMPT,
    "playbook": PLAYBOOK_PROMPT,
    "framework": FRAMEWORK_PROMPT,
}
