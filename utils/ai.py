import json
import random

import openai
from django.conf import settings

from companies.models import Company, TriviaQuestion, TriviaQuestionOption

openai.api_key = settings.OPENAI_KEY

DEFAULT_MODEL = "gpt-3.5-turbo-16k"


def prompt_gpt(prompt, model=DEFAULT_MODEL, temperature=1.5):
    completion = openai.ChatCompletion.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return completion.choices[0].message


def trivia_question(company_id=5):
    company = Company.objects.get(pk=company_id)
    user_data = []
    for user in company.users.all():
        user_data.append(user.answer_blob())
    random.shuffle(
        user_data
    )  # Shuffle the input data so that we get questions about different users
    prompt = """
    You are a trivia bot that creates multiple choice questions from real data. You will vary the questions and answers based on the real data. 
    You are given a list of information related to N users real data and you will return a multiple choice question with 2-5 options and a valid answer from the real data.
    The response should always be in the form of a question with 3-5 options and a valid answer from the real data in json format.
    Do not use any of the example questions or answers in your response.
    Do not make up any fake information, only use the information provided in the real data.
    You will be scored based on the quality of the questions and answers you generate.

    For example:
        Given the following information:
        [
            {
                "name": "Aaron Spindler",
                "title": "CEO",
                "location": "Toronto",
                "team": "Executive Office",
                "personality_type": "Architect (INTJ)",
                "chinese_zodiac": "Ox",
                "zodiac_sign": "Scorpio",
                "favourite_food": "Sushi",
                "favourite_movie": "The Accountant",
                "favourite_travel_destination": "Berlin",
            },
            {
                "name": "Fred Flintstone",
                "title": "VP Engineering",
                "location": "Seattle, Washington",
                "team": "Engineering",
                "personality_type": "Leader (ESTJ)",
                "chinese_zodiac": "Rat",
                "zodiac_sign": "Aries",
                "favourite_food": "Pizza",
                "favourite_movie": "Troy",
                "favourite_travel_destination": "Tokyo",
            },
            {
                "name": "Austin Powers",
                "title": "Sales Associate",
                "location": "NYC",
                "team": "Growth",
                "personality_type": "Inquisitor (ISTP)",
                "chinese_zodiac": "Rat",
                "zodiac_sign": "Gemini",
                "favourite_food": "Pasta",
                "favourite_movie": "The Social Network",
                "favourite_travel_destination": "Lake Como",
            },
        ]
        You will create a trivia question like:
        {
            "question": "Who is the CEO?",
            "options": [
                "Aaron Spindler",
                "Fred Flintstone",
                "Bob Bobberson",
                ],
            "answer": "Aaron Spindler",
        }
        OR
        {
            "question": "Whos favourite travel destination is Lake Como?",
            "options": [
                "Austin Powers",
                "Fred Flintstone",
                "Aaron Spindler",
                ],
            "answer": "Austin Powers",
        }
        OR
        {
            "question": "What is the most common chinese zodiac sign?",
            "options": [
                "Ox",
                "Rat",
                ],
            "answer": "Rat",
        }
    Real Data:
    \"\"\"
    """
    prompt = prompt + str(user_data)
    prompt = prompt + '"""'
    response = prompt_gpt(prompt)
    try:
        message_json = json.loads(response["content"])
        question_text = message_json["question"] or None
        options = message_json["options"] or None
        answer = message_json["answer"] or None

        # Make sure that none of the required elements are empty
        if (
            not question_text
            or not options
            or not answer
            or len(options) < 2
            or answer not in options
        ):
            raise Exception("Invalid response")

        # Check if the question already exists
        question = TriviaQuestion.objects.filter(
            question__icontains=question_text, company=company
        )
        if question.exists():
            raise Exception("Question already exists")

        # Create the question
        question_instance = TriviaQuestion.objects.create(
            question=question_text, company=company
        )

        # Create the options
        for option in options:
            correct = False
            if option == answer:
                correct = True
            TriviaQuestionOption.objects.create(
                question=question_instance, text=option, correct=correct
            )

        print(question_text)
        print(options)
        print(answer)
    except Exception as e:
        print(response)
        print(e)
