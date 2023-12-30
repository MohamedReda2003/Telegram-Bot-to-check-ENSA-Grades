import subprocess

subprocess.check_call([ "pip", "install", "pymongo"])
subprocess.check_call([ "pip", "install", "playwright"])
subprocess.check_call([ "pip", "install", "pyTelegramBotAPI"])



import telebot
from playwright.sync_api import Playwright, sync_playwright, expect
from pymongo import MongoClient
import time
import threading
import sys

subprocess.check_call([ "playwright", "install", "chromium"])
subprocess.check_call([ "playwright", "install-deps"]) 



  
TOKEN = 'Bot Token from BotFather'
CHAT_ID1 = 'the chat id'
CHAT_ID2 = 'another chat id'
bot = telebot.TeleBot(TOKEN)


#cluster=MongoClient("")
#db =cluster["ENSA2023"]
#collection=db["modules-ENSA2023"]
#bad_collection=db['bab_language']
#affiche=collection.find_one()
error_flag = False


def run(collection, affiche):
    with sync_playwright() as playwright:

   
        browser = playwright.chromium.launch()
        context = browser.new_context()
        # Open new page
        page = context.new_page()
    
        page.goto("https://ent.ensa-tetouan.ac.ma/?home/index", wait_until="load")
        page.wait_for_load_state("networkidle")
        page.is_visible('//html/body/doctype/section[1]/div/div/div[2]/div/div/h2')



    
        page.locator("[placeholder=\"Email\"]").click()
        page.locator("[placeholder=\"Email\"]").fill("your institutional email")

        page.locator("[placeholder=\"Mot de passe\"]").click()

        page.locator("[placeholder=\"Mot de passe\"]").fill("your password")
      
        page.locator("text=S'authentifier").click()
    
    

        page.wait_for_url("https://ent.ensa-tetouan.ac.ma/?home/home")
        page.locator("text=Mon résultat Consultation de vos notes. >> img").click()
        page.wait_for_url("https://ent.ensa-tetouan.ac.ma/?myscore/index")
        page.is_visible("//html/body/doctype/section/div/div[2]/div[1]/div/table/thead/tr/th[1]")
        te = page.wait_for_selector('//html/body/doctype/section/div/div[2]/div[1]/div/table', timeout=10000).inner_text()
            
        result = te.split('\t')
        matter=result[-3]
        print('\a')
        if matter != "":
            a=False
            modules=affiche['Module affiches']
            for module in modules :
                if matter==module or matter==module.replace('é','e'):
                    #bot.send_message('1798052577', matter)
                    a=True
                    break
            if a==False:
                mfg= f"{matter} est affiche!"
                new_list=modules+[f'{matter}']
                newvalues ={ "$set": { "Module affiches": new_list } }
                collection.update_one(affiche, newvalues)
            else :
                mfg=''
        else:
            mfg=''
    
        context.close()
        browser.close()
        return mfg



print('success')
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


def check():
    global error_flag
    counter=0
    while not error_flag:
        #bot.send_message('telegram id', str(error_flag))
        try:
            with MongoClient("Token from MongoDB") as cluster:
                db = cluster["ENSA2023"]
                collection = db["modules-ENSA2023-RATT"]
                bad_collection = db['bab_language']
                try:
                    affiche = collection.find_one()
                except :
                    affiche={}

                msg = run(collection, affiche)
                if msg != '':
                    try:
                        bot.send_message(CHAT_ID1, msg)
                    except :
                        bot.send_message(CHAT_ID2, msg)
                        

            time.sleep(10)
        except TypeError :
            pass
        except Exception as e :
            error_flag=True 
            bot.send_message('chat id', e)
            bot.send_message('chat id', str(counter))

        if counter%10==0:
            bot.send_message('chat id', str(counter))
            
            
        counter+=1
    
    
		
    
        
def the_main():
    global error_flag
    scraping_thread = threading.Thread(target=bot.infinity_polling)
    scraping_thread.daemon = True
    scraping_thread.start()

             




if __name__ == '__main__':
    the_main()
    # bot.infinity_polling()
    check()
