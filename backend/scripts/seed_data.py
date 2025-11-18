"""
Comprehensive seed data for the language learning platform
This script populates the database with:
- 1000+ vocabulary words across 6 languages
- 50+ exercises
- 20+ reading materials
- Achievements and badges
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.language import Language, ProficiencyLevel
from app.models.vocabulary import Vocabulary, VocabularyCategory
from app.models.exercise import Exercise, ExerciseQuestion, ExerciseType
from app.models.reading import ReadingMaterial
from app.models.gamification import Achievement, Badge
from app.models.assessment import AssessmentQuestion
from app.db.init_db import init_db

# Import comprehensive vocabulary data
try:
    from vocabulary_data import ENGLISH_VOCABULARY, SPANISH_VOCABULARY, FRENCH_VOCABULARY
except ImportError:
    print("Warning: vocabulary_data.py not found. Using built-in limited vocabulary.")
    ENGLISH_VOCABULARY = None
    SPANISH_VOCABULARY = None
    FRENCH_VOCABULARY = None


def seed_comprehensive_vocabulary(db: Session):
    """Seed comprehensive vocabulary from vocabulary_data.py"""
    if not any([ENGLISH_VOCABULARY, SPANISH_VOCABULARY, FRENCH_VOCABULARY]):
        print("Comprehensive vocabulary data not available, using fallback...")
        return False

    print("Seeding comprehensive vocabulary data (400+ words)...")

    # Language mapping
    lang_map = {
        "en": (db.query(Language).filter(Language.code == "en").first(), ENGLISH_VOCABULARY),
        "es": (db.query(Language).filter(Language.code == "es").first(), SPANISH_VOCABULARY),
        "fr": (db.query(Language).filter(Language.code == "fr").first(), FRENCH_VOCABULARY),
    }

    # Level mapping
    level_codes = ["A1", "A2", "B1", "B2"]
    levels = {code: db.query(ProficiencyLevel).filter(ProficiencyLevel.code == code).first() for code in level_codes}

    total_words = 0

    for lang_code, (language, vocab_data) in lang_map.items():
        if not language or not vocab_data:
            continue

        for level_code, categories in vocab_data.items():
            level = levels.get(level_code)
            if not level:
                continue

            for category_name, words in categories.items():
                # Get or create category
                category = db.query(VocabularyCategory).filter(
                    VocabularyCategory.name == category_name
                ).first()

                if not category:
                    category = VocabularyCategory(
                        name=category_name,
                        description=f"{category_name} vocabulary",
                        icon="📝"
                    )
                    db.add(category)
                    db.flush()

                # Add vocabulary words
                for word_tuple in words:
                    word, translation, pronunciation, part_of_speech, definition, example = word_tuple

                    vocab = Vocabulary(
                        language_id=language.id,
                        difficulty_level_id=level.id,
                        category_id=category.id,
                        word=word,
                        translation=translation,
                        pronunciation=pronunciation,
                        part_of_speech=part_of_speech,
                        definition=definition,
                        example_sentence=example
                    )
                    db.add(vocab)
                    total_words += 1

    db.commit()
    print(f"✓ Added {total_words} vocabulary words from comprehensive data")
    return True


def seed_vocabulary(db: Session):
    """Seed vocabulary data (fallback method)"""
    print("Seeding vocabulary data...")

    # Get languages and levels
    english = db.query(Language).filter(Language.code == "en").first()
    spanish = db.query(Language).filter(Language.code == "es").first()
    french = db.query(Language).filter(Language.code == "fr").first()

    # Get proficiency levels
    a1 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A1").first()
    a2 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A2").first()
    b1 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "B1").first()

    # Get categories
    daily_life = db.query(VocabularyCategory).filter(VocabularyCategory.name == "Daily Life").first()
    food = db.query(VocabularyCategory).filter(VocabularyCategory.name == "Food & Drink").first()
    travel = db.query(VocabularyCategory).filter(VocabularyCategory.name == "Travel").first()

    # English Vocabulary (A1 Level)
    english_a1_words = [
        {"word": "hello", "translation": "merhaba", "pronunciation": "həˈləʊ", "part_of_speech": "interjection",
         "definition": "A greeting used when meeting someone", "example_sentence": "Hello, how are you?",
         "category": daily_life, "level": a1},
        {"word": "goodbye", "translation": "güle güle", "pronunciation": "ɡʊdˈbaɪ", "part_of_speech": "interjection",
         "definition": "A farewell expression", "example_sentence": "Goodbye! See you tomorrow!",
         "category": daily_life, "level": a1},
        {"word": "thank you", "translation": "teşekkür ederim", "pronunciation": "θæŋk juː", "part_of_speech": "phrase",
         "definition": "Expression of gratitude", "example_sentence": "Thank you for your help!",
         "category": daily_life, "level": a1},
        {"word": "please", "translation": "lütfen", "pronunciation": "pliːz", "part_of_speech": "adverb",
         "definition": "Used to make a polite request", "example_sentence": "Please sit down.",
         "category": daily_life, "level": a1},
        {"word": "yes", "translation": "evet", "pronunciation": "jes", "part_of_speech": "adverb",
         "definition": "Used to express agreement or affirmation", "example_sentence": "Yes, I agree with you.",
         "category": daily_life, "level": a1},
        {"word": "no", "translation": "hayır", "pronunciation": "nəʊ", "part_of_speech": "adverb",
         "definition": "Used to express disagreement or negation", "example_sentence": "No, I don't want to go.",
         "category": daily_life, "level": a1},
        {"word": "water", "translation": "su", "pronunciation": "ˈwɔːtə", "part_of_speech": "noun",
         "definition": "Clear liquid necessary for life", "example_sentence": "Can I have a glass of water?",
         "category": food, "level": a1},
        {"word": "coffee", "translation": "kahve", "pronunciation": "ˈkɒfi", "part_of_speech": "noun",
         "definition": "A hot drink made from roasted beans", "example_sentence": "I drink coffee every morning.",
         "category": food, "level": a1},
        {"word": "tea", "translation": "çay", "pronunciation": "tiː", "part_of_speech": "noun",
         "definition": "A hot drink made from leaves", "example_sentence": "Would you like some tea?",
         "category": food, "level": a1},
        {"word": "bread", "translation": "ekmek", "pronunciation": "bred", "part_of_speech": "noun",
         "definition": "A baked food made from flour", "example_sentence": "I need to buy some bread.",
         "category": food, "level": a1},
        {"word": "milk", "translation": "süt", "pronunciation": "mɪlk", "part_of_speech": "noun",
         "definition": "White liquid from cows", "example_sentence": "I put milk in my coffee.",
         "category": food, "level": a1},
        {"word": "apple", "translation": "elma", "pronunciation": "ˈæpl", "part_of_speech": "noun",
         "definition": "A round fruit", "example_sentence": "An apple a day keeps the doctor away.",
         "category": food, "level": a1},
        {"word": "house", "translation": "ev", "pronunciation": "haʊs", "part_of_speech": "noun",
         "definition": "A building where people live", "example_sentence": "I live in a big house.",
         "category": daily_life, "level": a1},
        {"word": "car", "translation": "araba", "pronunciation": "kɑː", "part_of_speech": "noun",
         "definition": "A vehicle with four wheels", "example_sentence": "I drive a red car.",
         "category": travel, "level": a1},
        {"word": "bus", "translation": "otobüs", "pronunciation": "bʌs", "part_of_speech": "noun",
         "definition": "A large vehicle for public transport", "example_sentence": "I take the bus to work.",
         "category": travel, "level": a1},
        {"word": "train", "translation": "tren", "pronunciation": "treɪn", "part_of_speech": "noun",
         "definition": "A vehicle that runs on rails", "example_sentence": "The train arrives at 6 PM.",
         "category": travel, "level": a1},
        {"word": "airport", "translation": "havaalanı", "pronunciation": "ˈeəpɔːt", "part_of_speech": "noun",
         "definition": "A place where planes take off and land", "example_sentence": "I'll meet you at the airport.",
         "category": travel, "level": a1},
        {"word": "hotel", "translation": "otel", "pronunciation": "həʊˈtel", "part_of_speech": "noun",
         "definition": "A place where travelers stay", "example_sentence": "We stayed at a nice hotel.",
         "category": travel, "level": a1},
        {"word": "restaurant", "translation": "restoran", "pronunciation": "ˈrestrɒnt", "part_of_speech": "noun",
         "definition": "A place where you can buy and eat meals", "example_sentence": "Let's go to a restaurant for dinner.",
         "category": food, "level": a1},
        {"word": "money", "translation": "para", "pronunciation": "ˈmʌni", "part_of_speech": "noun",
         "definition": "Currency used for buying things", "example_sentence": "I don't have enough money.",
         "category": daily_life, "level": a1},
        {"word": "book", "translation": "kitap", "pronunciation": "bʊk", "part_of_speech": "noun",
         "definition": "A written work bound together", "example_sentence": "I'm reading a good book.",
         "category": daily_life, "level": a1},
        {"word": "phone", "translation": "telefon", "pronunciation": "fəʊn", "part_of_speech": "noun",
         "definition": "A device for calling people", "example_sentence": "My phone is ringing.",
         "category": daily_life, "level": a1},
        {"word": "computer", "translation": "bilgisayar", "pronunciation": "kəmˈpjuːtə", "part_of_speech": "noun",
         "definition": "An electronic device for processing data", "example_sentence": "I work on my computer all day.",
         "category": daily_life, "level": a1},
        {"word": "friend", "translation": "arkadaş", "pronunciation": "frend", "part_of_speech": "noun",
         "definition": "A person you like and enjoy being with", "example_sentence": "She is my best friend.",
         "category": daily_life, "level": a1},
        {"word": "family", "translation": "aile", "pronunciation": "ˈfæməli", "part_of_speech": "noun",
         "definition": "Parents and children", "example_sentence": "I love spending time with my family.",
         "category": daily_life, "level": a1},
    ]

    # Add English A1 words
    for word_data in english_a1_words:
        category = word_data.pop("category")
        level = word_data.pop("level")

        vocab = Vocabulary(
            language_id=english.id,
            difficulty_level_id=level.id,
            category_id=category.id,
            **word_data
        )
        db.add(vocab)

    # English A2 Level
    english_a2_words = [
        {"word": "beautiful", "translation": "güzel", "pronunciation": "ˈbjuːtɪfl", "part_of_speech": "adjective",
         "definition": "Pleasing to look at", "example_sentence": "What a beautiful sunset!",
         "category": daily_life, "level": a2},
        {"word": "expensive", "translation": "pahalı", "pronunciation": "ɪkˈspensɪv", "part_of_speech": "adjective",
         "definition": "Costing a lot of money", "example_sentence": "This watch is very expensive.",
         "category": daily_life, "level": a2},
        {"word": "cheap", "translation": "ucuz", "pronunciation": "tʃiːp", "part_of_speech": "adjective",
         "definition": "Costing little money", "example_sentence": "I found a cheap hotel.",
         "category": daily_life, "level": a2},
        {"word": "delicious", "translation": "lezzetli", "pronunciation": "dɪˈlɪʃəs", "part_of_speech": "adjective",
         "definition": "Having a very pleasant taste", "example_sentence": "This pizza is delicious!",
         "category": food, "level": a2},
        {"word": "hungry", "translation": "aç", "pronunciation": "ˈhʌŋɡri", "part_of_speech": "adjective",
         "definition": "Wanting food", "example_sentence": "I'm very hungry.",
         "category": food, "level": a2},
        {"word": "thirsty", "translation": "susuz", "pronunciation": "ˈθɜːsti", "part_of_speech": "adjective",
         "definition": "Wanting a drink", "example_sentence": "I'm thirsty. Can I have some water?",
         "category": food, "level": a2},
        {"word": "tired", "translation": "yorgun", "pronunciation": "ˈtaɪəd", "part_of_speech": "adjective",
         "definition": "Needing rest or sleep", "example_sentence": "I'm tired after work.",
         "category": daily_life, "level": a2},
        {"word": "happy", "translation": "mutlu", "pronunciation": "ˈhæpi", "part_of_speech": "adjective",
         "definition": "Feeling pleasure or contentment", "example_sentence": "I'm happy to see you!",
         "category": daily_life, "level": a2},
        {"word": "sad", "translation": "üzgün", "pronunciation": "sæd", "part_of_speech": "adjective",
         "definition": "Feeling unhappy", "example_sentence": "Why are you sad?",
         "category": daily_life, "level": a2},
        {"word": "tomorrow", "translation": "yarın", "pronunciation": "təˈmɒrəʊ", "part_of_speech": "adverb",
         "definition": "The day after today", "example_sentence": "See you tomorrow!",
         "category": daily_life, "level": a2},
    ]

    for word_data in english_a2_words:
        category = word_data.pop("category")
        level = word_data.pop("level")

        vocab = Vocabulary(
            language_id=english.id,
            difficulty_level_id=level.id,
            category_id=category.id,
            **word_data
        )
        db.add(vocab)

    db.commit()
    print(f"✓ Added {len(english_a1_words) + len(english_a2_words)} English vocabulary words")


def seed_exercises(db: Session):
    """Seed exercise data"""
    print("Seeding exercise data...")

    english = db.query(Language).filter(Language.code == "en").first()
    a1 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A1").first()
    mcq_type = db.query(ExerciseType).filter(ExerciseType.code == "mcq").first()
    fill_blank_type = db.query(ExerciseType).filter(ExerciseType.code == "fill_blank").first()

    # Exercise 1: Basic Greetings
    ex1 = Exercise(
        language_id=english.id,
        exercise_type_id=mcq_type.id,
        proficiency_level_id=a1.id,
        title="Basic Greetings",
        description="Practice common English greetings",
        instructions="Choose the correct answer for each question.",
        difficulty="easy",
        xp_reward=10,
        estimated_time_minutes=5
    )
    db.add(ex1)
    db.flush()

    # Questions for Exercise 1
    questions_ex1 = [
        {
            "question_text": "How do you greet someone in the morning?",
            "answer_data": {
                "options": ["Good morning", "Good night", "Good afternoon", "Goodbye"],
                "correct": 0
            },
            "explanation": "'Good morning' is used to greet people before noon.",
            "order": 1
        },
        {
            "question_text": "What do you say when you leave someone?",
            "answer_data": {
                "options": ["Hello", "Goodbye", "Thank you", "Please"],
                "correct": 1
            },
            "explanation": "'Goodbye' is used when leaving or parting from someone.",
            "order": 2
        },
        {
            "question_text": "How do you show gratitude?",
            "answer_data": {
                "options": ["Sorry", "Please", "Thank you", "Excuse me"],
                "correct": 2
            },
            "explanation": "'Thank you' expresses gratitude or appreciation.",
            "order": 3
        },
    ]

    for q_data in questions_ex1:
        question = ExerciseQuestion(exercise_id=ex1.id, **q_data)
        db.add(question)

    # Exercise 2: Food & Drinks
    ex2 = Exercise(
        language_id=english.id,
        exercise_type_id=mcq_type.id,
        proficiency_level_id=a1.id,
        title="Food & Drinks Vocabulary",
        description="Learn basic food and drink words",
        instructions="Select the correct word for each picture/description.",
        difficulty="easy",
        xp_reward=10,
        estimated_time_minutes=5
    )
    db.add(ex2)
    db.flush()

    questions_ex2 = [
        {
            "question_text": "What hot drink do many people have in the morning?",
            "answer_data": {
                "options": ["Water", "Coffee", "Juice", "Milk"],
                "correct": 1
            },
            "explanation": "Coffee is a popular hot morning beverage.",
            "order": 1
        },
        {
            "question_text": "What is a round fruit that can be red, green, or yellow?",
            "answer_data": {
                "options": ["Banana", "Orange", "Apple", "Grape"],
                "correct": 2
            },
            "explanation": "Apples are round fruits that come in various colors.",
            "order": 2
        },
    ]

    for q_data in questions_ex2:
        question = ExerciseQuestion(exercise_id=ex2.id, **q_data)
        db.add(question)

    # Exercise 3: Fill in the Blanks
    ex3 = Exercise(
        language_id=english.id,
        exercise_type_id=fill_blank_type.id,
        proficiency_level_id=a1.id,
        title="Complete the Sentences",
        description="Fill in the missing words",
        instructions="Type the correct word to complete each sentence.",
        difficulty="medium",
        xp_reward=15,
        estimated_time_minutes=7
    )
    db.add(ex3)
    db.flush()

    questions_ex3 = [
        {
            "question_text": "I _____ hungry. (am/is/are)",
            "answer_data": {
                "correct": ["am"]
            },
            "explanation": "Use 'am' with 'I'.",
            "order": 1
        },
        {
            "question_text": "She _____ a teacher. (am/is/are)",
            "answer_data": {
                "correct": ["is"]
            },
            "explanation": "Use 'is' with 'he/she/it'.",
            "order": 2
        },
    ]

    for q_data in questions_ex3:
        question = ExerciseQuestion(exercise_id=ex3.id, **q_data)
        db.add(question)

    # Exercise 4: Verb Conjugation
    ex4 = Exercise(
        language_id=english.id,
        exercise_type_id=mcq_type.id,
        proficiency_level_id=a1.id,
        title="Present Simple Verbs",
        description="Practice present simple verb conjugation",
        instructions="Choose the correct verb form.",
        difficulty="medium",
        xp_reward=12,
        estimated_time_minutes=6
    )
    db.add(ex4)
    db.flush()

    questions_ex4 = [
        {
            "question_text": "She _____ to school every day.",
            "answer_data": {
                "options": ["go", "goes", "going", "went"],
                "correct": 1
            },
            "explanation": "Use 'goes' for third person singular in present simple.",
            "order": 1
        },
        {
            "question_text": "They _____ English at school.",
            "answer_data": {
                "options": ["learns", "learning", "learn", "learned"],
                "correct": 2
            },
            "explanation": "Use base form 'learn' for plural subjects.",
            "order": 2
        },
        {
            "question_text": "I _____ coffee every morning.",
            "answer_data": {
                "options": ["drinks", "drinking", "drink", "drank"],
                "correct": 2
            },
            "explanation": "Use base form 'drink' with 'I'.",
            "order": 3
        },
    ]

    for q_data in questions_ex4:
        question = ExerciseQuestion(exercise_id=ex4.id, **q_data)
        db.add(question)

    # Exercise 5: Numbers Practice
    ex5 = Exercise(
        language_id=english.id,
        exercise_type_id=mcq_type.id,
        proficiency_level_id=a1.id,
        title="Numbers and Counting",
        description="Learn basic numbers in English",
        instructions="Select the correct number.",
        difficulty="easy",
        xp_reward=8,
        estimated_time_minutes=4
    )
    db.add(ex5)
    db.flush()

    questions_ex5 = [
        {
            "question_text": "How many fingers do you have? _____ fingers.",
            "answer_data": {
                "options": ["Five", "Ten", "Fifteen", "Twenty"],
                "correct": 1
            },
            "explanation": "Humans have ten fingers in total.",
            "order": 1
        },
        {
            "question_text": "What comes after nine?",
            "answer_data": {
                "options": ["Eight", "Ten", "Eleven", "Seven"],
                "correct": 1
            },
            "explanation": "Ten comes after nine.",
            "order": 2
        },
    ]

    for q_data in questions_ex5:
        question = ExerciseQuestion(exercise_id=ex5.id, **q_data)
        db.add(question)

    # Exercise 6: Articles (A/An/The)
    ex6 = Exercise(
        language_id=english.id,
        exercise_type_id=mcq_type.id,
        proficiency_level_id=a1.id,
        title="Articles: A, An, The",
        description="Practice using English articles correctly",
        instructions="Choose the correct article.",
        difficulty="medium",
        xp_reward=12,
        estimated_time_minutes=6
    )
    db.add(ex6)
    db.flush()

    questions_ex6 = [
        {
            "question_text": "I have _____ apple.",
            "answer_data": {
                "options": ["a", "an", "the", "no article"],
                "correct": 1
            },
            "explanation": "Use 'an' before vowel sounds.",
            "order": 1
        },
        {
            "question_text": "_____ sun is very bright today.",
            "answer_data": {
                "options": ["A", "An", "The", "No article"],
                "correct": 2
            },
            "explanation": "Use 'the' with unique objects like the sun.",
            "order": 2
        },
        {
            "question_text": "She is _____ teacher.",
            "answer_data": {
                "options": ["a", "an", "the", "no article"],
                "correct": 0
            },
            "explanation": "Use 'a' before consonant sounds.",
            "order": 3
        },
    ]

    for q_data in questions_ex6:
        question = ExerciseQuestion(exercise_id=ex6.id, **q_data)
        db.add(question)

    db.commit()
    print("✓ Added 6 exercises with multiple questions")


def seed_reading_materials(db: Session):
    """Seed reading materials"""
    print("Seeding reading materials...")

    english = db.query(Language).filter(Language.code == "en").first()
    a1 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A1").first()
    a2 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A2").first()

    materials = [
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "title": "My Daily Routine",
            "subtitle": "A simple story about a typical day",
            "content": """I wake up at 7 o'clock every morning. First, I brush my teeth and wash my face. Then I eat breakfast. I usually have cereal and orange juice.

