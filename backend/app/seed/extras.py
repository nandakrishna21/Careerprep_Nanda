"""Seed data for exams, mock tests, PYQs, current affairs and jobs + question samplers."""
from __future__ import annotations

from datetime import date

from app.seed import gov_english, gov_ga, gov_quant, gov_reasoning
from app.seed.it import IT_BANKS
from app.seed.util import QuestionDict, shuffled

EXAMS: list[dict] = [
    {"name": "SSC CGL", "slug": "ssc-cgl", "category": "ssc",
     "description": "Combined Graduate Level — Tier 1 (100 Q, 200 marks, 60 min) and Tier 2 for Group B/C posts.",
     "pattern": {"tier1": {"questions": 100, "marks": 200, "duration_minutes": 60, "sections": ["Reasoning", "General Awareness", "Quantitative Aptitude", "English"], "negative_marks": 0.25}, "medium": "English / Hindi"}},
    {"name": "SSC CHSL", "slug": "ssc-chsl", "category": "ssc",
     "description": "Combined Higher Secondary Level — Tier 1 for LDC/DEO posts, 100 questions in 60 minutes.",
     "pattern": {"tier1": {"questions": 100, "marks": 200, "duration_minutes": 60, "sections": ["Reasoning", "General Awareness", "Quantitative Aptitude", "English"], "negative_marks": 0.25}, "medium": "English / Hindi"}},
    {"name": "SSC MTS", "slug": "ssc-mts", "category": "ssc",
     "description": "Multi Tasking Staff — Session 1 objective test of 90 questions in 90 minutes.",
     "pattern": {"session1": {"questions": 90, "marks": 270, "duration_minutes": 90, "sections": ["Numerical & Mathematical Ability", "Reasoning Ability", "General Awareness"], "negative_marks": 0}, "medium": "English / Hindi"}},
    {"name": "SSC GD", "slug": "ssc-gd", "category": "ssc",
     "description": "General Duty constable recruitment for CAPFs, SSF and AR — 80 questions in 60 minutes.",
     "pattern": {"cbt": {"questions": 80, "marks": 160, "duration_minutes": 60, "sections": ["General Intelligence", "General Knowledge", "Elementary Mathematics", "English / Hindi"], "negative_marks": 0.25}}},
    {"name": "IBPS PO", "slug": "ibps-po", "category": "banking",
     "description": "Probationary Officer preliminary exam — 100 questions, 60 minutes, sectional timings.",
     "pattern": {"prelims": {"questions": 100, "marks": 100, "duration_minutes": 60, "sections": ["English Language", "Quantitative Aptitude", "Reasoning Ability"], "negative_marks": 0.25}, "mains": {"questions": 155, "duration_minutes": 180}}},
    {"name": "IBPS Clerk", "slug": "ibps-clerk", "category": "banking",
     "description": "Clerical cadre preliminary exam — 100 questions across English, quant and reasoning in 60 minutes.",
     "pattern": {"prelims": {"questions": 100, "marks": 100, "duration_minutes": 60, "sections": ["English Language", "Quantitative Aptitude", "Reasoning Ability"], "negative_marks": 0.25}}},
    {"name": "SBI PO", "slug": "sbi-po", "category": "banking",
     "description": "State Bank of India Probationary Officer — preliminary and mains rounds with sectional timing.",
     "pattern": {"prelims": {"questions": 100, "marks": 100, "duration_minutes": 60, "sections": ["English Language", "Quantitative Aptitude", "Reasoning Ability"], "negative_marks": 0.25}}},
    {"name": "SBI Clerk", "slug": "sbi-clerk", "category": "banking",
     "description": "Junior Associate recruitment — 100 question preliminary examination in 60 minutes.",
     "pattern": {"prelims": {"questions": 100, "marks": 100, "duration_minutes": 60, "sections": ["English Language", "Quantitative Aptitude", "Reasoning Ability"], "negative_marks": 0.25}}},
    {"name": "RBI Assistant", "slug": "rbi-assistant", "category": "rbi",
     "description": "Reserve Bank of India Assistant preliminary exam — 100 questions in 60 minutes with negative marking.",
     "pattern": {"prelims": {"questions": 100, "marks": 100, "duration_minutes": 60, "sections": ["Reasoning", "Quantitative Aptitude", "English Language"], "negative_marks": 0.25}, "language_test": "Local language"}},
    {"name": "RRB NTPC", "slug": "rrb-ntpc", "category": "railway",
     "description": "Non-Technical Popular Categories CBT 1 — 100 questions in 90 minutes for graduate and undergraduate posts.",
     "pattern": {"cbt1": {"questions": 100, "marks": 100, "duration_minutes": 90, "sections": ["General Awareness", "Mathematics", "Reasoning"], "negative_marks": 0.33}}},
    {"name": "RRB Group D", "slug": "rrb-group-d", "category": "railway",
     "description": "Level 1 posts CBT — 100 questions covering general science, general awareness and reasoning.",
     "pattern": {"cbt": {"questions": 100, "marks": 100, "duration_minutes": 90, "sections": ["General Science", "General Awareness", "Reasoning", "Mathematics"], "negative_marks": 0.33}}},
    {"name": "UPSC Foundation", "slug": "upsc-foundation", "category": "upsc",
     "description": "Foundation track for the Civil Services Examination — prelims CSAT pattern plus static GS preparation.",
     "pattern": {"prelims": {"papers": ["General Studies I (100 Q, 200 marks, 120 min)", "CSAT (80 Q, 200 marks, 120 min)"], "negative_marks": 0.66}, "focus": ["Polity", "History", "Geography", "Economy", "Science & Tech"]}},
    {"name": "State Government Exams", "slug": "state-government-exams", "category": "state",
     "description": "State PSC, police and clerical examinations — state-level patterns built on the same core subjects.",
     "pattern": {"common_sections": ["General Knowledge", "Reasoning", "Quantitative Aptitude", "Regional Language"], "varies_by_state": True}},
]

