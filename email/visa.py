import time
import logging
import tempfile
import sys
import ssl
import smtplib

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import config
import appointments

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

log_path = directory + 'visa.log'
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=log_path,level=logging.INFO)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1024,768')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        for address in mail_repicients:
            server.sendmail(sender_email, address, message)

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

def crawl_website_for_slot(url, filename, prefecture, visa_name, desk_ids):
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
            current_time = datetime.now().strftime("%H:%M:%S")
            message = "{} - {} : Creneau(x) detecte(s) pour {} : {}".format(current_time, prefecture, visa_name, url)
            last_result = file.read()
            if '1' in last_result:
                logging.info('{}: SLOT ALREADY AVAILABLE: SKIPPING EMAIL'.format(prefecture))
            else:
                logging.info('{}: NEW AVAILABLE SLOT: SENDING EMAIL!'.format(prefecture))

                send_email("""\
                VISA

                {}
                """.format(message))
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

for appointment in appointments:
    crawl_website_for_slot(appointment.url, appointment.unique_name, appointment.prefecture_name, appointment.appointment_name, appointment.desk_ids)

driver.quit()
logging.info('END: {}'.format(datetime.now() - start_time))

