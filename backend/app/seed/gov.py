"""Government module seed: 4 courses, 27 topics, lessons and quiz banks."""
from __future__ import annotations

from app.seed import gov_english, gov_ga, gov_quant, gov_reasoning
from app.seed.util import QuestionDict

GOV_COURSES: list[dict] = [
    {
        "title": "Quantitative Aptitude",
        "slug": "quantitative-aptitude",
        "icon": "calculator",
        "level": "Beginner",
        "description": "Arithmetic, algebra and geometry built from first principles, with 750 solved practice questions across three difficulty levels.",
        "topics": [
            ("percentage", "Percentage", "Fractions, successive changes and application-based percentage sums."),
            ("profit-and-loss", "Profit and Loss", "Cost price, selling price, discount, markup and dishonest dealing."),
            ("ratio", "Ratio", "Ratio, proportion, compounding and division of quantities in a given ratio."),
            ("time-and-work", "Time and Work", "Combined work rates, efficiency, pipes and cisterns, wage division."),
            ("speed-distance-time", "Speed Distance Time", "Relative speed, trains, boats and streams, unit conversions."),
            ("simple-interest", "Simple Interest", "Principal, rate, time, amount and instalment-based interest sums."),
            ("compound-interest", "Compound Interest", "Annual and half-yearly compounding, CI-SI differences, growth rates."),
            ("number-system", "Number System", "Divisibility, HCF and LCM, remainders, primes and number properties."),
            ("algebra", "Algebra", "Identities, factorisation, linear equations and algebraic substitution."),
            ("geometry", "Geometry", "Triangles, circles, polygons, quadrilaterals and mensuration formulae."),
        ],
    },
    {
        "title": "Reasoning",
        "slug": "reasoning",
        "icon": "brain",
        "level": "Beginner",
        "description": "Logical and analytical reasoning: coding-decoding, relationships, arrangements, puzzles, syllogisms and analogies with fully solved examples.",
        "topics": [
            ("coding-decoding", "Coding-Decoding", "Letter shifts, word reversal, number codes and rule inference."),
            ("blood-relations", "Blood Relations", "Family trees, pointing puzzles and relation decoding."),
            ("seating-arrangement", "Seating Arrangement", "Linear, circular and rectangular arrangements with fixed clues."),
            ("puzzles", "Puzzles", "Floor, box, scheduling and comparison puzzles solved with grids."),
            ("syllogism", "Syllogism", "Statements, conclusions, Venn diagrams and possibility cases."),
            ("analogy", "Analogy", "Letter, word, number and functional relationships plus odd-one-out."),
        ],
    },
    {
        "title": "English",
        "slug": "english",
        "icon": "languages",
        "level": "Beginner",
        "description": "Vocabulary, grammar, error spotting, reading comprehension and cloze tests, with an explanation attached to every single answer.",
        "topics": [
            ("vocabulary", "Vocabulary", "Synonyms, antonyms, one-word substitution, idioms and phrases."),
            ("grammar", "Grammar", "Tenses, agreement, prepositions, articles, modals and comparison."),
            ("error-spotting", "Error Spotting", "Spotting grammatical errors in sentences split into parts."),
            ("reading-comprehension", "Reading Comprehension", "Passage-based questions: detail, inference, tone and vocabulary."),
            ("cloze-test", "Cloze Test", "Fill-in-the-blank passages testing cohesion, tense and collocation."),
        ],
    },
    {
        "title": "General Awareness",
        "slug": "general-awareness",
        "icon": "globe",
        "level": "Beginner",
        "description": "History, geography, polity, economy, current affairs and science — the complete static GK base every government exam tests.",
        "topics": [
            ("history", "History", "Ancient, medieval and modern India with the landmark dates and movements."),
            ("geography", "Geography", "Indian physical geography, world superlatives, rivers, soils and climate."),
            ("polity", "Polity", "Constitution, Preamble, rights, Parliament, judiciary and key articles."),
            ("economy", "Economy", "National income, inflation, banking, budget and policy instruments."),
            ("current-affairs", "Current Affairs", "How to track, revise and retain national and international news."),
            ("science", "Science", "Physics, chemistry and biology fundamentals plus everyday science."),
        ],
    },
]

