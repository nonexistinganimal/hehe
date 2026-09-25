# Jev — research brief

Snapshot: 2026-09-25. Jev launched ten days ago (2026-09-15).

**How this was gathered.** The container's network policy blocks `typesafe.ai`, `docs.typesafe.ai` and almost every article host, so a HAR crawl of the live site wasn't possible. Everything below comes from:

- web-search snippets of the official launch post, docs and press coverage
- the **official SDK source code**: `typesafe-ai/typesafe-sdk-python` (PyPI `typesafe-sdk` 0.7.1), `typesafe-ai/typesafe-sdk-js` (`@typesafe-ai/sdk`) and `typesafe-ai/system-one-adapter-python`, all cloned from GitHub
- `Anil-matcha/awesome-jev-by-typesafe`, a community index with per-claim links into docs.typesafe.ai (snapshot 2026-09-19)

Anything marked *vendor claim* is TypeSafe's own number and hasn't been independently verified.

---

## 1. One sentence

**Jev is TypeSafe AI's first "System One" model: instead of writing text, it takes your program's state plus typed questions and returns typed answers with probabilities, in 70–500 ms, so ordinary code can branch on the result.**

## 2. The mental model (TypeSafe's own framing)

```text
text or JSON state + typed questions → constrained answers + probabilities → your code
```

- **System One / System Two.** The names come from Kahneman's fast/slow thinking. LLMs are "System Two": slow, token-by-token, conversational. Jev is "System One": fast, instinctive, a decision rather than a paragraph.
- **Non-autoregressive.** Jev doesn't generate tokens one at a time. It fills every question in a single parallel pass.
- **Built for machines, not chat.** TypeSafe says it "optimize[s] explicitly for AI-to-computer interactions rather than human-in-the-loop". The press line was "the model built to kill chat."
- **The rule it teaches:** *questions describe judgments; code owns composition, thresholds and side effects.*

## 3. The API: three primitives (verified in the SDK source)

| Primitive | Answers | Returns |
|---|---|---|
| `Choice` | "Which one of these known options?" (intent, department, tool, next link) | `choice`, `probabilities` per option, `confidence` |
| `Score` | "Where on this ordered rubric?" (severity, frustration, relevance) | `score` (probability-weighted, can land between levels), `legend`, `probabilities`, `confidence` |
| `Noul` | "How likely is this statement true?" (is urgent? is prompt injection?) | `noul` ∈ [0, 1]. Near 0.5 means *uncertain*, not "medium" |

The name `Noul` is TypeSafe's own coinage for a probabilistic yes/no. It's a distinctive, ownable word for the video.

**Endpoint:** `POST https://api.typesafe.ai/v1/systemone`. Model alias `jev-latest` (currently `jev-1.13.0`), with `jev-preview` also available.
**Response:** `answers` keyed by question name, plus `model` and `usage`.

### The canonical example (this exact ticket appears in the official SDK READMEs)

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state={"ticket": "I was charged twice and need the duplicate refunded today."},
        questions={
            "intent": Choice(
                instructions="What is the customer's main request?",
                criteria={"refund": "...", "technical_help": "...", "information": "...", "other": "..."},
            ),
            "is_urgent": Noul(instructions="Does the ticket explicitly communicate time pressure?"),
            "frustration": Score(
                instructions="How frustrated does the customer appear?",
                criteria=["Calm and neutral", "Concerned but civil", "Very angry or using strong language"],
            ),
        },
    )
