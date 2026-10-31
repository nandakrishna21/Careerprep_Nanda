export type TrackLevel = 'Beginner' | 'Intermediate' | 'Advanced';

export type TrackStage = {
  title: string;
  level: TrackLevel;
  duration: string;
  goal: string;
  topics: string[];
};

export type TrackResource = {
  name: string;
  url: string;
  description: string;
  level: TrackLevel;
  kind: 'Course' | 'Docs' | 'Video' | 'Practice' | 'Reading';
  tags: string[];
};

export type CareerTrack = {
  slug: string;
  title: string;
  shortTitle: string;
  tagline: string;
  about: string;
  roles: string[];
  skills: string[];
  stages: TrackStage[];
  resources: TrackResource[];
};

const FDE: CareerTrack = {
  slug: 'fde',
  title: 'Forward Deployed Engineer (FDE)',
  shortTitle: 'FDE',
  tagline:
    'The engineer who ships software inside the customer’s world — equal parts coder, data wrangler, product thinker and communicator.',
  about:
    'Forward Deployed Engineers work embedded with clients (the model Palantir pioneered): you take a messy real-world problem, build a solution on your company’s platform, demo it, iterate with stakeholders and hand it over. It is the fastest route from “junior dev” to owning end-to-end outcomes.',
  roles: ['Solution Engineer', 'Deployment Engineer', 'Product Engineer', 'Client-side Consultant'],
  skills: ['Python', 'SQL', 'REST APIs', 'Docker & Cloud', 'System Design', 'Stakeholder Communication'],
  stages: [
    {
      title: 'Programming foundations',
      level: 'Beginner',
      duration: '3–4 weeks',
      goal: 'Be comfortable writing small programs and using developer tools daily.',
      topics: [
        'Python syntax — variables, loops, functions, files',
        'Object-oriented basics: classes, modules, error handling',
        'Command line, Git, GitHub push/pull and pull requests',
        'Virtual environments and installing packages with pip',
      ],
    },
    {
      title: 'Software engineering core',
      level: 'Beginner',
      duration: '6–8 weeks',
      goal: 'Build and test a small web API that a teammate can use.',
      topics: [
        'Data structures: arrays, hash maps, sets, queues',
        'Relational databases — SQL SELECT, joins, indexes (PostgreSQL)',
        'REST APIs with FastAPI or Flask; JSON request/response',
        'Testing with pytest, logging, and code review basics',
      ],
    },
    {
      title: 'Data wrangling & analysis',
      level: 'Intermediate',
      duration: '4 weeks',
      goal: 'Turn a raw CSV or database dump into a clear insight a client would act on.',
      topics: [
        'pandas — filter, groupby, join, reshape messy datasets',
        'Advanced SQL — window functions, CTEs, query tuning',
        'Data modelling: star schema, fact vs dimension tables',
        'ETL basics: extract → clean → load pipelines and schedules',
      ],
    },
    {
      title: 'Cloud & deployment',
      level: 'Intermediate',
      duration: '4–6 weeks',
      goal: 'Deploy an app end-to-end so anyone can open a URL and use it.',
      topics: [
        'Linux servers, networking and environment variables',
        'Docker — containerize an app, compose services',
        'Cloud fundamentals on AWS or GCP: compute, storage, IAM',
        'CI/CD with GitHub Actions; databases in production',
      ],
    },
    {
      title: 'System design & architecture',
      level: 'Intermediate',
      duration: '4 weeks',
      goal: 'Design a scalable system on paper and defend every trade-off.',
      topics: [
        'Load balancing, caching (Redis), queues and rate limiting',
        'Monolith vs microservices; event-driven architecture',
        'API versioning, schemas and data migrations at scale',
        'Security basics: auth tokens, secrets, least privilege',
      ],
    },
    {
      title: 'Client-facing & product skills',
      level: 'Advanced',
      duration: 'Ongoing',
      goal: 'Run a discovery call, demo a build and get sign-off without a manager in the room.',
      topics: [
        'Requirement gathering — asking the right “why” questions',
        'Demoing: narrate the outcome, not the code',
        'Scoping an MVP and saying no to gold-plating',
        'Writing: README, one-pagers, runbooks, handover docs',
      ],
    },
    {
      title: 'Portfolio & interview prep',
      level: 'Advanced',
      duration: '4 weeks',
      goal: 'Two portfolio projects live and a rehearsed story for every round.',
      topics: [
        'Case-study rounds: walk through a real client problem you solved',
        'System design interview practice with timed mock sessions',
        'Resume focused on impact metrics (“cut report time 80%”)',
        'Behavioural stories using STAR for collaboration questions',
      ],
    },
  ],
  resources: [
    {
      name: 'Python Official Tutorial',
      url: 'https://docs.python.org/3/tutorial/',
      description: 'The authoritative free Python tutorial — start here for stage 1 and keep it as a reference.',
      level: 'Beginner',
      kind: 'Docs',
      tags: ['Python', 'Basics'],
    },
    {
      name: 'CS50x by Harvard',
      url: 'https://cs50.harvard.edu/x/',
      description: 'Harvard’s free intro to computer science — algorithms, C, Python, SQL and web builds with graded problem sets.',
      level: 'Beginner',
      kind: 'Course',
      tags: ['CS Fundamentals', 'SQL', 'Web'],
    },
    {
      name: 'freeCodeCamp',
      url: 'https://www.freecodecamp.org/learn/',
      description: 'Free full curriculum with hands-on projects: Responsive Web Design, JavaScript, APIs and Python certification.',
      level: 'Beginner',
      kind: 'Course',
      tags: ['Web', 'Projects', 'Certificate'],
    },
    {
      name: 'The Odin Project',
      url: 'https://www.theodinproject.com',
      description: 'Free full-stack curriculum with real projects — great for building the “ship something end-to-end” muscle.',
      level: 'Beginner',
      kind: 'Course',
      tags: ['Full Stack', 'Projects'],
    },
    {
      name: 'GitHub Skills',
      url: 'https://skills.github.com',
      description: 'Interactive labs teaching Git, branches and GitHub Actions directly inside a real repository.',
      level: 'Beginner',
      kind: 'Practice',
      tags: ['Git', 'CI/CD'],
    },
    {
      name: 'SQLBolt',
      url: 'https://sqlbolt.com',
      description: 'Short interactive SQL lessons in the browser — fastest way to learn SELECT, joins and schema basics.',
      level: 'Beginner',
      kind: 'Practice',
      tags: ['SQL', 'Database'],
    },
    {
      name: 'Kaggle Learn',
      url: 'https://www.kaggle.com/learn',
      description: 'Free micro-courses with in-browser notebooks: pandas, SQL, data visualization and feature engineering.',
      level: 'Intermediate',
      kind: 'Course',
      tags: ['pandas', 'SQL', 'Data'],
    },
    {
      name: 'PostgreSQL Tutorial',
      url: 'https://www.postgresqltutorial.com',
      description: 'Free step-by-step PostgreSQL guide — from CRUD to indexes, window functions and backup strategies.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['PostgreSQL', 'Database'],
    },
    {
      name: 'FastAPI Documentation',
      url: 'https://fastapi.tiangolo.com',
      description: 'Modern Python API framework with an outstanding free tutorial — build type-safe REST APIs quickly.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['API', 'Python', 'Backend'],
    },
    {
      name: 'Docker — Get Started',
      url: 'https://docs.docker.com/get-started/',
      description: 'Official hands-on Docker tutorial: containerize an app, wire services and ship images.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['Docker', 'DevOps'],
    },
    {
      name: 'AWS Skill Builder (Free Training)',
      url: 'https://skillbuilder.aws',
      description: 'Amazon’s free digital training catalog — Cloud Practitioner essentials and hands-on labs included.',
      level: 'Intermediate',
      kind: 'Course',
      tags: ['AWS', 'Cloud'],
    },
    {
      name: 'Google Cloud Skills Boost',
      url: 'https://www.cloudskillsboost.google',
      description: 'Free quests and labs on GCP fundamentals — some content free with an account, badge-verified.',
      level: 'Intermediate',
      kind: 'Practice',
      tags: ['GCP', 'Cloud', 'Labs'],
    },
    {
      name: '12factor.net',
      url: 'https://12factor.net',
      description: 'The classic checklist for building deployable, scalable SaaS apps — short, free and universally cited.',
      level: 'Intermediate',
      kind: 'Reading',
      tags: ['Architecture', 'Deployment'],
    },
    {
      name: 'System Design Primer',
      url: 'https://github.com/donnemartin/system-design-primer',
      description: 'Open-source guide to scalable systems with diagrams and real interview questions — core FDE architecture prep.',
      level: 'Advanced',
      kind: 'Reading',
      tags: ['System Design', 'Scalability'],
    },
    {
      name: 'ByteByteGo',
      url: 'https://www.youtube.com/@ByteByteGo',
      description: 'Free system-design videos with clear visuals — perfect review before design interviews and client architecture talks.',
      level: 'Advanced',
      kind: 'Video',
      tags: ['System Design', 'YouTube'],
    },
    {
      name: 'Tech Interview Handbook',
      url: 'https://www.techinterviewhandbook.org',
      description: 'Free guides on resumes, coding rounds, behavioural answers and negotiation for engineering roles.',
      level: 'Advanced',
      kind: 'Reading',
      tags: ['Interview', 'Resume'],
    },
    {
      name: 'Martin Fowler’s Bliki',
      url: 'https://martinfowler.com/bliki/',
      description: 'Free articles on refactoring, microservices and patterns — the thinking behind senior-level trade-offs.',
      level: 'Advanced',
      kind: 'Reading',
      tags: ['Architecture', 'Patterns'],
    },
    {
      name: 'Postman Learning Center',
      url: 'https://learning.postman.com',
      description: 'Free API testing tutorials — send requests, write tests and automate collections like a solution engineer.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['API', 'Testing'],
    },
  ],
};

