import smtplib

from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import time


def convert_age_to_hours(abracadabra):

    if abracadabra == None:
        return 999

    abracadabra = abracadabra.replace(' ago', '')
    listita = abracadabra.split(' ')
    listita.reverse()

    total_hours = 0

    #key_words = ['sec', 'secs', 'min', 'mins', 'hr', 'hrs', 'day', 'days']
    for i in range(0, len(listita)-1, 2):
        value = int(listita[i+1])
        #print(listita[i])
        if listita[i] in 'secs':
            total_hours += value/3600
        elif listita[i] in 'mins':
            total_hours += value/60
        elif listita[i] in 'hrs':
            total_hours += value
        elif listita[i] in 'days':
            total_hours += value*24

    #print(total_hours)
    return total_hours


class WalletChecker:

    BSCSCAN = 'https://bscscan.com/address/{}'
    ETHERSCAN = 'https://etherscan.io/address/{}'
    POLYGONSCAN = 'https://polygonscan.com/address/{}'
    FTMSCAN = 'https://ftmscan.com/address/{}'
    AVAXSCAN = 'https://avascan.info/blockchain/c/address/{}'

    chain_age_xpath = '//*[@id="transactions"]/div[2]/table/tbody/tr[1]/td[6]/span'
    ftm_age_xpath = '/html/body/div[1]/main/div[4]/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[5]/span'

    def __init__(self, wallet, run_in_background):

        self.found_something = False
        self.limit_hours = 10
        self.wallet_address = wallet

        self.driver = self.load_chrome_webdriver(run_in_background)

        self.check_bsc()
        self.check_ethereum()
        self.check_polygon()
        self.check_ftm()

        #self.check_avax()
        #self.check_solana()

        #if self.found_something:
        #    self.send_email('albduranlopez@gmail.com', "BlueDemise Wallet Movement", "Check Telegram")
        #    self.send_email('carloooox77@gmail.com', "BlueDemise Wallet Movement", "Check Telegram")
        self.driver.close()

    def load_chrome_webdriver(self, run_in_background):
        chrome_options = webdriver.ChromeOptions()
        if run_in_background:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
            chrome_options.add_argument('user-agent={0}'.format(user_agent))
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(options=chrome_options)
        return browser


    def notify(self, chain):
        image_name = 'found.png'
        os.system('./Escritorio/WalletChecker/senderbot/src/senderbot -m "Found wallet movement in ' + chain + '"')
        self.driver.save_screenshot(image_name)
        os.system('./Escritorio/WalletChecker/senderbot/src/senderbot -i ' + image_name)
        os.system('./Escritorio/WalletChecker/senderbot/src/senderbot -m "Check URL: ' + self.current_url + '"')


    def check_blockchain(self, url, chain, xpath):
        self.driver.get(url)
        self.current_url = url
        time.sleep(2)

        try:
            age = self.driver.find_element(By.XPATH, xpath).text
            #print(age)
        except:
            age = None
        hours = convert_age_to_hours(age)

        if hours < self.limit_hours:
            self.driver.execute_script("window.scrollTo(0, 250);")
            self.notify(chain)

    def check_bsc(self):
        url = self.BSCSCAN.format(self.wallet_address)
        chain = 'Binance Smart Chain'
        self.check_blockchain(url, chain, self.chain_age_xpath)

    def check_ethereum(self):
        url = self.ETHERSCAN.format(self.wallet_address)
        chain = 'Ethereum Network'
        #print("entra")
        self.check_blockchain(url, chain, self.chain_age_xpath)


    def check_polygon(self):
        url = self.POLYGONSCAN.format(self.wallet_address)
        chain = 'Polygon/Matic Network'
        self.check_blockchain(url, chain, self.chain_age_xpath)


    def check_ftm(self):
        url = self.FTMSCAN.format(self.wallet_address)
        chain = 'The Fantom Network'
        self.check_blockchain(url, chain, self.ftm_age_xpath)

    """
    def check_avax(self):
        self.notify("AVAX")
        self.found_something = True


    def check_solana(self):
        self.notify("Solana")
        self.found_something = True
    """


    def send_email(self, receiver, subject, body):
    	username = 'albertotesting1234a@gmail.com'
    	password = 'másquisierassaberesto'

    	session = smtplib.SMTP('smtp.gmail.com', 587)
    	#Initiate connection to the server
    	session.ehlo()
    	#Start encrypting everything you're sending to the server
    	session.starttls()
    	#Log into the server by sending them our username and password
    	session.login(username, password)
    	#Enter the headers of the email
    	headers = "\r\n".join(["from: " + username,
    	                       "subject: "+subject,
    	                       "to: " + receiver,
    	                       "mime-version: 1.0",
    	                       "content-type: text/html"])
    	#Enter the text of the body of the email
    	#Tie the headers and body together into the email's content
    	content = headers + "\r\n\r\n" + body
    	#Send the email!
    	session.sendmail(username, receiver, content)
    	#Close the connection to the SMTP server
    	session.quit()



if __name__ == '__main__':
    wallet_1 = '0x68ef343d589c2a58028af917fdb9361d11adc951'
    wallet_2 = '0x44f64ed22b3eee41ccdc8df4697d3da3632ee454'

    duro1 = WalletChecker(wallet=wallet_1, run_in_background=True)
    duro2 = WalletChecker(wallet=wallet_2, run_in_background=True)