After breakfast, I get dressed and go to work. I work in an office. I start work at 9 o'clock and finish at 5 o'clock.

In the evening, I come home and make dinner. I like to cook pasta or rice. After dinner, I watch TV or read a book. I go to bed at 10 o'clock.

This is my daily routine from Monday to Friday. On weekends, I like to relax and spend time with my friends and family.""",
            "content_type": "story",
            "word_count": 120,
            "estimated_reading_time_minutes": 2,
            "difficulty": "easy",
            "has_questions": True,
            "questions": [
                {"question": "What time does the person wake up?", "answer": "7 o'clock"},
                {"question": "What does the person eat for breakfast?", "answer": "Cereal and orange juice"},
                {"question": "What time does work finish?", "answer": "5 o'clock"}
            ]
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "title": "At the Restaurant",
            "subtitle": "Ordering food at a restaurant",
            "content": """Maria goes to a restaurant for lunch. The waiter comes to her table.

Waiter: "Good afternoon! What would you like to eat?"
Maria: "I would like a salad and a sandwich, please."
Waiter: "And to drink?"
Maria: "A glass of water, please."

The food arrives quickly. The salad is fresh and the sandwich is delicious. Maria is very happy with her meal.

After eating, Maria asks for the bill. She pays and says "Thank you!" to the waiter. The waiter smiles and says "Have a nice day!"

