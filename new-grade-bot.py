# import telebot
from playwright.sync_api import Playwright, sync_playwright, expect
from pymongo import MongoClient
import time
import threading
import sys
import requests
import urllib.parse
import traceback



# TOKEN = 'TElEGRAM TOKEN FROM BOTFATHER'
wts_number="YOUR WHATSAPP NUMBER including the country code (MOROCCO FOR EXAMPLE: 212*********)"
whatsapp_api_key="YOU CAN GET IT FOLLOWING THE SETUP STEPS ON https://malikaltawati.medium.com/free-api-to-send-whatsapp-messages-tutorial-7d63f07cd070 "
# bot = telebot.TeleBot(TOKEN)



error_flag = False


def run(collection, affiche):
    with sync_playwright() as playwright:   
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://ent.ensa-tetouan.ac.ma/?home/index", wait_until="load")
        page.wait_for_load_state("networkidle")
        page.is_visible('//html/body/doctype/section[1]/div/div/div[2]/div/div/h2')

        page.locator("[placeholder=\"Email\"]").click()
        page.locator("[placeholder=\"Email\"]").fill("YOUR INSTITUTIONAL EMAIL")

        page.locator("[placeholder=\"Mot de passe\"]").click()

        page.locator("[placeholder=\"Mot de passe\"]").fill("PASSWORD")
      
        page.locator("text=S'authentifier").click()
    

        page.goto("https://ent.ensa-tetouan.ac.ma/?myscore/index")
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


def check():
    global error_flag
    counter=0
    while not error_flag:
        #bot.send_message('1798052577', str(error_flag))
        try:
            with MongoClient("YOU CAN GET IT FROM MONGODB") as cluster:
                db = cluster["ENSA2024"]
                collection = db["modules-ENSA2024"]
                # bad_collection = db['affichage']
                try:
                    affiche = collection.find_one()
                except :
                    affiche={}

                msg = run(collection, affiche)
                if msg != '':
                    url_msg=urllib.parse.quote(msg)
                    requests.get(f"https://api.callmebot.com/whatsapp.php?phone={wts_number}&text={url_msg}t&apikey={whatsapp_api_key}")

            time.sleep(10)
        except TypeError :
            pass
        except Exception as e :
            error_flag=True 
            print(traceback.format_exc())
            
        if counter%10==0:
            # requests.get(f"https://api.callmebot.com/whatsapp.php?phone=212655979800&text={counter}&apikey=9508650")
            pass
            
        counter+=1
    
    
		
    
        
# def the_main():
#     global error_flag
#     # scraping_thread = threading.Thread(target=bot.infinity_polling)
#     scraping_thread.daemon = True
#     scraping_thread.start()

             




if __name__ == '__main__':
    # the_main()
    # bot.infinity_polling()
    check()
