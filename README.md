# Automatic Flashcard Generator For Anki
#### Video demo: https://www.youtube.com/watch?v=fourN3CpWRI
#### Description: 

Before my app, about Anki: Anki is a card-learning program, so it's perfect for students who 
want to learn or improve their foreign languages. In Anki, you can create a cards of deck, then create
cards in that deck. Later you can study these cards. For more information about Anki, visit: https://apps.ankiweb.net/

My app:
The problem: The issue arose when I started using Anki and realized that creating a card consumed a significant amount of time.
Created the cards as follows:
  - Front side: English word + pronunciation + audio file
  - Back side: The translated word in Hungarian language
  
The solution: I automated the process and made a python file which do the followings: 

- From a list one by one get the word, written pronunciation and the audio url from https://dictionary.cambridge.org
- From DeepL API translates the word one by one to Hungarian
- With this information the program create Anki cards automatically 

The Card Maker for Anki consists of two Python files:
- get_cards.py, handles the backend processes
- input_words.py, manages the GUI

#####get_cards.py

This file consist of the functions that answer for downloading the words and url, also for the 
translation. Then in Anki the cards will be created. More about the functions one by one:

- cards_to_anki(word_list): the main function of the file, it gets a list of word then 
run through get_url(original_word), translate the word to Hungarian and use the invoke function to 
create the cards in Anki
- request and invoke: Anki specific functions and are used for communication between the program and Anki.
'invoke()' gets two variable: 'action' and '**params'
  -action: What we want to do in Anki. I want to add a new card two times (1. English front, Hungarian back, 2. Hungarian front, English back):
in that case I use 'addnote'.
  - **params: Anki specific value to give every needed parameter which need to create a card. These values are in 'note_params' variable
- get_url(original_word): After we run this function we get a variable which is a list, consist of three
elements: 
  - words[0]: English word 
  - words[1]: written pronunciation of the said word 
  - words[2]: audio url of the pronunciation

For fetching I used the 'requests' module, so I can get the word's webpage and get the required informations.
For translation, I chose DeepL API, because it seemed the most simple and the registration took literally no effort.


#####input_words.py

This file consist of the program's GUI. With this, we have a window, where we can write any number of words
and add them to a list. After we have enough words we create that many Anki cards. The GUI has been made with the
tkinter module. 

There are three buttons in the file: 'btn,' 'btn_card,' and 'btn_delete:

- 'btn': add the word to the list -> run the 'clicked(event=None)' function
- 'btn_card': create Anki cards with the list's words -> run the 'create()' function
- 'btn_delete': delete word from the list in the GUI -> run the 'delete()' function

All three buttons 'connect' to a function. When the buttons are clicked the functions start running.