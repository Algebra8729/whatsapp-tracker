#!/bin/bash

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}--- WhatsApp Privacy Auditor : Initialisation ---${NC}"

pip install -r requirements.txt

echo -e "${GREEN}[+] Serveur démarré sur http://localhost:5000${NC}"
python3 app.py