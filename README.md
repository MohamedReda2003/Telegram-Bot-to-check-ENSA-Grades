
# Telegram Bot to Check ENSA Grades
This project involves automating the process of checking and notifying students of their grades on the ENSA school's platform. It uses Playwright and Selenium to automate the login process, check for new grades, and send notifications via Telegram. The project also stores the grade information in a MongoDB database and continuously monitors the website for updates.

## Features
- Automated Login: Automates the login process to the ENSA grades platform.
- Grade Check: Periodically checks for new grades.
- Telegram Notifications: Sends notifications to individual users and the promotion group on Telegram.
- Data Parsing: Uses Parsel to parse grade data from the website.
- Database Storage: Stores grade information in a MongoDB database.
- Continuous Monitoring: Keeps an eye on the website for any new updates.




## To run the code on your machine:
  - ### 1. Install the dependencies
  ```
  pip install -r requirements.txt
  ```
  - ### 2. Set up MongoDB:

    - Ensure you have MongoDB installed and running.
    - Update the database connection details in the script.
  - ### 3.Configure Telegram Bot:

    - Create a Telegram bot using BotFather and get the API token.
    - Update the bot token and chat IDs in the script.
  - ### 4.Then just run the file you chose out of the three 
  ```
  python ultimatetelegrambot.py
  ```
  or:
  ```
  python ultimatetelegrambot2.py
  ```
  or :
  ```
  python new-grade-bot.py
  ```
#### And here we go!
## Screenshots from the scripts execution

![Result Screenshot](https://github.com/MohamedReda2003/Telegram-Bot-to-check-ENSA-Grades/assets/61638355/2d3289d1-d1ae-4588-b1a8-d44432f1f701)

![Result Screenshot](https://github.com/MohamedReda2003/Telegram-Bot-to-check-ENSA-Grades/assets/61638355/124e1275-3514-486f-bc6b-bc12f4f430d8)

(The messages are written in French )