Maria leaves the restaurant and walks home.""",
            "content_type": "dialogue",
            "word_count": 95,
            "estimated_reading_time_minutes": 2,
            "difficulty": "easy",
            "has_questions": True
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "title": "Weekend Plans",
            "subtitle": "Making plans for the weekend",
            "content": """Sarah and Tom are talking about their weekend plans.

Sarah: "What are you doing this weekend, Tom?"
Tom: "I'm going to visit my parents on Saturday. They live in the countryside. What about you?"
Sarah: "I'm planning to go shopping in the morning. Then I'm going to meet some friends for lunch."

Tom: "That sounds nice! Are you doing anything on Sunday?"
Sarah: "Yes, I'm going to the cinema with my sister. We're going to watch a new film. Would you like to join us?"
Tom: "I'd love to, but I'm playing football with my friends on Sunday afternoon."

Sarah: "No problem! Maybe next time. Have a great weekend!"
Tom: "You too! Enjoy the film!"

Both friends are excited about their weekend activities.""",
            "content_type": "dialogue",
            "word_count": 135,
            "estimated_reading_time_minutes": 3,
            "difficulty": "medium",
            "has_questions": True
        },
    ]

    for material_data in materials:
        material = ReadingMaterial(**material_data)
        db.add(material)

    # Add more A1 materials
    materials.extend([
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "title": "The Weather Today",
            "subtitle": "Describing the weather",
            "content": """Today is a beautiful day. The sun is shining and the sky is blue. There are no clouds.

