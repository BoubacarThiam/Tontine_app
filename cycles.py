#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des cycles de tontine
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from utils import afficher_titre


class Cycle:
    """Représente un cycle de tontine"""
    
    def __init__(self, id_cycle: str, montant_cotisation: float, 
                 duree_mois: int, date_debut: str, membres_ids: List[str]):
        """
        Initialise un cycle
        
        Args:
            id_cycle: Identifiant unique du cycle
            montant_cotisation: Montant de la cotisation mensuelle
            duree_mois: Durée du cycle en mois
            date_debut: Date de début du cycle (YYYY-MM-DD)
            membres_ids: Liste des IDs des membres participants
        """
        self.id_cycle = id_cycle
        self.montant_cotisation = montant_cotisation
        self.duree_mois = duree_mois
        self.date_debut = date_debut
        self.membres_ids = membres_ids
        self.ordre_passage = []
        self.mois_actuel = 0
        self.termine = False
        self.date_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generer_ordre_passage(self) -> None:
        """Génère aléatoirement l'ordre de passage des membres"""
        self.ordre_passage = self.membres_ids.copy()
        random.shuffle(self.ordre_passage)
    
    def obtenir_beneficiaire_actuel(self) -> Optional[str]:
        """Retourne l'ID du bénéficiaire du mois actuel"""
        if self.mois_actuel < len(self.ordre_passage):
            return self.ordre_passage[self.mois_actuel]
        return None
    
    def passer_mois_suivant(self) -> bool:
        """
        Passe au mois suivant
        
        Returns:
            True si le cycle continue, False s'il est terminé
        """
        self.mois_actuel += 1
        if self.mois_actuel >= self.duree_mois:
            self.termine = True
            return False
        return True
    
    def to_dict(self) -> Dict:
        """Convertit le cycle en dictionnaire"""
        return {
            "id_cycle": self.id_cycle,
            "montant_cotisation": self.montant_cotisation,
            "duree_mois": self.duree_mois,
            "date_debut": self.date_debut,
            "membres_ids": self.membres_ids,
            "ordre_passage": self.ordre_passage,
            "mois_actuel": self.mois_actuel,
            "termine": self.termine,
            "date_creation": self.date_creation
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Cycle':
        """Crée un cycle à partir d'un dictionnaire"""
        cycle = cls(
            data["id_cycle"],
            data["montant_cotisation"],
            data["duree_mois"],
            data["date_debut"],
            data["membres_ids"]
        )
        cycle.ordre_passage = data.get("ordre_passage", [])
        cycle.mois_actuel = data.get("mois_actuel", 0)
        cycle.termine = data.get("termine", False)
        cycle.date_creation = data.get("date_creation", cycle.date_creation)
        return cycle
    
    def __str__(self) -> str:
        """Représentation textuelle du cycle"""
        statut = "Terminé" if self.termine else f"En cours (Mois {self.mois_actuel + 1}/{self.duree_mois})"
        return (f"Cycle {self.id_cycle} | Cotisation: {self.montant_cotisation} FCFA | "
                f"Durée: {self.duree_mois} mois | Début: {self.date_debut} | "
                f"Participants: {len(self.membres_ids)} | {statut}")


class GestionnaireCycles:
    """Gère l'ensemble des cycles de tontine"""
    
    def __init__(self, gestionnaire_membres, fichier_data: str = "data/tontine.json"):
        """
        Initialise le gestionnaire de cycles
        
        Args:
            gestionnaire_membres: Instance du gestionnaire de membres
            fichier_data: Chemin vers le fichier de données JSON
        """
        self.gestionnaire_membres = gestionnaire_membres
        self.fichier_data = fichier_data
        self.cycles: Dict[str, Cycle] = {}
        self.charger_donnees()
    
    def charger_donnees(self) -> None:
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.fichier_data):
            try:
                with open(self.fichier_data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cycles_data = data.get("cycles", {})
                    for id_cycle, cycle_dict in cycles_data.items():
                        self.cycles[id_cycle] = Cycle.from_dict(cycle_dict)
            except json.JSONDecodeError:
                pass
    
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
        
        # Mettre à jour les cycles
        data["cycles"] = {
            id_cycle: cycle.to_dict() 
            for id_cycle, cycle in self.cycles.items()
        }
        
        with open(self.fichier_data, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def generer_id(self) -> str:
        """Génère un ID unique pour un nouveau cycle"""
        if not self.cycles:
            return "C001"
        
        derniers_ids = [int(id_c[1:]) for id_c in self.cycles.keys()]
        nouveau_numero = max(derniers_ids) + 1
        return f"C{nouveau_numero:03d}"
    
    def obtenir_cycle_actif(self) -> Optional[Cycle]:
        """Retourne le cycle actif (non terminé)"""
        for cycle in self.cycles.values():
            if not cycle.termine:
                return cycle
        return None
    
    def creer_cycle(self) -> None:
        """Crée un nouveau cycle via interface CLI"""
        afficher_titre("CRÉER UN NOUVEAU CYCLE")
        
        # Vérifier qu'il n'y a pas de cycle actif
        cycle_actif = self.obtenir_cycle_actif()
        if cycle_actif:
            print(f"❌ Un cycle est déjà en cours: {cycle_actif.id_cycle}")
            print("Veuillez terminer le cycle actif avant d'en créer un nouveau.")
            return
        
        # Vérifier qu'il y a des membres actifs
        membres_actifs = self.gestionnaire_membres.obtenir_membres_actifs()
        if len(membres_actifs) < 2:
            print("❌ Il faut au moins 2 membres actifs pour créer un cycle.")
            return
        
        print(f"\nMembres actifs disponibles: {len(membres_actifs)}")
        for membre in membres_actifs:
            print(f"  - {membre.id_membre}: {membre.prenom} {membre.nom}")
        
        print("\nVeuillez entrer les informations du cycle:\n")
        
        # Montant de cotisation
        while True:
            try:
                montant = float(input("Montant de la cotisation mensuelle (FCFA): ").strip())
                if montant > 0:
                    break
                print("❌ Le montant doit être positif.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
        
        # Durée
        while True:
            try:
                duree = int(input("Durée du cycle (en mois): ").strip())
                if duree >= len(membres_actifs):
                    break
                print(f"❌ La durée doit être au moins égale au nombre de membres ({len(membres_actifs)}).")
            except ValueError:
                print("❌ Veuillez entrer un nombre entier.")
        
        # Date de début
        while True:
            date_str = input("Date de début (YYYY-MM-DD) ou Entrée pour aujourd'hui: ").strip()
            if not date_str:
                date_debut = datetime.now().strftime("%Y-%m-%d")
                break
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                date_debut = date_str
                break
            except ValueError:
                print("❌ Format de date invalide. Utilisez YYYY-MM-DD.")
        
        # Sélection des membres participants
        print("\nSélection des membres participants:")
        print("1. Tous les membres actifs")
        print("2. Sélection manuelle")
        
        choix = input("Votre choix (1 ou 2): ").strip()
        
        if choix == "1":
            membres_ids = [m.id_membre for m in membres_actifs]
        else:
            membres_ids = []
            print("\nEntrez les IDs des membres (séparés par des espaces):")
            ids_input = input().strip().upper().split()
            
            for id_m in ids_input:
                if id_m in [m.id_membre for m in membres_actifs]:
                    if id_m not in membres_ids:
                        membres_ids.append(id_m)
                else:
                    print(f"⚠️  {id_m} ignoré (membre inactif ou introuvable)")
            
            if len(membres_ids) < 2:
                print("❌ Il faut au moins 2 membres pour créer un cycle.")
                return
        
        # Création du cycle
        id_cycle = self.generer_id()
        nouveau_cycle = Cycle(id_cycle, montant, duree, date_debut, membres_ids)
        nouveau_cycle.generer_ordre_passage()
        
        self.cycles[id_cycle] = nouveau_cycle
        self.sauvegarder_donnees()
        
        print(f"\n✅ Cycle créé avec succès! ID: {id_cycle}")
        print(f"Nombre de participants: {len(membres_ids)}")
        print(f"Montant total par tour: {montant * len(membres_ids)} FCFA")
    
    def afficher_cycle_actif(self) -> None:
        """Affiche les détails du cycle actif"""
        afficher_titre("CYCLE ACTIF")
        
        cycle = self.obtenir_cycle_actif()
        if not cycle:
            print("❌ Aucun cycle actif.")
            return
        
        print(cycle)
        print("\n" + "="*80)
        print(f"Mois actuel: {cycle.mois_actuel + 1}/{cycle.duree_mois}")
        print(f"Montant total collecté par tour: {cycle.montant_cotisation * len(cycle.membres_ids)} FCFA")
        
        beneficiaire_id = cycle.obtenir_beneficiaire_actuel()
        if beneficiaire_id:
            beneficiaire = self.gestionnaire_membres.obtenir_membre(beneficiaire_id)
            if beneficiaire:
                print(f"Bénéficiaire actuel: {beneficiaire.prenom} {beneficiaire.nom} ({beneficiaire_id})")
        
        print("\n" + "-"*80)
        print("Ordre de passage:")
        print("-"*80)
        
        for i, membre_id in enumerate(cycle.ordre_passage, 1):
            membre = self.gestionnaire_membres.obtenir_membre(membre_id)
            if membre:
                statut = "✓ Passé" if i <= cycle.mois_actuel else "→ En attente" if i == cycle.mois_actuel + 1 else "  À venir"
                print(f"{i:2d}. {membre.prenom} {membre.nom:15s} ({membre_id}) {statut}")
        
        print("="*80)
    
    def afficher_tous_cycles(self) -> None:
        """Affiche tous les cycles"""
        afficher_titre("TOUS LES CYCLES")
        
        if not self.cycles:
            print("❌ Aucun cycle enregistré.")
            return
        
        print(f"\nNombre total de cycles: {len(self.cycles)}\n")
        print("-" * 120)
        
        for cycle in sorted(self.cycles.values(), key=lambda c: c.id_cycle):
            print(cycle)
        
        print("-" * 120)
    
    def terminer_cycle(self) -> None:
        """Termine manuellement le cycle actif"""
        afficher_titre("TERMINER LE CYCLE ACTIF")
        
        cycle = self.obtenir_cycle_actif()
        if not cycle:
            print("❌ Aucun cycle actif.")
            return
        
        print(f"Cycle: {cycle.id_cycle}")
        print(f"Progression: Mois {cycle.mois_actuel + 1}/{cycle.duree_mois}")
        
        confirmation = input("\nÊtes-vous sûr de vouloir terminer ce cycle? (oui/non): ").strip().lower()
        
        if confirmation == "oui":
            cycle.termine = True
            self.sauvegarder_donnees()
            print("\n✅ Cycle terminé avec succès!")
        else:
            print("\n❌ Opération annulée.")