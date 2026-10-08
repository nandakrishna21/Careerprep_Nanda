# CareerPrep Hub — API & Data Contract (v1)

Single source of truth for backend and frontend. All API routes are prefixed `/api`.
Errors: non-2xx returns `{"detail": "<message>"}`. Auth: `Authorization: Bearer <jwt>`.

## Conventions

- Backend: FastAPI + SQLAlchemy 2.0 (declarative, `Mapped[]`), Pydantic v2, SQLite/Postgres compatible (use `sqlalchemy.JSON` type everywhere).
- Frontend: React 18 + Vite + TS + Tailwind (`darkMode: 'class'`), zustand auth store, axios client with interceptor, react-router v6, recharts, lucide-react, react-hot-toast.
- Timestamps: ISO-8601 UTC (`datetime`). IDs: integer autoincrement. Slugs: unique strings.
- Pagination: `?page=1&page_size=20` → list endpoints return `{items: [...], total, page, page_size}` (plain arrays allowed for small fixed lists — noted per endpoint).

## Environment

```
DATABASE_URL=postgresql+psycopg://careerprep:careerprep@localhost:5432/careerprep
JWT_SECRET=<random>  JWT_ALGORITHM=HS256  ACCESS_TOKEN_EXPIRE_MINUTES=1440
GEMINI_API_KEY=  GEMINI_MODEL=gemini-2.0-flash
ADMIN_EMAIL=admin@careerprep.local  ADMIN_PASSWORD=Admin@12345
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
SMTP_HOST= SMTP_PORT=587 SMTP_USER= SMTP_PASSWORD= EMAIL_FROM=noreply@careerprep.local
ENVIRONMENT=development
```

## Roles

`student` (default), `admin`. Dependency `require_admin` guards `/api/admin/*`.

---

## 1. Database Schema

| Table | Key columns |
|---|---|
| users | id, email uq, hashed_password, full_name, role(str: student/admin), is_active bool, created_at |
| profiles | id, user_id FK uq, headline, bio, phone, education, skills JSON, target_exams JSON, avatar_color, xp int default 0, level int default 1, streak_days int default 0, last_active_date date |
| password_reset_tokens | id, user_id FK, token uq, expires_at, used bool |
| exams | id, name, slug uq, category(str), description, pattern JSON, is_published |
| courses | id, title, slug uq, category('government'/'it'), description, icon(str), level, order int, is_published, career_path bool |
| topics | id, course_id FK, title, slug uq, description, order int |
| lessons | id, topic_id FK, title, order int, content JSON `{notes, examples, practice, code, resources}` |
| quizzes | id, title, slug uq, quiz_type('topic'/'pyq'/'mock'/'current_affair'/'ai'), topic_id FK null, exam_id FK null, current_affair_id FK null, difficulty('beginner'/'intermediate'/'advanced'), duration_minutes int, negative_marks numeric, sections JSON null `[{name,question_count,marks}]`, total_questions int, is_published, created_by FK null, meta JSON `{"year":2023,"exam":"SSC CGL"}` |
| questions | id, quiz_id FK, question_text, options JSON `["a","b","c","d"]`, correct_index int, explanation text, difficulty str, order int, tags JSON |
| quiz_attempts | id, user_id FK, quiz_id FK, mode('practice'/'exam'), answers JSON `{question_id: index}`, score float, total int, correct int, wrong int, skipped int, accuracy float, time_taken_seconds int, rank int null, xp_awarded int, analysis JSON `{"weak_areas":[], "strong_areas":[], "topic_breakdown":[{name,total,correct}], "suggestions":[]}`, created_at |
| mock_tests | id, title, slug uq, category('ssc'/'banking'/'rbi'/'railway'/'chsl'), description, duration_minutes, total_questions, negative_marks, sections JSON, exam_pattern JSON, is_published, quiz_id FK uq |
| current_affairs | id, title, slug uq, period('daily'/'weekly'/'monthly'), content text, summary text, date date, ai_content JSON `{"mcqs":[...], "short_questions":[...], "revision_notes": str}`, is_published, created_at |
| study_plans | id, user_id FK, goal, exam, hours_per_day int, duration_days int, plan JSON `{"daily":[{day,items:[{time,task,hours}]}], "weekly":[...], "monthly":[...]}`, is_active bool, created_at |
| interview_sessions | id, user_id FK, role str, status('active'/'completed'), overall_score float null, summary JSON `{"strengths":[],"weaknesses":[]}`, created_at |
| interview_turns | id, session_id FK, question, user_answer, score int(1-10), strengths JSON, weaknesses JSON, improved_answer, created_at |
| resumes | id, user_id FK, title, template('modern'/'classic'/'minimal'), data JSON `{personal:{name,email,phone,location,summary}, education:[{degree,school,year}], skills:[], projects:[{name,description,link}], experience:[{role,company,period,description}]}`, ats_score int null, analysis JSON null, created_at, updated_at |
| jobs | id, title, company, type('government'/'it'), category(str: notification/upcoming_exam/admit_card/result/internship/fresher/walkin/remote), description, location, salary, apply_link, deadline date null, source, is_published, created_at |
| saved_jobs | id, user_id FK, job_id FK, status('saved'/'applied'/'interviewing'/'offer'/'rejected'), uq(user_id,job_id) |
| notifications | id, user_id FK, title, body, type, is_read bool, created_at |
| achievements | id, code uq, title, description, icon, xp_reward int, condition JSON |
| user_achievements | id, user_id FK, achievement_id FK, uq(user_id,achievement_id), unlocked_at |
| xp_events | id, user_id FK, points int, kind('quiz'/'mock'/'interview'/'streak'/'study'), ref_id null, created_at |
| study_sessions | id, user_id FK, minutes int, activity_type, topic_id FK null, created_at |

