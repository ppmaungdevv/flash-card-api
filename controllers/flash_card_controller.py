from flask import Blueprint, request, jsonify, send_file, make_response
from gtts import gTTS
import io
import json
import random

flash_card_blueprint = Blueprint('flash_card', __name__)

@flash_card_blueprint.route('/generate_quiz', methods = ['POST'])
def generate_quiz():

    """
    Generate a quiz with a specified number of consonants.

    Request JSON:
        consonant_count (int): Number of consonants to generate (1 <= num <= 44).
        is_random (bool): If True, randomly shuffle consonants; else, shuffle alphabetically.

    Returns (JSON):
        generated_consonants (list): List of generated consonants.
        quiz (dict): Contains:
            question (str): The consonant used as the quiz question.
            choices (list): List of dictionaries with:
                word (str): The consonant choice.
                pronunciation (str): The pronunciation of the consonant.
    """

    data = request.get_json()
    is_random = data.get('is_random')
    consonant_count = int(data.get('consonant_count'))
    lang = data.get('lang') or 'th'
    ja_kana = data.get('ja_kana')

    data_path = get_data_path(lang, ja_kana)
    
    consonants_json = get_json_data(data_path)
    # consonants_json = get_json_data('./data/u.json')

    generated_consonants_list = get_consonants(consonants_json, consonant_count, is_random)

    quiz = { 
            'question': generated_consonants_list[0],
            'choices': get_quiz_choices(consonants_json, generated_consonants_list[0], lang)
        }

    resp = {
        "generated_consonants": generated_consonants_list,
        "quiz": quiz,
        # "data_path": consonants_test
    }
    
    return jsonify(resp)

@flash_card_blueprint.route('/get_multiple_choice', methods = ['POST'])
def get_multiple_choice():

    data = request.get_json()
    question_consonant = data.get('question_consonant')
    lang = data.get('lang') or 'th'
    ja_kana = data.get('ja_kana')

    data_path = get_data_path(lang, ja_kana)

    consonants_json = get_json_data(data_path)

    choices = get_quiz_choices(consonants_json, question_consonant, lang)

    resp = {
        "question_consonant": question_consonant,
        "choices": choices
    }
    return jsonify(resp)

def get_data_path(lang, ja_kana):
    data_path = './data/'

    if lang == 'th':
        data_path += 'u.json'

    if lang == 'ja':
        if ja_kana == 'hiragana':
            data_path += 'hiragana_data.json'
        
        # 'mixed'

        if ja_kana == 'katakana':
            data_path += 'katakana_data.json'

    return data_path

def get_consonants(consonants_json, consonant_count, is_random):

    """
    Generate a list of consonants based on the specified count and randomness.

    Args:
        consonants_json (dict): Dictionary containing consonants data.
        consonant_count (int): Number of consonants to generate.
        is_random (bool): If True, select consonants randomly; if False, select alphabetically.

    Returns:
        list: List of generated consonants.
    """
    
    consonants_keys = list(consonants_json.keys())
    consonant_range = 43 if is_random else consonant_count - 1
    generated_consonants = set()

    while len(generated_consonants) < consonant_count:
        consonant = consonants_keys[random.randint(0, consonant_range)]
        generated_consonants.add(consonant)

    generated_consonants_list = list(generated_consonants)

    return generated_consonants_list

def get_quiz_choices(consonants_json, question_consonant,  lang, choice_count = 4):

    """
    Generate quiz choices based on the provided question consonant.

    Args:
        consonants_json (dict): Dictionary containing consonants data.
        question_consonant (str): The consonant that is the focus of the quiz question.
        choice_count (int, optional): Number of choices to generate. Defaults to 4.

    Returns:
        list: List of choices, each a dictionary with 'word' and 'pronunciation' keys.
    """

    consonants_keys = list(consonants_json.keys())

    words = { question_consonant }
    pronuns = { question_consonant: get_pronunciation(consonants_json, question_consonant, lang) }
    question_consonant_index = consonants_keys.index(question_consonant)

    if(question_consonant_index != len(consonants_keys) - 1):
        # question_consonant_index ka 43 so yin + 1 lote lo ma ya buu
        next_consonant = consonants_keys[question_consonant_index + 1]
        words.add(next_consonant)
        pronuns[next_consonant] = get_pronunciation(consonants_json, next_consonant, lang)

    while len(words) < choice_count:
        consonant = consonants_keys[random.randint(0, 43)]
        words.add(consonant)
        pronuns[consonant] = get_pronunciation(consonants_json, consonant, lang)

    choices = [ { "word": word, "pronuncation": pronuns[word] } for word in words ]

    random.shuffle(choices)

    return choices

def get_json_data(file_path):
    
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    return json_data

def get_pronunciation(consonants_json, consonant, lang):

    return consonants_json[consonant]["letter"] if lang == 'ja' else consonants_json[consonant]["pronunciation"]