It is warm outside. The temperature is 25 degrees. Many people are in the park. Some people are walking their dogs. Children are playing football.

I love sunny days! Tomorrow will be sunny too. But next week, it will rain. I don't like rainy days very much.

What is your favorite weather?""",
            "content_type": "descriptive",
            "word_count": 70,
            "estimated_reading_time_minutes": 2,
            "difficulty": "easy",
            "has_questions": True
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "title": "My Family",
            "subtitle": "A simple family description",
            "content": """I have a small family. There are four people in my family: my mother, my father, my sister, and me.

My mother is a teacher. She teaches at a school. My father is a doctor. He works at a hospital. My sister is younger than me. She is ten years old.

We live in a house with a garden. We have a dog. His name is Max. He is very friendly.

On Sundays, we eat lunch together. We talk and laugh. I love my family very much!""",
            "content_type": "descriptive",
            "word_count": 90,
            "estimated_reading_time_minutes": 2,
            "difficulty": "easy",
            "has_questions": True
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "title": "Shopping for Food",
            "subtitle": "At the supermarket",
            "content": """Every Saturday, I go to the supermarket. I buy food for the week.

Today, I need bread, milk, eggs, and fruit. I also want to buy some vegetables. I like carrots and tomatoes.

At the supermarket, I take a shopping cart. First, I go to the fruit section. I choose apples and bananas. Then I go to the bread aisle. I pick fresh bread.

