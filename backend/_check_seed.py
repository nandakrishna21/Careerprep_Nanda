from collections import Counter, defaultdict

from sqlalchemy import inspect, text

from app.core.database import SessionLocal
from app.models.entities import MockTest, Question, Quiz

db = SessionLocal()

quizzes = db.query(Quiz).all()
questions = db.query(Question).all()
qcount = Counter(q.quiz_id for q in questions)

print("--- quiz sizes by (type) ---")
sizes: dict = {}
for q in quizzes:
    sizes.setdefault(q.quiz_type, []).append(qcount.get(q.id, 0))
for key in sorted(sizes):
    vals = sizes[key]
    print(f"  {key}: n={len(vals)} min={min(vals)} max={max(vals)} total={sum(vals)}")

print("--- mocks ---")
for m in db.query(MockTest).all():
    print(
        f"  {m.slug}: category={m.category} questions={qcount.get(m.quiz_id, 0)}"
        f" total_q_field={m.total_questions} neg={m.negative_marks}"
        f" pattern_keys={sorted((m.exam_pattern or {}).keys())}"
    )

print("--- integrity ---")
bad_opt = bad_idx = empty_exp = dup_opt = 0
dup_keys = Counter()
for q in questions:
    opts = q.options if isinstance(q.options, list) else []
    if len(opts) != 4:
        bad_opt += 1
    if q.correct_index is None or not (0 <= q.correct_index < len(opts)):
        bad_idx += 1
    if not (q.explanation or "").strip():
        empty_exp += 1
    if len(set(opts)) != len(opts):
        dup_opt += 1
    dup_keys[(q.quiz_id, q.question_text)] += 1
print("  not 4 options:", bad_opt)
print("  bad correct_index:", bad_idx)
print("  empty explanation:", empty_exp)
print("  duplicate option lists:", dup_opt)
print("  duplicate question text within a quiz:", sum(1 for v in dup_keys.values() if v > 1))
print("  questions missing difficulty:", sum(1 for q in questions if not q.difficulty))

print("--- PYQ linkage ---")
pyqs = [q for q in quizzes if q.quiz_type == "pyq"]
print("  total:", len(pyqs))
print("  missing exam link:", sum(1 for q in pyqs if q.exam_id is None))
print("  missing topic link:", sum(1 for q in pyqs if q.topic_id is None))

print("--- current affairs ---")
for row in db.execute(text("SELECT slug, quiz_id, LENGTH(ai_content) FROM current_affairs")).all():
    print(" ", tuple(row))

print("--- demo attempts ---")
for row in db.execute(
    text(
        "SELECT u.email, q.slug, a.mode, a.percentage FROM quiz_attempts a "
        "JOIN users u ON u.id = a.user_id JOIN quizzes q ON q.id = a.quiz_id"
    )
).all():
    print(" ", tuple(row))

print("--- topics without lessons/quizzes ---")
print(
    db.execute(
        text(
            "SELECT COUNT(*) FROM topics t WHERE NOT EXISTS "
            "(SELECT 1 FROM lessons l WHERE l.topic_id = t.id)"
        )
    ).scalar(),
    "topics without lessons",
)
print(
    db.execute(
        text(
            "SELECT COUNT(*) FROM topics t WHERE NOT EXISTS "
            "(SELECT 1 FROM quizzes q WHERE q.topic_id = t.id)"
        )
    ).scalar(),
    "topics without quizzes",
)

print("--- courses/topics published ---")
print(db.execute(text("SELECT category, COUNT(*) FROM courses GROUP BY category")).all())
db.close()