MOCK_SPECS: list[dict] = [
    {"slug": "ssc-cgl-mock-1", "title": "SSC CGL Tier 1 Mock Test 1", "category": "ssc",
     "description": "Full-length SSC CGL Tier 1 pattern: 4 sections, 100 questions, 200 marks, 60 minutes with 0.25 negative marking.",
     "duration_minutes": 60, "marks_per_question": 2, "total_questions": 100,
     "sections": [("Reasoning", "reasoning", 25), ("General Awareness", "ga", 25), ("Quantitative Aptitude", "quant", 25), ("English Language", "english", 25)]},
    {"slug": "ssc-chsl-mock-1", "title": "SSC CHSL Tier 1 Mock Test 1", "category": "chsl",
     "description": "SSC CHSL Tier 1 simulation — 100 questions across reasoning, GA, quant and English in 60 minutes.",
     "duration_minutes": 60, "marks_per_question": 2, "total_questions": 100,
     "sections": [("Reasoning", "reasoning", 25), ("General Awareness", "ga", 25), ("Quantitative Aptitude", "quant", 25), ("English Language", "english", 25)]},
    {"slug": "ibps-po-mock-1", "title": "Banking (IBPS PO) Prelims Mock Test 1", "category": "banking",
     "description": "IBPS PO Prelims pattern — English 30, Quant 30, Reasoning 40 with sectional timing and negative marking.",
     "duration_minutes": 60, "marks_per_question": 1, "total_questions": 100,
     "sections": [("English Language", "english", 30), ("Quantitative Aptitude", "quant", 30), ("Reasoning Ability", "reasoning", 40)]},
    {"slug": "rbi-assistant-mock-1", "title": "RBI Assistant Prelims Mock Test 1", "category": "rbi",
     "description": "RBI Assistant Prelims simulation — Reasoning 35, Quant 35, English 30 in 60 minutes.",
     "duration_minutes": 60, "marks_per_question": 1, "total_questions": 100,
     "sections": [("Reasoning", "reasoning", 35), ("Quantitative Aptitude", "quant", 35), ("English Language", "english", 30)]},
    {"slug": "rrb-ntpc-mock-1", "title": "Railway (RRB NTPC) CBT 1 Mock Test 1", "category": "railway",
     "description": "RRB NTPC CBT 1 pattern — GA 40, Mathematics 30, Reasoning 30 in 90 minutes.",
     "duration_minutes": 90, "marks_per_question": 1, "total_questions": 100,
     "sections": [("General Awareness", "ga", 40), ("Mathematics", "quant", 30), ("Reasoning", "reasoning", 30)]},
]

IT_MOCK_SPECS: list[dict] = [
    {"slug": "it-python-developer-mock", "title": "Python Developer Mock Test", "category": "it",
     "description": "50-question timed assessment of Python fundamentals, libraries and problem solving for entry-level Python roles.",
     "duration_minutes": 45,
     "sections": [
         ("Core Concepts", ["python-basics", "python-variables", "python-loops", "python-functions"], 30),
         ("Applied Scenarios", ["python-oop", "python-file-handling", "python-apis", "python-fastapi"], 20),
     ]},
    {"slug": "it-backend-developer-mock", "title": "Backend Developer Mock Test", "category": "it",
     "description": "Backend engineering assessment covering FastAPI, REST design, PostgreSQL, SQLAlchemy and authentication.",
     "duration_minutes": 45,
     "sections": [
         ("Core Concepts", ["backend-fastapi", "backend-rest-apis", "backend-postgresql", "backend-sqlalchemy", "backend-authentication"], 30),
         ("Applied Scenarios", ["backend-deployment", "python-fastapi", "python-apis", "sql-joins"], 20),
     ]},
    {"slug": "it-fullstack-developer-mock", "title": "Full Stack Developer Mock Test", "category": "it",
     "description": "Combined frontend and backend assessment: HTML, CSS, JavaScript, React, FastAPI and API security.",
     "duration_minutes": 45,
     "sections": [
         ("Core Concepts", ["frontend-html", "frontend-css", "frontend-javascript", "backend-fastapi"], 30),
         ("Applied Scenarios", ["frontend-react", "frontend-tailwind", "backend-rest-apis", "backend-authentication"], 20),
     ]},
    {"slug": "it-data-analyst-mock", "title": "Data Analyst Mock Test", "category": "it",
     "description": "Analyst assessment across SQL queries, joins, aggregation, window functions and data handling in Python.",
     "duration_minutes": 45,
     "sections": [
         ("Core Concepts", ["sql-basic-queries", "sql-joins", "sql-group-by", "sql-subqueries"], 30),
         ("Applied Scenarios", ["sql-window-functions", "python-functions", "python-file-handling", "dsa-dp"], 20),
     ]},
    {"slug": "it-technical-support-mock", "title": "Technical Support Engineer Mock Test", "category": "it",
     "description": "Support engineering assessment: networking and deployment fundamentals, HTTP, troubleshooting and diagnostics.",
     "duration_minutes": 45,
     "sections": [
         ("Core Concepts", ["backend-deployment", "backend-rest-apis", "backend-authentication", "backend-postgresql"], 30),
         ("Applied Scenarios", ["python-basics", "python-loops", "dsa-graphs", "frontend-javascript"], 20),
     ]},
]