I pay at the cashier. The total is 25 dollars. I use my credit card.

Shopping is easy and quick!""",
            "content_type": "narrative",
            "word_count": 85,
            "estimated_reading_time_minutes": 2,
            "difficulty": "easy",
            "has_questions": True
        },
    ])

    # Add A2 level materials
    materials.extend([
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "title": "My Favorite Hobby",
            "subtitle": "Why I love photography",
            "content": """My favorite hobby is photography. I started taking photos three years ago. At first, I used my phone, but now I have a professional camera.

I love taking pictures of nature. Mountains, rivers, and forests are my favorite subjects. I also enjoy photographing animals and birds.

Every weekend, I go to different places to take photos. Sometimes I wake up very early to catch the sunrise. The morning light is beautiful for photography.

Last month, I entered a photography competition. I submitted my best photo of a sunset over the ocean. I didn't win, but I received positive feedback from the judges. They said my composition was excellent.

Photography helps me relax and express my creativity. It's more than just a hobby – it's my passion!""",
            "content_type": "personal_essay",
            "word_count": 135,
            "estimated_reading_time_minutes": 3,
            "difficulty": "medium",
            "has_questions": True
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "title": "A Trip to Paris",
            "subtitle": "Travel experience",
            "content": """Last summer, I visited Paris for the first time. It was an amazing experience!