---

## 2. Auth `/api/auth`

| Method/Path | Body → Response |
|---|---|
| POST /auth/register | `{full_name,email,password}` → `{access_token, token_type:"bearer", user:{id,full_name,email,role}}` (409 if email exists; password min 8) |
| POST /auth/login | `{email,password}` → same shape (401 bad creds) |
| GET /auth/me | → `{user:{...}, profile:{...}}` |
| POST /auth/forgot-password | `{email}` → `{message, reset_token?}` reset_token included only when ENVIRONMENT=development |
| POST /auth/reset-password | `{token, password}` → `{message}` |
| POST /auth/logout | → `{message}` (client discards token) |
| PUT /profile | `{headline,bio,phone,education,skills,target_exams,avatar_color}` → profile |

Password hashing: passlib bcrypt. JWT payload `{sub: str(user_id), role}`.

## 3. Catalog `/api`

- GET `/courses?category=government|it` → `[{id,title,slug,category,description,icon,level,topic_count,career_path}]` (array)
- GET `/courses/{slug}` → course + `topics:[{id,title,slug,description,order,lesson_count,quiz_count}]`
- GET `/topics/{slug}` → topic + `course` + `lessons:[{id,title,order}]` + `quizzes:[quiz meta]`
- GET `/lessons/{id}` → `{id,title,content:{notes,examples,practice,code},topic:{...}}`
- GET `/exams` → array of exams
- GET `/exams/{slug}` → exam + `quizzes:[{...}]` + related courses

## 4. Quiz engine

- GET `/quizzes/{id}` → `{id,title,quiz_type,difficulty,duration_minutes,total_questions,negative_marks,sections,topic:{id,title},exam?,meta,mode_options:{practice:true,exam:true}}` (NO answers)
- GET `/quizzes/{id}/questions` → `[{id,question_text,options:[4],order}]` (NO correct_index/explanation)
- POST `/quizzes/{id}/attempt` body `{answers:{"<question_id>":"<int index>"}, time_taken_seconds:int, mode:"practice"|"exam"}` →
  ```
  {attempt:{id,score,total,correct,wrong,skipped,accuracy,time_taken_seconds,rank,xp_awarded,created_at},
   report:{weak_areas:[{topic,accuracy}], strong_areas:[{topic,accuracy}],
           topic_breakdown:[{name,total,correct,accuracy}],
           suggestions:[str],
           questions:[{id,question_text,options,your_answer,correct_index,explanation,is_correct}]},
   achievements_unlocked:[{code,title,icon,xp_reward}]}
  ```
  Scoring: correct = 1 (+negative_marks wrong if exam mode & quiz.negative_marks>0). Rank = dense rank over same-quiz attempts by score desc, time asc. XP = correct*10*(difficulty multiplier: beginner 1, intermediate 1.5, advanced 2), rounded; update profile xp/level/streak; insert xp_events; auto-unlock achievements.
- GET `/attempts/mine?quiz_id=` → array (newest first)
- GET `/attempts/{id}` → same report shape as submit (full)

## 5. Government module

- GET `/mock-tests?category=` → `[{id,title,slug,category,description,duration_minutes,total_questions,negative_marks,sections,quiz_id,attempts_count}]`
- GET `/mock-tests/{slug}` → detail incl. sections & exam_pattern
- Submit mock via POST `/quizzes/{quiz_id}/attempt` (mock report additionally includes `section_analysis:[{name,attempted,correct,accuracy}]` and `improvement_suggestions:[str]`)
- GET `/pyqs?exam=&topic=&difficulty=` → quiz list (`quiz_type='pyq'`, meta.year). Practice & exam mode both hit standard engine endpoints.
- GET `/current-affairs?period=daily|weekly|monthly` → list `{id,title,slug,period,date,summary}`
- GET `/current-affairs/{slug}` → detail incl. `ai_content` + linked quiz id if generated
- POST `/current-affairs/{id}/generate-quiz` (admin) → creates quiz from ai_content.mcqs, returns quiz

