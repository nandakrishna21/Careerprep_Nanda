"""English question banks: Vocabulary, Grammar, Error Spotting, Reading Comprehension, Cloze Test."""
from __future__ import annotations

from app.seed.gov_reasoning import Bank
from app.seed.util import QuestionDict

VOCAB: Bank = {
    "beginner": [
        ("Choose the synonym of 'Happy'.", ["Joyful", "Angry", "Tired", "Sad"], 0, "Joyful means the same as happy."),
        ("Choose the antonym of 'Ancient'.", ["Old", "Modern", "Broken", "Heavy"], 1, "Ancient means very old; its opposite is modern."),
        ("What is the one-word substitution for 'a person who loves books'?", ["Bibliophile", "Philatelist", "Misogamist", "Numismatist"], 0, "A bibliophile is a lover of books."),
        ("Choose the synonym of 'Rapid'.", ["Slow", "Quick", "Heavy", "Quiet"], 1, "Rapid means quick."),
        ("Choose the antonym of 'Generous'.", ["Kind", "Selfish", "Rich", "Brave"], 1, "A generous person gives freely; a selfish person does not."),
        ("What is the meaning of the idiom 'to let the cat out of the bag'?", ["To free an animal", "To reveal a secret", "To make a mistake", "To start a fight"], 1, "The idiom means to reveal a secret, usually by mistake."),
    ],
    "intermediate": [
        ("Choose the synonym of 'Meticulous'.", ["Careless", "Precise", "Hasty", "Loud"], 1, "Meticulous means showing great attention to detail — precise."),
        ("Choose the antonym of 'Benevolent'.", ["Kind", "Cruel", "Generous", "Helpful"], 1, "Benevolent means well-meaning and kindly; cruel is its opposite."),
        ("What is the one-word substitution for 'one who does not believe in the existence of God'?", ["Atheist", "Theist", "Agnostic", "Pantheist"], 0, "An atheist denies the existence of God (an agnostic merely doubts)."),
        ("Choose the synonym of 'Ephemeral'.", ["Long-lasting", "Short-lived", "Beautiful", "Dangerous"], 1, "Ephemeral means lasting for a very short time."),
        ("Choose the antonym of 'Transparent'.", ["Clear", "Opaque", "Thin", "Bright"], 1, "Transparent lets light through; opaque does not."),
        ("What does the idiom 'a blessing in disguise' mean?", ["An obvious gift", "A misfortune that turns out well", "A religious ceremony", "A hidden danger"], 1, "It refers to something that seems bad at first but turns out to be good."),
    ],
    "advanced": [
        ("Choose the synonym of 'Obsequious'.", ["Arrogant", "Servile", "Honest", "Curious"], 1, "Obsequious means excessively obedient or servile."),
        ("Choose the antonym of 'Eloquent'.", ["Articulate", "Inarticulate", "Fluent", "Persuasive"], 1, "Eloquent means fluent and persuasive in speech; inarticulate is its opposite."),
        ("What is the one-word substitution for 'the study of ancient inscriptions'?", ["Epigraphy", "Etymology", "Ecology", "Ergonomics"], 0, "Epigraphy is the study of inscriptions; etymology studies word origins."),
        ("Choose the synonym of 'Laconic'.", ["Wordy", "Terse", "Rude", "Funny"], 1, "Laconic means using very few words — terse."),
        ("Choose the antonym of 'Benevolent' in the context of a ruler.", ["Merciful", "Tyrannical", "Generous", "Just"], 1, "A benevolent ruler is kindly; a tyrannical one is oppressive."),
        ("What does the idiom 'to burn the midnight oil' mean?", ["To waste resources", "To work late into the night", "To cause a fire", "To celebrate"], 1, "It means to work or study late into the night."),
    ],
}

