![crაtm](https://user-images.githubusercontent.com/47547779/227625794-296b28ef-1876-4dff-a8fb-7c2b51bb00fd.png)
# AI psychologist (rus)
This is a telegram bot in role of a personal psychologist. It's working with Openai api. 
## REMEMBER, this is a computer program I made for fun. 
## Don't use It to solve serious mental problems!

# Table of Contents

1. [Installation](#installation)
2. [Contributing](#contributing)
3. [Improving scenario](#improving-scenario)
4. [Credits](#credits)

## Installation
1. Download repo on you computer
2. Install dependencies from requirements.txt
3. Run file "dbscript.py" to create your local database

## Usage
To use this bot you need your own API keys for telegram and openai
1. Get telegram key from bot "BotFather" in telegram
2. Paste it into the file *main.py* as a TOKEN variable value. Line 34
```python
TOKEN = open("tg_TOKEN.txt", "r", encoding="utf-8").read()
```
3. Get API key for openai from your own account
4. Paste it into the file *gtp_logic.py* as a openai.api_key variable value. Line 12
```python
openai.api_key = open("gtp_TOKEN.txt", 'r', encoding="utf-8").read()
```
5. Run main script and your bot will become active
6. Prompts on Russian language. Change every prompt on language you need

## Contributing
1. Clone repo and create a new branch
2. Make changes and test
3. Submit pull request with comprehensive discription of changes

## Improving scenario
There is a lot of things can be done to improve this bot in my opnion.
Here some of them:
1. User data should be saved and sended to a "system" prompt
2. User authentification
3. Session shouldn't start from the beggining every time when connection is breaking
4. Bot menu should be always available
5. User should pass a little questionnaire to set bot more correctly through changing prompts
6. User data should be hashed
7. Secure methods

## Credits
Big thanks to [Ilya Lysov](https://github.com/LisovIlya) for idea
## Contact
- linkedin - https://www.linkedin.com/in/eugene-poluyakhtov-924181256/ 
- telegram - @epguitars
## Acknowledgments
- Thanks [python-telegram-bot](https://github.com/python-telegram-bot) team for python telegram library! 
- Thanks openai team for model and api!
