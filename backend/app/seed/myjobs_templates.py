"""Starter templates for My Jobs List: applied roles with syllabus + strategy.

Sources: UIICL AO Scale I 2024 notification (200 posts, Generalist/Specialist
patterns + descriptive test) and UPSC EPFO APFC/EO Combined Recruitment Test
syllabus (120 Q / 300 marks / 2 hrs, +2.5, -1/3, interview 100, 75:25).
"""
from __future__ import annotations

TEMPLATES: list[dict] = [
    {
        "template_key": "uiicl-ao-scale1",
        "title": "UIICL Recruitment of Administrative Officer (Scale I)",
        "organization": "United India Insurance Company Limited (UIICL)",
        "role_name": "Administrative Officer (Scale I) — Generalist",
        "notification_link": "https://uiic.co.in",
        "apply_link": "https://uiic.co.in",
        "exam_pattern": [
            {"section": "Reasoning", "questions": 50, "marks": 50, "duration": "40 min", "medium": "Eng / Hindi", "note": "Separately timed; sectional + overall cut-offs"},
            {"section": "English Language", "questions": 50, "marks": 60, "duration": "40 min", "medium": "English", "note": "Only English medium"},
            {"section": "Quantitative Aptitude", "questions": 40, "marks": 50, "duration": "30 min", "medium": "Eng / Hindi", "note": "Separately timed"},
            {"section": "General Awareness (Financial Sector)", "questions": 40, "marks": 50, "duration": "25 min", "medium": "Eng / Hindi", "note": "Insurance + banking + economy focus"},
            {"section": "Computer Knowledge", "questions": 20, "marks": 40, "duration": "15 min", "medium": "Eng / Hindi", "note": "High marks-per-question — accuracy pays"},
            {"section": "Descriptive English (qualifying)", "questions": 2, "marks": 30, "duration": "30 min", "medium": "English", "note": "Letter Writing 10 + Essay 20; must qualify, not counted for merit"},
        ],
        "syllabus": [
            {
                "section": "Reasoning Ability",
                "topics": ["Puzzles & Seating Arrangement", "Syllogism & Venn Diagram", "Blood Relations", "Direction & Distance", "Order & Ranking", "Inequalities", "Coding-Decoding", "Machine Input-Output", "Statement-Assumption / Conclusion / Argument", "Cause & Effect"],
            },
            {
                "section": "English Language",
                "topics": ["Reading Comprehension", "Cloze Test", "Error Spotting", "Sentence Rearrangement / Para Jumbles", "Double Fillers", "Vocabulary (synonyms, idioms)", "Letter Writing & Essay (descriptive)"],
            },
            {
                "section": "Quantitative Aptitude",
                "topics": ["Simplification & Number Series", "Data Interpretation", "Percentage, Profit-Loss, SI/CI", "Time-Work, Time-Speed-Distance, Trains", "Boats-Streams, Pipes-Cisterns", "Mixtures & Alligation, Partnership", "Ages, Average, Ratio-Proportion", "Mensuration, Linear/Quadratic Equations", "Data Sufficiency"],
            },
            {
                "section": "General Awareness (Financial Sector)",
                "topics": ["Banking & Insurance awareness (IRDAI, LIC, GIC)", "RBI monetary policy, SEBI/NABARD circulars", "Budget, Basel norms, NPA/SARFAESI", "Financial markets, mutual funds, credit ratings", "Mergers/MoUs in banks & insurers", "Current affairs last 6–12 months", "Static GK: days, awards, appointments, sports"],
            },
            {
                "section": "Computer Knowledge",
                "topics": ["Hardware, software, OS basics", "MS Office, DBMS, networks & internet", "Cyber security basics", "Insurance-tech: policy admin systems"],
            },
        ],
        "strategy": (
            "UIICL AO is won on sectional balance, not one strong subject. Every objective section has its own "
            "cut-off, so never sacrifice a section. Order of attack: (1) lock Computer Knowledge — 20 questions for "
            "40 marks, the best marks-per-minute in the paper; (2) bank Reasoning puzzles/seating daily with a timer; "
            "(3) Quant via DI + simplification first, then arithmetic. General Awareness is financial-sector heavy — "
            "revise RBI/SEBI/IRDAI news, budget, insurance terms and last 6–12 months current affairs weekly, not at "
            "the end. Descriptive English only needs qualifying marks, but scripts are evaluated only if you clear the "
            "objective cut-offs — practise one letter + one essay every week in 30 minutes. Negative marking is 1/4th: "
            "attempt only when you can eliminate 2+ options. Mock cadence: 1 full 150-min mock per week early, 2 per "
            "week in the last month, always with error-log review. Interview is overall-performance based — prepare a "
            "2-minute intro linking your degree to insurance, plus 10 likely questions on UIICL, IRDAI and why general "
            "insurance."
        ),
        "preparation_plan": [
            {"phase": "Phase 1 — Foundations (Weeks 1–4)", "weeks": "1-4", "focus": ["Quant basics + simplification speed", "Reasoning puzzles daily 45 min", "Grammar + RC 30 min/day", "Computer fundamentals"], "tasks": ["Finish topic notes for all 5 sections", "50 mixed MCQs/day with error log", "Weekly financial-awareness digest", "1 descriptive letter + essay"]},
            {"phase": "Phase 2 — Sectional mastery (Weeks 5–8)", "weeks": "5-8", "focus": ["DI sets + timed sectional tests", "High-weightage puzzles/seating", "Insurance & banking awareness depth", "Descriptive under time"], "tasks": ["2 sectional tests/week per subject", "Revise error log every Sunday", "Monthly GK + IRDAI/RBI circulars", "1 full mock every weekend"]},
            {"phase": "Phase 3 — Exam temperament (Weeks 9–12)", "weeks": "9-12", "focus": ["150-min mocks with sectional timers", "Negative-marking discipline", "Rapid revision sheets"], "tasks": ["2 full mocks/week + deep review", "Only revise weak topics from mocks", "Descriptive 30-min drill weekly", "Interview prep: intro + insurance FAQs"]},
        ],
        "resources": [
            {
                "subject": "Reasoning + Quant (free classes)",
                "youtube": [
                    {"title": "Adda247 — Reasoning & Quant playlists", "url": "https://www.youtube.com/@Adda247", "note": "Free daily reasoning/quant classes + Hindu editorial streams"},
                    {"title": "Oliveboard — Banking/Insurance reasoning", "url": "https://www.youtube.com/@Oliveboard", "note": "Free concept + shortcut videos"},
                ],
                "websites": [
                    {"title": "ixamBee — Free UIIC AO Generalist mocks", "url": "https://www.ixambee.com/free-mock-tests/uiic-ao-generalist", "note": "Completely free mocks, multiple retakes"},
                    {"title": "Oliveboard — Free UIIC AO mock test", "url": "https://www.oliveboard.in/uiic-ao-mock-test/", "note": "Free mock with analytics (English + Hindi)"},
                    {"title": "Adda247 — UIIC mock kit (1 free mock)", "url": "https://www.adda247.com/uiic/mock-tests-kit", "note": "Free demo mock before paid series"},
                ],
            },
            {
                "subject": "English + Descriptive",
                "youtube": [
                    {"title": "Adda247 — English + editorial analysis", "url": "https://www.youtube.com/@Adda247", "note": "Free Hindu editorial + grammar live streams"},
                ],
                "websites": [
                    {"title": "ixamBee — UIIC AO mocks (descriptive practice)", "url": "https://www.ixambee.com/free-mock-tests/uiic-ao-generalist", "note": "Pair with weekly 30-min letter + essay drill"},
                ],
            },
            {
                "subject": "General / Financial Awareness",
                "youtube": [
                    {"title": "Adda247 — Current affairs streams", "url": "https://www.youtube.com/@Adda247", "note": "Free daily CA + financial-sector updates"},
                    {"title": "Free Jobs Information", "url": "https://www.youtube.com/@freejobsinformation", "note": "Job + exam update videos"},
                ],
                "websites": [
                    {"title": "AffairsCloud — Banking & insurance GK", "url": "https://www.affairscloud.com", "note": "Free daily banking/insurance awareness + quizzes"},
                    {"title": "BankExamsToday — Insurance awareness", "url": "https://www.bankexamstoday.com", "note": "Free insurance/banking study notes"},
                    {"title": "PIB — Official releases", "url": "https://pib.gov.in", "note": "Primary source for govt schemes, RBI/IRDAI news"},
                ],
            },
            {
                "subject": "Computer Knowledge + Official",
                "youtube": [
                    {"title": "Oliveboard — Computer awareness", "url": "https://www.youtube.com/@Oliveboard", "note": "Free computer-knowledge concept videos"},
                    {"title": "V the Techee", "url": "https://www.youtube.com/@VtheTechee", "note": "Tech explainers (computers/IT basics)"},
                ],
                "websites": [
                    {"title": "UIICL — Official site & notifications", "url": "https://uiic.co.in", "note": "Notifications, admit cards, results"},
                    {"title": "IRDAI — Insurance regulator", "url": "https://irdai.gov.in", "note": "Insurance terms + circulars for GA"},
                ],
            },
        ],
    },
    {
        "template_key": "upsc-epfo-apfc",
        "title": "UPSC EPFO APFC (Assistant Provident Fund Commissioner)",
        "organization": "Union Public Service Commission — EPFO",
        "role_name": "Assistant Provident Fund Commissioner (APFC)",
        "notification_link": "https://upsc.gov.in",
        "apply_link": "https://upsconline.nic.in",
        "exam_pattern": [
            {"section": "Combined Recruitment Test (CRT) — all 9 units below", "questions": 120, "marks": 300, "duration": "2 hours", "medium": "Hindi + English", "note": "+2.5 per correct, −1/3rd per wrong; offline pen-paper, objective"},
            {"section": "Interview / Personality Test", "questions": 1, "marks": 100, "duration": "—", "medium": "English / Hindi", "note": "Qualifying: Gen 50+, OBC 45+, SC/ST 40+; final merit CRT:Interview = 75:25"},
        ],
        "syllabus": [
            {"section": "General English", "topics": ["Comprehension & unseen passages", "Cloze test, fillers, para jumbles", "Error spotting, sentence improvement", "Synonyms/antonyms, idioms, one-word subs", "Active-passive, tenses, prepositions"]},
            {"section": "Indian Culture, Heritage & Freedom Movements", "topics": ["Ancient/medieval culture: art, architecture, saints, music, paintings", "Freedom struggle: 1857, Congress phases, Gandhian movements, revolutionaries, INA", "Current events linkages"]},
            {"section": "Population, Development & Globalization", "topics": ["Demographics, migration, urbanisation", "Development concepts, SDGs", "Globalization, trade, climate justice, inequality"]},
            {"section": "Governance & Constitution of India", "topics": ["Constitution, FRs/DPSPs, Parliament, federalism", "Panchayati Raj, governance, rights & policies"]},
            {"section": "Present Trends in Indian Economy", "topics": ["Growth, fiscal policy, inclusion", "Budget, banking, financial markets (link to current affairs)"]},
            {"section": "Accounting, Auditing, IR, Labour Laws, Insurance", "topics": ["Accounting principles, journals, statements", "Auditing basics (APFC extra)", "Labour codes, industrial relations", "Insurance principles, types, subrogation (APFC extra)"]},
            {"section": "General Science & Computer Applications", "topics": ["Physics/chem/bio everyday science", "Space tech basics (APFC extra)", "OS, MS Office, DBMS, networks, internet"]},
            {"section": "Elementary Maths, Statistics & Mental Ability", "topics": ["Number system, %, P&L, SI/CI, time-work-speed", "Mean/median/mode, data interpretation (APFC extra)", "Reasoning: series, blood relations, syllogism, puzzles"]},
            {"section": "Social Security in India + Current Events", "topics": ["Social security history, schemes, EPFO/ESIC", "National/international current affairs, govt schemes"]},
        ],
        "strategy": (
            "APFC rewards breadth with accuracy. The paper is 120 questions for 300 marks with 1/3rd negative — "
            "blind guessing destroys rank. Toppers' split: lock Labour Laws + Social Security + Accounting/Auditing/Insurance "
            "first (highest weightage and most static — revise to 90%+ accuracy), then Constitution/Governance + Economy "
            "(concept + current linkages), then English + Mental Ability (daily practice, free marks). Culture/Population/Globalization "
            "and Science/Space-Tech are vast — cover via PYQs + monthly compilations, not textbooks end-to-end. Current events: "
            "maintain a 12-month note (schemes, indices, appointments, sports, summits) and revise weekly. Maths/Stats: formula sheet "
            "for mean/median/mode + DI drills. Attempt order in the hall: strong static blocks first, then English/reasoning, then "
            "current-heavy items last with strict elimination (attempt only if 2 options eliminated). Interview (100 marks, 75:25) "
            "needs EPFO specifics — EPF Act, schemes (EPS/EDLI), APFC role, plus DAF-based answers. Solve 5+ years of EO/AO/APFC PYQs "
            "under 2-hour timers."
        ),
        "preparation_plan": [
            {"phase": "Phase 1 — High-weightage core (Weeks 1–6)", "weeks": "1-6", "focus": ["Labour laws + social security", "Accounting + auditing + insurance", "Constitution & governance"], "tasks": ["Bare-act/code summaries + 30 MCQs/day", "Accounting drills + statements practice", "Polity notes + weekly revision", "English 20 min/day"]},
            {"phase": "Phase 2 — Breadth + current (Weeks 7–12)", "weeks": "7-12", "focus": ["Economy + culture/heritage", "Population/globalization/environment", "Science + computers + stats"], "tasks": ["Monthly current-affairs compilation", "Stats formula + DI sets weekly", "Culture via PYQs + maps/charts", "1 CRT mock every 2 weeks"]},
            {"phase": "Phase 3 — CRT temperament (Weeks 13–16)", "weeks": "13-16", "focus": ["2-hour mocks, negative-mark discipline", "Interview prep alongside"], "tasks": ["1–2 full 120Q mocks/week + error log", "Only revise weak units from mocks", "EPFO interview: Act, schemes, APFC role", "Rapid-fire revision sheets last 10 days"]},
        ],
        "resources": [
            {
                "subject": "Labour Laws & Industrial Relations (highest weightage)",
                "youtube": [
                    {"title": "EduTap — Complete Labour Law 7-hr marathon", "url": "https://www.youtube.com/watch?v=097lMfolgdA", "note": "All 12 key labour laws in one free session (EPFO-focused)"},
                ],
                "websites": [
                    {"title": "EduTap — Free EPFO EO/AO + APFC starter course", "url": "https://edutap.in/upsc-epfo-courses/free-course/", "note": "Free concept classes, notes + mock tests"},
                ],
            },
            {
                "subject": "Accounting, Auditing, Insurance + Social Security",
                "youtube": [
                    {"title": "EPFO — Official channel", "url": "https://www.youtube.com/socialepfo", "note": "Schemes (EPS/EDLI), acts and explainer videos"},
                ],
                "websites": [
                    {"title": "EduTap — Free EPFO course (accounts/audit)", "url": "https://edutap.in/upsc-epfo-courses/free-course/", "note": "Free accounting + audit concept material"},
                    {"title": "EPFO — Official site", "url": "https://www.epfindia.gov.in", "note": "Acts, schemes, annual reports — primary source"},
                ],
            },
            {
                "subject": "Polity, Governance, Economy, Culture",
                "youtube": [
                    {"title": "Drishti IAS — GS + polity/economy", "url": "https://www.youtube.com/c/DrishtiIASvideos", "note": "Free polity, economy, culture lectures"},
                ],
                "websites": [
                    {"title": "PRS India — Laws & policy research", "url": "https://prsindia.org", "note": "Free bills, acts and policy briefs for governance"},
                    {"title": "PIB — Official releases", "url": "https://pib.gov.in", "note": "Schemes, indices and economy updates"},
                ],
            },
            {
                "subject": "Current Affairs + English, Maths, Reasoning",
                "youtube": [
                    {"title": "Drishti IAS — Current affairs", "url": "https://www.youtube.com/c/DrishtiIASvideos", "note": "Free daily CA + editorial analysis"},
                    {"title": "Free Jobs Information", "url": "https://www.youtube.com/@freejobsinformation", "note": "Job + exam update videos"},
                ],
                "websites": [
                    {"title": "AffairsCloud — Daily CA + quizzes", "url": "https://www.affairscloud.com", "note": "Free daily current affairs with MCQs"},
                    {"title": "UPSC — PYQs & notifications", "url": "https://upsc.gov.in", "note": "Official EPFO papers, syllabus, notices"},
                ],
            },
        ],
    },
]


def get_template(key: str) -> dict | None:
    for tpl in TEMPLATES:
        if tpl["template_key"] == key:
            return {k: (list(v) if isinstance(v, list) else v) for k, v in tpl.items()}
    return None