```

```ts
import { choice, noul, score, TypeSafeClient } from "@typesafe-ai/sdk";
const r = await new TypeSafeClient().systemOne({ state, questions: {
  intent: choice("What is the customer's main request?", { refund: "...", technical_help: "...", information: "...", other: "..." }),
  isUrgent: noul("Does the ticket explicitly communicate time pressure?"),
}});
r.answers.intent.choice // "refund"  (answer types are inferred from the questions)
```

→ **This is "the thing" the video shows.** It's real API surface, real field names and the real example, not invented UI.

## 4. Numbers (vendor claims unless noted)

| Claim | Value |
|---|---|
| End-to-end latency | **70–500 ms** |
| Speed vs frontier LLMs on System-One-shaped tasks | **40×–200× faster** (marketing shorthand: "100× faster, 100× cheaper") |
| Price | **$0.042 per 1M input tokens** ($42 per *billion*). **Output tokens are free.** |
| Structured-output error rate | **0%**. Schema-match is a property of the architecture, not something you hope the model complies with |
| Context | 64k tokens per request (32k for state + longest question) |
| Rate limits | 250k tokens/s, 1,200 req/min |
| Modalities | Text only (no images, audio or video yet) |
| Availability | Limited early access at launch, via console.typesafe.ai |
| Also on | Vercel AI Gateway (`typesafe-ai/jev`), Cloudflare Workers AI (`typesafe/jev`), OpenRouter community SDK, Pydantic AI |

**Critical coverage worth knowing:** one piece ("Claims 193x Faster and 444x Cheaper. Its Own Eval Scores Against Two Other Models' Answers") questions how the evals were scored. **For the video: stick to the numbers TypeSafe publishes on its own pages** (70–500 ms, $0.042/1M, output free) and don't invent multipliers.

## 5. Company

- **TypeSafe AI**, San Francisco, founded 2024 by **Diogo Almeida** (CEO; ~4 years at OpenAI on RLHF, InstructGPT, ChatGPT, GPT-4), **Erik Gafni** and **Sasha Sheng**. Alumni of OpenAI and Meta AI.
- Came out of stealth with Jev on **2026-09-15**, alongside a **$40M seed led by DCVC**.
- Self-description: "a research lab building large language models for automation, not conversation." Site title: *"Structured Artificial Intelligence."*

## 6. Launch demos (the "look at this" moments)

- **Doom.** Jev plays Doom from *structured game state* (enemy positions, distances and angles as JSON, not pixels) at **~10 decisions/second, ~$7/hour**.
- **Wikiracing.** Each step picks one link from hundreds or thousands. Because `Choice` can only return an option that exists, it *never picks a link that doesn't exist*, and that's what lets the run finish.
- **Smart home.** Fans out over category, domain, device and action in one call.
- **1kpapers.com.** 1,018 papers classified into 24 topics for **$0.08 total**, median **256 ms** per paper.
- **Paper Radar** (community): 501 papers for $0.0196.

## 7. Use cases (why it matters, by who's watching)

| Who | What Jev does for them |
|---|---|
| Support / ops teams | Inbox triage: intent + urgency + frustration in one call → route with `if` statements |
| Agent builders | Router in front of tools, skills and expensive LLMs: "does this turn need a tool or retrieval?" |
| RAG engineers | Score passage relevance and answer support, catch prompt injection before the answering model |
| Trust & safety | Moderation with an explicit *uncertain* band → human review instead of auto-removal |
| Fintech / insurance | Invoice matching, fraud signals, claims triage. Code does the math, Jev does the semantic reads |
| Game / robotics / sim devs | Decisions *inside* a real-time loop (Doom, 10 Hz) |
| ML teams | Turn text into numeric `Score`/`Noul` features for classical models |
| CI / DevEx | Semantic lint rules as yes/no checks on PRs |

**Core patterns:** speculative fan-out (ask everything at once and ignore what you don't need), confidence-gated routing, composite scoring, intent routing, two-stage dependency.

## 8. What sets it apart (the angle)

1. **It can't return a wrong-shaped answer.** Output is typed by construction, so there's no JSON parsing, retrying or "please respond in valid JSON."
2. **It tells you how sure it is.** Probabilities and confidence let code decide: act, ask a human, or fall back.
3. **It's fast and cheap enough to sit inside a loop.** 70–500 ms, output free. That opens up places LLMs can't go: games, UIs, per-row data pipelines.

## 9. What the video has to land (brag "clear to a stranger" test)

- **What:** a model that answers with typed decisions, not text.
- **Who:** developers wiring AI into software (automation, routing, agents, real-time).
- **Why care:** milliseconds, probabilities, free output, no parsing.
- **How to get it:** Jev by TypeSafe, early access, `typesafe.ai`.
- **Share caption candidate:** "Your code never wanted a paragraph. Jev answers in types, in milliseconds. Output tokens are free."

## Sources

- [Introducing System One Models & Jev (TypeSafe blog)](https://typesafe.ai/blog/introducing-system-one-models-and-jev) · [typesafe.ai](https://typesafe.ai/) · [docs: Introduction](https://docs.typesafe.ai/introduction) · [docs: Quick start](https://docs.typesafe.ai/introduction/quickstart) · [docs: System One](https://docs.typesafe.ai/concepts/system-one)
- [typesafe-sdk-python](https://github.com/typesafe-ai/typesafe-sdk-python) · [typesafe-sdk-js](https://github.com/typesafe-ai/typesafe-sdk-js) · [system-one-adapter-python](https://github.com/typesafe-ai/system-one-adapter-python)
- [awesome-jev-by-typesafe](https://github.com/Anil-matcha/awesome-jev-by-typesafe)
- [Jev (AI model), Wikipedia](https://en.wikipedia.org/wiki/Jev_(AI_model)) · [MindStudio explainer](https://www.mindstudio.ai/blog/jev-system-one-model-launch) · [DataCamp](https://www.datacamp.com/blog/system-one-models-jev) · [MarkTechPost](https://www.marktechpost.com/2026/09/19/typesafe-ai-releases-jev/) · [You.com](https://you.com/resources/what-is-jev) · [StartupHub: "the model built to kill chat"](https://www.startuphub.ai/ai-news/artificial-intelligence/2026/typesafe-jev-model-kills-chat) · [Medium: plays Doom](https://medium.com/@creativeaininja/typesafes-jev-makes-ai-decisions-fast-enough-to-play-doom-68fdcce1159a) · [Cherry Creek News: eval critique](https://thecherrycreeknews.com/typesafe-jev-system-one-model-claims-evals-independent-tests-cherry_creek/)
