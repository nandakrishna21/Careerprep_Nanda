"""IT module seed: 5 learning-path courses, 9 career paths, lessons and quizzes."""
from __future__ import annotations

import importlib

from app.seed.gov_english import ERROR_SPOTTING, GRAMMAR, VOCAB
from app.seed.gov_reasoning import ANALOGY, PUZZLES, SYLLOGISM
from app.seed.util import QuestionDict, shuffled

_BANK_MODULES = [
    importlib.import_module("app.seed.it_banks_python"),
    importlib.import_module("app.seed.it_banks_sql_dsa"),
    importlib.import_module("app.seed.it_banks_web_backend"),
]

IT_BANKS: dict[str, list[tuple]] = {}
IT_LESSONS: dict[str, dict] = {}
for _m in _BANK_MODULES:
    IT_BANKS.update(_m.IT_BANKS)
    IT_LESSONS.update(_m.IT_LESSONS)

IT_COURSES: list[dict] = [
    {
        "title": "Python",
        "slug": "python",
        "icon": "terminal",
        "level": "Beginner",
        "order": 1,
        "description": "Python from first syntax to FastAPI services: 8 topics, worked examples, practice sets and a quiz per topic.",
        "topics": [
            ("python-basics", "Python Basics", "Beginner", "Values, expressions, types and how Python executes your code."),
            ("python-variables", "Variables", "Beginner", "Naming, mutability, casting and the built-in data types."),
            ("python-loops", "Loops", "Beginner", "for and while loops, range, comprehensions and loop control."),
            ("python-functions", "Functions", "Intermediate", "Parameters, return values, scope, lambdas and decorators."),
            ("python-oop", "OOP", "Intermediate", "Classes, inheritance, dunder methods and composition."),
            ("python-file-handling", "File Handling", "Intermediate", "Reading and writing files, context managers and JSON I/O."),
            ("python-apis", "APIs", "Intermediate", "Calling HTTP APIs with requests/httpx, status codes and payloads."),
            ("python-fastapi", "FastAPI", "Intermediate", "Routes, Pydantic models, dependencies and validation."),
        ],
    },
    {
        "title": "SQL",
        "slug": "sql",
        "icon": "database",
        "level": "Beginner",
        "order": 2,
        "description": "Query data like an analyst: SELECT to window functions, with result-prediction questions at every step.",
        "topics": [
            ("sql-basic-queries", "Basic Queries", "Beginner", "SELECT, WHERE, ORDER BY, LIMIT and conditional logic."),
            ("sql-joins", "Joins", "Intermediate", "INNER, LEFT, RIGHT, FULL joins and join conditions."),
            ("sql-group-by", "Group By", "Intermediate", "Aggregates, HAVING and grouping rules."),
            ("sql-subqueries", "Subqueries", "Intermediate", "Nested queries in WHERE, FROM and SELECT."),
            ("sql-window-functions", "Window Functions", "Advanced", "ROW_NUMBER, RANK, LAG/LEAD and frame clauses."),
        ],
    },
    {
        "title": "DSA",
        "slug": "dsa",
        "icon": "binary",
        "level": "Intermediate",
        "order": 3,
        "description": "The eight core data structures and algorithm families asked in every coding round, with complexity drill questions.",
        "topics": [
            ("dsa-arrays", "Arrays", "Beginner", "Contiguous storage, traversal, two pointers and complexity."),
            ("dsa-strings", "Strings", "Beginner", "Immutability, manipulation, patterns and matching."),
            ("dsa-linked-lists", "Linked Lists", "Intermediate", "Singly and doubly linked lists, insertion and cycle detection."),
            ("dsa-stacks", "Stacks", "Intermediate", "LIFO behaviour, monotonic stacks and expression evaluation."),
            ("dsa-queues", "Queues", "Intermediate", "FIFO behaviour, deques, queues and BFS traversal."),
            ("dsa-trees", "Trees", "Intermediate", "Binary trees, BST, traversals and height/depth."),
            ("dsa-graphs", "Graphs", "Advanced", "Representation, BFS, DFS, cycles and shortest paths."),
            ("dsa-dp", "Dynamic Programming", "Advanced", "Memoisation, tabulation and classic DP patterns."),
        ],
    },
    {
        "title": "Frontend",
        "slug": "frontend",
        "icon": "layout",
        "level": "Beginner",
        "order": 4,
        "description": "HTML to React: structure, styling, language fundamentals and component thinking, verified by code-output MCQs.",
        "topics": [
            ("frontend-html", "HTML", "Beginner", "Semantic markup, forms, accessibility and document structure."),
            ("frontend-css", "CSS", "Beginner", "Box model, selectors, specificity, flexbox and grid."),
            ("frontend-javascript", "JavaScript", "Intermediate", "Functions, closures, async behaviour and the event loop."),
            ("frontend-react", "React", "Intermediate", "Components, props, state, hooks and list keys."),
            ("frontend-tailwind", "Tailwind", "Beginner", "Utility classes, variants and layout primitives."),
        ],
    },
    {
        "title": "Backend",
        "slug": "backend",
        "icon": "server",
        "level": "Intermediate",
        "order": 5,
        "description": "FastAPI services end to end: REST design, PostgreSQL, SQLAlchemy, authentication and production deployment.",
        "topics": [
            ("backend-fastapi", "FastAPI", "Intermediate", "App setup, routing, Pydantic schemas and dependencies."),
            ("backend-rest-apis", "REST APIs", "Intermediate", "Resources, methods, status codes and idempotency."),
            ("backend-postgresql", "PostgreSQL", "Intermediate", "Tables, indexes, transactions and query tuning."),
            ("backend-sqlalchemy", "SQLAlchemy", "Intermediate", "ORM sessions, models, relationships and migrations."),
            ("backend-authentication", "Authentication", "Intermediate", "Passwords, JWT, OAuth2 flows and authorization."),
            ("backend-deployment", "Deployment", "Advanced", "Docker, environment config, servers and CI/CD."),
        ],
    },
]