PYQ_SPECS: list[dict] = [
    {"slug": "pyq-ssc-cgl-2023-percentage", "title": "SSC CGL 2023 — Percentage PYQs", "exam_slug": "ssc-cgl", "topic_slug": "percentage", "kind": "quant", "year": 2023, "count": 15},
    {"slug": "pyq-ssc-cgl-2022-profit-loss", "title": "SSC CGL 2022 — Profit and Loss PYQs", "exam_slug": "ssc-cgl", "topic_slug": "profit-and-loss", "kind": "quant", "year": 2022, "count": 15},
    {"slug": "pyq-ssc-chsl-2023-coding", "title": "SSC CHSL 2023 — Coding-Decoding PYQs", "exam_slug": "ssc-chsl", "topic_slug": "coding-decoding", "kind": "reasoning", "year": 2023, "count": 15},
    {"slug": "pyq-ssc-chsl-2022-vocabulary", "title": "SSC CHSL 2022 — Vocabulary PYQs", "exam_slug": "ssc-chsl", "topic_slug": "vocabulary", "kind": "english", "year": 2022, "count": 15},
    {"slug": "pyq-ibps-po-2023-syllogism", "title": "IBPS PO 2023 — Syllogism PYQs", "exam_slug": "ibps-po", "topic_slug": "syllogism", "kind": "reasoning", "year": 2023, "count": 15},
    {"slug": "pyq-ibps-clerk-2023-ratio", "title": "IBPS Clerk 2023 — Ratio PYQs", "exam_slug": "ibps-clerk", "topic_slug": "ratio", "kind": "quant", "year": 2023, "count": 15},
    {"slug": "pyq-sbi-po-2022-speed", "title": "SBI PO 2022 — Speed, Distance and Time PYQs", "exam_slug": "sbi-po", "topic_slug": "speed-distance-time", "kind": "quant", "year": 2022, "count": 15},
    {"slug": "pyq-sbi-clerk-2022-cloze", "title": "SBI Clerk 2022 — Cloze Test PYQs", "exam_slug": "sbi-clerk", "topic_slug": "cloze-test", "kind": "english", "year": 2022, "count": 15},
    {"slug": "pyq-rbi-assistant-2023-grammar", "title": "RBI Assistant 2023 — Grammar PYQs", "exam_slug": "rbi-assistant", "topic_slug": "grammar", "kind": "english", "year": 2023, "count": 15},
    {"slug": "pyq-rrb-ntpc-2023-history", "title": "RRB NTPC 2023 — History PYQs", "exam_slug": "rrb-ntpc", "topic_slug": "history", "kind": "ga", "year": 2023, "count": 15},
    {"slug": "pyq-rrb-group-d-2023-number-system", "title": "RRB Group D 2023 — Number System PYQs", "exam_slug": "rrb-group-d", "topic_slug": "number-system", "kind": "quant", "year": 2023, "count": 15},
    {"slug": "pyq-ssc-mts-2022-geography", "title": "SSC MTS 2022 — Geography PYQs", "exam_slug": "ssc-mts", "topic_slug": "geography", "kind": "ga", "year": 2022, "count": 15},
    {"slug": "pyq-upsc-2022-polity", "title": "UPSC Foundation 2022 — Polity PYQs", "exam_slug": "upsc-foundation", "topic_slug": "polity", "kind": "ga", "year": 2022, "count": 15},
    {"slug": "pyq-state-2023-science", "title": "State Exams 2023 — Science PYQs", "exam_slug": "state-government-exams", "topic_slug": "science", "kind": "ga", "year": 2023, "count": 15},
]

# Year-wise PYQ papers (2020-2026): one 15-question mixed-subject set per exam
# per year, mirroring each exam family's real paper weightage. Topics rotate so
# neighbouring years share as little as possible.
PYQ_YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]

_QUANT_ROT = [
    "percentage", "profit-and-loss", "ratio", "time-and-work",
    "speed-distance-time", "simple-interest", "compound-interest",
    "number-system", "algebra", "geometry",
]
_REAS_ROT = [
    "coding-decoding", "analogy", "blood-relations",
    "syllogism", "seating-arrangement", "puzzles",
]
_ENG_ROT = ["vocabulary", "grammar", "error-spotting"]
_GA_ROT = ["history", "geography", "polity", "economy", "science"]

_SUBJECT_ROT = {"quant": _QUANT_ROT, "reasoning": _REAS_ROT, "english": _ENG_ROT, "ga": _GA_ROT}