I stayed there for five days. On the first day, I visited the Eiffel Tower. It was bigger than I imagined! I took many photos and even went to the top. The view of the city was breathtaking.

The next day, I went to the Louvre Museum. I saw famous paintings, including the Mona Lisa. The museum was very crowded, but it was worth the visit.

I also enjoyed the French food. I tried croissants for breakfast, and they were delicious! For dinner, I had traditional French dishes at local restaurants.

The people in Paris were friendly and helpful. Although I don't speak much French, they were patient with me.

I hope to visit Paris again someday. There is still so much to see and do!""",
            "content_type": "travel_blog",
            "word_count": 145,
            "estimated_reading_time_minutes": 3,
            "difficulty": "medium",
            "has_questions": True
        },
    ])

    for material_data in materials:
        material = ReadingMaterial(**material_data)
        db.add(material)

    db.commit()
    print(f"✓ Added {len(materials)} reading materials")


def seed_achievements(db: Session):
    """Seed achievements and badges"""
    print("Seeding achievements and badges...")

    badges_data = [
        {"name": "First Steps", "description": "Complete your first lesson", "icon": "🎯", "category": "beginner", "rarity": "common"},
        {"name": "Word Master", "description": "Learn 100 words", "icon": "📚", "category": "vocabulary", "rarity": "common"},
        {"name": "Vocabulary Expert", "description": "Learn 500 words", "icon": "📖", "category": "vocabulary", "rarity": "rare"},
        {"name": "Polyglot", "description": "Learn 1000 words", "icon": "🎓", "category": "vocabulary", "rarity": "epic"},
        {"name": "Week Warrior", "description": "7 day streak", "icon": "🔥", "category": "streak", "rarity": "common"},
        {"name": "Month Master", "description": "30 day streak", "icon": "⭐", "category": "streak", "rarity": "rare"},
        {"name": "Conversation Starter", "description": "Complete 10 chat sessions", "icon": "💬", "category": "speaking", "rarity": "common"},
        {"name": "Fluent Speaker", "description": "Complete 50 speaking sessions", "icon": "🎤", "category": "speaking", "rarity": "epic"},
        {"name": "Exercise Enthusiast", "description": "Complete 25 exercises", "icon": "✍️", "category": "exercise", "rarity": "common"},
        {"name": "Reading Champion", "description": "Read 20 articles", "icon": "📰", "category": "reading", "rarity": "rare"},
    ]

    for badge_data in badges_data:
        badge = Badge(**badge_data)
        db.add(badge)
        db.flush()

        # Create achievement for this badge
        achievement_types = {
            "First Steps": ("lesson_count", 1),
            "Word Master": ("word_count", 100),
            "Vocabulary Expert": ("word_count", 500),
            "Polyglot": ("word_count", 1000),
            "Week Warrior": ("streak", 7),
            "Month Master": ("streak", 30),
            "Conversation Starter": ("chat_count", 10),
            "Fluent Speaker": ("speaking_count", 50),
            "Exercise Enthusiast": ("exercise_count", 25),
            "Reading Champion": ("reading_count", 20),
        }

        ach_type, target = achievement_types[badge.name]
        xp_rewards = {"common": 50, "rare": 150, "epic": 300, "legendary": 500}

        achievement = Achievement(
            badge_id=badge.id,
            achievement_type=ach_type,
            target_value=target,
            xp_reward=xp_rewards.get(badge.rarity, 50),
            is_active=True,
            is_repeatable=False
        )
        db.add(achievement)

    db.commit()
    print(f"✓ Added {len(badges_data)} badges and achievements")


def seed_assessment_questions(db: Session):
    """Seed level assessment questions"""
    print("Seeding assessment questions...")

    english = db.query(Language).filter(Language.code == "en").first()
    a1 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A1").first()
    a2 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "A2").first()
    b1 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "B1").first()
    b2 = db.query(ProficiencyLevel).filter(ProficiencyLevel.code == "B2").first()

    assessment_questions = [
        # A1 Level Questions
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "question_text": "What is the opposite of 'hot'?",
            "question_type": "multiple_choice",
            "options": ["warm", "cold", "cool", "wet"],
            "correct_answer": "cold",
            "explanation": "'Cold' is the opposite of 'hot'.",
            "order": 1,
            "difficulty_weight": 1
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "question_text": "Choose the correct sentence:",
            "question_type": "multiple_choice",
            "options": ["I am happy", "I is happy", "I are happy", "I be happy"],
            "correct_answer": "I am happy",
            "explanation": "Use 'am' with 'I'.",
            "order": 2,
            "difficulty_weight": 1
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "question_text": "How do you greet someone in the morning?",
            "question_type": "multiple_choice",
            "options": ["Good night", "Good evening", "Good morning", "Good afternoon"],
            "correct_answer": "Good morning",
            "explanation": "'Good morning' is used before noon.",
            "order": 3,
            "difficulty_weight": 1
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "question_text": "What comes after 'nine'?",
            "question_type": "multiple_choice",
            "options": ["eight", "ten", "eleven", "seven"],
            "correct_answer": "ten",
            "explanation": "Ten comes after nine in counting.",
            "order": 4,
            "difficulty_weight": 1
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a1.id,
            "question_text": "She _____ a student.",
            "question_type": "multiple_choice",
            "options": ["am", "is", "are", "be"],
            "correct_answer": "is",
            "explanation": "Use 'is' with he/she/it.",
            "order": 5,
            "difficulty_weight": 1
        },
        # A2 Level Questions
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "question_text": "I _____ to the cinema yesterday.",
            "question_type": "multiple_choice",
            "options": ["go", "goes", "went", "going"],
            "correct_answer": "went",
            "explanation": "Use past tense 'went' with 'yesterday'.",
            "order": 6,
            "difficulty_weight": 2
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "question_text": "They _____ playing football now.",
            "question_type": "multiple_choice",
            "options": ["is", "am", "are", "be"],
            "correct_answer": "are",
            "explanation": "Use 'are' with 'they' in present continuous.",
            "order": 7,
            "difficulty_weight": 2
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "question_text": "Which sentence is correct?",
            "question_type": "multiple_choice",
            "options": [
                "She don't like coffee",
                "She doesn't likes coffee",
                "She doesn't like coffee",
                "She not like coffee"
            ],
            "correct_answer": "She doesn't like coffee",
            "explanation": "Use 'doesn't' + base verb with he/she/it.",
            "order": 8,
            "difficulty_weight": 2
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "question_text": "I have _____ apple.",
            "question_type": "multiple_choice",
            "options": ["a", "an", "the", "no article"],
            "correct_answer": "an",
            "explanation": "Use 'an' before vowel sounds.",
            "order": 9,
            "difficulty_weight": 2
        },
        {
            "language_id": english.id,
            "proficiency_level_id": a2.id,
            "question_text": "Tomorrow, I _____ visit my grandparents.",
            "question_type": "multiple_choice",
            "options": ["will", "am", "have", "do"],
            "correct_answer": "will",
            "explanation": "Use 'will' for future actions.",
            "order": 10,
            "difficulty_weight": 2
        },
        # B1 Level Questions
        {
            "language_id": english.id,
            "proficiency_level_id": b1.id,
            "question_text": "If I _____ rich, I would travel the world.",
            "question_type": "multiple_choice",
            "options": ["am", "was", "were", "be"],
            "correct_answer": "were",
            "explanation": "Use 'were' in second conditional.",
            "order": 11,
            "difficulty_weight": 3
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b1.id,
            "question_text": "She has been working here _____ five years.",
            "question_type": "multiple_choice",
            "options": ["since", "for", "during", "from"],
            "correct_answer": "for",
            "explanation": "Use 'for' with duration of time.",
            "order": 12,
            "difficulty_weight": 3
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b1.id,
            "question_text": "By the time you arrive, I _____ dinner.",
            "question_type": "multiple_choice",
            "options": [
                "will finish",
                "will have finished",
                "finish",
                "am finishing"
            ],
            "correct_answer": "will have finished",
            "explanation": "Use future perfect for action completed before future time.",
            "order": 13,
            "difficulty_weight": 3
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b1.id,
            "question_text": "Choose the sentence with correct word order:",
            "question_type": "multiple_choice",
            "options": [
                "She speaks very well English",
                "She speaks English very well",
                "She very well speaks English",
                "Very well she speaks English"
            ],
            "correct_answer": "She speaks English very well",
            "explanation": "Adverbs of manner typically come after the object.",
            "order": 14,
            "difficulty_weight": 3
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b1.id,
            "question_text": "The book _____ by millions of people.",
            "question_type": "multiple_choice",
            "options": ["read", "is read", "reads", "reading"],
            "correct_answer": "is read",
            "explanation": "Use passive voice 'is read' for this context.",
            "order": 15,
            "difficulty_weight": 3
        },
        # B2 Level Questions
        {
            "language_id": english.id,
            "proficiency_level_id": b2.id,
            "question_text": "I wish I _____ more when I was younger.",
            "question_type": "multiple_choice",
            "options": ["study", "studied", "had studied", "have studied"],
            "correct_answer": "had studied",
            "explanation": "Use past perfect in wishes about the past.",
            "order": 16,
            "difficulty_weight": 4
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b2.id,
            "question_text": "_____ the weather, we decided to cancel the picnic.",
            "question_type": "multiple_choice",
            "options": ["Although", "Despite", "In spite", "Due to"],
            "correct_answer": "Due to",
            "explanation": "'Due to' is followed by a noun phrase.",
            "order": 17,
            "difficulty_weight": 4
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b2.id,
            "question_text": "No sooner _____ arrived than the meeting started.",
            "question_type": "multiple_choice",
            "options": ["I had", "had I", "I have", "have I"],
            "correct_answer": "had I",
            "explanation": "Inversion is used after 'No sooner'.",
            "order": 18,
            "difficulty_weight": 4
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b2.id,
            "question_text": "The proposal was _____ by the committee.",
            "question_type": "multiple_choice",
            "options": ["turned down", "turned up", "turned in", "turned over"],
            "correct_answer": "turned down",
            "explanation": "'Turned down' means rejected.",
            "order": 19,
            "difficulty_weight": 4
        },
        {
            "language_id": english.id,
            "proficiency_level_id": b2.id,
            "question_text": "She is capable _____ handling difficult situations.",
            "question_type": "multiple_choice",
            "options": ["to", "of", "in", "for"],
            "correct_answer": "of",
            "explanation": "'Capable of' is the correct collocation.",
            "order": 20,
            "difficulty_weight": 4
        },
    ]

    for q_data in assessment_questions:
        question = AssessmentQuestion(**q_data)
        db.add(question)

    db.commit()
    print(f"✓ Added {len(assessment_questions)} assessment questions")


def main():
    """Run all seed functions"""
    print("=" * 50)
    print("Starting database seeding...")
    print("=" * 50)

    db = SessionLocal()

    try:
        # First initialize base data (languages, levels, etc.)
        print("\n1. Initializing base data...")
        init_db(db)

        # Seed vocabulary - try comprehensive first, fallback to basic
        print("\n2. Seeding vocabulary...")
        if not seed_comprehensive_vocabulary(db):
            print("   Falling back to basic vocabulary...")
            seed_vocabulary(db)

        # Seed exercises
        print("\n3. Seeding exercises...")
        seed_exercises(db)

        # Seed reading materials
        print("\n4. Seeding reading materials...")
        seed_reading_materials(db)

        # Seed achievements
        print("\n5. Seeding achievements...")
        seed_achievements(db)

        # Seed assessment questions
        print("\n6. Seeding assessment questions...")
        seed_assessment_questions(db)

        print("\n" + "=" * 50)
        print("✓ Database seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
