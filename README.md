# 🕵️‍♂️ WhatsApp-Forensics-PoC

> **Note :** Ce projet a été développé à des fins éducatives.

## 🧪 Le Concept
Contrairement aux outils classiques, ce script utilise des **Shadow Selectors** et des techniques de **Bypass de détection Webdriver** pour observer les fuites de métadonnées sans alerter les systèmes de sécurité de la plateforme.

## 🛠️ Stack Technique
- **Engine** : Python 3.x / Selenium
- **Furtivité** : Spoofing du User-Agent et désactivation des flags d'automatisation.
- **Data** : Export JSON structuré pour analyse comportementale ultérieure.

## 📖 Utilisation
1. `pip install -r requirements.txt`
2. Lancez `python auditor.py`
3. Scannez le QR Code (votre session est sauvegardée localement dans `/vault_session`).

## 🛡️ Défense
Pour vous protéger contre ce type d'audit, désactivez les options "Vu à" et "En ligne" dans vos paramètres de confidentialité.
