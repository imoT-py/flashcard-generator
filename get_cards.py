# This is the second python file from Project: Automatic Flashcard Generator For Anki

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import urllib.request
import deepl
import sys

# DeepL API key
auth_key = "PLACE OF THE API KEY (because I can't share it)"
translator = deepl.Translator(auth_key)


# Get words as input and upload them to Anki
def cards_to_anki(words_list):

    for word in words_list:
        # translate the English word to Hungarian
        translated_word = translator.translate_text(word, target_lang="HU").text

        # words is a list; with get_url we get the following from https://dictionary.cambridge.org/:
        # words[0]: English word
        # words[1]: written pronunciation of the said word
        # words[2]: audio url of the pronunciation
        words = get_url(word)
        if words is None:
            continue

        front = words[0].text + ' ' + '/' + words[1].text + '/'

        # The parameters what Anki need to be able to create a card
        # Front side will be the English word, the written pronunciation and the audio
        # Back side will be the translated word in Hungarian
        note_params = {
            "deckName": "English words",
            "modelName": "Basic (and reversed card)",
            "fields": {
                "Front": front,
                "Back": translated_word
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "audio": [{
                "url": words[2],
                "filename": word + ".mp3",
                "fields": ["Front"]
            }]
        }
        # Make a card in Anki
        try:
            invoke('addNote', note=note_params)
        except:
            continue


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


# request and invoke need to send the data from python to Anki
def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


# Get the required data from https://dictionary.cambridge.org/
def get_url(original_word):

    url = "https://dictionary.cambridge.org/dictionary/english/" + original_word

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        english_word = soup.find('span', class_='hw dhw')
        pronounce_word = soup.find('span', class_='ipa dipa lpr-2 lpl-1')

        try:
            audio_link = 'https://dictionary.cambridge.org/' + soup.find('source')['src']

            info_list = [english_word, pronounce_word, audio_link]
            return info_list
        except AttributeError:
            return None
    else:
        sys.exit()