## 6. IT module

Same catalog endpoints (courses category=it; courses with `career_path=true` for the 9 career paths). Learning paths = courses (Python, SQL, DSA, Frontend, Backend); lessons carry notes/examples/practice/code.

## 7. AI `/api/ai` (Gemini via REST httpx, JSON mode, graceful 503 `{detail:"AI not configured"}` if no key)

- POST `/ai/quiz-generate` `{topic, difficulty, count(1-50), save?:bool, title?}` → `{questions:[{question_text,options[4],correct_index,explanation,difficulty}]}`; if save → also `{quiz_id}`
- POST `/ai/interview/start` `{role}` → `{session_id, question, question_number:1}`
- POST `/ai/interview/answer` `{session_id, answer}` → `{score(1-10), strengths:[], weaknesses:[], improved_answer, next_question|null, progress:{answered,overall_score}}` (persists turns; final turn sets session status/summary)
- GET `/ai/interview/sessions` → list; GET `/ai/interview/sessions/{id}` → session + turns
- POST `/ai/study-plan` `{goal, exam, hours_per_day, duration_days, performance?}` → `{id, plan}` (saved)
- GET `/ai/study-plans` → list; GET `/ai/study-plans/{id}`; DELETE
- POST `/ai/resume/analyze` multipart `file` (PDF) → `{ats_score, missing_keywords:[], suggestions:[], job_recommendations:[{title,reason}], extracted_text}` (pypdf extract → Gemini)
- POST `/ai/resume/polish` `{section, content, target_role}` → `{content}`
- POST `/ai/current-affairs` `{date?, articles?}` → generates daily CA content `{title,summary,content,ai_content}` (admin saves via POST /admin/current-affairs)

## 8. Resumes `/api/resumes`

- POST `/resumes` `{title, template, data}` → resume; GET `/resumes/mine` → list; GET/PUT/DELETE `/resumes/{id}`
- POST `/resumes/{id}/analyze` → runs ATS analysis on resume data, stores `ats_score`+`analysis`, returns it

## 9. Jobs `/api/jobs`

- GET `/jobs?type=government|it&category=&q=&page=` → paged `{items,total,page,page_size}` + each item `is_saved`
- GET `/jobs/{id}`; POST `/jobs/{id}/save`; PATCH `/jobs/{id}/save` `{status}`; DELETE `/jobs/{id}/save`; GET `/jobs/saved`

## 10. Progress / Leaderboard / Gamification

- GET `/progress/dashboard` → `{total_study_hours, total_quizzes, average_score, strong_topics:[{name,accuracy}], weak_topics:[], streak_days, xp, level, weekly_xp, mock_tests_taken, badges_unlocked, daily_activity:[{date,hours,quizzes}], performance_trend:[{date,score}], mock_performance:[{title,score,accuracy,date}]}`
- POST `/progress/study-session` `{minutes, activity_type, topic_id?}` → `{study_session, streak_days}`
- GET `/leaderboard?period=weekly|monthly|all_time&exam=` → `[{rank,id,full_name,avatar_color,xp,streak_days,level}]`
- GET `/achievements` → all achievements + `unlocked` bool; GET `/achievements/mine` → unlocked list
- GET `/notifications`; POST `/notifications/read` `{ids?:[]}` → all read if omitted

## 11. Search

- GET `/search?q=` → `{courses:[], topics:[], lessons:[], quizzes:[], mock_tests:[], jobs:[], current_affairs:[]}` each item `{type,title,subtitle,url}` where url is frontend path (`/gov/...`, `/it/...`, `/jobs/...`).

## 12. Admin `/api/admin` (role=admin)

- CRUD: GET/POST `/admin/courses`, PUT/DELETE `/admin/courses/{id}`; same for `/admin/topics` (`{course_id,...}`), `/admin/lessons` (`{topic_id,...}`), `/admin/quizzes`, `/admin/questions` (`{quiz_id,question_text,options,correct_index,explanation,difficulty}`)
- POST `/admin/quizzes/{id}/publish`
- GET/POST/PUT/DELETE `/admin/current-affairs`
- GET/POST/PUT/DELETE `/admin/jobs`
- GET `/admin/users?page&q=` → users w/ profile; PATCH `/admin/users/{id}` `{role?,is_active?}`; DELETE `/admin/users/{id}`
- GET `/admin/analytics` → `{users_total, users_new_7d, quizzes_total, attempts_total, jobs_total, courses_total, top_quizzes:[{title,attempts}], signups_by_day:[{date,count}], avg_score_by_day:[{date,avg}]}`

