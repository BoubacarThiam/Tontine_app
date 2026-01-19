#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module contenant les fonctions utilitaires
"""

import os
import re
import sys
from typing import List


def effacer_ecran() -> None:
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher_titre(titre: str) -> None:
    """
    Affiche un titre formaté
    
    Args:
        titre: Le texte du titre à afficher
    """
    largeur = 80
    print("\n" + "="*largeur)
    print(titre.center(largeur))
    print("="*largeur + "\n")


def afficher_menu(options: List[str]) -> None:
    """
    Affiche un menu numéroté
    
    Args:
        options: Liste des options du menu
    """
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()


def valider_choix(min_val: int, max_val: int) -> int:
    """
    Valide et retourne un choix numérique de l'utilisateur
    
    Args:
        min_val: Valeur minimale acceptée
        max_val: Valeur maximale acceptée
    
    Returns:
        Le choix validé de l'utilisateur
    """
    while True:
        try:
            choix = int(input(f"Votre choix ({min_val}-{max_val}): ").strip())
            if min_val <= choix <= max_val:
                return choix
            print(f"❌ Veuillez entrer un nombre entre {min_val} et {max_val}.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            print("\n\nOpération annulée.")
            sys.exit(0)


def pause() -> None:
    """Attend que l'utilisateur appuie sur Entrée"""
    input("\nAppuyez sur Entrée pour continuer...")


def valider_email(email: str) -> bool:
    """
    Valide le format d'une adresse email
    
    Args:
        email: L'adresse email à valider
    
    Returns:
        True si l'email est valide, False sinon
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def valider_telephone(telephone: str) -> bool:
    """
    Valide le format d'un numéro de téléphone
    
    Args:
        telephone: Le numéro de téléphone à valider
    
    Returns:
        True si le téléphone est valide, False sinon
    """
    # Accepte les formats: +221771234567, 771234567, 77-123-45-67, etc.
    telephone_clean = re.sub(r'[\s\-\(\)]', '', telephone)
    
    # Vérifier que c'est bien des chiffres (avec un + optionnel au début)
    if not re.match(r'^\+?\d{8,15}$', telephone_clean):
        return False
    
    return True


def formater_montant(montant: float, devise: str = "FCFA") -> str:
    """
    Formate un montant avec séparateurs de milliers
    
    Args:
        montant: Le montant à formater
        devise: La devise à afficher
    
    Returns:
        Le montant formaté
    """
    return f"{montant:,.2f} {devise}".replace(',', ' ')


def confirmer_action(message: str = "Êtes-vous sûr?") -> bool:
    """
    Demande une confirmation à l'utilisateur
    
    Args:
        message: Le message de confirmation
    
    Returns:
        True si l'utilisateur confirme, False sinon
    """
    reponse = input(f"{message} (oui/non): ").strip().lower()
    return reponse in ['oui', 'o', 'yes', 'y']


def afficher_ligne_separation(caractere: str = "-", longueur: int = 80) -> None:
    """
    Affiche une ligne de séparation
    
    Args:
        caractere: Le caractère à utiliser pour la ligne
        longueur: La longueur de la ligne
    """
    print(caractere * longueur)


def centrer_texte(texte: str, largeur: int = 80) -> str:
    """
    Centre un texte dans une largeur donnée
    
    Args:
        texte: Le texte à centrer
        largeur: La largeur totale
    
    Returns:
        Le texte centré
    """
    return texte.center(largeur)


def afficher_message_succes(message: str) -> None:
    """
    Affiche un message de succès formaté
    
    Args:
        message: Le message à afficher
    """
    print(f"\n✅ {message}\n")


def afficher_message_erreur(message: str) -> None:
    """
    Affiche un message d'erreur formaté
    
    Args:
        message: Le message à afficher
    """
    print(f"\n❌ {message}\n")


def afficher_message_attention(message: str) -> None:
    """
    Affiche un message d'avertissement formaté
    
    Args:
        message: Le message à afficher
    """
    print(f"\n⚠️  {message}\n")


def formater_date(date_str: str, format_entree: str = "%Y-%m-%d", 
                  format_sortie: str = "%d/%m/%Y") -> str:
    """
    Reformate une date
    
    Args:
        date_str: La date sous forme de chaîne
        format_entree: Le format d'entrée de la date
        format_sortie: Le format de sortie souhaité
    
    Returns:
        La date reformatée
    """
    from datetime import datetime
    
    try:
        date_obj = datetime.strptime(date_str, format_entree)
        return date_obj.strftime(format_sortie)
    except ValueError:
        return date_str


def creer_repertoire_si_inexistant(chemin: str) -> None:
    """
    Crée un répertoire s'il n'existe pas
    
    Args:
        chemin: Le chemin du répertoire à créer
    """
    if not os.path.exists(chemin):
        os.makedirs(chemin)
        print(f"📁 Répertoire créé: {chemin}")


def afficher_tableau(headers: List[str], data: List[List[str]], 
                     largeurs: List[int] = None) -> None:
    """
    Affiche un tableau formaté
    
    Args:
        headers: Liste des en-têtes de colonnes
        data: Liste de listes contenant les données
        largeurs: Liste des largeurs de colonnes (optionnel)
    """
    if not largeurs:
        largeurs = [max(len(str(row[i])) for row in [headers] + data) + 2 
                   for i in range(len(headers))]
    
    # Ligne de séparation
    ligne_sep = "+" + "+".join("-" * l for l in largeurs) + "+"
    
    # En-têtes
    print(ligne_sep)
    header_row = "|" + "|".join(
        str(headers[i]).center(largeurs[i]) for i in range(len(headers))
    ) + "|"
    print(header_row)
    print(ligne_sep)
    
    # Données
    for row in data:
        data_row = "|" + "|".join(
            str(row[i]).ljust(largeurs[i]) if i < len(row) else " " * largeurs[i]
            for i in range(len(headers))
        ) + "|"
        print(data_row)
    
    print(ligne_sep)


def saisir_nombre(prompt: str, min_val: float = None, 
                  max_val: float = None, type_nombre: type = float) -> float:
    """
    Saisit et valide un nombre
    
    Args:
        prompt: Le message à afficher
        min_val: Valeur minimale (optionnel)
        max_val: Valeur maximale (optionnel)
        type_nombre: Type de nombre (int ou float)
    
    Returns:
        Le nombre saisi et validé
    """
    while True:
        try:
            valeur = type_nombre(input(prompt).strip())
            
            if min_val is not None and valeur < min_val:
                print(f"❌ La valeur doit être supérieure ou égale à {min_val}.")
                continue
            
            if max_val is not None and valeur > max_val:
                print(f"❌ La valeur doit être inférieure ou égale à {max_val}.")
                continue
            
            return valeur
        except ValueError:
            type_nom = "entier" if type_nombre == int else "décimal"
            print(f"❌ Veuillez entrer un nombre {type_nom} valide.")
        except KeyboardInterrupt:
            print("\n\nOpération annulée.")
            sys.exit(0)