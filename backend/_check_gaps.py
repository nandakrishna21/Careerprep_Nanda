from collections import Counter

from sqlalchemy import text

from app.core.database import SessionLocal

db = SessionLocal()
rows = db.execute(
    text(
        "SELECT c.category, c.slug AS course, t.slug AS topic, q.slug AS quiz, COUNT(x.id) AS n "
        "FROM quizzes q JOIN questions x ON x.quiz_id = q.id "
        "JOIN topics t ON t.id = q.topic_id JOIN courses c ON c.id = t.course_id "
        "WHERE q.quiz_type = 'topic' GROUP BY q.id ORDER BY n"
    )
).all()
under = [r for r in rows if r[4] < 10]
print(f"topic quizzes: {len(rows)}, under 10: {len(under)}")
by_course = Counter((r[0], r[1]) for r in under)
for k, v in sorted(by_course.items()):
    print("  ", k, v, "quizzes need topping up")
print("--- details (course/topic -> count across difficulties) ---")
agg = Counter()
for r in rows:
    agg[(r[1], r[2])] += r[4]
for r in under:
    print(f"  {r[2]:28} {r[3]:40} {r[4]}")
db.close()
