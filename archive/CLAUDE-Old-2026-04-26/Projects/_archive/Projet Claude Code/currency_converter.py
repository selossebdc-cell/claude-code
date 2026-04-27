#!/usr/bin/env python3
"""
Application de conversion de devises
Permet de convertir un montant d'une devise à une autre
"""

from typing import Optional
import requests


def get_exchange_rates(base_currency: str) -> Optional[dict]:
    """Récupère les taux de change depuis l'API exchangerate-api.com"""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des taux: {e}")
        return None


def convert_currency(amount: float, from_currency: str, to_currency: str) -> Optional[float]:
    """Convertit un montant d'une devise à une autre"""
    data = get_exchange_rates(from_currency.upper())
    if data is None:
        return None

    rates = data.get("rates", {})
    to_currency = to_currency.upper()

    if to_currency not in rates:
        print(f"Devise '{to_currency}' non trouvée")
        return None

    return amount * rates[to_currency]


def display_available_currencies():
    """Affiche les devises les plus courantes"""
    currencies = {
        "EUR": "Euro",
        "USD": "Dollar américain",
        "GBP": "Livre sterling",
        "JPY": "Yen japonais",
        "CHF": "Franc suisse",
        "CAD": "Dollar canadien",
        "AUD": "Dollar australien",
        "CNY": "Yuan chinois",
        "INR": "Roupie indienne",
        "BRL": "Real brésilien",
        "MXN": "Peso mexicain",
        "KRW": "Won sud-coréen",
    }
    print("\nDevises disponibles:")
    print("-" * 30)
    for code, name in currencies.items():
        print(f"  {code} - {name}")
    print("-" * 30)


def main():
    """Fonction principale de l'application"""
    print("=" * 40)
    print("   Convertisseur de Devises")
    print("=" * 40)

    while True:
        print("\nOptions:")
        print("  1. Convertir une devise")
        print("  2. Voir les devises disponibles")
        print("  3. Quitter")

        choice = input("\nVotre choix (1-3): ").strip()

        if choice == "1":
            try:
                amount = float(input("\nMontant à convertir: "))
            except ValueError:
                print("Erreur: Veuillez entrer un nombre valide")
                continue

            from_currency = input("Devise de départ (ex: EUR): ").strip().upper()
            to_currency = input("Devise d'arrivée (ex: USD): ").strip().upper()

            if not from_currency or not to_currency:
                print("Erreur: Veuillez entrer les deux devises")
                continue

            print(f"\nConversion en cours...")
            result = convert_currency(amount, from_currency, to_currency)

            if result is not None:
                print(f"\n  {amount:.2f} {from_currency} = {result:.2f} {to_currency}")

        elif choice == "2":
            display_available_currencies()

        elif choice == "3":
            print("\nAu revoir!")
            break

        else:
            print("Choix invalide, veuillez réessayer")


if __name__ == "__main__":
    main()
