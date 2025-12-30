import os
import time
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class WhatsAppPrivacyAuditor:
    def __init__(self):
        self.session_dir = os.path.join(os.getcwd(), "vault_session")
        self.results_file = "audit_report.json"
        self.driver = self._init_engine()
        self.active_audit = None

    def _init_engine(self):
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

        options = Options()
        options.add_argument(f"--user-data-dir={self.session_dir}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        # Masquage de l'automatisation
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Script pour bypasser la détection de Selenium
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def target_acquisition(self, contact_name):
        print(f"[*] Acquisition de la cible : {contact_name}")
        self.driver.get("https://web.whatsapp.com/")
        
        # Attente de l'interface
        wait = WebDriverWait(self.driver, 60)
        search_xpath = "//div[@contenteditable='true']"
        wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
        
        # Recherche précise
        search_box = self.driver.find_element(By.XPATH, search_xpath)
        search_box.click()
        search_box.send_keys(contact_name)
        
        time.sleep(2)
        contact_selector = f"//span[@title='{contact_name}']"
        self.driver.find_element(By.XPATH, contact_selector).click()
        
        self.active_audit = contact_name
        print(f"[+] Focus établi sur {contact_name}. Monitoring démarré.")

    def run_recon(self):
        last_state = None
        try:
            while True:
                # Analyse des indicateurs de statut (Online / Typing)
                # Utilise des sélecteurs CSS complexes pour éviter les changements de classe
                selectors = ["span[title='online']", "span[title='en ligne']", "span[title='typing...']"]
                
                is_active = False
                for s in selectors:
                    if self.driver.find_elements(By.CSS_SELECTOR, s):
                        is_active = True
                        break
                
                current_state = "ACTIVE" if is_active else "IDLE"
                
                if current_state != last_state:
                    self._log_event(current_state)
                    last_state = current_state
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Statut : {current_state}")
                
                # Anti-timeout : simule un scroll invisible
                self.driver.execute_script("document.querySelector('#pane-side').scrollTop += 1")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.driver.quit()

    def _log_event(self, state):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "target": self.active_audit,
            "event": state
        }
        with open(self.results_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    auditor = WhatsAppPrivacyAuditor()
    target = input("Entrez le nom exact du contact : ")
    auditor.target_acquisition(target)
    auditor.run_recon()