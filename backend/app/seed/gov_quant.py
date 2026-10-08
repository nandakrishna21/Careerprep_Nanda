"""Programmatic question generators for Quantitative Aptitude (25 unique per difficulty per topic)."""
from __future__ import annotations

import random

from app.seed.util import mcq, num_mcq, pick

QuestionDict = dict


def _percentage(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        for _ in range(25):
            k = rng.randrange(2, 40)
            pct = pick(rng, [5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
            n = 20 * k
            ans = n * pct // 100
            out.append(num_mcq(f"What is {pct}% of {n}?", ans, f"{pct}/100 x {n} = {ans}.", difficulty))
    elif difficulty == "intermediate":
        for _ in range(25):
            base = 100 * rng.randrange(2, 30)
            pct = pick(rng, [10, 20, 25, 40, 50, 60])
            final = base + base * pct // 100
            out.append(
                num_mcq(
                    f"The population of a town increased from {base} to {final}. What is the percentage increase?",
                    pct,
                    f"Increase = {final} - {base} = {final - base}. ({final - base})/{base} x 100 = {pct}%.",
                    difficulty,
                )
            )
    else:
        for _ in range(25):
            if rng.random() < 0.4:
                pct = pick(rng, [10, 20, 30, 40, 50, 60])
                net = pct * pct // 100
                out.append(
                    mcq(
                        f"If the price of an article is increased by {pct}% and then decreased by {pct}%, what is the net change in price?",
                        f"{net}% decrease",
                        [f"{pct}% decrease", f"{net}% increase", "No change"],
                        f"Equal rise and fall of x% gives a net x²/100% decrease = {pct}²/100 = {net}% decrease.",
                        difficulty,
                    )
                )
            else:
                a, b = pick(
                    rng,
                    [
                        (10, 20), (20, 10), (20, 20), (40, 10), (10, 40), (50, 10), (10, 50),
                        (20, 50), (50, 20), (40, 20), (20, 40), (25, 20), (20, 25), (50, 40),
                        (40, 50), (25, 40), (40, 25), (30, 20), (20, 30), (30, 40), (40, 30),
                        (60, 10), (10, 60), (60, 20), (20, 60),
                    ],
                )
                net = a - b - a * b // 100
                if net > 0:
                    answer = f"{net}% increase"
                elif net < 0:
                    answer = f"{-net}% decrease"
                else:
                    answer = "No change"
                out.append(
                    mcq(
                        f"The price of an article is increased by {a}% and then decreased by {b}%. What is the net change?",
                        answer,
                        [f"{a}% increase", f"{b}% decrease", "No change"],
                        f"(1 + {a}/100)(1 - {b}/100) - 1 = {net / 100:+.2f}, i.e. {answer.lower()}.",
                        difficulty,
                    )
                )
    return out


def _profit_loss(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        for _ in range(25):
            cp = pick(rng, [100, 200, 400, 500, 800, 1000, 1200, 1500, 2000, 2500])
            gain = pick(rng, [10, 15, 20, 25, 50])
            sp = cp + cp * gain // 100
            out.append(
                num_mcq(
                    f"A shopkeeper bought an article for Rs. {cp} and sold it at a profit of {gain}%. Find the selling price.",
                    sp,
                    f"SP = CP x (100 + gain)/100 = {cp} x {100 + gain}/100 = Rs. {sp}.",
                    difficulty,
                )
            )
    elif difficulty == "intermediate":
        for _ in range(25):
            loss = pick(rng, [10, 20, 25, 50])
            sp = (100 - loss) * pick(rng, [4, 6, 8, 10, 12, 15, 20, 24, 25, 30, 40])
            cp = sp * 100 // (100 - loss)
            out.append(
                num_mcq(
                    f"An article is sold for Rs. {sp} at a loss of {loss}%. What was the cost price?",
                    cp,
                    f"CP = SP x 100/(100 - loss) = {sp} x 100/{100 - loss} = Rs. {cp}.",
                    difficulty,
                )
            )
    else:
        cps = [200, 400, 600, 800, 1000, 1200, 1600, 2000, 2400, 3000, 4000, 5000, 6000, 8000]
        for _ in range(25):
            cp = pick(rng, cps)
            mp = cp * 3 // 2
            disc = pick(rng, [10, 20, 30])
            sp = mp - mp * disc // 100
            profit_pct = (sp - cp) * 100 // cp
            out.append(
                num_mcq(
                    f"An article costing Rs. {cp} is marked at Rs. {mp} and a discount of {disc}% is given. Find the profit percentage.",
                    profit_pct,
                    f"SP = {mp} - {mp * disc // 100} = {sp}. Profit% = ({sp} - {cp})/{cp} x 100 = {profit_pct}%.",
                    difficulty,
                )
            )
    return out


_RATIO_PAIRS = [(2, 3), (3, 5), (4, 5), (1, 4), (5, 7), (2, 9), (3, 7), (4, 9), (5, 9), (3, 8), (7, 9), (1, 6), (6, 7), (5, 8), (7, 10), (9, 10)]
_RATIO_TRIPLE_COMBOS = [
    ((2, 3), (4, 6)), ((3, 4), (8, 12)), ((2, 5), (10, 15)), ((4, 5), (15, 20)),
    ((5, 7), (14, 21)), ((3, 5), (5, 10)), ((2, 3), (6, 9)), ((3, 4), (6, 8)),
    ((4, 5), (8, 10)), ((5, 6), (10, 12)), ((3, 7), (7, 21)), ((2, 7), (7, 14)),
    ((5, 4), (8, 40)), ((7, 3), (9, 63)), ((9, 4), (12, 48)), ((6, 5), (15, 60)),
    ((7, 5), (10, 70)), ((8, 3), (6, 48)), ((9, 5), (10, 90)), ((4, 7), (7, 28)),
    ((6, 5), (10, 15)), ((7, 6), (12, 18)), ((8, 9), (18, 24)), ((9, 8), (4, 12)),
    ((4, 3), (9, 15)), ((5, 6), (12, 20)), ((7, 8), (16, 28)), ((3, 2), (8, 14)),
    ((11, 12), (6, 18)), ((13, 15), (5, 20)), ((6, 7), (7, 21)), ((9, 10), (10, 25)),
    ((8, 5), (15, 40)), ((7, 10), (10, 35)), ((12, 11), (11, 33)),
]


def _ratio(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        for _ in range(25):
            a, b = pick(rng, _RATIO_PAIRS)
            parts = a + b
            total = parts * pick(rng, [50, 100, 150, 200, 250, 300, 400, 500])
            share_a = total * a // parts
            out.append(
                num_mcq(
                    f"Rs. {total} is divided between A and B in the ratio {a}:{b}. What is A's share?",
                    share_a,
                    f"Total parts = {a} + {b} = {parts}. A's share = {a}/{parts} x {total} = {share_a}.",
                    difficulty,
                )
            )
    elif difficulty == "intermediate":
        combos = [(2, 3, 4), (1, 2, 3), (3, 4, 5), (2, 5, 3), (4, 5, 6), (1, 3, 6), (3, 5, 7), (2, 7, 5), (4, 7, 9), (5, 8, 11), (6, 7, 13), (3, 8, 13), (7, 9, 14), (9, 11, 20), (5, 12, 17), (8, 15, 23), (11, 14, 25), (13, 17, 30), (2, 9, 13), (6, 11, 19)]
        for _ in range(25):
            a, b, c = pick(rng, combos)
            parts = a + b + c
            total = parts * pick(rng, [60, 90, 120, 150, 200, 250, 300])
            share_b = total * b // parts
            out.append(
                num_mcq(
                    f"Rs. {total} is divided among A, B and C in the ratio {a}:{b}:{c}. Find B's share.",
                    share_b,
                    f"Total parts = {parts}. B's share = {b}/{parts} x {total} = {share_b}.",
                    difficulty,
                )
            )
    else:
        for _ in range(25):
            (a, b), (b2, c) = pick(rng, _RATIO_TRIPLE_COMBOS)
            a2 = a * b2
            c2 = c * b
            g = _hcf(a2, c2)
            ra, rc = a2 // g, c2 // g
            out.append(
                mcq(
                    f"If a : b = {a} : {b} and b : c = {b2} : {c}, then a : c is:",
                    f"{ra}:{rc}",
                    [f"{rc}:{ra}", f"{ra + 1}:{rc}", f"{ra}:{rc + 1}"],
                    f"Make b common: a : c = {a} x {b2} : {c} x {b} = {a2}:{c2}. Dividing by HCF {g} gives {ra}:{rc}.",
                    difficulty,
                )
            )
    return out


def _work_pairs() -> list[tuple[int, int]]:
    values = [6, 8, 10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 48, 60, 72]
    return [(a, b) for a in values for b in values if a <= b and (a * b) % (a + b) == 0]


def _work_solo_pairs() -> list[tuple[int, int]]:
    a_values = [6, 8, 10, 12, 15, 16, 18, 20, 24, 30, 36, 40]
    t_values = [4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 30]
    return [(a, t) for a in a_values for t in t_values if t < a and (a * t) % (a - t) == 0]


def _time_work(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty in ("beginner", "intermediate"):
        pairs = _work_pairs()
        for _ in range(25):
            a, b = pick(rng, pairs)
            together = a * b // (a + b)
            out.append(
                num_mcq(
                    f"A can do a piece of work in {a} days and B can do it in {b} days. Working together, in how many days will they finish it?",
                    together,
                    f"One day's work = 1/{a} + 1/{b} = {a + b}/{a * b}. Time = {a * b}/{a + b} = {together} days.",
                    difficulty,
                )
            )
    else:
        pairs = _work_solo_pairs()
        for _ in range(25):
            a, t = pick(rng, pairs)
            b = a * t // (a - t)
            out.append(
                num_mcq(
                    f"A and B together can do a work in {t} days. A alone can do it in {a} days. In how many days can B alone finish it?",
                    b,
                    f"B's 1 day work = 1/{t} - 1/{a} = {a - t}/{a * t}. B alone = {a * t}/{a - t} = {b} days.",
                    difficulty,
                )
            )
    return out


def _speed(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        speeds = [30, 40, 45, 50, 60, 72, 75, 80, 90, 100, 120, 150]
        for _ in range(25):
            speed = pick(rng, speeds)
            hours = pick(rng, [2, 3, 4, 5, 6, 7, 8])
            dist = speed * hours
            out.append(
                num_mcq(
                    f"A car travels at {speed} km/h for {hours} hours. What distance does it cover?",
                    dist,
                    f"Distance = Speed x Time = {speed} x {hours} = {dist} km.",
                    difficulty,
                )
            )
    elif difficulty == "intermediate":
        for _ in range(25):
            if rng.random() < 0.5:
                kmh = 18 * rng.randrange(1, 26)
                ms = kmh * 5 // 18
                out.append(
                    num_mcq(
                        f"Convert {kmh} km/h into metres per second.",
                        ms,
                        f"m/s = km/h x 5/18 = {kmh} x 5/18 = {ms} m/s.",
                        difficulty,
                    )
                )
            else:
                ms = 5 * rng.randrange(1, 26)
                kmh = ms * 18 // 5
                out.append(
                    num_mcq(
                        f"Convert {ms} m/s into kilometres per hour.",
                        kmh,
                        f"km/h = m/s x 18/5 = {ms} x 18/5 = {kmh} km/h.",
                        difficulty,
                    )
                )
    else:
        for _ in range(25):
            boat = pick(rng, [8, 10, 12, 15, 16, 18, 20])
            stream = pick(rng, [2, 3, 4, 5])
            down = boat + stream
            dist = down * pick(rng, [4, 5, 6, 7, 8, 10, 12, 15])
            hours = dist // down
            out.append(
                num_mcq(
                    f"A boat's speed in still water is {boat} km/h and the stream flows at {stream} km/h. How long will it take to go {dist} km downstream?",
                    hours,
                    f"Downstream speed = {boat} + {stream} = {down} km/h. Time = {dist}/{down} = {hours} hours.",
                    difficulty,
                )
            )
    return out


def _simple_interest(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty in ("beginner", "intermediate"):
        for _ in range(25):
            principal = pick(rng, [1000, 2000, 2500, 4000, 5000, 8000, 10000, 12000, 15000, 20000])
            rate = pick(rng, [2, 3, 4, 5, 6, 8, 10, 12])
            years = pick(rng, [1, 2, 3, 4, 5, 6])
            si = principal * rate * years // 100
            out.append(
                num_mcq(
                    f"Find the simple interest on Rs. {principal} at {rate}% per annum for {years} years.",
                    si,
                    f"SI = P x R x T / 100 = {principal} x {rate} x {years} / 100 = Rs. {si}.",
                    difficulty,
                )
            )
    else:
        rates = [2, 3, 4, 5, 6, 8, 10, 12]
        years_list = [1, 2, 3, 4, 5, 6]
        principals = [1000, 2000, 2500, 4000, 5000, 6000, 8000, 10000, 12000, 12500, 15000, 16000, 20000, 25000, 40000]
        drawn = 0
        while drawn < 25:
            rate = pick(rng, rates)
            years = pick(rng, years_list)
            principal = pick(rng, principals)
            if principal * rate * years % 100:
                continue
            si = principal * rate * years // 100
            out.append(
                num_mcq(
                    f"The simple interest earned in {years} years at {rate}% per annum is Rs. {si}. Find the principal.",
                    principal,
                    f"P = SI x 100 / (R x T) = {si} x 100 / ({rate} x {years}) = Rs. {principal}.",
                    difficulty,
                )
            )
            drawn += 1
    return out


def _compound_interest(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    principals = [10000, 20000, 30000, 40000, 50000, 60000, 80000, 100000, 120000, 150000, 160000, 200000]
    rates = [4, 5, 8, 10, 12, 15, 20]
    if difficulty in ("beginner", "intermediate"):
        drawn = 0
        while drawn < 25:
            principal = pick(rng, principals)
            rate = pick(rng, rates)
            if principal * (100 + rate) ** 2 % 10000:
                continue
            amount = principal * (100 + rate) ** 2 // 10000
            ci = amount - principal
            out.append(
                num_mcq(
                    f"Find the compound interest on Rs. {principal} for 2 years at {rate}% per annum (compounded annually).",
                    ci,
                    f"Amount = {principal} x (1 + {rate}/100)^2 = {amount}. CI = {amount} - {principal} = Rs. {ci}.",
                    difficulty,
                )
            )
            drawn += 1
    else:
        drawn = 0
        while drawn < 25:
            principal = pick(rng, principals)
            rate = pick(rng, rates)
            if principal * rate * rate % 10000:
                continue
            diff = principal * rate * rate // 10000
            out.append(
                num_mcq(
                    f"For a principal of Rs. {principal} at {rate}% per annum compounded annually, what is the difference between CI and SI for 2 years?",
                    diff,
                    f"Difference = P x (R/100)^2 = {principal} x ({rate}/100)^2 = Rs. {diff}.",
                    difficulty,
                )
            )
            drawn += 1
    return out


def _number_system(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        rules = {
            2: "A number is divisible by 2 when its last digit is even.",
            3: "A number is divisible by 3 when the sum of its digits is divisible by 3.",
            4: "A number is divisible by 4 when its last two digits form a number divisible by 4.",
            5: "A number is divisible by 5 when its last digit is 0 or 5.",
            6: "A number is divisible by 6 when it is divisible by both 2 and 3.",
            7: "Use the divisibility test for 7 or simply divide to confirm.",
            8: "A number is divisible by 8 when its last three digits form a number divisible by 8.",
            9: "A number is divisible by 9 when the sum of its digits is divisible by 9.",
        }
        bases = [125, 250, 400, 500, 750, 1000, 1200, 1500, 2000, 2500, 3000, 4000]
        factors = [2, 3, 4, 5, 6, 7, 8, 9]
        for _ in range(25):
            base = pick(rng, bases)
            factor = pick(rng, factors)
            remainder = rng.randrange(0, factor)
            number = base * factor + remainder
            out.append(
                num_mcq(
                    f"What is the remainder when {number} is divided by {factor}?",
                    remainder,
                    f"{number} = {base} x {factor} + {remainder}, so the remainder is {remainder}. {rules[factor]}",
                    difficulty,
                )
            )
    elif difficulty == "intermediate":
        pairs = [
            (12, 18), (8, 12), (15, 25), (24, 36), (9, 12), (14, 21), (16, 24), (20, 30),
            (18, 30), (21, 28), (22, 33), (26, 39), (10, 15), (14, 35), (28, 42), (30, 45),
            (24, 60), (12, 30), (15, 60), (18, 24), (20, 45), (25, 40), (27, 45), (32, 48),
            (20, 28), (33, 44), (12, 45), (16, 36),
        ]
        for _ in range(25):
            a, b = pick(rng, pairs)
            hcf = _hcf(a, b)
            lcm = a * b // hcf
            ask_hcf = rng.random() < 0.5
            out.append(
                num_mcq(
                    f"What is the {'HCF' if ask_hcf else 'LCM'} of {a} and {b}?",
                    hcf if ask_hcf else lcm,
                    f"HCF({a}, {b}) = {hcf}, LCM({a}, {b}) = {lcm} (product = HCF x LCM).",
                    difficulty,
                )
            )
    else:
        divisors = [7, 9, 11, 13, 15, 17, 19, 21]
        for _ in range(25):
            divisor = pick(rng, divisors)
            remainder = rng.randrange(0, divisor)
            multiplier = rng.randrange(1000, 9000)
            number = divisor * multiplier + remainder
            out.append(
                num_mcq(
                    f"What is the remainder when {number} is divided by {divisor}?",
                    remainder,
                    f"{number} = {divisor} x {multiplier} + {remainder}, so the remainder is {remainder}.",
                    difficulty,
                )
            )
    return out


def _algebra(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        for _ in range(25):
            a = pick(rng, [2, 3, 4, 5, 6, 7, 8, 9])
            b = pick(rng, [3, 5, 7, 9, 11, 13, 15, 17])
            x = pick(rng, [2, 3, 4, 5, 6, 7, 8, 9, 10])
            lhs = a * x + b
            out.append(
                num_mcq(
                    f"Solve for x: {a}x + {b} = {lhs}",
                    x,
                    f"{a}x = {lhs} - {b} = {a * x}. x = {a * x}/{a} = {x}.",
                    difficulty,
                )
            )
    elif difficulty == "intermediate":
        pairs = [
            (3, 7), (4, 6), (2, 8), (5, 5), (4, 9), (6, 7), (1, 9), (8, 8), (2, 12), (9, 11),
            (3, 12), (6, 10), (7, 13), (4, 16), (5, 15), (8, 12), (9, 15), (10, 10), (7, 7),
            (11, 13), (12, 14), (15, 20), (13, 16), (14, 18), (16, 24), (18, 30), (20, 25),
            (21, 28), (25, 40), (30, 50), (9, 20), (12, 16), (14, 21), (15, 25),
        ]
        for _ in range(25):
            a, b = pick(rng, pairs)
            ab = a * b
            square_sum = a * a + b * b
            out.append(
                num_mcq(
                    f"If a + b = {a + b} and ab = {ab}, find a² + b².",
                    square_sum,
                    f"a² + b² = (a + b)² - 2ab = {a + b}² - 2 x {ab} = {square_sum}.",
                    difficulty,
                )
            )
    else:
        for _ in range(25):
            if rng.random() < 0.6:
                root_sum = pick(rng, [5, 7, 9, 11, 13, 15, 17, 19])
                first = rng.randrange(1, root_sum // 2 + 1)
                second = root_sum - first
                root_prod = first * second
                out.append(
                    mcq(
                        f"Find the roots of the quadratic equation x² - {root_sum}x + {root_prod} = 0.",
                        f"{first} and {second}",
                        [f"-{first} and {second}", f"{root_sum} and {root_prod}", "No real roots"],
                        f"Two numbers adding to {root_sum} and multiplying to {root_prod} are {first} and {second}.",
                        difficulty,
                    )
                )
            else:
                val = pick(rng, [3, 4, 5, 6, 7, 8, 9, 10])
                out.append(
                    num_mcq(
                        f"If x + 1/x = {val}, then x² + 1/x² equals:",
                        val * val - 2,
                        f"x² + 1/x² = (x + 1/x)² - 2 = {val}² - 2 = {val * val - 2}.",
                        difficulty,
                    )
                )
    return out


def _geometry(topic_slug: str, difficulty: str, rng: random.Random) -> list[QuestionDict]:
    out: list[QuestionDict] = []
    if difficulty == "beginner":
        values = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
        pairs = [(a, b) for a in values for b in values if a < b and a + b < 180]
        for _ in range(25):
            a, b = pick(rng, pairs)
            third = 180 - a - b
            out.append(
                num_mcq(
                    f"Two angles of a triangle measure {a}° and {b}°. What is the third angle?",
                    third,
                    f"Angle sum of a triangle = 180°. Third angle = 180 - {a} - {b} = {third}°.",
                    difficulty,
                )
            )
    elif difficulty == "intermediate":
        radii = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70]
        bases = [10, 12, 14, 16, 20, 24, 25, 30]
        heights = [6, 8, 9, 12, 15, 16, 18, 20]
        for _ in range(25):
            if rng.random() < 0.5:
                r = pick(rng, radii)
                area = 22 * r * r // 7
                out.append(
                    num_mcq(
                        f"Find the area of a circle of radius {r} cm (take π = 22/7).",
                        area,
                        f"Area = πr² = 22/7 x {r} x {r} = {area} cm².",
                        difficulty,
                    )
                )
            else:
                base = pick(rng, bases)
                height = pick(rng, heights)
                area = base * height // 2
                out.append(
                    num_mcq(
                        f"Find the area of a triangle with base {base} cm and height {height} cm.",
                        area,
                        f"Area = 1/2 x base x height = 1/2 x {base} x {height} = {area} cm².",
                        difficulty,
                    )
                )
    else:
        triples = [
            (3, 4), (5, 12), (8, 15), (7, 24), (9, 12), (20, 21), (12, 16), (9, 40),
            (10, 24), (11, 60), (20, 99), (6, 8), (15, 20), (18, 24), (28, 45), (33, 56),
            (16, 63), (36, 48), (48, 55), (24, 32),
        ]
        for _ in range(25):
            if rng.random() < 0.5:
                p, q = pick(rng, triples)
                hyp = int((p * p + q * q) ** 0.5)
                out.append(
                    num_mcq(
                        f"A right-angled triangle has perpendicular sides {p} cm and {q} cm. Find the hypotenuse.",
                        hyp,
                        f"Hypotenuse = √({p}² + {q}²) = √{p * p + q * q} = {hyp} cm.",
                        difficulty,
                    )
                )
            else:
                n = pick(rng, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20])
                total = (n - 2) * 180
                out.append(
                    num_mcq(
                        f"What is the sum of the interior angles of a polygon with {n} sides?",
                        total,
                        f"Sum = (n - 2) x 180° = {n - 2} x 180 = {total}°.",
                        difficulty,
                    )
                )
    return out


def _hcf(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def _pair_for(total: int, product: int) -> tuple[int, int]:
    for candidate in range(1, total):
        if candidate * (total - candidate) == product:
            return candidate, total - candidate
    return 1, product


GENERATORS = {
    "percentage": _percentage,
    "profit-and-loss": _profit_loss,
    "ratio": _ratio,
    "time-and-work": _time_work,
    "speed-distance-time": _speed,
    "simple-interest": _simple_interest,
    "compound-interest": _compound_interest,
    "number-system": _number_system,
    "algebra": _algebra,
    "geometry": _geometry,
}


def generate(topic_slug: str, difficulty: str, seed: str, count: int = 25) -> list[QuestionDict]:
    fn = GENERATORS[topic_slug]
    seen: dict[str, QuestionDict] = {}
    for attempt in range(12):
        rng = random.Random(seed if attempt == 0 else f"{seed}-{attempt}")
        for item in fn(topic_slug, difficulty, rng):
            seen.setdefault(item["question_text"], item)
        if len(seen) >= count:
            break
    if len(seen) < count:
        raise RuntimeError(f"{topic_slug}/{difficulty}: only {len(seen)} unique questions generated")
    return list(seen.values())[:count]