# exam_slug -> (display name, difficulty, negative marks, [(subject, count)])
PYQ_PAPER_PLAN: dict[str, tuple[str, str, float, list[tuple[str, int]]]] = {
    "ssc-cgl": ("SSC CGL", "intermediate", 0.5, [("quant", 6), ("reasoning", 4), ("english", 2), ("ga", 3)]),
    "ssc-chsl": ("SSC CHSL", "intermediate", 0.5, [("quant", 6), ("reasoning", 4), ("english", 2), ("ga", 3)]),
    "ssc-mts": ("SSC MTS", "beginner", 0.5, [("quant", 6), ("reasoning", 4), ("english", 2), ("ga", 3)]),
    "ssc-gd": ("SSC GD", "beginner", 0.5, [("quant", 6), ("reasoning", 4), ("english", 2), ("ga", 3)]),
    "ibps-po": ("IBPS PO", "intermediate", 0.25, [("quant", 6), ("reasoning", 5), ("english", 4)]),
    "ibps-clerk": ("IBPS Clerk", "intermediate", 0.25, [("quant", 6), ("reasoning", 5), ("english", 4)]),
    "sbi-po": ("SBI PO", "intermediate", 0.25, [("quant", 6), ("reasoning", 5), ("english", 4)]),
    "sbi-clerk": ("SBI Clerk", "intermediate", 0.25, [("quant", 6), ("reasoning", 5), ("english", 4)]),
    "rbi-assistant": ("RBI Assistant", "intermediate", 0.25, [("quant", 6), ("reasoning", 5), ("english", 4)]),
    "rrb-ntpc": ("RRB NTPC", "intermediate", 0.33, [("quant", 5), ("reasoning", 4), ("ga", 6)]),
    "rrb-group-d": ("RRB Group D", "beginner", 0.33, [("quant", 5), ("reasoning", 4), ("ga", 6)]),
    "upsc-foundation": ("UPSC Foundation", "advanced", 0.66, [("ga", 8), ("quant", 4), ("reasoning", 3)]),
    "state-government-exams": ("State Government Exams", "intermediate", 0.25, [("quant", 4), ("reasoning", 3), ("english", 3), ("ga", 5)]),
}


def _split_chunks(count: int) -> list[int]:
    if count >= 8:
        return [3, 3, 2]
    if count == 6:
        return [3, 3]
    if count == 5:
        return [3, 2]
    if count == 4:
        return [2, 2]
    return [count]


def _build_pyq_paper_specs() -> list[dict]:
    specs: list[dict] = []
    for exam_idx, (exam_slug, (name, difficulty, negative, plan)) in enumerate(
        PYQ_PAPER_PLAN.items()
    ):
        for year_idx, year in enumerate(PYQ_YEARS):
            mix: list[tuple[str, str, int]] = []
            for subj_pos, (subject, count) in enumerate(plan):
                rotation = _SUBJECT_ROT[subject]
                offset = (exam_idx * 3 + year_idx * 2 + subj_pos) % len(rotation)
                for step, chunk in enumerate(_split_chunks(count)):
                    topic = rotation[(offset + step) % len(rotation)]
                    mix.append((subject, topic, chunk))
            specs.append(
                {
                    "slug": f"pyq-{exam_slug}-{year}",
                    "title": f"{name} {year} PYQs",
                    "exam_slug": exam_slug,
                    "year": year,
                    "difficulty": difficulty,
                    "negative": negative,
                    "count": 15,
                    "mix": mix,
                }
            )
    return specs


PYQ_SPECS.extend(_build_pyq_paper_specs())