CAREER_QUIZ_POOLS: dict[str, list[str]] = {
    "path-python-core": ["python-basics", "python-variables", "python-loops", "python-functions"],
    "path-python-databases": ["sql-basic-queries", "sql-joins", "backend-sqlalchemy", "sql-group-by"],
    "path-testing-packaging": ["python-functions", "python-oop", "backend-deployment", "backend-rest-apis"],
    "path-python-interview": ["python-oop", "python-fastapi", "python-apis", "dsa-arrays"],
    "path-rest-api-design": ["backend-rest-apis", "backend-fastapi", "backend-authentication"],
    "path-fastapi-mastery": ["backend-fastapi", "python-fastapi", "python-apis"],
    "path-data-modelling-sql": ["backend-postgresql", "sql-basic-queries", "sql-joins", "backend-sqlalchemy"],
    "path-api-security-performance": ["backend-authentication", "backend-rest-apis", "backend-postgresql"],
    "path-semantic-html-css": ["frontend-html", "frontend-css", "frontend-tailwind"],
    "path-modern-javascript": ["frontend-javascript", "frontend-html"],
    "path-react-patterns": ["frontend-react", "frontend-javascript"],
    "path-tailwind-ui": ["frontend-tailwind", "frontend-css"],
    "path-frontend-foundations": ["frontend-html", "frontend-css", "frontend-javascript"],
    "path-backend-foundations": ["backend-fastapi", "backend-rest-apis", "backend-postgresql"],
    "path-database-design": ["backend-postgresql", "sql-joins", "sql-group-by"],
    "path-ship-deploy": ["backend-deployment", "backend-fastapi"],
    "path-sql-analysis": ["sql-basic-queries", "sql-group-by", "sql-window-functions"],
    "path-data-cleaning-python": ["python-file-handling", "python-functions", "sql-basic-queries"],
    "path-visualisation-dashboards": ["frontend-javascript", "python-functions"],
    "path-statistics-analysts": ["sql-group-by", "sql-subqueries"],
    "path-python-data-science": ["python-functions", "python-oop", "python-loops"],
    "path-statistics-probability": ["dsa-dp", "dsa-arrays"],
    "path-ml-basics": ["python-functions", "dsa-dp", "dsa-graphs"],
    "path-model-evaluation": ["dsa-dp", "sql-group-by"],
    "path-networking-fundamentals": ["backend-deployment", "backend-rest-apis"],
    "path-linux-fundamentals": ["backend-deployment", "backend-authentication"],
    "path-troubleshooting-method": ["backend-deployment", "backend-fastapi"],
    "path-customer-communication": ["backend-rest-apis", "backend-authentication"],
    "path-research-secondary-data": ["sql-basic-queries", "sql-group-by"],
    "path-advanced-ms-excel": ["sql-group-by", "sql-subqueries"],
    "path-business-communication": ["frontend-html", "backend-rest-apis"],
    "path-analytical-reasoning": ["reasoning:analogy", "reasoning:puzzles", "reasoning:syllogism"],
    "path-linux-shell-scripting": ["backend-deployment", "backend-postgresql"],
    "path-cicd-pipelines": ["backend-deployment", "backend-fastapi"],
    "path-containers-docker": ["backend-deployment", "backend-rest-apis"],
    "path-cloud-monitoring": ["backend-deployment", "backend-postgresql"],
}


