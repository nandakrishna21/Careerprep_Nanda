from app.seed.gov_reasoning import _shift, generate_coding

for d in ("beginner", "intermediate", "advanced"):
    qs = generate_coding(d, f"coding-{d}")
    texts = [q["question_text"] for q in qs]
    assert len(set(texts)) == 25, (d, len(set(texts)))
    for q in qs:
        opts = q["options"]
        assert len(opts) == 4 and len(set(opts)) == 4, (d, opts)
        assert 0 <= q["correct_index"] < len(opts), q
        if d == "advanced":
            w2 = q["question_text"].split("code for ")[1].rstrip("?")
            k = int(q["question_text"].split("each letter ")[1].split(" ")[0])
            assert opts[q["correct_index"]] == _shift(w2, k)[::-1], q
    print(d, "OK: 25 unique, options+answer verified")