CURRENT_AFFAIRS: list[dict] = [
    {
        "slug": "daily-current-affairs-2023-08-24",
        "title": "Daily Current Affairs — 24 August 2023",
        "period": "daily",
        "date": date(2023, 8, 24),
        "summary": "Chandrayaan-3 creates history with a soft landing near the lunar south pole, plus national and international round-up.",
        "content": (
            "Chandrayaan-3's Vikram lander touched down near the Moon's south pole on 23 August 2023, making India the first "
            "country to land a spacecraft in that region and the fourth overall to soft-land on the Moon. ISRO named the "
            "landing site 'Shiv Shakti Point' — Statio Shiv Shakti — and the Pragyan rover began its 14-day exploration of the "
            "lunar surface.\n\n"
            "The mission was ISRO's second attempt after Chandrayaan-2's orbiter-only success in 2019. Chairman S. Somanath "
            "credited the failure-tolerant design that allowed a second chance, and the nation celebrated 'National Space Day' "
            "on 23 August.\n\n"
            "In other news, India continued its preparations for the G20 Leaders' Summit scheduled for New Delhi in September "
            "2023 under its year-long presidency, whose theme is 'Vasudhaiva Kutumbakam — One Earth, One Family, One Future'."
        ),
        "ai_content": {
            "mcqs": [
                {"question": "Chandrayaan-3's landing site near the lunar south pole is named:", "options": ["Shiv Shakti Point", "Vikram Point", "Bharat Point", "Apex Point"], "correct_index": 0, "explanation": "ISRO named the site 'Shiv Shakti Point' after the landing."},
                {"question": "Chandrayaan-3 achieved a soft landing in which year?", "options": ["2019", "2021", "2023", "2024"], "correct_index": 2, "explanation": "The landing took place on 23 August 2023."},
                {"question": "Who was the Chairman of ISRO during the Chandrayaan-3 mission?", "options": ["K. Sivan", "S. Somanath", "U. R. Rao", "R. Chidambaram"], "correct_index": 1, "explanation": "S. Somanath led ISRO during the mission."},
                {"question": "The G20 Summit 2023 was hosted by:", "options": ["Indonesia", "Brazil", "India", "Italy"], "correct_index": 2, "explanation": "India hosted the G20 Leaders' Summit in New Delhi in September 2023."},
                {"question": "India's G20 presidency theme was:", "options": ["Vasudhaiva Kutumbakam", "Earth for All", "Inclusive Growth", "Digital Future"], "correct_index": 0, "explanation": "'Vasudhaiva Kutumbakam — One Earth, One Family, One Future' was India's theme."},
            ],
            "short_questions": [
                "Why is the Moon's south pole scientifically important?",
                "What does the name 'Shiv Shakti Point' signify?",
                "List three technologies that made the soft landing possible.",
            ],
            "revision_notes": (
                "Chandrayaan-3: launched July 2023; Vikram lander soft-landed 23 Aug 2023 near south pole; site = Shiv Shakti "
                "Point; rover Pragyan explored 14 days; ISRO chairman S. Somanath; India = 4th country to soft-land, 1st near "
                "south pole; 23 Aug observed as National Space Day. G20 2023: host India, venue New Delhi, theme Vasudhaiva "
                "Kutumbakam."
            ),
        },
    },
    {
        "slug": "weekly-current-affairs-2023-08-20",
        "title": "Weekly Current Affairs — 14 to 20 August 2023",
        "period": "weekly",
        "date": date(2023, 8, 20),
        "summary": "Independence Day highlights, Chandrayaan-3's final approach and the week's key national developments.",
        "content": (
            "The 76th Independence Day was celebrated on 15 August 2023, with the Prime Minister addressing the nation from "
            "the Red Fort. The week's headline story remained Chandrayaan-3, whose orbit-raising manoeuvres brought the "
            "propulsion module and lander into position for the powered descent planned for 23 August.\n\n"
            "The Prime Minister's address emphasised the next decade as a period of unprecedented growth and highlighted "
            "India's achievements in space, digital public infrastructure and inclusive development.\n\n"
            "Internationally, attention stayed on India's G20 presidency ahead of the September summit, and the week also "
            "saw continued focus on monsoon coverage across the country."
        ),
        "ai_content": {
            "mcqs": [
                {"question": "The 76th Independence Day was celebrated on:", "options": ["14 August 2023", "15 August 2023", "26 January 2023", "2 October 2023"], "correct_index": 1, "explanation": "India celebrated its 76th Independence Day on 15 August 2023."},
                {"question": "The Prime Minister addresses the nation on Independence Day from:", "options": ["Rashtrapati Bhavan", "Red Fort", "Parliament", "India Gate"], "correct_index": 1, "explanation": "The Red Fort flag-hoisting ceremony is the Independence Day tradition."},
                {"question": "Which mission was in its final approach during this week?", "options": ["Gaganyaan", "Mangalyaan", "Chandrayaan-3", "Aditya-L1"], "correct_index": 2, "explanation": "Chandrayaan-3 was preparing for its 23 August landing."},
            ],
            "short_questions": [
                "Summarise the main themes of the 2023 Independence Day address.",
                "Why was Chandrayaan-3 in the news every day this week?",
            ],
            "revision_notes": (
                "Week of 14-20 Aug 2023: 76th Independence Day (15 Aug, Red Fort); Chandrayaan-3 orbit adjustments before "
                "23 Aug landing; G20 summit preparations for New Delhi; focus on digital public infrastructure and space "
                "achievements in the national address."
            ),
        },
    },
    {
        "slug": "monthly-current-affairs-2023-07",
        "title": "Monthly Current Affairs — July 2023",
        "period": "monthly",
        "date": date(2023, 7, 31),
        "summary": "Chandrayaan-3's launch, six years of GST, space-sector reforms and the month's essential revisions.",
        "content": (
            "Chandrayaan-3 lifted off from the Satish Dhawan Space Centre, Sriharikota, on 14 July 2023 aboard a LVM3 "
            "rocket. The mission carried the Vikram lander and Pragyan rover with the goal of demonstrating a safe soft "
            "landing and rover mobility on the lunar surface.\n\n"
            "July also marked six years of the Goods and Services Tax, introduced on 1 July 2017 through the 101st "
            "Constitutional Amendment. GST unified India's indirect tax structure into a single national market tax on "
            "value addition at each stage.\n\n"
            "Continued progress on India's space-sector reforms — opening avenues for private participation through IN-SPACe "
            "and NSIL — kept space entrepreneurship in the spotlight through the month."
        ),
        "ai_content": {
            "mcqs": [
                {"question": "Chandrayaan-3 was launched on:", "options": ["14 July 2023", "23 August 2023", "1 August 2023", "15 August 2023"], "correct_index": 0, "explanation": "The launch took place on 14 July 2023 from Sriharikota."},
                {"question": "GST came into force on:", "options": ["1 July 2016", "1 July 2017", "26 January 2017", "1 April 2018"], "correct_index": 1, "explanation": "GST was rolled out on 1 July 2017."},
                {"question": "Chandrayaan-3 was launched using which rocket?", "options": ["PSLV", "LVM3", "GSLV Mk II", "SSLV"], "correct_index": 1, "explanation": "The LVM3 (Launch Vehicle Mark-3) carried the mission."},
            ],
            "short_questions": [
                "What were the primary objectives of the Chandrayaan-3 mission?",
                "What problem did GST solve in India's tax structure?",
                "How do IN-SPACe and NSIL support private space participation?",
            ],
            "revision_notes": (
                "July 2023: Chandrayaan-3 launched 14 July on LVM3 from Sriharikota; payload = Vikram lander + Pragyan rover; "
                "GST completed 6 years (launched 1 July 2017, 101st Amendment); space-sector reforms enable private "
                "participation via IN-SPACe (regulator/promoter) and NSIL (commercial arm of ISRO)."
            ),
        },
    },
]

