PyQt5 Flashcards
================

A simple yet decent flashcards apps for desktop - run on popular operating systems such as Windows, MacOS and Linux. Executable files (.exe, .app, etc) will be available soon.

Description
-----------

- This is a basic flashcards app made of **Python** and **Qt**. Add some decks and cards, then start reviewing with flashcards mode (real-life flashcards simulation - to review any time) and game mode (play some games with the cards and ) 
- Python version is used here: **<a href="https://docs.python.org/3/whatsnew/3.8.html">Python 3.8</a>**.
- Qt version is used here: **<a href="https://pypi.org/project/PyQt5/">PyQt5</a> (Qt bindings for Python)**, with Qt 5.15

Functions
---------
* Add decks and cards to study 
* Use flashcards mode to review (w/ spaced repetition and process record) 
* Edit and delete decks and cards 
* Play simple games (multiple choices and box filling) with simple uniform spaced repetition algorithms

User manual
-----------
Run `flashcards.py` as the main script (executable files is out soon). Run 
```bash
   pip install -r requirements.txt
```
to install all neccessary packages from pip.
1. Home page/ Browse deck.

   This is the first thing showing up when starting the program.
   * If there is no deck, click the icon or the `Add deck` button to add a new deck. <br>
     Note: If nothing shows up after add deck, please `right click > Refresh` to fix (I will fix this bug soon) <br>
     A deck is displayed as white group boxes with the deck's name, number of cards in deck and number of cards to review
   * The white button on the top: currently, the options from that button is 'Settings' (now is in development)
   * To delete a deck, click `... > Delete this deck`
   * To rename a deck, click `... > Rename this deck`
2. Cards list
   * To access here, click the `View cards list' button
   * To add cards, click the `Add cards` button, and type the information for the front and the back of the card. Adding an image is optional. <br>
     If no card shows up after adding cards, please try `Right click > Refresh`.
   * To delete a card, click `... > Delete this card`.
   * To edit a card, click `... > Edit this card`, a popup will show to edit it
   * To reset review date, click `... > Reset review date`
3. Flashcards mode
   * From the home page (browse deck mode), click `Flashcards Mode`.
   * Click `flip` or click on the card to see both faces of the card (like paper flashcards).
   * Click `>` (Next) to move to the next card, `<` (Previous) to move to the previous card
   * Click the `Shuffle` button to shuffle the deck
   * Click the `Practice` button to practice with game mode
5. Game mode

   There are two games in game mode: 'multiple choices' and 'filling in the box':
   - 'Multiple choice': The back of a card will be asked, and there are four choices with just one correct answer, which is the text in the front of the card
   - 'Filling in the box': The back of a card will be asked, and user needs to type their answers in the grey box below and click `Submit` to check their answer
   - Notes:
      - In 'Filling in the box' game, don't worry if you type some trailing space or tabs (so-called "whitespace characters") because the program will omit them.
      - The score given will be 10 for each correct answer, and 0 for the wrong one.

7. Import/Export deck to CSV, XML and JSON
   (CSV recommended)
   * To import deck, go to home page, click `Add deck` <br>
     Tick the choice `Import files (JSON, XML and CSV are supported)', choose files
   * To export deck, click `... > Export cards` in the expected deck on the home page
   * Note: the format of exported file:
      - CSV: `id, front, back, ""` (any delimeter are accepted, and the whitespace character in the fourth place can be omitted)
      - XML: E.g
           ```xml
               <? xml version="1.0" ?>
               <deck name=demo>
                  <card>
                     <id>1</id>
                     <front>foo</front>
                     <back>bar</back>
                  </card>
                  <card>
                     <id>2</id>
                     <front>front</front>
                     <back>back</back>
                  </card>
               </deck>
           ```
      - JSON: `{id: {"front": front_text, "back": back_text}}.`<br>
         E.g:
         ```json
         {"1": {"front":"Facebook", "back":"The most popular social network where people share and communicate together"},
            "2": {"front":"Github", "back": "A website using git, where people store, share and collaborate on their code"}
         ```