## 13. Seed data requirements

- 13 gov exams (SSC CGL, SSC CHSL, SSC MTS, SSC GD, IBPS PO, IBPS Clerk, SBI PO, SBI Clerk, RBI Assistant, RRB NTPC, RRB Group D, UPSC Foundation, State Government Exams).
- Government course with 4 subject topics: Quantitative Aptitude (Percentage, Profit and Loss, Ratio, Time and Work, Speed Distance Time, Simple Interest, Compound Interest, Number System, Algebra, Geometry), Reasoning (Coding-Decoding, Blood Relations, Seating Arrangement, Puzzles, Syllogism, Analogy), English (Vocabulary, Grammar, Error Spotting, Reading Comprehension, Cloze Test), General Awareness (History, Geography, Polity, Economy, Current Affairs, Science). Subject = course-level grouping → model as: course "Government Exams" with topics = subjects; each subject topic has child topics? Spec says subject→topics. Model: courses(category=government): "Quantitative Aptitude","Reasoning","English","General Awareness" (each a course); topics = the individual topics above; lessons = 1+ per topic; quizzes = 3 per topic (beginner/intermediate/advanced), aiming 25 questions each — generate via parameterized template generators for quant + curated banks elsewhere; quiz.total_questions reflects actual count (min 10, target 25).
- IT courses: Python Basics-path (Python, SQL, DSA, Frontend, Backend learning paths) + 9 career path courses (`career_path=true`): Python Developer, Backend Developer, Frontend Developer, Full Stack Developer, Data Analyst, Data Scientist, Technical Support Engineer, KPO Analyst, DevOps Engineer. Topics/lessons exactly per product spec (Python: Basics, Variables, Loops, Functions, OOP, File Handling, APIs, FastAPI; SQL: Basic Queries, Joins, Group By, Subqueries, Window Functions; DSA: Arrays, Strings, Linked Lists, Stacks, Queues, Trees, Graphs, DP; Frontend: HTML, CSS, JavaScript, React, Tailwind; Backend: FastAPI, REST APIs, PostgreSQL, SQLAlchemy, Authentication, Deployment). Each lesson content JSON has notes/examples/practice; each topic has ≥1 quiz.
- Mock tests: SSC CGL, SSC CHSL, Banking (IBPS PO), RBI Assistant, Railway (RRB NTPC) — 100 questions each where feasible, otherwise documented actual count; sections per exam pattern; negative marking 0.25.
- PYQ quizzes (quiz_type='pyq', meta.year) across exams/topics; 1 sample current_affairs daily item.
- Jobs: ~12 government (notifications/admit cards/results/upcoming) + ~12 IT (internship/fresher/walkin/remote).
- Achievements: first_quiz, quiz_streak_7, score_90, mock_first, interview_first, resume_first, xp_1000, night_owl? (keep ≥8).
- Admin user from env; demo student `student@careerprep.com` / `Student@123`.

## 14. Frontend routes

```
/                        Landing (logo, hero, search, Gov card, IT card, login/register)
/login /register /forgot-password /reset-password
/gov                     Gov dashboard (exam grid, subjects, mock tests, PYQ, current affairs)
/gov/exam/:slug
/gov/topic/:slug
/gov/quizzes/:id         Quiz runner (timer, review report)
/gov/mock                /gov/mock/:slug
/gov/pyqs
/gov/current-affairs  /gov/current-affairs/:slug
/it                      IT dashboard (career paths grid)
/it/path/:slug           Career path detail
/it/learn/:slug          Learning path (topic accordion, lesson view)
/it/quizzes/:id          (reuses quiz runner)
/it/mock                 IT mock tests + runner
/dashboard               Progress dashboard (charts, streak, badges)
/leaderboard
/ai/quiz-generator  /ai/interview  /ai/planner  /ai/resume  /ai/resume/analyze
/jobs                    Jobs board (+ saved, tracking)
/search?q=
/admin  /admin/:tab      (courses, quizzes, content, users, jobs, analytics)
/profile
```
Layout: public header on landing/auth; app shell with collapsible sidebar + topbar (search, theme toggle, XP/streak, avatar menu) for all `/app`-style pages. Dark/light via `class` on `<html>`, persisted in localStorage.

## 15. Core frontend files

```
src/lib/api.ts (axios instance + interceptors + typed helpers)
src/stores/auth.ts (zustand: token,user,profile,login/register/logout,hydrate from /auth/me)
src/stores/theme.ts
src/components/: Button, Input, Card, Modal, Spinner, ProgressBar, StatCard, QuizRunner, Timer, Sidebar, Topbar, DataTable, EmptyState, Badge, ThemeToggle
src/pages/... per routes above
```