JOBS: list[dict] = [
    {"title": "SSC CGL 2026 Notification — 18,000+ Vacancies", "company": "Staff Selection Commission", "type": "government", "category": "notification",
     "description": "Combined Graduate Level Examination 2026 for Group B and Group C posts across ministries. Online application, Tier 1 and Tier 2 pattern.",
     "location": "All India", "salary": "Pay Level 4-8 (₹25,500-₹81,100)", "apply_link": "https://ssc.gov.in", "deadline": date(2026, 11, 15), "source": "ssc"},
    {"title": "SSC CHSL 2026 Application Window Open", "company": "Staff Selection Commission", "type": "government", "category": "notification",
     "description": "Combined Higher Secondary Level recruitment for LDC and DEO posts. 12th pass eligible; Tier 1 scheduled in the next cycle.",
     "location": "All India", "salary": "Pay Level 2-5", "apply_link": "https://ssc.gov.in", "deadline": date(2026, 10, 30), "source": "ssc"},
    {"title": "IBPS PO 2026 Recruitment — Probationary Officers", "company": "Institute of Banking Personnel Selection", "type": "government", "category": "notification",
     "description": "Prelims and mains for Probationary Officer posts in 11 participating public sector banks. Graduate candidates 20-30 years.",
     "location": "All India", "salary": "₹48,480-₹85,920 (initial basic)", "apply_link": "https://www.ibps.in", "deadline": date(2026, 11, 5), "source": "ibps"},
    {"title": "SBI PO 2026 Notification Released", "company": "State Bank of India", "type": "government", "category": "notification",
     "description": "Probationary Officer recruitment with preliminary, mains and psychometric assessment rounds.",
     "location": "All India", "salary": "₹48,480-₹85,920", "apply_link": "https://sbi.co.in/web/careers", "deadline": date(2026, 10, 25), "source": "sbi"},
    {"title": "RBI Assistant 2026 — 450 Vacancies", "company": "Reserve Bank of India", "type": "government", "category": "notification",
     "description": "Assistant post recruitment across RBI offices. Prelims, mains and a language proficiency test.",
     "location": "Multiple cities", "salary": "₹24,050-₹64,480", "apply_link": "https://www.rbi.org.in/Scripts/Vacancies.aspx", "deadline": date(2026, 11, 1), "source": "rbi"},
    {"title": "RRB NTPC CBT-1 Admit Card Download", "company": "Railway Recruitment Board", "type": "government", "category": "admit-card",
     "description": "Call letters for the Non-Technical Popular Categories computer-based Test 1 are live on the official RRB portal.",
     "location": "All India", "salary": "Level 2-6", "apply_link": "https://rrbonline.gov.in", "deadline": date(2026, 10, 18), "source": "rrb"},
    {"title": "SSC CGL Tier 1 Admit Card 2026", "company": "Staff Selection Commission", "type": "government", "category": "admit-card",
     "description": "Region-wise hall tickets for SSC CGL Tier 1 examination released. Carry a photo ID and reach the centre 60 minutes early.",
     "location": "All India", "salary": "-", "apply_link": "https://ssc.gov.in", "deadline": date(2026, 10, 20), "source": "ssc"},
    {"title": "RRB Group D Stage-1 Result 2026 Declared", "company": "Railway Recruitment Board", "type": "government", "category": "result",
     "description": "Provisional result and shortlist for Stage 1 CBT published with cut-off marks and normalisation details.",
     "location": "All India", "salary": "Level 1", "apply_link": "https://rrbonline.gov.in", "deadline": None, "source": "rrb"},
    {"title": "IBPS Clerk Prelims Result 2026", "company": "Institute of Banking Personnel Selection", "type": "government", "category": "result",
     "description": "Preliminary examination results and mains shortlisting for clerical cadre posts announced.",
     "location": "All India", "salary": "₹24,050-₹64,480", "apply_link": "https://www.ibps.in", "deadline": None, "source": "ibps"},
    {"title": "UPSC Civil Services 2026 Examination Calendar", "company": "Union Public Service Commission", "type": "government", "category": "upcoming",
     "description": "Annual calendar released — notification, prelims and mains dates for CSE, Engineering Services and other examinations.",
     "location": "All India", "salary": "Pay Level 10-12", "apply_link": "https://upsc.gov.in", "deadline": date(2026, 12, 10), "source": "upsc"},
    {"title": "SSC MTS 2026 Exam Dates Announced", "company": "Staff Selection Commission", "type": "government", "category": "upcoming",
     "description": "Multi Tasking Staff examination schedule published; session-wise shifts and centre allotment to follow.",
     "location": "All India", "salary": "Pay Level 1-2", "apply_link": "https://ssc.gov.in", "deadline": date(2026, 11, 28), "source": "ssc"},
    {"title": "State PSC Clerical & Secretariat Grade Notification", "company": "State Public Service Commission", "type": "government", "category": "upcoming",
     "description": "State-level clerical and secretariat services recruitment with written examination and interview stages.",
     "location": "State-wide", "salary": "State Pay Matrix Level 6-9", "apply_link": "https://upsconline.nic.in", "deadline": date(2026, 12, 5), "source": "state-psc"},
    {"title": "Python Development Intern (Paid)", "company": "Nexlify Technologies", "type": "it", "category": "internship",
     "description": "6-month paid internship building internal tools with Python and FastAPI. Mentorship, stipend and pre-placement offer potential for strong interns.",
     "location": "Remote", "salary": "₹25,000/month", "apply_link": "https://internshala.com/internships/", "deadline": date(2026, 11, 10), "source": "internshala"},
    {"title": "Frontend Engineering Intern — React", "company": "PixelForge Labs", "type": "it", "category": "internship",
     "description": "Work with the design system team on React and Tailwind components used by 2M+ users. Portfolio projects reviewed weekly.",
     "location": "Bengaluru", "salary": "₹30,000/month", "apply_link": "https://internshala.com/internships/", "deadline": date(2026, 10, 31), "source": "internshala"},
    {"title": "Data Analyst — Freshers Welcome (2026 Batch)", "company": "InsightWorks Analytics", "type": "it", "category": "fresher",
     "description": "Entry-level analyst role: SQL reporting, dashboard building and stakeholder updates. Training period of 8 weeks.",
     "location": "Hyderabad", "salary": "₹4.5-6 LPA", "apply_link": "https://www.naukri.com/data-analyst-jobs", "deadline": date(2026, 11, 20), "source": "naukri"},
    {"title": "Backend Developer (Fresher) — FastAPI", "company": "Cloudnine Systems", "type": "it", "category": "fresher",
     "description": "Build REST services with FastAPI and PostgreSQL. Strong DSA and project work preferred; 2 rounds of technical interviews.",
     "location": "Pune", "salary": "₹5-7 LPA", "apply_link": "https://www.naukri.com/backend-developer-jobs", "deadline": date(2026, 11, 18), "source": "naukri"},
    {"title": "Full Stack Trainee — MERN/Python", "company": "StackMint", "type": "it", "category": "fresher",
     "description": "12-week paid trainee programme with rotation across frontend and backend teams; conversion to full-time on completion.",
     "location": "Chennai", "salary": "₹30,000/month stipend", "apply_link": "https://www.naukri.com/", "deadline": date(2026, 10, 29), "source": "naukri"},
    {"title": "Walk-in Drive: Technical Support Engineers", "company": "HelpStack Services", "type": "it", "category": "walkin",
     "description": "Immediate openings for L1/L2 support engineers. Carry copies of your resume and ID. Voice process, rotational shifts.",
     "location": "Gurugram", "salary": "₹3.6-4.8 LPA", "apply_link": "https://www.naukri.com/", "deadline": date(2026, 10, 22), "source": "walkin"},
    {"title": "Walk-in: Junior QA Automation Engineer", "company": "TestBee Technologies", "type": "it", "category": "walkin",
     "description": "Fresher walk-in for Selenium and API test automation roles. Bring a laptop if available; coding round on the spot.",
     "location": "Noida", "salary": "₹4-5.5 LPA", "apply_link": "https://www.naukri.com/", "deadline": date(2026, 10, 24), "source": "walkin"},
    {"title": "Remote React Developer (Contract, 12 months)", "company": "RemoteBase", "type": "it", "category": "remote",
     "description": "Build dashboard interfaces with React, TypeScript and Tailwind for a global SaaS product. Async-first team across 4 time zones.",
     "location": "Remote", "salary": "₹8-12 LPA", "apply_link": "https://www.linkedin.com/jobs/", "deadline": date(2026, 11, 12), "source": "linkedin-sample"},
    {"title": "Remote Junior DevOps Engineer", "company": "ShipIt Cloud", "type": "it", "category": "remote",
     "description": "Maintain CI/CD pipelines, Dockerised services and monitoring dashboards. Linux comfort and one cloud certification preferred.",
     "location": "Remote", "salary": "₹6-9 LPA", "apply_link": "https://www.linkedin.com/jobs/", "deadline": date(2026, 11, 25), "source": "linkedin-sample"},
    {"title": "Python Developer — Automation", "company": "Zentech Solutions", "type": "it", "category": "fresher",
     "description": "Scripting and automation of business workflows using Python, pandas and REST integrations. 0-2 years experience.",
     "location": "Bengaluru", "salary": "₹5-8 LPA", "apply_link": "https://www.naukri.com/python-developer-jobs", "deadline": date(2026, 11, 8), "source": "naukri"},
    {"title": "KPO Analyst Trainee — Research", "company": "Analytix Global", "type": "it", "category": "fresher",
     "description": "Business research and market analysis for US/UK clients. Excel modelling, secondary research and client reporting.",
     "location": "Mumbai", "salary": "₹3.5-5 LPA", "apply_link": "https://www.naukri.com/", "deadline": date(2026, 11, 2), "source": "naukri"},
    {"title": "UI Engineering Intern — Design Systems", "company": "DesignOps Studio", "type": "it", "category": "internship",
     "description": "Convert Figma designs into accessible, responsive components. Ideal for someone learning React and CSS deeply.",
     "location": "Remote", "salary": "₹20,000/month", "apply_link": "https://internshala.com/internships/", "deadline": date(2026, 10, 27), "source": "internshala"},
]

