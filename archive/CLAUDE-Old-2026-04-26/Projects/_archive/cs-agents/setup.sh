#!/bin/bash
# Setup CS Agents — a lancer une seule fois

set -e

echo "=== CS Agents Setup ==="
echo ""

# 1. Verifier Python
echo "[1/4] Verification Python..."
python3 --version

# 2. Installer les dependances
echo "[2/4] Installation des dependances..."
pip3 install -r requirements.txt

# 3. Verifier la cle API
echo "[3/4] Verification de la cle API..."
if grep -q "REMPLACER" .env 2>/dev/null; then
    echo ""
    echo "⚠  IMPORTANT : Tu dois ajouter ta cle API Anthropic dans .env"
    echo "   1. Va sur https://console.anthropic.com/settings/keys"
    echo "   2. Cree une nouvelle cle"
    echo "   3. Edite .env et remplace la valeur de ANTHROPIC_API_KEY"
    echo ""
else
    echo "   Cle API configuree."
fi

# 4. Creer les dossiers de logs
echo "[4/4] Creation des dossiers de logs..."
mkdir -p logs/conversations logs/runs logs/briefings

echo ""
echo "=== Setup termine ==="
echo ""
echo "Usage :"
echo "  python3 cli.py dg \"Bonjour, briefing du matin\""
echo "  python3 cli.py daf \"Ou en sont les paiements?\""
echo "  python3 cli.py dg   (mode interactif)"
echo ""
echo "Cron (optionnel) — ajouter avec 'crontab -e' :"
echo "  30 7 * * 1-5 cd $(pwd) && python3 routines/morning_briefing.py >> logs/runs/cron.log 2>&1"
echo "  0 9 * * 5 cd $(pwd) && python3 routines/weekly_invoice_check.py >> logs/runs/cron.log 2>&1"
