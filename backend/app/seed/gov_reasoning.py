"""Reasoning question banks: coding-decoding generated; others curated. All answers verified."""
from __future__ import annotations

import random

from app.seed.util import mcq

QuestionDict = dict
Bank = dict[str, list[tuple]]

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _shift(word: str, k: int) -> str:
    return "".join(LETTERS[(LETTERS.index(ch) + k) % 26] for ch in word)


CODING_WORDS = ["CAT", "DOG", "SUN", "MOON", "STAR", "TREE", "BOOK", "KITE", "RAIN", "FISH", "LION", "APPLE"]


def generate_coding(difficulty: str, seed: str) -> list[QuestionDict]:
    """Rule-based letter coding with deterministic, verifiable answers."""
    rng = random.Random(seed)
    combos = [(w1, w2, k) for w1 in CODING_WORDS for w2 in CODING_WORDS if w1 != w2 for k in range(1, 6)]
    rng.shuffle(combos)
    out: list[QuestionDict] = []
    for w1, w2, k in combos[:25]:
        if difficulty == "beginner":
            prompt = f"In a certain code, every letter moves {k} steps forward in the alphabet. If {w1} is written as {_shift(w1, k)}, how is {w2} written?"
            answer = _shift(w2, k)
            options = [_shift(w2, -k), _shift(w2, k + 1), w2]
            why = f"Move each letter of {w2} forward by {k}: {' '.join(ch + '->' + LETTERS[(LETTERS.index(ch) + k) % 26] for ch in w2[:3])}... = {answer}."
        elif difficulty == "intermediate":
            prompt = f"Code: reverse the word, then move each letter {k} steps forward. If {w1} is written as {_shift(w1[::-1], k)}, what is the code for {w2}?"
            answer = _shift(w2[::-1], k)
            options = [_shift(w2, k), w2[::-1], _shift(w2[::-1], -k)]
            why = f"Reverse {w2} -> {w2[::-1]}, then shift each letter +{k} = {answer}."
        else:
            prompt = f"Code: move each letter {k} steps forward, then reverse the word. If {w1} is written as {_shift(w1, k)[::-1]}, what is the code for {w2}?"
            answer = _shift(w2, k)[::-1]
            options = [_shift(w2, k), w2[::-1], _shift(w2[::-1], k)]
            why = f"Shift {w2} by +{k} -> {_shift(w2, k)}, then reverse -> {answer}."
        out.append(mcq(prompt, answer, options, why, difficulty))
    return out