GRAMMAR: Bank = {
    "beginner": [
        ("Choose the correct sentence about her school routine.", ["She go to school every day.", "She goes to school every day.", "She going to school every day.", "She is go to school every day."], 1, "Third-person singular subjects take 'goes' in the simple present."),
        ("Fill in the blank: He ____ a book yesterday.", ["reads", "read", "is reading", "has read"], 1, "'Yesterday' signals the simple past — 'read' (past form)."),
        ("Choose the correct article: ____ sun rises in the east.", ["A", "An", "The", "No article"], 2, "Unique celestial bodies take 'the'."),
        ("Fill in the blank: I am good ____ mathematics.", ["in", "on", "at", "of"], 2, "The fixed preposition is 'good at' a subject."),
        ("Choose the plural of 'child'.", ["childs", "children", "childrens", "childes"], 1, "Child has the irregular plural 'children'."),
        ("Fill in the blank: They ____ playing cricket now.", ["is", "are", "was", "am"], 1, "'They' takes 'are'; 'now' indicates the present continuous."),
    ],
    "intermediate": [
        ("Fill in the blank: If it rains, we ____ the match.", ["cancel", "cancelled", "will cancel", "would cancel"], 2, "In a first conditional, the if-clause uses simple present and the main clause uses 'will + verb'."),
        ("Choose the correct sentence about the number of students.", ["The number of students are increasing.", "The number of students is increasing.", "The number of students have increased.", "A number of students is increasing."], 1, "'The number of' is singular and takes a singular verb."),
        ("Fill in the blank: He has been working here ____ 2019.", ["for", "since", "from", "by"], 1, "'Since' is used with a point in time; 'for' with a duration."),
        ("Identify the correct tag: Let's go for a walk, ____?", ["will we", "shall we", "don't we", "won't we"], 1, "'Let's' (let us) takes the tag 'shall we'."),
        ("Choose the correct sentence using 'neither of'.", ["Neither of the boys were present.", "Neither of the boys was present.", "Neither of the boys have been present.", "Neither the boys was present."], 1, "'Neither of' takes a singular verb — 'was'."),
        ("Fill in the blank: She spoke ____ than her brother.", ["more fluently", "most fluently", "fluenter", "most fluent"], 0, "Two subjects are compared, so the comparative 'more fluently' is correct."),
    ],
    "advanced": [
        ("Choose the correct sentence using 'hardly'.", ["Hardly had he arrived when it started raining.", "Hardly had he arrived than it started raining.", "Hardly he had arrived when it started raining.", "Hardly did he arrived when it started raining."], 0, "'Hardly ... when' is the correct correlative pair, with inversion after 'Hardly had'."),
        ("Fill in the blank: The committee ____ divided in their opinions.", ["is", "are", "was being", "has"], 1, "When members act individually, a collective noun takes a plural verb — 'are'."),
        ("Identify the error: 'One of my friend is a doctor.'", ["One of", "my friend", "is", "a doctor"], 1, "It should be 'one of my friends' — 'one of' is always followed by a plural noun."),
        ("Choose the correct passive: 'Who wrote this poem?'", ["By whom was this poem written?", "Whom was this poem written?", "Who was this poem written?", "This poem was written by who?"], 0, "Passive of 'who wrote' is 'by whom was ... written'."),
        ("Fill in the blank: ____ he worked hard, he failed to qualify.", ["Although", "Because", "Unless", "Since"], 0, "The sentence shows contrast, so the concessive conjunction 'although' fits."),
        ("Choose the correct sentence about the noun 'data'.", ["The data is sufficient for the analysis.", "The data are sufficient for the analysis.", "Both are acceptable depending on usage.", "Neither is correct."], 2, "'Data' is traditionally plural but singular usage is widely accepted — both are in use."),
    ],
}