def questions_for(topic_slug: str, difficulty: str = "beginner") -> list[QuestionDict]:
    if topic_slug in IT_BANKS:
        return [
            {
                "question_text": q,
                "options": list(opts),
                "correct_index": idx,
                "explanation": expl,
                "difficulty": difficulty,
            }
            for q, opts, idx, expl in IT_BANKS[topic_slug]
        ]
    return _gov_bank_questions(topic_slug, difficulty)


def _gov_bank_questions(topic_slug: str, difficulty: str) -> list[QuestionDict]:
    """Reasoning/English banks reused for soft-skill career topics."""
    if topic_slug.startswith("reasoning:"):
        bank = {"reasoning:analogy": ANALOGY, "reasoning:puzzles": PUZZLES, "reasoning:syllogism": SYLLOGISM}[
            topic_slug
        ]
    elif topic_slug.startswith("grammar"):
        bank = {"grammar": GRAMMAR, "grammar:error-spotting": ERROR_SPOTTING, "grammar:vocabulary": VOCAB}[
            topic_slug
        ]
    else:
        raise KeyError(topic_slug)
    return [
        {"question_text": q, "options": list(opts), "correct_index": idx, "explanation": expl, "difficulty": difficulty}
        for q, opts, idx, expl in bank[difficulty]
    ]


def career_questions(topic_slug: str, limit: int = 10) -> list[QuestionDict]:
    pools = CAREER_QUIZ_POOLS.get(topic_slug)
    if not pools:
        raise KeyError(f"No quiz pool for career topic {topic_slug}")
    picked: list[QuestionDict] = []
    seen: set[str] = set()
    base, extra = divmod(limit, len(pools))
    for i, source in enumerate(pools):
        candidates = questions_for(source, "intermediate")
        rng = shuffled(f"{topic_slug}-{source}")
        take = min(base + (1 if i < extra else 0), len(candidates))
        for question in rng.sample(candidates, take):
            if question["question_text"] not in seen:
                seen.add(question["question_text"])
                picked.append(question)
    if len(picked) < limit:
        for source in pools:
            for question in questions_for(source, "intermediate"):
                if question["question_text"] not in seen:
                    seen.add(question["question_text"])
                    picked.append(question)
                    if len(picked) == limit:
                        break
            if len(picked) == limit:
                break
    rng = shuffled(topic_slug)
    rng.shuffle(picked)
    for question in picked:
        question["difficulty"] = "intermediate"
    return picked[:limit]