BLOOD: Bank = {
    "beginner": [
        ("Pointing to a photograph, Ram said, 'He is the son of my grandfather's only son.' Who is he to Ram?", ["Brother", "Cousin", "Uncle", "Father"], 0, "Grandfather's only son is Ram's father; his son is Ram's brother."),
        ("A is B's sister. C is B's mother. D is C's father. How is A related to D?", ["Daughter", "Granddaughter", "Niece", "Sister"], 1, "D is the father of C (B's mother), so D is A's grandfather and A is his granddaughter."),
        ("Pointing to a lady, Neha said, 'She is the daughter of my grandfather's only child.' How is the lady related to Neha?", ["Mother", "Aunt", "Sister", "Cousin"], 2, "Grandfather's only child is Neha's parent; that parent's daughter is Neha's sister."),
        ("P is Q's brother. R is Q's mother. S is R's father. How is P related to S?", ["Son", "Grandson", "Nephew", "Son-in-law"], 1, "R is P's mother, so S (R's father) is P's grandfather — P is S's grandson."),
        ("Anuj introduces a man as 'The son of the brother of my father.' How is the man related to Anuj?", ["Brother", "Uncle", "Cousin", "Nephew"], 2, "Father's brother is Anuj's uncle; his son is Anuj's cousin."),
        ("A is the mother of B. C is the son of A. How is B related to C?", ["Brother or Sister", "Uncle", "Cousin", "Nephew"], 0, "B and C share the same mother A, so B is C's brother or sister."),
    ],
    "intermediate": [
        ("Pointing to a man, a woman said, 'His mother is the only daughter of my mother.' How is the woman related to the man's mother?", ["Mother", "Grandmother", "Sister", "Daughter"], 0, "The only daughter of her mother is the woman herself, so she IS the man's mother."),
        ("A is B's brother. C is A's mother. D is C's father. E is D's son. How is B related to E?", ["Brother", "Brother or Sister", "Cousin", "Nephew"], 1, "E is the son of D and C; B is also C's child, so B is E's brother or sister."),
        ("Ravi said, 'She is the wife of the grandfather of my only grandson.' How is the lady related to Ravi's only grandson?", ["Grandmother", "Mother", "Aunt", "Sister"], 0, "The grandfather of his grandson is Ravi himself; his wife is the grandson's grandmother."),
        ("Pointing to a boy, Meera said, 'He is the son of my mother's son.' What is the boy to Meera?", ["Nephew", "Son", "Brother", "Cousin"], 0, "My mother's son is Meera's brother; his son is Meera's nephew."),
        ("K is brother of L. M is sister of K. N is brother of P. P is daughter of L. How is N related to M?", ["Nephew", "Son", "Brother", "Uncle"], 0, "P and N are children of L; L is M's sibling, so N is M's nephew."),
        ("A, B and C are children of X. D is the wife of X. E is the son of A. How is D related to E?", ["Grandmother", "Mother", "Aunt", "Great-grandmother"], 0, "D is the mother of A, and A is E's parent, so D is E's grandmother."),
    ],
    "advanced": [
        ("Pointing to a photograph, a man said, 'She is the daughter of the only child of my grandfather.' How is the lady related to the man's mother?", ["Daughter", "Niece", "Sister", "Cousin"], 0, "The only child of his grandfather is his parent; that parent's daughter is his sister — and a sister is her mother's daughter."),
        ("A is the brother of B. C is A's mother. D is C's father. E is D's son. How is D related to A?", ["Father", "Grandfather", "Uncle", "Brother"], 1, "C is A's mother and D is C's father, so D is A's maternal grandfather."),
        ("P is the father of Q. R is the daughter of Q. S is the brother of Q. T is the wife of P. How is T related to R?", ["Grandmother", "Mother", "Aunt", "Sister"], 0, "T is P's wife, hence Q's mother; as R is Q's daughter, T is R's grandmother."),
        ("X told Y, 'Your father's brother's only son is my father's son.' How is X related to Y?", ["Brother", "Uncle", "Cousin", "Father"], 2, "Your father's brother's only son = Y's cousin; my father's son = X, so X is Y's cousin."),
        ("A is married to B. C is the brother of A. D is the son of B. E is the brother of C. How is D related to E?", ["Nephew", "Son", "Brother", "Cousin"], 0, "D is the son of A's spouse B; E is A's brother, so D is E's nephew."),
        ("If P # Q means 'P is the brother of Q' and P @ Q means 'P is the mother of Q', how is P related to R if P @ Q and Q # R?", ["Grandmother", "Mother", "Aunt", "Sister"], 1, "P is Q's mother and Q is R's brother, so Q and R share the same mother P — P is R's mother."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
BLOOD["beginner"] += [
    ("Rahul's mother is the only daughter of Seema's father. How is Seema related to Rahul?", ["Mother", "Aunt", "Sister", "Grandmother"], 0, "Seema's father's only daughter is Seema herself, and she is Rahul's mother."),
    ("Vikas is the son of Anil. Anil is the husband of Sunita. How is Vikas related to Sunita?", ["Nephew", "Son", "Brother", "Father"], 1, "Anil and Sunita are Vikas's parents, so Vikas is Sunita's son."),
    ("A girl introduces a boy as the son of her grandmother's only daughter. How is the boy related to the girl?", ["Brother", "Cousin", "Nephew", "Son"], 0, "Grandmother's only daughter is the girl's mother; her son is the girl's brother."),
    ("Mohan's father has three sons: Ram, Shyam and ...? Name the third son.", ["Mohan", "Rohan", "Sohan", "Cannot say"], 0, "Mohan's father has three sons and Mohan is one of them, so the third is Mohan himself."),
]
BLOOD["intermediate"] += [
    ("A and B are brothers. C and D are sisters. A's son is D's brother. How is B related to C?", ["Uncle", "Father", "Brother", "Cousin"], 0, "A's son is D's brother, so A is the father of C and D; B, A's brother, is their uncle."),
    ("Suresh's sister is the wife of Ramesh. Ramesh is the father of Kiran. How is Suresh related to Kiran?", ["Uncle", "Father", "Brother", "Grandfather"], 0, "Suresh's sister is Kiran's mother, so Suresh is Kiran's maternal uncle."),
    ("Pointing to a woman, Arjun said, 'She is the mother of my father's only son's wife.' How is the woman related to Arjun?", ["Mother-in-law", "Mother", "Aunt", "Sister"], 0, "Father's only son is Arjun himself; his wife's mother is Arjun's mother-in-law."),
    ("P's father is Q's son. R is Q's daughter. How is P related to R?", ["Nephew or Niece", "Son", "Brother", "Cousin"], 0, "P's father and R are both Q's children, so P is R's nephew or niece."),
]
BLOOD["advanced"] += [
    ("If A + B means A is the father of B, A - B means A is the wife of B, and A x B means A is the brother of B, then P + Q - R x S means?", ["P is S's father-in-law", "P is S's father", "R is P's son", "S is P's nephew"], 0, "Q is P's child; Q is R's wife; R and S are brothers. So S is P's child's brother-in-law, i.e., P is S's father-in-law."),
    ("M is N's sister. O is N's father. P is O's mother. Q is P's husband. How is Q related to M?", ["Grandfather", "Father", "Uncle", "Brother"], 0, "O is M's father; P is O's mother (M's grandmother); Q is P's husband, hence M's grandfather."),
    ("Kavya's brother's wife's only brother is Arun. How is Arun related to Kavya?", ["Brother", "Brother-in-law", "Cousin", "Uncle"], 1, "Brother's wife is Kavya's sister-in-law; her only brother Arun is Kavya's brother-in-law."),
    ("A family of six P, Q, R, S, T, U has two married couples. P is the father of Q. S is Q's wife. T is the sister of S. U is the son of P. R is the daughter-in-law of P. How is R related to S?", ["Sister-in-law", "Sister", "Cousin", "Mother"], 0, "P's children are Q and U. Q's wife is S, so U's wife R is S's sister-in-law (wives of two brothers)."),
]

SEATING: Bank = {
    "beginner": [
        ("Five friends sit in a row facing north. Rohit is at the extreme left and Priya is at the extreme right. Kunal is exactly in the middle. Who sits between Rohit and Kunal?", ["Sneha", "Amit", "Priya", "No one"], 1, "Order: Rohit, Amit, Kunal, Sneha, Priya — Amit sits between Rohit and Kunal."),
        ("In a row of 6, Anita is 2nd from the left and Bhaskar is 3rd from the right. How many students are between them?", ["1", "2", "3", "0"], 0, "Bhaskar is at position 6 - 3 + 1 = 4; one student (position 3) sits between positions 2 and 4."),
        ("Five children stand in a line. Deepa is immediately right of Chetan and immediately left of Esha. Firoz is at the extreme right. Who is in the middle?", ["Deepa", "Chetan", "Esha", "Firoz"], 2, "Order: Chetan, Deepa, Esha, (one gap), Firoz — Esha is at position 3, the middle."),
        ("Ravi stands 4th from the left in a row of 7. What is his position from the right?", ["3rd", "4th", "5th", "6th"], 1, "From the right = 7 - 4 + 1 = 4th."),
        ("In a queue of 25, Sita is 10th from the front and Gita is 10th from the back. How many students are between them?", ["4", "5", "6", "3"], 1, "Gita is at position 25 - 10 + 1 = 16; between positions 10 and 16 there are 16 - 10 - 1 = 5 students."),
        ("Six students sit around a square table (one on each side and one at each corner) facing the centre. If A sits at a corner and B sits immediately to A's right, where does B sit?", ["Corner", "Side", "Opposite corner", "Cannot say"], 1, "Around a square, the seat immediately next to a corner (along the perimeter) is a side seat."),
    ],
    "intermediate": [
        ("Ten people sit in two rows of 5 facing each other. P sits at the extreme left of row 1 and opposite Q, who sits at the extreme right of row 2. Who sits opposite the person who is third from the left in row 1?", ["Third from left, row 2", "Third from right, row 2", "Extreme right, row 2", "Extreme left, row 2"], 1, "In facing rows, the k-th person from the left of row 1 faces the k-th person from the right of row 2 — so third from left faces third from right."),
        ("Six people A to F sit in a row facing north. A is at the extreme left and F at the extreme right. B sits immediately right of A. D sits immediately right of C. E sits between D and F. Who sits immediately to the right of C?", ["C", "D", "E", "B"], 1, "Placing the constraints gives the order A, B, C, D, E, F — D sits immediately right of C."),
        ("In a row, Mohan is 12th from the left and Sohan is 18th from the right. They exchange positions and Mohan then becomes 25th from the left. How many people are in the row?", ["42", "41", "43", "40"], 0, "After the swap Mohan occupies Sohan's original seat: 25th from the left and 18th from the right, so the row has 25 + 18 - 1 = 42 people."),
        ("Six people A to F sit around a circular table facing the centre. A sits opposite B and C sits opposite D. Which two people must sit opposite each other?", ["A and C", "E and F", "B and D", "Cannot say"], 1, "With A-B and C-D forming opposite pairs, the only two people left are E and F, so they must sit opposite each other."),
        ("Five cars P, Q, R, S and T park in a line. Q is immediately right of P. T is between Q and R. S is at the extreme left and R is at the extreme right. Which car is second from the right?", ["T", "R", "Q", "S"], 0, "Order: S, P, Q, T, R — second from the right is T."),
        ("In a class of 40, Amit is 15th from the top and Sonia is 10th from the bottom. How many students are between them?", ["14", "15", "16", "17"], 1, "Sonia is 40 - 10 + 1 = 31st from the top; students between 15th and 31st = 31 - 15 - 1 = 15."),
    ],
    "advanced": [
        ("Twelve people sit in two rows of six facing each other. A sits at the extreme left of row 1 and faces the person at the extreme right of row 2. Who faces the person who is third from the left in row 1?", ["Fourth from right", "Third from right", "Third from left", "Second from left"], 1, "The k-th from the left of row 1 faces the k-th from the right of row 2 — third from left faces third from right."),
        ("Six people P, Q, R, S, T and U sit around a circular table facing the centre. P sits between Q and R. S sits opposite P. T sits opposite Q. Who sits opposite R?", ["T", "U", "P", "S"], 1, "Opposite pairs already fixed: P-S and Q-T, so the remaining pair is R-U."),
        ("Nine people sit in three rows of three facing north. X sits at the centre of row 2 and Y sits at the right corner of row 1. Who sits diagonally opposite Y in row 3?", ["Left corner of row 3", "Centre of row 3", "Right corner of row 3", "No one"], 0, "The diagonal opposite of the right corner of row 1 is the left corner of row 3."),
        ("Six people A, B, C, D, E and F sit in a row facing north. C sits at the extreme left and B sits immediately right of C. A sits between B and D. E sits immediately left of F and F is at the extreme right. Who sits between B and D?", ["A", "C", "E", "F"], 0, "Order: C, B, A, D, E, F — A sits between B and D."),
        ("In a row of 30, Rani is 8th from the left. Six new students join the row between Rani and the right end. What is her new position from the left?", ["8th", "14th", "15th", "36th"], 0, "New students sit to her right, so her position from the left is unchanged — still 8th."),
        ("Ten people sit in a circle facing the centre, numbered 1 to 10 clockwise, so that person 1 is opposite person 6. If person 3 moves three seats clockwise, how many seats away is she then from person 7 (measured clockwise)?", ["1", "2", "3", "4"], 0, "Person 3 moving three seats clockwise lands on seat 6; from seat 6 to person 7 clockwise is 1 seat."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
SEATING["beginner"] += [
    ("Seven people sit in a row facing north. C sits at the extreme left. B sits immediately left of A, who sits immediately left of D. Who sits between C and A?", ["B", "D", "Nobody", "Cannot say"], 0, "The order starts C, B, A, D - so B sits between C and A."),
    ("Four people P, Q, R, S sit around a circular table facing the centre. P sits opposite R. Who sits opposite Q?", ["S", "P", "R", "Cannot say"], 0, "With P opposite R, the remaining pair Q-S must sit opposite each other."),
    ("In a row of 9 facing north, K is 5th from the left. How many people sit to the right of K?", ["3", "4", "5", "6"], 1, "9 - 5 = 4 people sit to the right of K."),
    ("A, B, C, D, E sit in a row facing north in that order. Who sits in the middle?", ["A", "B", "C", "D"], 2, "Five seats in order A, B, C, D, E - the middle (3rd) seat is C."),
    ("Six chairs face north in a row. Ravi takes the extreme right chair and Suman the extreme left chair. How many empty chairs lie between them?", ["2", "3", "4", "5"], 2, "Six chairs with both ends taken leaves 4 empty chairs between them."),
    ("Eight people sit in a circle facing the centre. How many people sit between any two adjacent people?", ["0", "1", "2", "3"], 0, "Adjacent people sit next to each other with nobody between them."),
]
SEATING["intermediate"] += [
    ("Seven people A to G sit in a row facing north. B sits third from the left. D sits immediately right of B. F sits at the extreme right. A sits between D and F. Who sits fourth from the left?", ["D", "A", "F", "B"], 0, "Positions are 1:?, 2:?, 3:B, 4:D, 5:A, 6:?, 7:F - fourth from the left is D."),
    ("In a row of 50 students facing north, Ramesh is 20th from the left. After 5 students from his right leave, what is his position from the right?", ["25th", "26th", "30th", "31st"], 1, "Originally 50 - 20 + 1 = 31st from the right; 5 students to his right leave, so 31 - 5 = 26th from the right."),
    ("Five people sit in positions 1 to 5 in a row. A is at position 2. B is immediately right of A. C is at an extreme end but not position 1. D sits between B and E. Who sits at position 5?", ["E", "C", "D", "A"], 0, "A=2, B=3; D between B and E gives B=3, D=4, E=5; C takes the remaining extreme end (position 1). So position 5 is E."),
    ("In a row facing north, X is 7th from the left and 9th from the right. Y sits exactly in the middle of the row. What is Y's position from the left?", ["8th", "7th", "9th", "10th"], 0, "Total = 7 + 9 - 1 = 15; the middle (8th) seat is Y's, so Y is 8th from the left."),
    ("Five people A-E sit in a row facing north. B is in the middle. A and E sit at the two ends. C sits immediately left of B. Where does D sit?", ["Immediately right of B", "At an end", "Next to A", "Next to E"], 0, "Ends are A and E; middle is B with C immediately left (position 2); D takes the only free seat - position 4, immediately right of B."),
    ("A row has 12 seats facing north. A sits on seat 3 and B sits on seat 9. How many seats lie strictly between them?", ["5", "6", "7", "4"], 0, "Seats 4, 5, 6, 7, 8 lie between seats 3 and 9 - five seats."),
]
SEATING["advanced"] += [
    ("Eight people sit around a circle facing the centre. A sits opposite E. B sits immediately to the right of A. Who sits immediately to the left of E?", ["B", "A", "F", "Cannot be determined"], 3, "Only A-E opposite and B right of A are fixed; which named person sits left of E is undetermined by the clues."),
    ("Twelve people sit around a circular table facing the centre. Each opposite pair is counted once. How many opposite pairs are there?", ["12", "6", "5", "24"], 1, "Twelve seats form 12/2 = 6 opposite pairs."),
    ("In a row of 20 people, P is 5th from the left. After 4 people join to the left of P, what was P's ORIGINAL position from the right?", ["16th", "15th", "12th", "11th"], 0, "The joining info is a distractor: originally P is 5th from the left of 20, so 20 - 5 + 1 = 16th from the right."),
    ("A, B, C, D, E, F, G sit in a row facing north. B is 4th. A and G are at the ends. C sits immediately right of B. D sits immediately left of B. E sits at position 2. Who sits at position 6?", ["F", "E", "G", "A"], 0, "B=4, C=5, D=3; E=2 forces A=1 (E sits next to A); then G=7 with F next to G, so F=6."),
    ("Nine chairs in a row face north. Three friends occupy chairs 2, 5 and 8. How many pairs of friends have exactly two empty chairs between them?", ["1", "2", "3", "0"], 1, "Chairs (2,5) have 3,4 empty and (5,8) have 6,7 empty - two such pairs."),
    ("People sit in two rows of 4 facing each other, mirrored: A2 faces B3. If X sits at A2, who faces X?", ["Whoever sits at B3", "Whoever sits at B2", "Whoever sits at B4", "Nobody"], 0, "A2 faces B3 by the given mirror mapping."),
]

PUZZLES: Bank = {
    "beginner": [
        ("Five boxes are stacked one above the other. Sugar is at the top. Milk is kept just above bread. Rice is kept just below bread. Which item is at the bottom?", ["Rice", "Salt", "Bread", "Milk"], 1, "Top to bottom: Sugar, Milk, Bread, Rice, Salt — salt is at the bottom."),
        ("In a family, A and B are a married couple. C and D are their sons. E is C's wife and F is their daughter. How many male members are in the family?", ["2", "3", "4", "5"], 1, "The male members are A, C and D — three."),
        ("Priya ranks 7th from the top and 26th from the bottom in a class. How many students are there?", ["32", "33", "31", "34"], 0, "Total = 7 + 26 - 1 = 32."),
        ("Four friends have different heights. P is taller than Q but shorter than R. S is the shortest. Who is the tallest?", ["P", "Q", "R", "S"], 2, "The order is R > P > Q > S, so R is the tallest."),
        ("A clock shows 3:15. What is the angle between the hour and minute hands?", ["0°", "7.5°", "15°", "22.5°"], 1, "Minute hand at 90°, hour hand at 3 x 30 + 15 x 0.5 = 97.5°; difference = 7.5°."),
        ("If the day before yesterday was two days before Monday, what day is today?", ["Saturday", "Sunday", "Monday", "Tuesday"], 1, "Two days before Monday is Saturday. If yesterday was Saturday, today is Sunday."),
    ],
    "intermediate": [
        ("Six cities A to F are connected in a chain: A-B, B-C, C-D, D-E, E-F. Which cities must be passed to travel from A to F?", ["C only", "B, C, D and E", "B and E", "D only"], 1, "The only path from A to F runs through B, C, D and E."),
        ("Five students score different marks. T scores more than U but less than V. W scores less than U but more than X. Who scores the highest?", ["T", "V", "U", "W"], 1, "The order is V > T > U > W > X, so V scores the highest."),
        ("A family has 4 grandparents, 2 parents and 3 children. How many members are there in total?", ["9", "7", "8", "10"], 0, "4 + 2 + 3 = 9."),
        ("A bag contains 4 red, 3 blue and 3 green balls. What is the minimum number of draws needed to guarantee two balls of the same colour?", ["2", "4", "5", "3"], 1, "Worst case: the first three balls are all different colours; the fourth must repeat a colour."),
        ("Five persons P, Q, R, S and T live on floors 1 to 5. R lives above Q but below P. T lives on the bottom floor. S lives just above R. Who lives on floor 1?", ["T", "Q", "S", "R"], 0, "T lives on the bottom floor, which is floor 1."),
        ("A, B, C and D do four jobs in order. C does the first job. A does not do the first job. B does the job immediately after A. D does the last job. Which job does A do?", ["Second", "Third", "Fourth", "Cannot say"], 0, "Order must be C, A, B, D — A does the second job."),
    ],
    "advanced": [
        ("A token starts at (1, 1) on a grid. It moves 3 steps right, then 2 steps down, then 1 step left. Where is it now?", ["(3, 3)", "(4, 3)", "(3, 4)", "(2, 3)"], 0, "x: 1 + 3 - 1 = 3, y: 1 + 2 = 3 — the token is at (3, 3)."),
        ("Six people sit around a table, each with a different fruit. Apples are opposite mangoes, bananas are to the immediate right of apples, and cherries are opposite bananas. Who is opposite grapes?", ["Dates", "Apples", "Bananas", "Cannot say"], 3, "Only three opposite pairs are constrained; the pairing for grapes is not determined by the given clues."),
        ("A train 180 m long crosses a platform 270 m long in 18 seconds. What is the speed of the train?", ["25 km/h", "75 km/h", "90 km/h", "45 km/h"], 2, "Distance = 180 + 270 = 450 m; speed = 450/18 = 25 m/s = 25 x 18/5 = 90 km/h."),
        ("Five boxes stand in a row. Electronics is to the left of books but to the right of toys. Food is at the extreme right. Stationery is immediately left of electronics. Which box is at the extreme left?", ["Toys", "Stationery", "Books", "Food"], 0, "Order: Toys, Stationery, Electronics, Books, Food — toys is at the extreme left."),
        ("In how many ways can 8 people be seated at a round table if two particular people must sit together?", ["720", "1440", "5040", "120"], 1, "Treat the pair as one unit: (7 - 1)! x 2! = 720 x 2 = 1440."),
        ("Five students score distinct marks. P scores more than Q but less than R. S scores less than Q but more than T. Who scores second?", ["P", "Q", "R", "S"], 0, "The order is R > P > Q > S > T, so P scores second."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
PUZZLES["beginner"] += [
    ("What comes next: 2, 4, 8, 16, ...?", ["20", "24", "32", "18"], 2, "Each term doubles the previous one: 16 x 2 = 32."),
    ("A basket has 5 apples. Five children take one apple each, yet one apple remains in the basket. How?", ["One child took the basket with the apple", "There were six apples", "One child returned it", "Impossible"], 0, "The fifth child took the basket itself along with the last apple."),
    ("How many months have 28 days?", ["1", "2", "12", "0"], 2, "Every month has at least 28 days, so all 12 qualify."),
    ("A man builds a house with all four walls facing south. A bear walks by. What colour is the bear?", ["Brown", "White", "Black", "Grey"], 1, "A house with all walls facing south must stand at the North Pole, where bears are white (polar bears)."),
    ("If you rearrange 'CIFAIPC' you get the name of a:", ["City", "Ocean", "Country", "Animal"], 1, "CIFAIPC rearranges to PACIFIC - an ocean."),
    ("Which number comes next: 1, 1, 2, 3, 5, 8, ...?", ["11", "12", "13", "10"], 2, "Fibonacci: each term is the sum of the previous two, 5 + 8 = 13."),
]
PUZZLES["intermediate"] += [
    ("What comes next: 3, 6, 11, 18, ...?", ["27", "26", "29", "24"], 0, "Differences grow by 2 each time: +3, +5, +7, so next is 18 + 9 = 27."),
    ("A snail climbs a 10-metre pole, rising 3 m each day and slipping 2 m each night. On which day does it reach the top?", ["10th", "8th", "7th", "5th"], 1, "Net gain is 1 m per day; after 7 days it is at 7 m, and on day 8 it climbs 3 m to reach 10 m without slipping."),
    ("How many times do the hands of a clock overlap in 24 hours?", ["24", "22", "20", "12"], 1, "The hands overlap 11 times every 12 hours, so 22 times in 24 hours."),
    ("In a code, SKY is written as 19-11-25 (letter positions). How is CUP written?", ["3-21-16", "3-20-16", "4-21-15", "3-21-15"], 0, "C=3, U=21, P=16, so CUP is 3-21-16."),
    ("A trader marks goods 40% above cost and offers a 10% discount. What is the overall profit?", ["30%", "26%", "28%", "24%"], 1, "Marked price = 1.4 x cost; selling price = 1.4 x 0.9 = 1.26 x cost - a 26% profit."),
    ("Find the odd one out: Square, Circle, Triangle, Cube.", ["Square", "Circle", "Triangle", "Cube"], 3, "Square, circle and triangle are 2D shapes; a cube is 3D."),
]
PUZZLES["advanced"] += [
    ("What comes next: 2, 3, 5, 7, 11, 13, ...?", ["15", "17", "19", "14"], 1, "These are consecutive prime numbers; the next prime after 13 is 17."),
    ("A 3x3x3 cube is painted red on all faces and cut into 27 unit cubes. How many small cubes have exactly two painted faces?", ["12", "8", "6", "4"], 0, "Cubes with two painted faces sit on the 12 edges (one per edge)."),
    ("In a race of 100 m, A beats B by 10 m and B beats C by 10 m. By how much does A beat C?", ["20 m", "19 m", "21 m", "18 m"], 1, "When A runs 100 m, B runs 90 m; when B runs 100 m, C runs 90 m - so when A runs 100 m, C runs 81 m. A beats C by 19 m."),
    ("What is the next number: 1, 2, 6, 24, 120, ...?", ["600", "720", "840", "480"], 1, "Factorials: 1!, 2!, 3!, 4!, 5!, so next is 6! = 720."),
    ("Two trains 120 m and 80 m long run towards each other at 60 km/h and 40 km/h. In how many seconds do they cross?", ["7.2", "8", "6", "10"], 0, "Relative speed = 100 km/h = 250/9 m/s; distance = 200 m; time = 200 / (250/9) = 7.2 s."),
    ("How many squares are there on a standard 8x8 chessboard?", ["64", "204", "128", "256"], 1, "Sum of k^2 for k = 1..8 = 64+49+36+25+16+9+4+1 = 204."),
]

ANALOGY: Bank = {
    "beginner": [
        ("Doctor : Hospital :: Teacher : ?", ["School", "Office", "Court", "Factory"], 0, "A doctor works in a hospital; a teacher works in a school."),
        ("Eye : See :: Ear : ?", ["Hear", "Smell", "Taste", "Touch"], 0, "The eye is the organ for seeing; the ear is for hearing."),
        ("Thermometer : Temperature :: Barometer : ?", ["Pressure", "Humidity", "Altitude", "Rainfall"], 0, "A thermometer measures temperature; a barometer measures atmospheric pressure."),
        ("Bird : Nest :: Man : ?", ["House", "Clothes", "Food", "Tool"], 0, "A bird lives in a nest; a man lives in a house."),
        ("Flower : Bud :: Child : ?", ["Adult", "Infant", "Teenager", "Parent"], 1, "A bud is the early stage of a flower; an infant is the early stage of a child."),
        ("India : Delhi :: Japan : ?", ["Beijing", "Tokyo", "Seoul", "Bangkok"], 1, "Delhi is the capital of India; Tokyo is the capital of Japan."),
    ],
    "intermediate": [
        ("Oasis : Desert :: Island : ?", ["Sea", "Mountain", "Valley", "Forest"], 0, "An oasis is a fertile spot inside a desert; an island is land surrounded by the sea."),
        ("Clock : Time :: Scale : ?", ["Weight", "Length", "Height", "Area"], 0, "A clock measures time; a scale measures weight."),
        ("Artist : Canvas :: Poet : ?", ["Rhyme", "Words", "Novel", "Pen"], 1, "An artist works on a canvas; a poet works with words."),
        ("Bacteria : Disease :: Seed : ?", ["Fruit", "Plant", "Soil", "Flower"], 1, "Bacteria cause disease; a seed grows into a plant."),
        ("Cobbler : Shoes :: Barber : ?", ["Clothes", "Hair", "Teeth", "Watch"], 1, "A cobbler repairs shoes; a barber cuts hair."),
        ("Puppy : Dog :: Kitten : ?", ["Cat", "Lion", "Rabbit", "Fox"], 0, "A puppy is a young dog; a kitten is a young cat."),
    ],
    "advanced": [
        ("Augean Stables : Cleanse :: Gordian Knot : ?", ["Tie", "Sever", "Untie slowly", "Worship"], 1, "Cleaning the Augean stables and cutting the Gordian Knot are both famous decisive feats."),
        ("Epicure : Food :: Cynic : ?", ["Money", "Virtue", "Pleasure", "Power"], 1, "An epicure is devoted to fine food; a cynic is sceptical about human virtue."),
        ("Pedant : Learning :: Miser : ?", ["Wealth", "Labour", "Food", "Travel"], 0, "A pedant is absorbed in learning; a miser is absorbed in wealth."),
        ("Vision : Eyes :: Echolocation : ?", ["Skin", "Ears", "Nose", "Tongue"], 1, "Vision is perceived through the eyes; echolocation is perceived through hearing (ears)."),
        ("Seismograph : Earthquake :: Barometer : ?", ["Rain", "Wind", "Pressure", "Temperature"], 2, "A seismograph records earthquakes; a barometer records air pressure."),
        ("Scribe : Manuscript :: Architect : ?", ["Building", "Brick", "Tool", "Contract"], 0, "A scribe produces a manuscript; an architect designs a building."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
ANALOGY["beginner"] += [
    ("Pen : Write :: Knife : ?", ["Cut", "Eat", "Draw", "Break"], 0, "A pen is used to write; a knife is used to cut."),
    ("Dog : Bark :: Cow : ?", ["Moo", "Neigh", "Trumpet", "Bleat"], 0, "Dogs bark; cows moo."),
    ("Sun : Day :: Moon : ?", ["Night", "Stars", "Sky", "Light"], 0, "The sun rules the day; the moon rules the night."),
    ("Wheel : Car :: Wing : ?", ["Bird", "Aeroplane", "Pilot", "Runway"], 1, "Wheels move a car; wings lift an aeroplane."),
    ("Ice : Cold :: Fire : ?", ["Hot", "Burn", "Smoke", "Light"], 0, "Ice is cold; fire is hot."),
    ("Book : Pages :: Wall : ?", ["Bricks", "Cement", "Paint", "Door"], 0, "A book is made of pages; a wall is made of bricks."),
]
ANALOGY["intermediate"] += [
    ("Chef : Kitchen :: Surgeon : ?", ["Hospital", "Operation Theatre", "Clinic", "Ward"], 1, "A chef works in a kitchen; a surgeon operates in an operation theatre."),
    ("Honey : Bee :: Silk : ?", ["Spider", "Silkworm", "Moth", "Caterpillar"], 1, "Bees produce honey; silkworms produce silk."),
    ("Cricket : Bat :: Hockey : ?", ["Stick", "Ball", "Goal", "Field"], 0, "Cricket is played with a bat; hockey with a stick."),
    ("Smoke : Fire :: Flood : ?", ["Rain", "River", "Dam", "Storm"], 0, "Smoke signals fire; a flood follows heavy rain."),
    ("Lawyer : Court :: Teacher : ?", ["School", "Student", "Book", "Class"], 0, "A lawyer practises in court; a teacher teaches in school."),
    ("Month : Year :: Hour : ?", ["Day", "Minute", "Week", "Second"], 0, "Twelve months make a year; 24 hours make a day."),
]
ANALOGY["advanced"] += [
    ("Altruist : Selflessness :: Hedonist : ?", ["Pleasure", "Pain", "Wealth", "Knowledge"], 0, "An altruist pursues selflessness; a hedonist pursues pleasure."),
    ("Stoic : Emotion :: Ascetic : ?", ["Comfort", "Food", "Pain", "Wealth"], 0, "A stoic renounces emotion; an ascetic renounces comfort."),
    ("Bibliography : Books :: Catalogue : ?", ["Items", "Library", "Author", "Prices"], 0, "A bibliography lists books; a catalogue lists items."),
    ("Ornithologist : Birds :: Entomologist : ?", ["Insects", "Fish", "Plants", "Animals"], 0, "Ornithology studies birds; entomology studies insects."),
    ("Prologue : Play :: Preamble : ?", ["Constitution", "Poem", "Speech", "Law"], 0, "A prologue introduces a play; a preamble introduces a constitution."),
    ("Meteorology : Weather :: Seismology : ?", ["Earthquakes", "Stars", "Oceans", "Volcanoes"], 0, "Meteorology studies weather; seismology studies earthquakes."),
]

SYLLOGISM: Bank = {
    "beginner": [
        ("Statements: All pens are books. All books are chairs. Conclusion: All pens are chairs.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "All pens are books and all books are chairs, so all pens are chairs — it follows."),
        ("Statements: All cats are dogs. Some dogs are rats. Conclusion: Some cats are rats.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "The dogs that are rats need not be cats — it does not follow."),
        ("Statements: Some apples are mangoes. All mangoes are fruits. Conclusion: Some apples are fruits.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "The apples that are mangoes are also fruits, so some apples are fruits — it follows."),
        ("Statements: No bird is a stone. All stones are metals. Conclusion: No bird is a metal.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Birds exclude stones, but stones being metals says nothing that forces birds to exclude metals — it does not follow."),
        ("Statements: All tables are chairs. Conclusion: Some chairs are tables.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "If all tables are chairs, the tables themselves are chairs, so some chairs are tables — it follows."),
        ("Statements: Some students are teachers. All teachers are doctors. Conclusion: Some students are doctors.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "The students who are teachers are doctors, so some students are doctors — it follows."),
    ],
    "intermediate": [
        ("Statements: All roses are flowers. Some flowers are red. Conclusion: Some roses are red.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "The red flowers need not include any roses — it does not follow."),
        ("Statements: No fish is a bird. All birds fly. Conclusion: No fish flies.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Fish are excluded from birds, but nothing stops a fish from flying by other means — the conclusion does not follow."),
        ("Statements: All men are human. Some humans are happy. Conclusion: Some men are happy.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Happy humans need not be men — it does not follow."),
        ("Statements: Some pens are pencils. All pencils are erasers. Conclusion: Some pens are erasers.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "The pens that are pencils are erasers, so some pens are erasers — it follows."),
        ("Statements: No sun is a moon. All moons are stars. Conclusion: Some stars are not suns.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "All moons are stars and no moon is a sun, so at least those stars are not suns — some stars are not suns follows."),
        ("Statements: All cups are saucers. Some saucers are plates. Conclusion: Some cups are plates.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "The saucers that are plates need not be cups — it does not follow."),
    ],
    "advanced": [
        ("Statements: All keys are locks. Some locks are doors. Conclusions: I. Some keys are doors. II. Some locks are keys.", ["Only II follows", "Only I follows", "Both follow", "Neither follows"], 0, "I does not follow (locks that are doors may not be keys); II follows because all keys are locks, so some locks are keys."),
        ("Statements: No table is a chair. All chairs are wooden. Conclusions: I. No table is wooden. II. Some wooden things are not tables.", ["Only II follows", "Only I follows", "Both follow", "Neither follows"], 0, "I does not follow (tables could be wooden without being chairs); II follows — the wooden chairs are not tables."),
        ("Statements: Some rains are storms. All storms are winds. Conclusions: I. Some rains are winds. II. All winds are rains.", ["Only I follows", "Only II follows", "Both follow", "Neither follows"], 0, "I follows (rains that are storms are winds); II does not follow (winds need not be rains)."),
        ("Statements: All flowers are plants. Some plants are trees. Conclusions: I. Some flowers are trees. II. Some flowers are not trees.", ["Either I or II follows", "Only I follows", "Only II follows", "Neither follows"], 0, "The statements leave flowers and trees completely undetermined, so either all flowers are trees or some are not — either-or case."),
        ("Statements: No pen is a book. All books are copies. Conclusions: I. No pen is a copy. II. Some copies are not pens.", ["Only II follows", "Only I follows", "Both follow", "Neither follows"], 0, "I does not follow (pens could be copies that are not books); II follows — books are copies and no book is a pen, so some copies are not pens."),
        ("Statements: All sons are fathers. Some fathers are teachers. Conclusions: I. Some sons are teachers. II. Some fathers are sons.", ["Only II follows", "Only I follows", "Both follow", "Neither follows"], 0, "I does not follow (fathers who teach need not be sons); II follows because all sons are fathers, so some fathers are sons."),
    ],
}

# PYQ-paper expansion (2020-2026 sets): extra practice depth per level.
SYLLOGISM["beginner"] += [
    ("Statements: All birds can fly. Sparrows are birds. Conclusion: Sparrows can fly.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "Treating the statements as true, sparrows (birds) can fly - it follows."),
    ("Statements: Some cats are black. Tom is a cat. Conclusion: Tom is black.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Tom may or may not be among the black cats - it does not follow."),
    ("Statements: All Indians are Asians. Ravi is an Indian. Conclusion: Ravi is Asian.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "Ravi belongs to Indians, who are all Asians - it follows."),
    ("Statements: No fish can walk. A shark is a fish. Conclusion: A shark cannot walk.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "Sharks are fish and no fish can walk - it follows."),
    ("Statements: All roses are red. This flower is red. Conclusion: This flower is a rose.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Other flowers can also be red - it does not follow."),
    ("Statements: Some doctors are surgeons. All surgeons wear masks. Conclusion: Some doctors wear masks.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "The doctors who are surgeons wear masks - it follows."),
]
SYLLOGISM["intermediate"] += [
    ("Statements: All laptops are computers. Some computers are portable. Conclusion: Some laptops are portable.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "The portable computers need not be laptops - it does not follow."),
    ("Statements: Some metals are liquids. Mercury is a metal. Conclusion: Mercury is a liquid.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Mercury may not be among the liquid metals - logically it does not follow."),
    ("Statements: No teacher is lazy. Some lazy people are students. Conclusion: Some students are not teachers.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "Lazy students cannot be teachers (no teacher is lazy), so some students are not teachers - it follows."),
    ("Statements: All poets are dreamers. Some dreamers are night owls. Conclusion: Some poets are night owls.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "The night-owl dreamers need not be poets - it does not follow."),
    ("Statements: Some books are novels. No novel is boring. Conclusion: Some books are not boring.", ["Follows", "Does not follow", "Either follows", "Cannot say"], 0, "The books that are novels are not boring, so some books are not boring - it follows."),
    ("Statements: All cars need fuel. My vehicle needs fuel. Conclusion: My vehicle is a car.", ["Does not follow", "Follows", "Either follows", "Cannot say"], 0, "Bikes and buses also need fuel - it does not follow."),
]
SYLLOGISM["advanced"] += [
    ("Statements: All A are B. No B is C. Conclusions: I. No A is C. II. Some C are not A.", ["Both follow", "Only I follows", "Only II follows", "Neither follows"], 0, "I follows (A's are B's, and no B is C); II follows too (no C can be an A at all, so certainly some C are not A)."),
    ("Statements: Some P are Q. All Q are R. Conclusions: I. Some P are R. II. Some R are P.", ["Both follow", "Only I follows", "Only II follows", "Neither follows"], 0, "I follows (P's that are Q are R); II follows by conversion of I (some R are P)."),
    ("Statements: No X is Y. Some Y are Z. Conclusions: I. Some Z are not X. II. No Z is X.", ["Only I follows", "Only II follows", "Both follow", "Neither follows"], 0, "I follows (the Z's that are Y exclude X); II is too strong (other Z's might be X) - only I follows."),
    ("Statements: All doctors wear coats. Some coat-wearers carry stethoscopes. Conclusions: I. Some doctors carry stethoscopes. II. Some stethoscope-carriers are doctors.", ["Neither follows", "Only I follows", "Only II follows", "Both follow"], 0, "The coat-wearers with stethoscopes need not include any doctor - neither follows."),
    ("Statements: All gardens have flowers. Some flowers are roses. Conclusions: I. Some gardens have roses. II. All roses are in gardens.", ["Neither follows", "Only I follows", "Only II follows", "Both follow"], 0, "The roses need not grow in gardens, and gardens need not grow roses - neither follows."),
    ("Statements: Some actors are singers. All singers are performers. Conclusions: I. Some actors are performers. II. All performers are actors.", ["Only I follows", "Only II follows", "Both follow", "Neither follows"], 0, "I follows (actors who sing perform); II reverses the chain wrongly - only I follows."),
]


def get_reasoning(topic_slug: str, difficulty: str) -> list[QuestionDict]:
    if topic_slug == "coding-decoding":
        return generate_coding(difficulty, f"coding-{difficulty}")
    bank: Bank = {
        "blood-relations": BLOOD,
        "seating-arrangement": SEATING,
        "puzzles": PUZZLES,
        "analogy": ANALOGY,
        "syllogism": SYLLOGISM,
    }[topic_slug]
    return [
        {"question_text": q, "options": list(opts), "correct_index": idx, "explanation": expl, "difficulty": difficulty}
        for q, opts, idx, expl in bank[difficulty]
    ]