LESSONS: dict[str, dict] = {
    "percentage": {
        "title": "Percentage — Core Concepts",
        "notes": "- Percent means 'per 100'. x% of N = x/100 × N.\n- To turn a fraction into a percent, multiply by 100: 3/4 = 75%.\n- Percentage change = (change ÷ original value) × 100.\n- Two successive changes of a% and b% combine to a + b + ab/100. Use negative numbers for decreases.\n- If A is p% more than B, then B is 100p/(100 + p)% less than A — the base has changed.\n- Quick technique: find 10% (divide by 10) and scale up; find 1% (divide by 100) for precise work.\n- In exams, always identify the reference (original) value before applying the percentage.",
        "examples": [
            "20% of 250 = 20/100 × 250 = 50.",
            "A price rises from ₹40 to ₹50. Increase = (10/40) × 100 = 25%.",
            "Successive 20% rise then 20% fall = 20 − 20 − (20×20)/100 = −4%, so the net change is a 4% decrease.",
        ],
        "practice": [
            "A student scores 45 out of 60. What percent is that?",
            "A town's population grows from 20,000 to 22,500. Find the growth percent.",
            "A quantity increases by 25% and then decreases by 20%. What is the net change?",
        ],
    },
    "profit-and-loss": {
        "title": "Profit and Loss — Core Concepts",
        "notes": "- Cost Price (CP) is what you pay; Selling Price (SP) is what you receive.\n- Profit = SP − CP; Loss = CP − SP. Percentages are always calculated on CP.\n- Profit% = (Profit/CP) × 100; Loss% = (Loss/CP) × 100.\n- Discount is on Marked Price (MP): SP = MP × (1 − discount%/100), so MP = SP/(1 − d/100).\n- Two successive discounts of a% and b% equal a single discount of a + b − ab/100.\n- Dishonest dealing: if a dealer gains x% by weight fraud, actual gain% = x/(100 − x) × 100.\n- Always convert to CP when percentages are asked.",
        "examples": [
            "CP = ₹200, SP = ₹250 → profit = ₹50, profit% = 50/200 × 100 = 25%.",
            "MP = ₹800 with 20% discount → SP = 800 × 0.8 = ₹640.",
            "Two discounts 10% and 20% → 10 + 20 − (10×20)/100 = 28% single equivalent discount.",
        ],
        "practice": [
            "An article bought for ₹480 is sold at a 15% profit. Find the SP.",
            "After a 25% discount a shirt sells for ₹900. What was the marked price?",
            "A trader cheats by 20% in weight. What is his profit percent?",
        ],
    },
    "ratio": {
        "title": "Ratio, Proportion and Partnership",
        "notes": "- A ratio compares two quantities of the same unit; simplify by dividing by the HCF.\n- a:b = c:d is a proportion; ad = bc (product of extremes = product of means).\n- To compare ratios, make denominators equal or convert to decimals.\n- Compounding ratios: if A:B = 2:3 and B:C = 4:5, make B equal (12) → A:B:C = 8:12:15.\n- Divide an amount in ratio a:b by working with total parts: share = amount × a/(a+b).\n- Unitary method: find the value of one unit first, then scale.\n- Partnership profits divide in the ratio of (capital × time).",
        "examples": [
            "Divide ₹7,200 in the ratio 5:7 → total parts 12, shares = ₹3,000 and ₹4,200.",
            "A:B = 2:3, B:C = 4:5 → A:B:C = 8:12:15.",
            "If 12 pens cost ₹180, one pen = ₹15 and 20 pens = ₹300 (unitary method).",
        ],
        "practice": [
            "Simplify 45:75 to its lowest form.",
            "Two partners invest ₹8,000 for 6 months and ₹12,000 for 4 months. Divide profit of ₹7,800.",
            "If a:b = 3:4 and b:c = 6:5, find a:b:c.",
        ],
    },
    "time-and-work": {
        "title": "Time, Work and Wages",
        "notes": "- Treat the whole work as 1 unit. If A finishes in a days, A's one-day work = 1/a.\n- Working together, rates add: (1/a + 1/b) per day.\n- Time taken together = ab/(a + b) for two people.\n- Efficiency method: convert days into work units (LCM of days) so efficiency = units/day — faster in exams.\n- If A is k times as good as B, A takes 1/k of B's time.\n- Wages are shared in proportion to (efficiency × days worked).\n- Pipes: an inlet adds positive rate, an outlet subtracts.",
        "examples": [
            "A does a job in 10 days, B in 15 → together 1/(1/10 + 1/15) = 6 days.",
            "A is twice as fast as B; B takes 20 days, so A takes 10 days.",
            "Work of 60 units, A does 6/day and B does 4/day → together 10/day = 6 days.",
        ],
        "practice": [
            "A and B together finish work in 8 days; A alone in 12 days. How long does B take?",
            "An inlet fills a tank in 12 hours and an outlet empties it in 18 hours. With both open, time to fill?",
            "₹2,400 is to be divided between A and B who work 5 and 7 days at equal daily wages.",
        ],
    },
    "speed-distance-time": {
        "title": "Speed, Distance and Time",
        "notes": "- Core relation: distance = speed × time. Keep units consistent.\n- Convert km/h to m/s by multiplying by 5/18; m/s to km/h by 18/5.\n- Average speed for equal distances at x and y km/h = 2xy/(x + y).\n- Relative speed: opposite directions add speeds; same direction subtract.\n- Trains: to cross a pole use train length; to cross a platform use train + platform length.\n- Boats: downstream speed = still + stream; upstream = still − stream.\n- Two objects moving towards each other: meeting time = total distance/(sum of speeds).",
        "examples": [
            "72 km/h = 72 × 5/18 = 20 m/s.",
            "A 150 m train at 54 km/h (15 m/s) crosses a pole in 150/15 = 10 seconds.",
            "Boat at 8 km/h in still water, stream 2 km/h → downstream 10, upstream 6 km/h.",
        ],
        "practice": [
            "A car covers 240 km in 3 hours. What is its speed in m/s?",
            "Two trains of 120 m and 180 m move towards each other at 20 m/s and 10 m/s. Time to cross?",
            "A man rows 15 km downstream in 3 hours and upstream in 5 hours. Find his speed in still water.",
        ],
    },
    "simple-interest": {
        "title": "Simple Interest",
        "notes": "- SI = (P × R × T)/100 where P = principal, R = rate% per annum, T = time in years.\n- Amount A = P + SI.\n- For 2 or 3 years, SI scales linearly: SI for 2 years = 2 × SI for 1 year.\n- Derivations: P = SI×100/(R×T), R = SI×100/(P×T), T = SI×100/(P×R).\n- If a sum doubles in T years, rate = 100/T %.\n- In instalment problems, interest applies for the period each instalment is outstanding.\n- Compare with compound interest: SI is on the original principal every year.",
        "examples": [
            "P = ₹5,000, R = 6%, T = 3 → SI = 5000×6×3/100 = ₹900; A = ₹5,900.",
            "SI for 1 year at 8% = ₹400 → P = 400×100/8 = ₹5,000.",
            "A sum doubles in 12 years → rate = 100/12 ≈ 8.33%.",
        ],
        "practice": [
            "Find the SI on ₹7,500 at 12% for 2 years 6 months.",
            "At what rate will ₹6,000 yield ₹900 interest in 3 years?",
            "If ₹3,000 amounts to ₹3,450 in 3 years, find the rate percent.",
        ],
    },
    "compound-interest": {
        "title": "Compound Interest",
        "notes": "- A = P(1 + R/100)^n and CI = A − P, with n the number of compounding periods.\n- Half-yearly: use R/2 and 2n; quarterly: R/4 and 4n.\n- For 2 years, CI − SI = P × (R/100)²; SI for 2 years = 2P × R/100.\n- Growth/population problems use the same formula with plus (growth) or minus (decay) rates.\n- Depreciation: value = P(1 − R/100)^n.\n- For small rates and n = 2, expanding (1 + r)² ≈ 1 + 2r + r² gives quick approximations.\n- 'Find CI' means total interest only; 'find amount' includes principal.",
        "examples": [
            "P = ₹10,000, R = 10%, n = 2 → A = 10,000 × 1.21 = ₹12,100; CI = ₹2,100.",
            "SI for 2 years at 10% on ₹5,000 = ₹1,000; CI = 5,000 × (1.1² − 1) = ₹1,050; difference ₹50 = 5,000 × 0.1².",
            "Population 8,000 growing 10% for 2 years = 8,000 × 1.21 = 9,680.",
        ],
        "practice": [
            "Find the CI on ₹16,000 at 10% per annum for 2 years.",
            "Find the difference between CI and SI on ₹20,000 at 5% for 2 years.",
            "₹25,000 depreciates at 10% per year. What is its value after 2 years?",
        ],
    },
    "number-system": {
        "title": "Number System and Divisibility",
        "notes": "- Divisibility: by 2 (even), 3 (digit sum), 4 (last two digits), 5 (ends 0/5), 8 (last three digits), 9 (digit sum), 11 (alternating sum).\n- For two numbers, HCF × LCM = product of the numbers (true for two numbers only).\n- HCF divides the difference of two numbers; LCM is a multiple of both.\n- Remainder of a^b forms cycles: keep the base's powers modulo the divisor.\n- n² − 1 is divisible by 24 when n is prime and greater than 3; squares end in 0,1,4,5,6,9.\n- (a + b)(a − b) = a² − b² is the fastest tool for products near round numbers.\n- Count factors via prime factorization exponents: (e₁+1)(e₂+1)...",
        "examples": [
            "HCF(36, 48) = 12 → LCM = 36×48/12 = 144.",
            "343 × 343 × 343 ends in 3×3×3 = 7 (last digit only).",
            "Number of factors of 72 = 2³×3² → (3+1)(2+1) = 12 factors.",
        ],
        "practice": [
            "Find the HCF and LCM of 84 and 126.",
            "What is the remainder when 7^100 is divided by 5?",
            "How many factors does 96 have?",
        ],
    },
    "algebra": {
        "title": "Algebra — Identities and Equations",
        "notes": "- Key identities: (a+b)² = a² + 2ab + b²; (a−b)² = a² − 2ab + b²; a² − b² = (a+b)(a−b).\n- Cubes: (a+b)³ = a³ + b³ + 3ab(a+b); a³ + b³ = (a+b)(a² − ab + b²); a³ − b³ = (a−b)(a² + ab + b²).\n- If a + 1/a = k, then a² + 1/a² = k² − 2 and a³ + 1/a³ = k³ − 3k.\n- To solve linear equations, isolate the variable using inverse operations.\n- Symmetric systems (x + y = a, xy = b) are solved by recognising (x + y)² = x² + y² + 2xy.\n- Factorisation first, substitution second — never expand blindly in timed exams.",
        "examples": [
            "If x + y = 10 and xy = 21, then x² + y² = 100 − 42 = 58.",
            "99² = (100 − 1)² = 10,000 − 200 + 1 = 9,801.",
            "Solve 3x − 7 = 14 → 3x = 21 → x = 7.",
        ],
        "practice": [
            "Expand (2x + 3)².",
            "If x − 1/x = 5, find x² + 1/x².",
            "Solve the system x + y = 12, x − y = 4 for x and y.",
        ],
    },
    "geometry": {
        "title": "Geometry and Mensuration",
        "notes": "- Triangle angle sum = 180°; exterior angle = sum of the two opposite interior angles.\n- Pythagoras: in a right triangle, hypotenuse² = base² + height² (3-4-5 and 5-12-13 triples are common).\n- Congruence (SSS, SAS, ASA, RHS) and similarity (AA) fix equal sides/angles and scale ratios of areas.\n- Circle: area = πr², circumference = 2πr; angle at centre = 2 × angle at the remaining arc.\n- Rectangle area = l×b; square = a²; trapezium = ½(sum of parallel sides)×height.\n- Polygon interior angles = (n − 2) × 180°; each interior angle of a regular n-gon = (n−2)×180/n.\n- Volume of cylinder = πr²h; cone = ⅓πr²h; sphere = 4/3πr³.",
        "examples": [
            "Right triangle legs 6 and 8 → hypotenuse = √(36+64) = 10.",
            "Circle radius 7 cm → area = 22/7 × 49 = 154 cm², circumference = 44 cm.",
            "Sum of interior angles of a hexagon = (6−2)×180 = 720°.",
        ],
        "practice": [
            "Find the area of a triangle with base 14 cm and height 9 cm.",
            "A rectangle has perimeter 48 cm and length 15 cm. Find its area.",
            "What is each interior angle of a regular octagon?",
        ],
    },
    "coding-decoding": {
        "title": "Coding-Decoding Techniques",
        "notes": "- Letter-shift codes: map every letter a fixed number of steps forward/backward (A→D is +3).\n- Reverse codes: reverse the word first, then shift, or shift then reverse — check both orders.\n- If 'CAT is coded as XZG', solve the rule from one word and apply it to the target word.\n- Number codes: replace letters with positions (A=1, Z=26) or reverse positions (A=26).\n- Always test the rule against all options — the first plausible match can be a trap.\n- Matrix/pair coding: read the letter pairs across rows and columns before jumping to conclusions.\n- For 'if word A is coded, how is B coded', never guess: derive the exact transformation first.",
        "examples": [
            "Shift +3: DOG → GRJ (D+3=G, O+3=R, G+3=J).",
            "Reverse then +1: SUN → NUS → OVT.",
            "A=1, Z=26 coding: 'RAM' = 18+1+13 = 32.",
        ],
        "practice": [
            "In a code, each letter moves 2 steps backward. What is the code for TREE?",
            "If PENCIL is written as LECPNI (reversed), how is ERASER written?",
            "In a code '2 9 1' means 'you are good'. What does '9 1' mean?",
        ],
    },
    "blood-relations": {
        "title": "Blood Relations and Family Trees",
        "notes": "- Draw a tree: males as □ or '−', females as ○ or '+', and connect generations top-down.\n- Decode definitions literally: 'brother's son' = nephew; 'father's mother' = grandmother.\n- Phrases like 'pointing to a photograph' introduce a third person — write the relation as an equation.\n- 'Only son/only daughter' pins the family; 'son of my mother's son' = my nephew.\n- Direction puzzles (pointing north) combine with relations — handle them separately, one step at a time.\n- When gender is undetermined (e.g., 'brother or sister'), keep both possibilities in the option.\n- Eliminate options by proving one relation wrong rather than proving another right.",
        "examples": [
            "'Son of my grandfather's only son' → grandfather's only son is my father, so his son is my brother.",
            "'Only daughter of my mother' → myself (if female) or my sister — check gender clues.",
            "A is B's sister, C is B's mother → A is C's daughter.",
        ],
        "practice": [
            "Pointing to a man, Neha said, 'His wife is the sister of my mother.' How is the man related to Neha's mother?",
            "P is Q's brother. R is Q's mother. S is R's father. How is P related to S?",
            "A is the mother of B and C. D is the son of A. How is B related to D?",
        ],
    },
    "seating-arrangement": {
        "title": "Seating Arrangement Puzzles",
        "notes": "- Linear: fix left/right orientation first — for people facing north, left is the west side; facing south it flips.\n- Circular: always place the definite clue (person X sits opposite Y) first, then attach relatives.\n- Use a scratch grid; never hold positions in your head.\n- 'Third to the left of' counts three seats; 'immediate left' is one seat.\n- Alternating conditions (boys/girls alternate) reduce free choices to two mirror cases — test both.\n- Height/age ordering problems are separate vertical sequences linked to the seating positions.\n- After placing everyone, re-check every condition — most wrong answers come from one missed clue.",
        "examples": [
            "6 facing north: A third from left end → positions A at 3rd seat from the left.\nIf B is immediate right of A, B is at 4.",
            "Circular with 8: fix P opposite Q, then use 'R is next to P but not next to Q' to place R.\nIf U is immediate right of T, fix T and U together first.",
            "Alternating boys and girls in a row: two arrangements exist (boy first or girl first) — resolve with a second clue.",
        ],
        "practice": [
            "Five people sit in a row facing north. C is at the extreme right, A is third from the right, B is between A and C. Who is at the extreme left?",
            "Around a table of 8, P sits opposite Q and R is to the immediate right of P. Where does S sit if S is opposite R?",
            "In a row of 7 facing south, who is at position 4 if the person at position 4 is the third from the left end?",
        ],
    },
    "puzzles": {
        "title": "Logic Puzzles with Grids",
        "notes": "- Classify the puzzle: floor/box (vertical), scheduling (time slots), comparison (taller/richer) or direction.\n- Build a table: rows = people, columns = attributes; mark ✓ and ✗ as you eliminate.\n- Start with the most constrained clue (the one that fixes one person/attribute exactly).\n- 'Lives on an even floor above X' style clues combine conditions — resolve them last, after anchors are fixed.\n- If two mirror solutions appear, look for a condition that breaks the tie ('is not at the corner').\n- Never assume order from the order clues are listed; transcribe every clue into the grid immediately.\n- Re-check the final arrangement against all statements — puzzle answers are all-or-nothing.",
        "examples": [
            "5 floors: B on floor 3 (anchor), A above B, C not top/bottom, D immediately above C, E on floor 1 → solve step by step in a grid.",
            "Box puzzle: box with keys is above the box with pen; use the fixed anchor and stack upwards/downwards.",
            "Scheduling: fix the person with the unique time slot first, then chain before/after relations.",
        ],
        "practice": [
            "Five people A-E live on floors 1-5. A is above B, B is on floor 2, E is on floor 1, C is immediately above D. Who lives on floor 5?",
            "Boxes 1-6 stacked: T is two boxes above S, S directly above R. If R is 4th from the bottom, where is T?",
            "Four friends visit on Mon-Thu: P on Tuesday, Q before R but after S. On which day does R visit?",
        ],
    },
    "syllogism": {
        "title": "Syllogism and Venn Diagrams",
        "notes": "- Draw a Venn diagram for every statement before reading the conclusions.\n- 'All A are B' → circle A inside B. 'Some A are B' → overlapping circles. 'No A is B' → separate circles.\n- A conclusion is valid only if it holds in EVERY possible diagram, not just one.\n- 'Some A are not B' does not imply 'Some B are not A' — but it does imply 'All A are B' is false.\n- Possibility questions ask whether a diagram can be drawn where the conclusion holds — one case is enough.\n- Complementary pairs: 'All A are B' and 'Some A are not B' form an either-or pair if they cover all cases.\n- Unknown pairs ('Some rains are storms') force both polarities — beware either-or conclusions.",
        "examples": [
            "All pens are books, all books are copies → all pens are copies (chain), some copies are not pens is not certain.",
            "Some cats are dogs: Venn overlap exists; 'All cats are dogs' is not certain.",
            "No fish is a bird, all fish are animals → some animals are not birds (certain).",
        ],
        "practice": [
            "Statements: All flowers are plants. Some plants are trees. Do 'Some flowers are trees' follow?",
            "Statements: No pen is a book. All books are copies. Which conclusion certainly follows?",
            "Statements: Some rains are storms. All storms are winds. Conclusions: I. Some rains are winds. II. All winds are rains.",
        ],
    },
    "analogy": {
        "title": "Analogy and Classification",
        "notes": "- Identify the relationship first, then look for the SAME relationship — not a related word.\n- Common pairs: tool-worker, synonym, part-whole, cause-effect, function, category-member.\n- Letter analogies: count positions (CAT → DBU is +1 each) and check forward/backward movement.\n- Number analogies: look at squares, cubes, sums or digit operations.\n- Odd-one-out requires the same rigor: two items share a category, one does not.\n- In 'A : B :: C : ?', apply the transformation rule derived from A→B to C.\n- Beware words with two meanings — the exam expects the relationship used in the given pair.",
        "examples": [
            "Doctor : Hospital :: Teacher : ? → School (workplace pair).",
            "Book : Pages :: Wheel : ? → Spokes (part of whole).",
            "ACEG : BDFH :: IKMO : ? → JLNP (each letter +1).",
        ],
        "practice": [
            "FISH : SHOAL :: BIRD : ?",
            "Find the odd one out: Copper, Brass, Bronze, Iron.",
            "If 'MANGO' is coded as 'NBHPF' (each letter +1), what is 'GUAVA' coded as?",
        ],
    },
    "vocabulary": {
        "title": "Vocabulary Building",
        "notes": "- Synonym = same meaning, antonym = opposite meaning. Read the sentence context before choosing.\n- One-word substitution: learn common sets (bibliophile = book lover, misanthrope = hater of people).\n- Idioms are non-literal: 'let the cat out of the bag' means to reveal a secret.\n- Prefixes/suffixes decode unfamiliar words: 'bene-' = good, '-cide' = killing, '-ology' = study of.\n- Learn words in pairs (word + antonym) — memory improves when anchored.\n- Eliminate options whose tone does not match (intense vs mild words are not synonyms).\n- Maintain a daily list of 10 words with a sentence each; revise weekly.",
        "examples": [
            "Ephemeral (short-lived): 'The ephemeral fame of a meme fades fast.'",
            "Meticulous → precise; antonym → careless.",
            "Idiom: 'a blessing in disguise' = a misfortune that turns out well.",
        ],
        "practice": [
            "Choose the synonym of 'Obsequious'.",
            "Give the antonym of 'Benevolent'.",
            "What is the one-word substitution for 'one who does not believe in God'?",
        ],
    },
    "grammar": {
        "title": "English Grammar Essentials",
        "notes": "- Subject-verb agreement: singular subject takes a singular verb (each, neither, either, 'the number of' are singular).\n- Tenses: keep one tense per clause unless the time frame genuinely changes.\n- Articles: 'the' for unique/specific nouns; 'a/an' for singular countable first mentions; no article for plurals generally.\n- Prepositions are collocations: good AT, depend ON, arrive AT/IN, senior TO (not than).\n- Conditionals: if + present, will + verb (first); if + past, would + verb (second).\n- Reported speech shifts tense back one step when the reporting verb is past.\n- Comparatives: two things → comparative; more than two → superlative.",
        "examples": [
            "'Neither of the boys was present' — 'neither' is singular.",
            "'If it rains, we will cancel the match' — first conditional.",
            "'She has been living here since 2019' — present perfect continuous with 'since'.",
        ],
        "practice": [
            "Fill in: He ____ (go/goes/going) to the office every day.",
            "Fill in: I am good ____ mathematics.",
            "Choose the correct tag: Let's start, ____?",
        ],
    },
    "error-spotting": {
        "title": "Error Spotting Method",
        "notes": "- Read the whole sentence for meaning first, then scan each part for grammar.\n- Part (a) usually holds subject/verb; check agreement and articles there.\n- Watch for: 'one of the + plural noun', 'each/either/neither + singular verb', 'senior to' (not than), 'despite of' (wrong — use despite).\n- 'The number of' takes a singular verb; 'a number of' takes plural.\n- Redundancy errors: 'the reason is because', 'each and every', double negatives.\n- If a sentence reads grammatically perfect, the answer is 'No error' — do not overthink.\n- Past tense signals: 'yesterday/last year/ago' must pair with simple past, not present perfect.",
        "examples": [
            "'He do not like coffee' → error in part (a): 'does not'.",
            "'One of the boy has won' → 'one of the boys'.",
            "'I have seen him yesterday' → 'I saw him yesterday'.",
        ],
        "practice": [
            "Find the error: 'Each of the students have submitted the assignment.'",
            "Find the error: 'Despite of the rain, they went out.'",
            "Find the error: 'The number of applicants were increasing every year.'",
        ],
    },
    "reading-comprehension": {
        "title": "Reading Comprehension Strategy",
        "notes": "- Skim for the main idea first; details can be located after reading the questions.\n- Underline contrast words (however, but, although) — the author's real opinion usually follows them.\n- Eliminate extreme options (always, never, all, none) unless the passage states them explicitly.\n- Inference questions need what is IMPLIED, not what is true outside the passage.\n- Tone questions: informative, critical, optimistic, skeptical — choose from the author's word choices.\n- 'Not true' questions are easier: three options are directly stated, one is not.\n- Vocabulary-in-context means the word's meaning in that sentence, not its dictionary meaning.",
        "examples": [
            "If the passage says 'untreated waste threatens rivers', the inference is that pollution harms river health — not that rivers dried up.",
            "A paragraph ending with 'however' signals the author's main point follows it.",
            "For 'the sun is a star', a question asking location of the sun is answered by the first line — always re-read that line.",
        ],
        "practice": [
            "Read a short passage about rivers and identify the author's tone in one word.",
            "Which word in a paragraph about automation signals disagreement with the previous sentence?",
            "In an RC passage, which option type should you eliminate first — extreme or moderate?",
        ],
    },
    "cloze-test": {
        "title": "Cloze Test Technique",
        "notes": "- Read the entire passage first to fix the tense, tone and subject before filling blanks.\n- Blank 1 often sets the tense — check verb forms across the whole passage for consistency.\n- Connectors matter: 'although' needs contrast, 'therefore' needs result, 'because' needs cause.\n- Collocations decide close calls: 'make a decision' not 'do a decision'; 'strong demand' not 'powerful demand'.\n- Parallelism: items joined by 'and' must share the same grammatical form.\n- Pronouns and articles give free clues: 'a fundamental ____' needs a singular noun.\n- Re-read the completed passage aloud — the correct answer makes it flow.",
        "examples": [
            "'The committee ____ divided' → 'are' when members disagree individually.",
            "'Completed ____ the next two years' → 'within' (deadline), not 'from'.",
            "'Not only the students but also the teacher ____ present' → 'was' (nearer subject).",
        ],
        "practice": [
            "Fill: 'He has been working here ____ 2019.' (since/for)",
            "Fill: 'The scheme ____ be completed within two years.' (shall/has)",
            "Fill: 'Ravi ____ to school every morning.' (go/goes)",
        ],
    },
    "history": {
        "title": "History — Timeline Approach",
        "notes": "- Ancient: Indus Valley cities (Harappa, Mohenjo-daro), Vedic age, Mahajanapadas, Mauryas (Ashoka) and Guptas.\n- Medieval: Delhi Sultanate (1206-1526), Mughals (Babur 1526 → Aurangzeb), regional kingdoms, Bhakti/Sufi movements.\n- Modern: British arrival (Plassey 1757, Buxar 1764), 1857 revolt, INC founded 1885, extremist phase, Gandhi's movements (Non-Cooperation 1920, Civil Disobedience 1930, Quit India 1942), independence 1947.\n- Learn dates in pairs: 1905 partition, 1909 Morley-Minto, 1919 Rowlatt/Jallianwala, 1935 Act, 1947 Partition.\n- Movements matter more than battles: names, leaders, demands, and outcomes.\n- Link reforms to leaders: Raja Ram Mohan Roy (sati), Dayananda (cow protection, Arya Samaj), Ambedkar (caste rights).\n- Revision trick: build a single one-page timeline and hang every fact on it.",
        "examples": [
            "1757 Battle of Plassey — Battle of Wandiwash (1760) — Battle of Buxar (1764) → British political power in Bengal.",
            "1919: Rowlatt Act → Jallianwala Bagh (13 April) → Non-Cooperation (1920) — protests chain.",
            "1942: Quit India ('Do or Die'); 1947: Mountbatten plan and independence on 15 August.",
        ],
        "practice": [
            "In which year was the Permanent Settlement of Bengal introduced?",
            "Match: Brahmo Samaj, Arya Samaj, Home Rule League with their founders.",
            "Which session of the Congress split Moderates and Extremists?",
        ],
    },
    "geography": {
        "title": "Geography — Physical and World Facts",
        "notes": "- India: Himalayas in the north, Peninsular plateau (Deccan) in the south, Thar desert in the west.\n- Rivers: Ganga (longest in India), Godavari (largest peninsular), Narmada/Tapi flow west into the Arabian Sea.\n- Tropic of Cancer passes through 8 Indian states; latitude lines: Equator 0°, Arctic/Antarctic 66.5°.\n- Climate: southwest monsoon (June-September), retreating monsoon, factors — latitude, altitude, relief, distance from sea.\n- Soils: black (cotton, Deccan), alluvial (north plains, agriculture), laterite (rice/tea, heavy rain).\n- World superlatives: longest river Nile, largest ocean Pacific, largest desert Sahara, deepest trench Mariana, highest peak Everest (Nepal-China border).\n- Map practice: mark rivers, mountain ranges and straits — visual memory beats rote lists.",
        "examples": [
            "Sundarbans = Ganga-Brahmaputra delta (world's largest delta).",
            "Cotton grows on black soil because it retains moisture.",
            "Lake Superior = largest freshwater lake by area; Baikal = deepest.",
        ],
        "practice": [
            "Name the 8 states the Tropic of Cancer crosses (any 5).",
            "Which Indian state has the longest coastline?",
            "Which line divides the Earth into Northern and Southern hemispheres?",
        ],
    },
    "polity": {
        "title": "Polity — Constitution Essentials",
        "notes": "- Drafting: Constituent Assembly elected 1946; Dr. B. R. Ambedkar is the 'Father of the Indian Constitution'. Adopted 26 Nov 1949, in force 26 Jan 1950.\n- Preamble: Sovereign Socialist Secular Democratic Republic ('Socialist', 'Secular', 'Integrity' added by 42nd Amendment 1976).\n- Fundamental Rights (Part III): 6 today — equality (14-18), freedom (19-22), exploitation (23-24), religion (25-28), education (21A), constitutional remedies (32).\n- Fundamental Duties: 11 (added 42nd Amendment, borrowed from USSR).\n- Parliament: President + Lok Sabha (max 552) + Rajya Sabha (max 250); Money Bill only in Lok Sabha (Art 110).\n- Judiciary: SC (Art 124-147), writs — habeas corpus, mandamus, prohibition, certiorari, quo warranto.\n- Key articles: 32 (writs), 356 (President's Rule), 360 (Financial Emergency), 280 (Finance Commission).\n- Federal features: union list, state list, concurrent list; residuary powers with the Centre.",
        "examples": [
            "42nd Amendment = 'mini constitution' (1976): added socialist, secular, integrity + Fundamental Duties.",
            "Kesavananda Bharati (1973) — basic structure doctrine.",
            "73rd Amendment (1992) — constitutional status to Panchayati Raj.",
        ],
        "practice": [
            "Which article provides for Habeas Corpus?",
            "Who appoints the Chief Election Commissioner?",
            "How many Fundamental Rights are guaranteed today?",
        ],
    },
    "economy": {
        "title": "Economy — Macro Basics",
        "notes": "- GDP = value of final goods/services produced within a country in a year; GNP adds net income from abroad.\n- Sectors: primary (agriculture/mining), secondary (manufacturing), tertiary (services).\n- Inflation = sustained rise in general price level; measured in India via CPI (retail) and WPI (wholesale).\n- Fiscal policy = government spending/taxing (budget, deficit, GST); monetary policy = RBI (repo, reverse repo, CRR, SLR, OMO).\n- Repo rate = RBI lends to banks; bank rate = long-term lending; CRR = % of deposits kept with RBI.\n- Fiscal deficit = total expenditure − total receipts excluding borrowings; financed by borrowing.\n- Budget: revenue account (taxes, salaries) vs capital account (loans, assets); 'made in' index — remember NITI Aayog replaced Planning Commission (2015).\n- Money supply measures: M0 (reserve money), M1/M2/M3 (narrow/broad money).",
        "examples": [
            "Repo 6% → banks borrow cheaper → lending rates fall → growth up, inflation risk up.",
            "Price rises ₹50 → ₹60 = 20% inflation on that item (10/50).",
            "GST (2017) = one nation, one tax on the value chain at each stage.",
        ],
        "practice": [
            "Which body compiles the CPI in India?",
            "Define fiscal deficit with the formula.",
            "Name the repo-rate-like instrument RBI uses to absorb excess liquidity.",
        ],
    },
    "current-affairs": {
        "title": "Current Affairs — Track and Retain",
        "notes": "- Sources: The Hindu/Indian Express editorials, PIB, PRS Legislative Research, RBI bulletin, ISRO/DRDO releases.\n- Categories to track daily: polity & governance, economy, science & tech, environment, sports, awards, international.\n- Note format: date — event — why it matters (one line each). Facts without context are forgotten.\n- Static linkage: every current event maps to a static topic (a new scheme → economy; a launch → science). Link them.\n- Weekly revision of the month's notes beats daily cramming; monthly compilation before the exam.\n- For MCQs: eliminate two options immediately, then decide between the remaining using your note's exact wording.\n- Keep a 'confusables' list (committee names, indices, headquarters) — exams love swapping those.",
        "examples": [
            "Chandrayaan-3 landed 23 Aug 2023; site = Shiv Shakti Point → links to science + space section.",
            "G20 2023 in New Delhi → links to international relations + India's diplomacy.",
            "RBI inflation target 4% ±2% → links directly to the monetary policy static topic.",
        ],
        "practice": [
            "Which stadium hosted the 2023 Cricket World Cup final?",
            "Name India's Aditya-L1's orbit location.",
            "Write a one-line note on the most recent major sports event you read about.",
        ],
    },
    "science": {
        "title": "Science — Physics, Chemistry, Biology Basics",
        "notes": "- Physics: force = mass × acceleration (Newton), unit of force = newton, light speed ≈ 3×10⁸ m/s, sound needs a medium.\n- Physics laws: inertia (1st), F=ma (2nd), action-reaction (3rd), Boyle (pressure-volume), Newton's gravitation.\n- Chemistry: atom → molecule → compound; pH < 7 acidic, = 7 neutral, > 7 basic; common formulas — NaCl, H₂O, CaCO₃.\n- Periodic table trends: metals left, non-metals right, noble gases at the far right.\n- Biology: cell is the unit of life; mitochondria = powerhouse; lysosome = suicide bag; chloroplast = photosynthesis.\n- Vitamins: A (night blindness), B1 (beriberi), C (scurvy), D (rickets), K (clotting); fat-soluble = A, D, E, K.\n- Diseases: diabetes (insulin), anaemia (haemoglobin/iron), goitre (iodine).\n- Everyday science: LPG is butane/propane mix, CNG = compressed natural gas, neutron star/heavy water D₂O facts recur in exams.",
        "examples": [
            "100°C boiling, 0°C freezing — the Celsius scale anchors most numerical GK questions.",
            "O negative = universal donor; AB positive = universal recipient.",
            "1 HP = 746 watts — frequent in physics MCQs.",
        ],
        "practice": [
            "Which vitamin is fat-soluble: C or D?",
            "What is the pH of pure water at 25°C?",
            "Name the powerhouse of the cell and its function.",
        ],
    },
}


def questions_for(topic_slug: str, difficulty: str) -> list[QuestionDict]:
    quant = set(gov_quant.GENERATORS)
    if topic_slug in quant:
        return gov_quant.generate(topic_slug, difficulty, f"{topic_slug}-{difficulty}")
    if topic_slug in {"vocabulary", "grammar", "error-spotting", "reading-comprehension", "cloze-test"}:
        return gov_english.get_english(topic_slug, difficulty)
    if topic_slug in {"history", "geography", "polity", "economy", "current-affairs", "science"}:
        return gov_ga.get_ga(topic_slug, difficulty)
    return gov_reasoning.get_reasoning(topic_slug, difficulty)


def all_topic_slugs() -> list[str]:
    return [slug for course in GOV_COURSES for slug, _, _ in course["topics"]]
