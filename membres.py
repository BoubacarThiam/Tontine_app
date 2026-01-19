#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des membres de la tontine
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from utils import afficher_titre, valider_email, valider_telephone


class Membre:
    """Représente un membre de la tontine"""
    
    def __init__(self, id_membre: str, nom: str, prenom: str, 
                 email: str, telephone: str, actif: bool = True):
        """
        Initialise un membre
        
        Args:
            id_membre: Identifiant unique du membre
            nom: Nom de famille
            prenom: Prénom
            email: Adresse email
            telephone: Numéro de téléphone
            actif: Statut du membre (actif/inactif)
        """
        self.id_membre = id_membre
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.actif = actif
        self.date_inscription = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convertit le membre en dictionnaire"""
        return {
            "id_membre": self.id_membre,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "telephone": self.telephone,
            "actif": self.actif,
            "date_inscription": self.date_inscription
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Membre':
        """Crée un membre à partir d'un dictionnaire"""
        membre = cls(
            data["id_membre"],
            data["nom"],
            data["prenom"],
            data["email"],
            data["telephone"],
            data["actif"]
        )
        membre.date_inscription = data.get("date_inscription", membre.date_inscription)
        return membre
    
    def __str__(self) -> str:
        """Représentation textuelle du membre"""
        statut = "✓ Actif" if self.actif else "✗ Inactif"
        return (f"ID: {self.id_membre} | {self.prenom} {self.nom} | "
                f"{self.email} | {self.telephone} | {statut}")


