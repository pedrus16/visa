import time
import logging
import tempfile
import sys

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from twython import Twython

twitter_nanterre = {
    'api_key': '',
    'api_key_secret': '',
    'access_token': '',
    'access_token_secret': ''
}

directory = '/path/to/temporary/directory/'

log_path = directory + 'visa.log'
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=log_path,level=logging.INFO)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1024,768')

# driver = webdriver.Remote('http://127.0.0.1:9515', options=chrome_options)

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

def check_for_error_in_page():
    assert '502 Bad Gateway' not in driver.page_source, '502 Bad Gateway'
    assert '503 Service Unavailable' not in driver.page_source, '503 Service Unavailable'
    assert '504 Gateway Timeout' not in driver.page_source, '504 Gateway Timeout'

    return True

def slot_available(url, desk_id=None, delay_second=10):
    driver.get(url)
    driver.delete_all_cookies()
    time.sleep(delay_second)

    check_for_error_in_page()

    # Step #1
    condition_checkbox = driver.find_element_by_id('condition')
    submit_button = driver.find_element_by_name('nextButton')
    condition_checkbox.send_keys(Keys.SPACE)
    submit_button.send_keys(Keys.SPACE)
    time.sleep(delay_second)

    check_for_error_in_page()

    if desk_id and 'Veuillez recommencer' in driver.page_source:
        return False

    # Step 2
    if desk_id:
        radio_button_list = driver.find_element_by_id(desk_id)
        submit_button = driver.find_element_by_name('nextButton')
        radio_button_list.send_keys(Keys.SPACE)
        submit_button.send_keys(Keys.SPACE)
        time.sleep(delay_second)

    check_for_error_in_page()
    
    # Result Page
    try:
        next_button = driver.find_element_by_name('nextButton')
        
        return True
    except:
        pass
    
    return False

def crawl_website_for_slot(url, filename, prefecture, visa_name, desk_ids, twitter_keys):
    try:
        file = open(filename, 'r+')
    except OSError:
        file = open(filename, 'w+')

    try:
        found = False
        if desk_ids:
            for desk_id in desk_ids:
                found = found or slot_available(url, desk_id)
                if found:
                    break
                time.sleep(15)
        else:
            found = slot_available(url)
        
        if found:
            logging.info('{}: SLOT AVAILABLE'.format(prefecture))
            twitter = Twython(twitter_keys['api_key'], twitter_keys['api_key_secret'], twitter_keys['access_token'], twitter_keys['access_token_secret'])
            current_time = datetime.now().strftime("%H:%M:%S")
            message = "{} - {} : Créneau(x) détecté(s) pour {} : {}".format(current_time, prefecture, visa_name, url)
            last_result = file.read()
            if '1' in last_result:
                logging.info('{}: SLOT ALREADY AVAILABLE: SKIPPING TWEET'.format(prefecture))
            else:
                logging.info('{}: NEW AVAILABLE SLOT: TWEETING!'.format(prefecture))

                # print(message)
                driver.save_screenshot(directory + 'screenshot.png')
                screenshot = open(directory + 'screenshot.png', 'rb')
                response = twitter.upload_media(media=screenshot)
                twitter.update_status(status=message, media_ids=[response['media_id']])
            file.seek(0)
            file.write('1')
            file.truncate()
        else:
            logging.info('{}: NO SLOT AVAILABLE'.format(prefecture))
            file.seek(0)
            file.write('0')
            file.truncate()

    except AssertionError as err:
        logging.error('{}: SITE KO ({})'.format(prefecture, err))
    except:
        logging.error('{}: UNEXPECTED ERROR: {}'.format(prefecture, sys.exc_info()))
    finally:
        file.close()

logging.info('START')
start_time = datetime.now()

# NANTERRE - renouvellement "vie privee et familiale"
crawl_website_for_slot('http://www.hauts-de-seine.gouv.fr/booking/create/12069/0', directory + 'nanterre_last.txt', 'NANTERRE', 'renouvellement de titre de séjour \"vie privée et familiale\"', ['planning12078', 'planning13642'], twitter_nanterre)

# NANTERRE - renouvellement "etudiant", "jeune au pair" ou "stagiaire"
crawl_website_for_slot('http://www.hauts-de-seine.gouv.fr/booking/create/4129/0', directory + 'nanterre_etudiant_last.txt', 'NANTERRE', 'renouvellement de titre de séjour \"étudiant\", "jeune au pair", "stagiaire"', None, twitter_nanterre)

# NANTERRE - remise de titre de sejour
crawl_website_for_slot('http://www.hauts-de-seine.gouv.fr/booking/create/12083/0', directory + 'nanterre_remise_last.txt', 'NANTERRE', 'remise de titre de séjour', ['planning14673', 'planning14806', 'planning14932'], twitter_nanterre)

# NANTERRE - biometrie
crawl_website_for_slot('http://www.hauts-de-seine.gouv.fr/booking/create/11681/0', directory + 'nanterre_biometrie_last.txt', 'NANTERRE', 'biometrie - prise des empreintes digitales', None, twitter_nanterre)

# SARCELLES - renouvellement "vie privee et familiale"
crawl_website_for_slot('http://www.val-doise.gouv.fr/booking/create/11404', directory + 'sarcelles_last.txt', 'SARCELLES', 'renouvellement de titre de séjour \"vie privée et familiale\"', None, twitter_nanterre)

# BOULOGNE - renouvellement titre de sejour
crawl_website_for_slot('http://www.hauts-de-seine.gouv.fr/booking/create/12249/0', directory + 'boulogne_last.txt', 'BOULOGNE', 'renouvellement de titre de séjour', ['planning15538', 'planning15537', 'planning12250'], twitter_nanterre)

# # NANTERRE - renouvellement "creation d'entreprise recherche emploi"
# crawl_website_for_slot('http://www.hauts-de-seine.gouv.fr/booking/create/11658', directory + 'test_last.txt', 'TEST', 'ceci est un test', None, twitter_nanterre)

# # TEST
# crawl_website_for_slot('https://www.hauts-de-seine.gouv.fr/booking/create/8485/0', directory + 'test_last.txt', 'TEST', twitter_nanterre)

driver.quit()

logging.info('END: {}'.format(datetime.now() - start_time))