DEMO_STUDENT = {
    "email": "student@careerprep.com",
    "password": "Student@123",
    "full_name": "Demo Student",
    "headline": "Aspirant — SSC CGL & Full Stack",
    "education": "B.Tech Computer Science, 2025",
    "skills": ["Python", "SQL", "Quantitative Aptitude", "Reasoning"],
    "target_exams": ["SSC CGL", "IBPS PO"],
}


def _topic_pool(kind: str, topic_slug: str) -> list[QuestionDict]:
    seen: dict[str, QuestionDict] = {}
    for difficulty in ("beginner", "intermediate", "advanced"):
        if kind == "quant":
            items = gov_quant.generate(topic_slug, difficulty, f"{topic_slug}-{difficulty}")
        elif kind == "reasoning":
            items = gov_reasoning.get_reasoning(topic_slug, difficulty)
        elif kind == "english":
            items = gov_english.get_english(topic_slug, difficulty)
        else:
            items = gov_ga.get_ga(topic_slug, difficulty)
        for item in items:
            seen.setdefault(item["question_text"], item)
    return list(seen.values())


_SUBJECT_TOPICS = {
    "quant": ["percentage", "profit-and-loss", "ratio", "time-and-work", "speed-distance-time", "simple-interest", "compound-interest", "number-system", "algebra", "geometry"],
    "reasoning": ["coding-decoding", "blood-relations", "seating-arrangement", "puzzles", "syllogism", "analogy"],
    "english": ["vocabulary", "grammar", "error-spotting", "reading-comprehension", "cloze-test"],
    "ga": ["history", "geography", "polity", "economy", "current-affairs", "science"],
}


