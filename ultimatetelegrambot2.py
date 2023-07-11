import subprocess
subprocess.check_call([ "pip", "install", "pymongo"])
subprocess.check_call([ "pip", "install", "playwright"])
subprocess.check_call([ "pip", "install", "pyTelegramBotAPI"])
subprocess.check_call([ "pip", "install", "selenium"])
subprocess.check_call([ "pip", "install", "webdriver_manager"])


from telebot import types
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time
import threading


#subprocess.check_call([ "playwright", "install", "chromium"])

TOKEN = 'Bot Token from BotFather'
CHAT_ID = 'the chatID'
print("Here we go")
bot = telebot.TeleBot(TOKEN)


cluster=MongoClient("Token from MongoDB")
db =cluster["ENSA2023"]
collection=db["modules-ENSA2023"]
bad_collection=db['bab_language']
affiche=collection.find_one()

def run():
    options = webdriver.ChromeOptions()
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    # options.binary_location = '/usr/bin/chromium'
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    
    print('the page')
    driver.get("https://ent.ensa-tetouan.ac.ma/?home/index")
    
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Email"]'))).click()
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Email"]').send_keys("email")
    
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Mot de passe"]').click()
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Mot de passe"]').send_keys("password")
    
    driver.find_element(By.XPATH, "/html/body/doctype/section[1]/div/div/div[2]/div/div/form/div/div[3]/button").click()
    print('logged')
    
    wait.until(EC.url_to_be("https://ent.ensa-tetouan.ac.ma/?home/home"))
    
    driver.find_element(By.XPATH, "/html/body/doctype/section/div/div/div[2]/div/h5/a").click()
    
    wait.until(EC.url_to_be("https://ent.ensa-tetouan.ac.ma/?myscore/index"))
    # time.sleep(30)
    table_element = wait.until(EC.presence_of_element_located((By.XPATH, '//html/body/doctype/section/div/div[2]/div[1]/div/table')))
    te = table_element.get_attribute("innerText")
    
    try:
        with open("notes.txt", "r") as file:
            file_contents = file.read()
    except:
        file_contents = ""
    
    if file_contents == te:
        print('pas de nouvelles ...')
        mfg = ''
    elif file_contents != te:
        result = te.split('\t')
        matter = result[-3]
        print('\a')
        if matter != "":
            a=False
            modules=affiche['Module affiches']
            for module in modules :
                if matter==module:
                    bot.send_message('chat id', matter)
                    a=True
                    break
            if a==False:
                mfg= f"{matter} est affiche!".replace('é','e')
                new_list=modules+[f'{matter}']
                newvalues ={ "$set": { "Module affiches": new_list } }
                collection.update_one(affiche, newvalues)
            else :
                mfg=''
        else:
            mfg=''
        
        print(mfg)
            # sendwhat(message)
            # with open("notes.txt", "w") as file:
            #   file.write(te)
    
        # ---------------------
        driver.quit()
        return mfg
print('success')
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print(message.text)
    bot.reply_to(message, "Howdy, how are you doing?")

#def greet_user(messages):
    #for message in messages:
        #for new_member in message.new_chat_members:
            #bot.send_message(message.chat.id, f'Welcome {new_member.first_name} to the group!')



#bot.set_update_listener(greet_user)

def check():
    while True :
        print('running...')
        try:
            msg=run()
            bot.send_message(CHAT_ID, msg)
        except Exception as e :
            print(e)
            bot.send_message('Chat id', e)
            pass
		
        time.sleep(50)
scraping_thread = threading.Thread(target=check)
scraping_thread.daemon = True
scraping_thread.start()


if __name__ == '__main__':

	bot.infinity_polling()
