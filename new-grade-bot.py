"""
BEFORE you run the code, create an account on mongodb, create a database, in the case of this code, name it "ENSA2024" and name the collection "modules-ENSA2024"
"""
from playwright.sync_api import Playwright, sync_playwright, expect
from pymongo import MongoClient
import time
import sys
import requests
import urllib.parse
import traceback
from parsel import Selector


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
        page.wait_for_selector("#dentoNav > a.nav-brand > img")
       
        
        html=page.content()
        response=Selector(text=html)
        for row in response.css("table > tbody"):
            matter=row.css("td:nth-child(2)::text").get()
            # print(matter)

        if matter != "":
            print(matter)
            a=False
            modules=affiche['Module affiches']
            # if len(modules)>0:
            for module in modules :
                if matter==module or matter==module.replace('é','e'):
                    #bot.send_message('YOUR TELEGRAM CHAT ID', matter)
                    a=True
                    break
            if a==False:
                mfg= f"{matter} est affiche!"
                new_list=modules+[f'{matter}']
                print(new_list)
                newvalues ={ "$set": { "Module affiches": new_list } }
                try:
                    if len(new_list)>1:
                        collection.update_one(affiche, newvalues)
                        print('done updating')
                    elif len(new_list)==1:
                        collection.insert_one( { "Module affiches": new_list } )
                        print('done inserting')
                except Exception as e :
                    print(e)
                    print('error occured on line 95')
            else :
                mfg=''
        else:
            mfg=''
    
        context.close()
        browser.close()
        # print(mfg)
        return mfg


def check():
    global error_flag
    counter=0
    while not error_flag:
        #bot.send_message('YOUR TELEGRAM CHAT ID', str(error_flag))
        try:
            with MongoClient("YOU CAN GET IT FROM MONGODB") as cluster:
                db = cluster["ENSA2024"]
                collection = db["modules-ENSA2024"]
                # bad_collection = db['affichage']
                try:
                    affiche = collection.find_one()
                    if affiche==None:
                        affiche={'Module affiches':[]}
                except Exception as e:
                    print('line 120')
                    # print(e)
                    affiche={'Module affiches':[]}
                # print(len(affiche['Module affiches']))
                try:
                    msg = run(collection, affiche)
                except Exception as e:
                    print(traceback.format_exc())
                if msg != '':
                    # try:
                    #     bot.send_message(CHAT_ID1, msg)
                    # except :
                    #     bot.send_message(CHAT_ID2, msg)
                    url_msg=urllib.parse.quote(msg)
                    requests.get(f"https://api.callmebot.com/whatsapp.php?phone={wts_number}&text={url_msg}t&apikey={whatsapp_api_key}")

            time.sleep(10)
        except TypeError :
            pass
        except Exception as e :
            #error_flag=True 
		#I commented the previous line so that the program does not stop when encountering an error, instead, it just restart automatically.
            print(traceback.format_exc())
            
        if counter%50==0:
		#you can uncomment the following line so that you will be sure the bot is still working.
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
