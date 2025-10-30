# AI-Assisted Coding Workshop: Building with AI Coding Agents

This is a hands-on workshop about **working with AI coding agents**. You'll learn how to plan and specify requirements, provide context, and build software interactively using AI coding tools.

The project we'll build together is a **multi-agent system** that automatically creates flashcards from Wikipedia articles — but the real focus is on **learning to code with AI**.

You'll learn:
- 🎯 **How to plan and specify requirements** for AI-assisted development
- 📝 **How to provide effective context** to AI coding tools
- 💬 **How to communicate with AI agents** to get the code you want
- 🔄 **How to iterate and refine** when AI doesn't get it right the first time
- 🐛 **How to debug** with AI assistance
- 🏗️ **How to build incrementally** — testing each component before moving forward
- 🤖 **Real-world AI coding workflows** used by professionals

**The flashcard generator** is our vehicle for learning these skills. By the end, you'll have:
- ✅ A working multi-agent system
- ✅ Practical experience with AI-assisted development
- ✅ Techniques you can apply to any coding project

**No prior experience with AI coding tools required** — just bring your curiosity!

---

> 🎓 This workshop is part of [Hugo Bowne-Anderson's course, *Building LLM-Powered Applications for Data Scientists and Software Engineers*](https://maven.com/hugo-stefan/building-ai-apps-ds-and-swe-from-first-principles?promoCode=vibe25).
>
> Next cohort starts **November 3** — use code `vibe25` for 25% off (valid until Nov 2, 2025)!

---

## 🛠 Workshop Flow

1. **Introduction: Setting Context and Planning** — Kicking off an AI-assisted coding project.
2. **Building the Agents** — Creating the multi-agent system step-by-step with AI assistance.
3. **Q&A / Discussion** — Open floor for questions about AI-assisted coding techniques, challenges, and best practices.

---

## ⚡ Requirements

### To Follow Along (Watching)
- 💡 **Just curiosity!** No setup needed to watch and learn the AI coding techniques

### To Code Along (Optional)
- ✅ **Python** installed on your system
- 🔑 **API keys for your favourit LLM provider (_OpenAI, Anthropic, OpenRouter, ..._)**
- 📦 **Dependencies:** Install with `uv`
- 🤖 **AI coding tool** of your choice (_Copilot, Claude Code, Codex, Cursor, ..._)

### No Experience Required
- ❌ No prior AI coding experience needed
- ❌ No agent-building experience needed

---

## 📚 What's Next?

> 🎓 This workshop is presented by Isaac Flath and Eleanor Berger of the course **[Elite AI-Assisted Coding](https://maven.com/kentro/context-engineering-for-coding?promoCode=HUGO)**.
>
> Next cohort starts **January 12** — use code `HUGO` for 25% 💥 discount!
>
> **Join us to learn about AI-assisted software development in depth.**

---

## What We're Building

```
+---------------------------------------------------------------------+
|                         USER QUERY (CLI)                            |
|                  "quantum physics" or similar                       |
+-------------------------------+-------------------------------------+
                                |
                                v
+---------------------------------------------------------------------+
|                      AGENT 1: Wikipedia Search                      |
|                                                                     |
|  Search Wikipedia -> Fetch 2-3 articles -> Return full content      |
|                                                                     |
|  Output: WikipediaSearchResult (2-3 articles with title + content)  |
+-------------------------------+-------------------------------------+
                                |
                                v
                     +------------------+
                     |  Combine Articles |
                     +---------+---------+
                               |
                               v
+---------------------------------------------------------------------+
|                    AGENT 2: Analysis & Summary                      |
|                                                                     |
|  Read articles -> Identify concepts -> Create unified narrative     |
|                                                                     |
|  Output: Summary string (500-1500 words)                            |
+-------------------------------+-------------------------------------+
                                |
                                v
+---------------------------------------------------------------------+
|                   AGENT 3: Flashcard Creator                        |
|                                                                     |
|  Extract facts -> Generate Q&A pairs -> Validate structure          |
|                                                                     |
|  Output: FlashcardCollection (10-30 flashcards)                     |
+-------------------------------+-------------------------------------+
                                |
                                v
                     +------------------+
                     |  Write to File   |
                     +---------+--------+
                               |
                               v
+---------------------------------------------------------------------+
|                   flashcards_quantum_physics.md                     |
|                                                                     |
|  **Question:** What is quantum superposition?                       |
|  **Answer:** A fundamental principle stating...                     |
|  ---                                                                |
|                                                                     |
|  **Question:** Who developed the Schrodinger equation?              |
|  **Answer:** Erwin Schrodinger in 1926...                           |
|  ---                                                                |
|  ...                                                                |
+---------------------------------------------------------------------+
```

---

## 🚀 Usage

The project is now complete and ready to use! Here's how to generate flashcards for any topic:

### Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/intellectronica/wikipedia-flashcards-agent.git
   cd wikipedia-flashcards-agent
   ```

2. **Set up your OpenAI API key**:
   Create a `.env` file in the project root:
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

3. **Install dependencies** (handled automatically by `uv`):
   No manual installation needed! `uv` will handle everything.

### Running the Generator

Generate flashcards for any topic:

```bash
uv run src/cli.py "Your Topic Here"
```

**Examples:**

```bash
# Generate flashcards about Machine Learning
uv run src/cli.py Machine Learning

# Generate flashcards about Quantum Computing
uv run src/cli.py Quantum Computing

# Generate flashcards about Python Programming
uv run src/cli.py Python programming language
```

### What Happens

The system will:
1. 🔍 **Search Wikipedia** for 2-3 relevant articles about your topic
2. 📝 **Generate a summary** (500-1500 words) synthesizing the articles
3. 🎴 **Create flashcards** (20-50 Q/A pairs) from the summary
4. 💾 **Save to file** in `tmp/flashcards_{topic}_{timestamp}.md`

The entire process takes about **45-60 seconds** and you'll see detailed logging showing progress at each stage.

### Output

Flashcards are saved as Markdown files in the `tmp/` directory with filenames like:
- `tmp/flashcards_machine-learning_20251031_0008.md`
- `tmp/flashcards_quantum-computing_20251031_1430.md`

Each file contains:
- Topic and generation timestamp
- Numbered flashcards with clear Q/A format
- Easy to import into flashcard apps like Anki, Quizlet, or use directly

---

Enjoy building! 🚀