ERROR_SPOTTING: Bank = {
    "beginner": [
        ("Find the error: (a) Ram and Sita / (b) goes to school / (c) every day. / (d) No error", ["(a)", "(b)", "(c)", "(d)"], 1, "'Ram and Sita' is plural, so the verb should be 'go', not 'goes'."),
        ("Find the error: (a) He do not / (b) like coffee. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 0, "'He' takes 'does not' — 'do not' is wrong."),
        ("Find the error: (a) I have seen him / (b) yesterday. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'Yesterday' requires simple past — 'I saw him yesterday'."),
        ("Find the error: (a) She is senior / (b) than me. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'Senior' takes 'to', not 'than' — 'senior to me'."),
        ("Find the error: (a) The furniture / (b) are new. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'Furniture' is uncountable and takes a singular verb — 'is new'."),
        ("Find the error: (a) One of the boy / (b) has won the prize. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 0, "'One of the' must be followed by a plural noun — 'one of the boys'."),
    ],
    "intermediate": [
        ("Find the error: (a) Each of the students / (b) have submitted the assignment. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'Each of' takes a singular verb — 'has submitted'."),
        ("Find the error: (a) He is one of the best / (b) player in the team. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'One of the best' takes a plural noun — 'players'."),
        ("Find the error: (a) Despite of the rain, / (b) they went out. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 0, "'Despite' is never followed by 'of' — 'despite the rain'."),
        ("Find the error: (a) The number of applicants / (b) were increasing every year. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'The number of' is singular — 'was increasing'."),
        ("Find the error: (a) He asked me / (b) that whether I had finished. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'That' and 'whether' cannot be used together — use 'whether' alone."),
        ("Find the error: (a) I would like / (b) to help you in this matter. / (c) No error", ["(a)", "(b)", "(c)", "No error in any part"], 3, "'I would like to help you in this matter' is grammatically correct — there is no error."),
    ],
    "advanced": [
        ("Find the error: (a) Hardly had the meeting begun / (b) when the power went off. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 2, "The construction 'hardly had ... when ...' is correct — no error."),
        ("Find the error: (a) He was, / (b) I knew, the best candidate. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 2, "Parenthetical insertion of 'I knew' is correct — no error."),
        ("Find the error: (a) The reason why / (b) he failed is / (c) because he was lazy. / (d) No error", ["(a)", "(b)", "(c)", "(d)"], 2, "'The reason is because' is redundant — it should be 'the reason ... is that he was lazy'."),
        ("Find the error: (a) Between you and I, / (b) the plan will not work. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 0, "After a preposition, the objective case is required — 'between you and me'."),
        ("Find the error: (a) He insisted / (b) to go with me. / (c) No error", ["(a)", "(b)", "(c)", "(a) and (b)"], 1, "'Insist' takes the gerund or 'that' clause — 'insisted on going'."),
        ("Find the error: (a) Not only the students / (b) but also the teacher / (c) were present. / (d) No error", ["(a)", "(b)", "(c)", "(d)"], 2, "With 'not only ... but also', the verb agrees with the nearer subject — 'the teacher was present'."),
    ],
}

RC_PASSAGES = {
    "beginner": (
        "The sun is a star at the centre of our solar system. It gives the earth light and heat. "
        "Plants use sunlight to make their own food in a process called photosynthesis. "
        "Without the sun, life on earth would not be possible."
    ),
    "intermediate": (
        "Rivers have supported human civilisation for thousands of years. Cities grew along river banks because "
        "water made farming, trade and transport easy. Even today rivers supply drinking water and hydroelectric "
        "power. However, untreated waste and plastic pollution threaten the health of many rivers, and cleaning "
        "them requires cooperation between governments and citizens."
    ),
    "advanced": (
        "Automation has transformed industries by taking over repetitive tasks, but economists disagree about its "
        "effect on employment. Optimists argue that machines create new kinds of work faster than they destroy "
        "old ones, while pessimists point to regions where factories closed and never reopened. Most researchers "
        "agree that the key lies in retraining workers, so that the benefits of higher productivity are shared "
        "rather than concentrated among a few."
    ),
}

READING: Bank = {
    "beginner": [
        (f"Passage: '{RC_PASSAGES['beginner']}'\n\nWhere is the sun located?", ["At the edge of the solar system", "At the centre of our solar system", "Beyond the moon", "Inside the earth"], 1, "The first line states the sun is at the centre of our solar system."),
        (f"Passage: '{RC_PASSAGES['beginner']}'\n\nWhat do plants use to make food?", ["Moonlight", "Soil", "Sunlight", "Rainwater"], 2, "The passage says plants use sunlight for photosynthesis."),
        (f"Passage: '{RC_PASSAGES['beginner']}'\n\nWhat is the process of making food called?", ["Respiration", "Photosynthesis", "Transpiration", "Condensation"], 1, "The process is called photosynthesis."),
        (f"Passage: '{RC_PASSAGES['beginner']}'\n\nWhat does the sun give the earth?", ["Only light", "Only heat", "Light and heat", "Water"], 2, "The passage says the sun gives the earth light and heat."),
        (f"Passage: '{RC_PASSAGES['beginner']}'\n\nThe sun is a:", ["Planet", "Moon", "Star", "Comet"], 2, "The passage calls the sun a star."),
        (f"Passage: '{RC_PASSAGES['beginner']}'\n\nWithout the sun, life on earth:", ["Would continue normally", "Would not be possible", "Would move underground", "Would become colder only"], 1, "The last line says life on earth would not be possible without the sun."),
    ],
    "intermediate": [
        (f"Passage: '{RC_PASSAGES['intermediate']}'\n\nWhy did cities grow along river banks?", ["Rivers provided defence", "Water supported farming, trade and transport", "Rivers were beautiful", "Land was cheaper there"], 1, "The passage says water made farming, trade and transport easy."),
        (f"Passage: '{RC_PASSAGES['intermediate']}'\n\nWhat do rivers still supply today?", ["Only water for farming", "Drinking water and hydroelectric power", "Nothing useful", "Only transport"], 1, "The passage states rivers still supply drinking water and hydroelectric power."),
        (f"Passage: '{RC_PASSAGES['intermediate']}'\n\nWhat threatens many rivers?", ["Too much rainfall", "Untreated waste and plastic pollution", "Drought only", "Fishing"], 1, "The passage identifies untreated waste and plastic pollution as the threats."),
        (f"Passage: '{RC_PASSAGES['intermediate']}'\n\nCleaning rivers requires:", ["Only foreign aid", "Cooperation between governments and citizens", "Stopping all farming", "Building new rivers"], 1, "The last line says it requires cooperation between governments and citizens."),
        (f"Passage: '{RC_PASSAGES['intermediate']}'\n\nCivilisations have been supported by rivers for:", ["A few years", "Thousands of years", "Centuries only since 1900", "Millions of years"], 1, "The first line says thousands of years."),
        (f"Passage: '{RC_PASSAGES['intermediate']}'\n\nThe tone of the passage is mainly:", ["Humorous", "Informative and concerned", "Angry", "Sarcastic"], 1, "It explains facts about rivers and expresses concern about pollution."),
    ],
    "advanced": [
        (f"Passage: '{RC_PASSAGES['advanced']}'\n\nWhat do optimists believe about automation?", ["Machines destroy jobs permanently", "New work is created faster than old work disappears", "Factories will reopen by themselves", "Retraining is useless"], 1, "Optimists argue machines create new kinds of work faster than they destroy old ones."),
        (f"Passage: '{RC_PASSAGES['advanced']}'\n\nWhat do pessimists point to?", ["Regions where factories closed permanently", "New software companies", "Higher wages for all", "Shorter working hours"], 0, "Pessimists point to regions where factories closed and never reopened."),
        (f"Passage: '{RC_PASSAGES['advanced']}'\n\nWhere do most researchers place their hope?", ["In banning machines", "In retraining workers", "In lower taxes", "In shorter weeks"], 1, "Most researchers agree the key lies in retraining workers."),
        (f"Passage: '{RC_PASSAGES['advanced']}'\n\nThe phrase 'benefits of higher productivity are shared' implies:", ["Productivity should fall", "Gains should not be concentrated among a few", "Machines should be banned", "Workers should retire early"], 1, "Shared means distributed widely rather than concentrated among a few."),
        (f"Passage: '{RC_PASSAGES['advanced']}'\n\nWhy do economists disagree?", ["Over the effect of automation on employment", "Over the price of machines", "Over the age of workers", "Over internet speeds"], 0, "The passage says economists disagree about automation's effect on employment."),
        (f"Passage: '{RC_PASSAGES['advanced']}'\n\nAutomation has mainly transformed industries by:", ["Taking over repetitive tasks", "Ending all work", "Reducing productivity", "Closing every factory"], 0, "The first line says automation takes over repetitive tasks."),
    ],
}

CLOZE_PASSAGES = {
    "beginner": "Ravi (1)____ to school every morning. He (2)____ his uniform before leaving. At school, he (3)____ hard in class and (4)____ his lunch with friends. In the evening, he (5)____ his homework and then (6)____ with his younger sister.",
    "intermediate": "The government (1)____ a new scheme to (2)____ clean water to every village. Under the plan, local teams (3)____ the existing pipelines and (4)____ new connections. Officials claim the scheme (5)____ be completed (6)____ the next two years.",
    "advanced": "Although the new policy was (1)____ with much fanfare, its (2)____ have been uneven. Rural districts, which (3)____ the greatest need, received the (4)____ funds. Economists therefore (5)____ a fundamental (6)____ in how resources are allocated.",
}

CLOZE: Bank = {
    "beginner": [
        ("Passage: 'Ravi (1)____ to school every morning...'\n\nChoose the word for blank (1).", ["go", "goes", "going", "gone"], 1, "'Ravi' is third-person singular, so 'goes' fits the simple present."),
        ("Passage: 'Ravi ... (2)____ his uniform before leaving...'\n\nChoose the word for blank (2).", ["wear", "wears", "wearing", "wore"], 1, "Third-person singular simple present: 'wears'."),
        ("Passage: '...he (3)____ hard in class...'\n\nChoose the word for blank (3).", ["work", "works", "worked", "working"], 1, "'Works hard' agrees with 'he' in the simple present."),
        ("Passage: '...and (4)____ his lunch with friends...'\n\nChoose the word for blank (4).", ["share", "shares", "sharing", "shared"], 1, "'Shares' agrees with 'he'."),
        ("Passage: 'In the evening, he (5)____ his homework...'\n\nChoose the word for blank (5).", ["do", "does", "doing", "did"], 1, "'Does his homework' is correct for third-person singular."),
        ("Passage: '...and then (6)____ with his younger sister.'\n\nChoose the word for blank (6).", ["play", "plays", "playing", "played"], 1, "'Plays' agrees with 'he' — the passage is in simple present."),
    ],
    "intermediate": [
        ("Passage: 'The government (1)____ a new scheme...'\n\nChoose the word for blank (1).", ["launch", "launched", "launches", "launching"], 1, "A completed policy announcement takes the simple past — 'launched'."),
        ("Passage: '...to (2)____ clean water to every village.'\n\nChoose the word for blank (2).", ["provide", "providing", "provided", "provides"], 0, "After 'to' the base form 'provide' is required (infinitive of purpose)."),
        ("Passage: '...local teams (3)____ the existing pipelines...'\n\nChoose the word for blank (3).", ["inspect", "inspected", "inspects", "inspecting"], 1, "Past tense 'inspected' keeps the narrative consistent."),
        ("Passage: '...and (4)____ new connections.'\n\nChoose the word for blank (4).", ["install", "installed", "installs", "installing"], 1, "Past tense 'installed' follows 'and' parallel to 'inspected'."),
        ("Passage: '...the scheme (5)____ be completed...'\n\nChoose the word for blank (5).", ["shall", "has", "was", "did"], 0, "'Shall be completed' expresses an official promise about the future."),
        ("Passage: '...completed (6)____ the next two years.'\n\nChoose the word for blank (6).", ["within", "since", "from", "by"], 0, "'Within the next two years' is the correct collocation for a deadline."),
    ],
    "advanced": [
        ("Passage: 'Although the new policy was (1)____ with much fanfare...'\n\nChoose the word for blank (1).", ["launched", "launch", "launching", "launches"], 0, "Passive voice needs the past participle — 'was launched'."),
        ("Passage: '...its (2)____ have been uneven.'\n\nChoose the word for blank (2).", ["effects", "effect", "affects", "effective"], 0, "The noun 'effects' (results) with plural verb 'have been' fits."),
        ("Passage: 'Rural districts, which (3)____ the greatest need...'\n\nChoose the word for blank (3).", ["face", "faces", "faced", "facing"], 0, "'Which' refers to plural 'districts', so 'face' agrees."),
        ("Passage: '...received the (4)____ funds.'\n\nChoose the word for blank (4).", ["least", "fewest", "less", "little"], 1, "Countable plural 'funds' takes 'fewest' — the least funds would be for uncountables."),
        ("Passage: 'Economists therefore (5)____ a fundamental (6)____...'\n\nChoose the word for blank (5).", ["urge", "urges", "urged", "urging"], 0, "Plural subject 'economists' takes 'urge'."),
        ("Passage: '...a fundamental (6)____ in how resources are allocated.'\n\nChoose the word for blank (6).", ["change", "changing", "changed", "changes"], 0, "After 'a fundamental' the singular noun 'change' fits."),
    ],
}


def get_english(topic_slug: str, difficulty: str) -> list[QuestionDict]:
    bank: Bank = {
        "vocabulary": VOCAB,
        "grammar": GRAMMAR,
        "error-spotting": ERROR_SPOTTING,
        "reading-comprehension": READING,
        "cloze-test": CLOZE,
    }[topic_slug]
    return [
        {"question_text": q, "options": list(opts), "correct_index": idx, "explanation": expl, "difficulty": difficulty}
        for q, opts, idx, expl in bank[difficulty]
    ]