class GestionnaireMembres:
    """Gère l'ensemble des membres de la tontine"""
    
    def __init__(self, fichier_data: str = "data/tontine.json"):
        """
        Initialise le gestionnaire de membres
        
        Args:
            fichier_data: Chemin vers le fichier de données JSON
        """
        self.fichier_data = fichier_data
        self.membres: Dict[str, Membre] = {}
        self.charger_donnees()
    
    def charger_donnees(self) -> None:
        """Charge les données depuis le fichier JSON"""
        if not os.path.exists("data"):
            os.makedirs("data")
        
        if os.path.exists(self.fichier_data):
            try:
                with open(self.fichier_data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    membres_data = data.get("membres", {})
                    for id_membre, membre_dict in membres_data.items():
                        self.membres[id_membre] = Membre.from_dict(membre_dict)
            except json.JSONDecodeError:
                print("Erreur lors du chargement des données. Nouveau fichier créé.")
                self.sauvegarder_donnees()
        else:
            self.sauvegarder_donnees()
    
    def sauvegarder_donnees(self) -> None:
        """Sauvegarde les données dans le fichier JSON"""
        data = {}
        
        # Charger les données existantes
        if os.path.exists(self.fichier_data):
            try:
                with open(self.fichier_data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass
        
        # Mettre à jour les membres
        data["membres"] = {
            id_membre: membre.to_dict() 
            for id_membre, membre in self.membres.items()
        }
        
        with open(self.fichier_data, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def generer_id(self) -> str:
        """Génère un ID unique pour un nouveau membre"""
        if not self.membres:
            return "M001"
        
        derniers_ids = [int(id_m[1:]) for id_m in self.membres.keys()]
        nouveau_numero = max(derniers_ids) + 1
        return f"M{nouveau_numero:03d}"
    
    def ajouter_membre(self) -> None:
        """Ajoute un nouveau membre via interface CLI"""
        afficher_titre("AJOUTER UN NOUVEAU MEMBRE")
        
        print("Veuillez entrer les informations du membre:\n")
        
        nom = input("Nom: ").strip()
        if not nom:
            print("❌ Le nom ne peut pas être vide.")
            return
        
        prenom = input("Prénom: ").strip()
        if not prenom:
            print("❌ Le prénom ne peut pas être vide.")
            return
        
        while True:
            email = input("Email: ").strip()
            if valider_email(email):
                break
            print("❌ Format d'email invalide. Réessayez.")
        
        while True:
            telephone = input("Téléphone: ").strip()
            if valider_telephone(telephone):
                break
            print("❌ Format de téléphone invalide. Réessayez.")
        
        id_membre = self.generer_id()
        nouveau_membre = Membre(id_membre, nom, prenom, email, telephone)
        self.membres[id_membre] = nouveau_membre
        self.sauvegarder_donnees()
        
        print(f"\n✅ Membre ajouté avec succès! ID: {id_membre}")
    
    def modifier_membre(self) -> None:
        """Modifie les informations d'un membre"""
        afficher_titre("MODIFIER UN MEMBRE")
        
        if not self.membres:
            print("❌ Aucun membre enregistré.")
            return
        
        self.afficher_membres()
        
        id_membre = input("\nEntrez l'ID du membre à modifier: ").strip().upper()
        
        if id_membre not in self.membres:
            print("❌ Membre introuvable.")
            return
        
        membre = self.membres[id_membre]
        print(f"\nModification de: {membre.prenom} {membre.nom}")
        print("(Laissez vide pour conserver la valeur actuelle)\n")
        
        nom = input(f"Nom [{membre.nom}]: ").strip()
        if nom:
            membre.nom = nom
        
        prenom = input(f"Prénom [{membre.prenom}]: ").strip()
        if prenom:
            membre.prenom = prenom
        
        email = input(f"Email [{membre.email}]: ").strip()
        if email and valider_email(email):
            membre.email = email
        
        telephone = input(f"Téléphone [{membre.telephone}]: ").strip()
        if telephone and valider_telephone(telephone):
            membre.telephone = telephone
        
        self.sauvegarder_donnees()
        print("\n✅ Membre modifié avec succès!")
    
    def supprimer_membre(self) -> None:
        """Supprime un membre"""
        afficher_titre("SUPPRIMER UN MEMBRE")
        
        if not self.membres:
            print("❌ Aucun membre enregistré.")
            return
        
        self.afficher_membres()
        
        id_membre = input("\nEntrez l'ID du membre à supprimer: ").strip().upper()
        
        if id_membre not in self.membres:
            print("❌ Membre introuvable.")
            return
        
        membre = self.membres[id_membre]
        confirmation = input(
            f"Êtes-vous sûr de vouloir supprimer {membre.prenom} {membre.nom}? (oui/non): "
        ).strip().lower()
        
        if confirmation == "oui":
            del self.membres[id_membre]
            self.sauvegarder_donnees()
            print("\n✅ Membre supprimé avec succès!")
        else:
            print("\n❌ Suppression annulée.")
    
    def toggle_statut_membre(self) -> None:
        """Active ou désactive un membre"""
        afficher_titre("ACTIVER/DÉSACTIVER UN MEMBRE")
        
        if not self.membres:
            print("❌ Aucun membre enregistré.")
            return
        
        self.afficher_membres()
        
        id_membre = input("\nEntrez l'ID du membre: ").strip().upper()
        
        if id_membre not in self.membres:
            print("❌ Membre introuvable.")
            return
        
        membre = self.membres[id_membre]
        membre.actif = not membre.actif
        self.sauvegarder_donnees()
        
        statut = "activé" if membre.actif else "désactivé"
        print(f"\n✅ Membre {statut} avec succès!")
    
    def afficher_membres(self) -> None:
        """Affiche la liste de tous les membres"""
        afficher_titre("LISTE DES MEMBRES")
        
        if not self.membres:
            print("❌ Aucun membre enregistré.")
            return
        
        print(f"\nNombre total de membres: {len(self.membres)}\n")
        print("-" * 100)
        
        for membre in sorted(self.membres.values(), key=lambda m: m.id_membre):
            print(membre)
        
        print("-" * 100)
    
    def obtenir_membre(self, id_membre: str) -> Optional[Membre]:
        """Retourne un membre par son ID"""
        return self.membres.get(id_membre)
    
    def obtenir_membres_actifs(self) -> List[Membre]:
        """Retourne la liste des membres actifs"""
        return [m for m in self.membres.values() if m.actif]