const AGENTS: CareerTrack = {
  slug: 'agents',
  title: 'AI Agent Engineer',
  shortTitle: 'AI Agent Engineer',
  tagline:
    'Build LLM-powered agents that plan, call tools, retrieve knowledge and complete real work — the most in-demand AI engineering role in 2026.',
  about:
    'An AI Agent Engineer designs systems where a language model is the brain and your code gives it hands: tools, memory, retrieval and guardrails. You move from single prompt calls to reliable multi-step agents that ship to production with evals, tracing and cost control.',
  roles: ['AI Engineer', 'LLM Applications Engineer', 'Agent Developer', 'Applied AI Engineer'],
  skills: ['Python', 'LLM APIs', 'RAG & Embeddings', 'Agent Frameworks', 'Evals & Observability', 'MCP'],
  stages: [
    {
      title: 'Python & developer foundations',
      level: 'Beginner',
      duration: '3–4 weeks',
      goal: 'Comfortable calling a REST API from Python and pushing code to GitHub.',
      topics: [
        'Python — functions, classes, async/await, type hints',
        'Virtual envs, pip, requests/httpx and JSON handling',
        'Git, GitHub and running scripts from the terminal',
        'How HTTP, JSON and webhooks work',
      ],
    },
    {
      title: 'LLM fundamentals & prompting',
      level: 'Beginner',
      duration: '2–3 weeks',
      goal: 'Understand how LLMs generate text and engineer prompts that produce reliable output.',
      topics: [
        'How transformers/LLMs work conceptually: tokens, context, temperature',
        'Prompt patterns: role framing, few-shot, chain-of-thought, XML structure',
        'Structured output: JSON mode, schemas, function calling basics',
        'Safety: jailbreaks, prompt injection, refusals and guardrail prompts',
      ],
    },
    {
      title: 'Building with LLM APIs',
      level: 'Intermediate',
      duration: '3–4 weeks',
      goal: 'Ship an app that streams responses, calls your tools and answers from your own documents.',
      topics: [
        'Gemini / OpenAI APIs — streaming, system instructions, retries',
        'Tool calling: define tools, execute code, feed results back',
        'Embeddings + vector databases (Chroma/Pinecone) for semantic search',
        'RAG pipelines: chunk, embed, retrieve, cite — with relevance testing',
      ],
    },
    {
      title: 'Agent frameworks & patterns',
      level: 'Intermediate',
      duration: '4–6 weeks',
      goal: 'Build a goal-seeking agent that plans steps, uses tools and recovers from errors.',
      topics: [
        'LangChain & LangGraph — chains, state graphs, checkpoints',
        'LlamaIndex for retrieval-first agents',
        'Design patterns: planner, reflection, ReAct, retry/fallback',
        'Memory: short-term context vs long-term vector memory',
        'MCP (Model Context Protocol) — plug tools and context servers',
      ],
    },
    {
      title: 'Multi-agent systems',
      level: 'Intermediate',
      duration: '3–4 weeks',
      goal: 'Orchestrate specialised agents that delegate, debate and hand off work.',
      topics: [
        'CrewAI roles and tasks; AutoGen conversational agents',
        'Orchestrator–worker patterns and dynamic delegation',
        'Human-in-the-loop approval gates for risky actions',
        'Shared state, message passing and failure isolation',
      ],
    },
    {
      title: 'Production, evals & observability',
      level: 'Advanced',
      duration: '4 weeks',
      goal: 'Deploy an agent users trust — measured, traced and cost-bounded.',
      topics: [
        'Evals: golden datasets, LLM-as-judge, regression suites',
        'Tracing with LangSmith or Arize Phoenix; prompt versioning',
        'Latency & cost: caching, smaller models, batching, streaming',
        'Guardrails, rate limits, permissions and audit logging',
        'Deploying: FastAPI service, queueing, background workers',
      ],
    },
    {
      title: 'Advanced edge & career launch',
      level: 'Advanced',
      duration: 'Ongoing',
      goal: 'Three portfolio agents live, an open-source contribution and a prepared interview story.',
      topics: [
        'When to fine-tune vs RAG vs prompt — and evaluation-driven choices',
        'Build and publish your own MCP server for a real tool',
        'Voice/vision agents, computer-use and browser agents',
        'Portfolio: support agent, research agent, code-review agent',
        'Interview prep: agent design cases and live debugging rounds',
      ],
    },
  ],
  resources: [
    {
      name: 'Google AI for Developers',
      url: 'https://ai.google.dev',
      description: 'Official Gemini API docs and quickstarts — free API tier, multimodal inputs and function calling guides.',
      level: 'Beginner',
      kind: 'Docs',
      tags: ['Gemini', 'API', 'LLM'],
    },
    {
      name: 'Google Prompt Engineering Course',
      url: 'https://www.cloudskillsboost.google/course_templates/1134',
      description: 'Free “Introduction to Prompt Engineering” course on Google Cloud Skills Boost — fundamentals with hands-on labs.',
      level: 'Beginner',
      kind: 'Course',
      tags: ['Prompting', 'Gemini'],
    },
    {
      name: 'Prompt Engineering Guide (dair.ai)',
      url: 'https://www.promptingguide.ai',
      description: 'Open-source guide covering all major prompting techniques, patterns and LLM concepts — free on GitHub.',
      level: 'Beginner',
      kind: 'Reading',
      tags: ['Prompting', 'Open Source'],
    },
    {
      name: 'Hugging Face Learn',
      url: 'https://huggingface.co/learn',
      description: 'Free courses on NLP, LLMs, agents and generative AI with hands-on notebooks on the Hub.',
      level: 'Beginner',
      kind: 'Course',
      tags: ['Hugging Face', 'NLP', 'Agents'],
    },
    {
      name: 'DeepLearning.AI Short Courses',
      url: 'https://www.deeplearning.ai/short-courses/',
      description: 'Free 1–2 hour courses with industry instructors — “AI Agentic Design Patterns”, “Functions, Tools & Agents”, “Building Agentic RAG”.',
      level: 'Intermediate',
      kind: 'Course',
      tags: ['Agents', 'LangChain', 'RAG'],
    },
    {
      name: 'OpenAI Cookbook',
      url: 'https://cookbook.openai.com',
      description: 'Hundreds of free runnable recipes — tool calling, structured outputs, RAG, agents and evaluation patterns.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['OpenAI', 'Recipes', 'Tools'],
    },
    {
      name: 'LangChain Academy',
      url: 'https://academy.langchain.com',
      description: 'Free interactive courses on LangChain and LangGraph — build stateful agents step by step in the browser.',
      level: 'Intermediate',
      kind: 'Course',
      tags: ['LangGraph', 'LangChain'],
    },
    {
      name: 'LangGraph Documentation',
      url: 'https://langchain-ai.github.io/langgraph/',
      description: 'Official docs for the leading agent orchestration library — graphs, persistence, streaming and human-in-the-loop.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['LangGraph', 'Agents'],
    },
    {
      name: 'Model Context Protocol (MCP)',
      url: 'https://modelcontextprotocol.io',
      description: 'The open standard for connecting LLMs to tools — build and host your own MCP servers, free docs and spec.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['MCP', 'Tools', 'Standard'],
    },
    {
      name: 'Pinecone — Learn Center',
      url: 'https://www.pinecone.io/learn/',
      description: 'Free lessons on embeddings, vector search and RAG architecture with code examples (works with free tiers).',
      level: 'Intermediate',
      kind: 'Reading',
      tags: ['Vector DB', 'RAG'],
    },
    {
      name: 'LlamaIndex Documentation',
      url: 'https://docs.llamaindex.ai',
      description: 'Data framework for LLM apps — ingestion, indexing, retrieval agents and workplace integrations.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['LlamaIndex', 'RAG'],
    },
    {
      name: 'CrewAI Documentation',
      url: 'https://docs.crewai.com',
      description: 'Free framework for role-playing multi-agent crews — tasks, tools, processes and Flows.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['CrewAI', 'Multi-agent'],
    },
    {
      name: 'Microsoft AutoGen',
      url: 'https://microsoft.github.io/autogen/',
      description: 'Open-source framework for conversational multi-agent apps — free docs, notebooks and samples.',
      level: 'Intermediate',
      kind: 'Docs',
      tags: ['AutoGen', 'Multi-agent'],
    },
    {
      name: 'Building Effective Agents (Anthropic)',
      url: 'https://www.anthropic.com/research/building-effective-agents',
      description: 'Concise, free essay on when simple workflows beat agents and the patterns that actually work in production.',
      level: 'Advanced',
      kind: 'Reading',
      tags: ['Design', 'Patterns'],
    },
    {
      name: 'Hugging Face Agents Course',
      url: 'https://huggingface.co/learn/agents-course',
      description: 'Free community course: tools, MCP, smolagents, OpenHands and evaluating agent trajectories.',
      level: 'Advanced',
      kind: 'Course',
      tags: ['Agents', 'MCP', 'Evaluation'],
    },
    {
      name: 'LangSmith Docs (Evals & Tracing)',
      url: 'https://docs.smith.langchain.com',
      description: 'How to trace, monitor and evaluate LLM apps — datasets, online evals and prompt experiments.',
      level: 'Advanced',
      kind: 'Docs',
      tags: ['Evals', 'Observability'],
    },
    {
      name: 'Arize Phoenix',
      url: 'https://arize.com/docs/phoenix',
      description: 'Open-source LLM observability — traces, evals and datasets for agent debugging, free to self-host.',
      level: 'Advanced',
      kind: 'Docs',
      tags: ['Tracing', 'Open Source'],
    },
    {
      name: 'Vercel AI SDK',
      url: 'https://sdk.vercel.ai/docs',
      description: 'Free framework-agnostic TypeScript toolkit for streaming chat UIs, tools and agents in production apps.',
      level: 'Advanced',
      kind: 'Docs',
      tags: ['TypeScript', 'Streaming', 'UI'],
    },
  ],
};

export const CAREER_TRACKS: Record<string, CareerTrack> = {
  [FDE.slug]: FDE,
  [AGENTS.slug]: AGENTS,
};

export const TRACK_LEVELS: ('all' | TrackLevel)[] = ['all', 'Beginner', 'Intermediate', 'Advanced'];