def subject_pool(subject: str) -> list[QuestionDict]:
    seen: dict[str, QuestionDict] = {}
    for topic_slug in _SUBJECT_TOPICS[subject]:
        for item in _topic_pool(subject, topic_slug):
            seen.setdefault(item["question_text"], item)
    return list(seen.values())


def sample(pool: list[QuestionDict], count: int, seed: str) -> list[QuestionDict]:
    if len(pool) < count:
        raise ValueError(f"Pool too small: {len(pool)} < {count} ({seed})")
    return shuffled(seed).sample(pool, count)


def build_mock_sections(spec: dict) -> tuple[list[dict], list[QuestionDict]]:
    sections: list[dict] = []
    questions: list[QuestionDict] = []
    marks_per = spec["marks_per_question"]
    for name, subject, count in spec["sections"]:
        picked = sample(subject_pool(subject), count, f"{spec['slug']}-{subject}")
        for item in picked:
            item = dict(item)
            item["tags"] = [name]
            questions.append(item)
        sections.append({"name": name, "question_count": count, "marks": count * marks_per})
    if len(questions) != spec["total_questions"]:
        raise ValueError(f"{spec['slug']}: expected {spec['total_questions']} questions, got {len(questions)}")
    return sections, questions


def build_it_mock_sections(spec: dict) -> tuple[list[dict], list[QuestionDict]]:
    sections: list[dict] = []
    questions: list[QuestionDict] = []
    for name, source_slugs, count in spec["sections"]:
        pool: list[QuestionDict] = []
        seen: set[str] = set()
        for slug in source_slugs:
            for item in IT_BANKS[slug]:
                text = item[0]
                if text in seen:
                    continue
                seen.add(text)
                pool.append(
                    {
                        "question_text": item[0],
                        "options": list(item[1]),
                        "correct_index": item[2],
                        "explanation": item[3],
                        "difficulty": "intermediate",
                        "tags": [name],
                    }
                )
        picked = sample(pool, count, f"{spec['slug']}-{name}")
        questions.extend(picked)
        sections.append({"name": name, "question_count": count, "marks": count})
    return sections, questions


def build_pyq_questions(spec: dict) -> list[QuestionDict]:
    if "mix" in spec:
        out: list[QuestionDict] = []
        for kind, topic_slug, count in spec["mix"]:
            pool = _topic_pool(kind, topic_slug)
            picked = sample(pool, count, f"{spec['slug']}-{topic_slug}")
            topic_title = topic_slug.replace("-", " ").title()
            out.extend({**item, "tags": [topic_title]} for item in picked)
        return out
    pool = _topic_pool(spec["kind"], spec["topic_slug"])
    picked = sample(pool, spec["count"], spec["slug"])
    topic_title = spec["topic_slug"].replace("-", " ").title()
    return [{**item, "tags": [topic_title]} for item in picked]
