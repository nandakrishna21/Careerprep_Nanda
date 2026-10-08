from sqlalchemy import inspect, text

from app.core.database import SessionLocal
from app.models.entities import CurrentAffair, Quiz

db = SessionLocal()
print("ca cols:", [c.name for c in inspect(CurrentAffair).columns])

print("--- topic quizzes ordered by question count ---")
rows = db.execute(
    text(
        "SELECT q.slug, c.category, COUNT(x.id) AS n FROM quizzes q "
        "LEFT JOIN questions x ON x.quiz_id = q.id "
        "LEFT JOIN topics t ON t.id = q.topic_id "
        "LEFT JOIN courses c ON c.id = t.course_id "
        "WHERE q.quiz_type = 'topic' GROUP BY q.id ORDER BY n"
    )
).all()
for row in rows[:20]:
    print(" ", tuple(row))
print("  ... max:", rows[-1])

print("--- current affairs via ORM ---")
for ca in db.query(CurrentAffair).all():
    print(" ", {c: getattr(ca, c) for c in [c.name for c in inspect(CurrentAffair).columns] if c not in ("body",)})
    if ca.id:
        pass

print("--- CA-linked quizzes ---")
for q in db.query(Quiz).filter(Quiz.quiz_type == "current_affair").all():
    print(" ", q.slug, "ai_content_keys:", sorted((q.ai_content or {}).keys()) if q.ai_content else None)
db.close()
