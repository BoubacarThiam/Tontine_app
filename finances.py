#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des finances et cotisations
"""

import json
import os
import csv
from datetime import datetime
from typing import List, Dict, Optional
from utils import afficher_titre


class Transaction:
    """Représente une transaction financière"""
    
    def __init__(self, id_transaction: str, id_membre: str, id_cycle: str,
                 montant: float, type_transaction: str, mois: int, 
                 penalite: float = 0.0):
        """
        Initialise une transaction
        
        Args:
            id_transaction: Identifiant unique
            id_membre: ID du membre
            id_cycle: ID du cycle
            montant: Montant de la transaction
            type_transaction: Type (cotisation, penalite, distribution)
            mois: Numéro du mois dans le cycle
            penalite: Montant de pénalité éventuelle
        """
        self.id_transaction = id_transaction
        self.id_membre = id_membre
        self.id_cycle = id_cycle
        self.montant = montant
        self.type_transaction = type_transaction
        self.mois = mois
        self.penalite = penalite
        self.date_transaction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convertit la transaction en dictionnaire"""
        return {
            "id_transaction": self.id_transaction,
            "id_membre": self.id_membre,
            "id_cycle": self.id_cycle,
            "montant": self.montant,
            "type_transaction": self.type_transaction,
            "mois": self.mois,
            "penalite": self.penalite,
            "date_transaction": self.date_transaction
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """Crée une transaction à partir d'un dictionnaire"""
        transaction = cls(
            data["id_transaction"],
            data["id_membre"],
            data["id_cycle"],
            data["montant"],
            data["type_transaction"],
            data["mois"],
            data.get("penalite", 0.0)
        )
        transaction.date_transaction = data.get("date_transaction", transaction.date_transaction)
        return transaction


class GestionnaireFinances:
    """Gère les finances de la tontine"""
    
    TAUX_PENALITE = 0.10  # 10% de pénalité pour retard
    
    def __init__(self, gestionnaire_membres, gestionnaire_cycles, 
                 fichier_data: str = "data/tontine.json"):
        """
        Initialise le gestionnaire de finances
        
        Args:
            gestionnaire_membres: Instance du gestionnaire de membres
            gestionnaire_cycles: Instance du gestionnaire de cycles
            fichier_data: Chemin vers le fichier de données JSON
        """
        self.gestionnaire_membres = gestionnaire_membres
        self.gestionnaire_cycles = gestionnaire_cycles
        self.fichier_data = fichier_data
        self.transactions: List[Transaction] = []
        self.soldes: Dict[str, float] = {}
        self.charger_donnees()
    
    def charger_donnees(self) -> None:
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.fichier_data):
            try:
                with open(self.fichier_data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Charger les transactions
                    transactions_data = data.get("transactions", [])
                    self.transactions = [
                        Transaction.from_dict(t) for t in transactions_data
                    ]
                    
                    # Charger les soldes
                    self.soldes = data.get("soldes", {})
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
        
        # Mettre à jour les finances
        data["transactions"] = [t.to_dict() for t in self.transactions]
        data["soldes"] = self.soldes
        
        with open(self.fichier_data, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def generer_id_transaction(self) -> str:
        """Génère un ID unique pour une nouvelle transaction"""
        if not self.transactions:
            return "T0001"
        
        derniers_ids = [int(t.id_transaction[1:]) for t in self.transactions]
        nouveau_numero = max(derniers_ids) + 1
        return f"T{nouveau_numero:04d}"
    
    def enregistrer_cotisation(self) -> None:
        """Enregistre une cotisation via interface CLI"""
        afficher_titre("ENREGISTRER UNE COTISATION")
        
        cycle = self.gestionnaire_cycles.obtenir_cycle_actif()
        if not cycle:
            print("❌ Aucun cycle actif.")
            return
        
        print(f"Cycle actif: {cycle.id_cycle}")
        print(f"Mois actuel: {cycle.mois_actuel + 1}/{cycle.duree_mois}")
        print(f"Montant de cotisation: {cycle.montant_cotisation} FCFA\n")
        
        # Afficher les membres du cycle
        print("Membres participants:")
        for membre_id in cycle.membres_ids:
            membre = self.gestionnaire_membres.obtenir_membre(membre_id)
            if membre:
                print(f"  - {membre_id}: {membre.prenom} {membre.nom}")
        
        id_membre = input("\nID du membre qui cotise: ").strip().upper()
        
        if id_membre not in cycle.membres_ids:
            print("❌ Ce membre ne participe pas au cycle actif.")
            return
        
        membre = self.gestionnaire_membres.obtenir_membre(id_membre)
        if not membre:
            print("❌ Membre introuvable.")
            return
        
        # Vérifier si déjà payé ce mois
        deja_paye = any(
            t.id_membre == id_membre and 
            t.id_cycle == cycle.id_cycle and 
            t.mois == cycle.mois_actuel and
            t.type_transaction == "cotisation"
            for t in self.transactions
        )
        
        if deja_paye:
            print(f"⚠️  {membre.prenom} {membre.nom} a déjà cotisé ce mois.")
            return
        
        # Saisir le montant
        while True:
            try:
                montant = float(input(f"Montant versé (attendu: {cycle.montant_cotisation} FCFA): ").strip())
                if montant > 0:
                    break
                print("❌ Le montant doit être positif.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
        
        # Calculer pénalité si paiement insuffisant ou en retard
        penalite = 0.0
        if montant < cycle.montant_cotisation:
            penalite = (cycle.montant_cotisation - montant) * self.TAUX_PENALITE
            print(f"⚠️  Paiement partiel détecté. Pénalité appliquée: {penalite:.2f} FCFA")
        
        # Créer la transaction
        id_transaction = self.generer_id_transaction()
        transaction = Transaction(
            id_transaction,
            id_membre,
            cycle.id_cycle,
            montant,
            "cotisation",
            cycle.mois_actuel,
            penalite
        )
        
        self.transactions.append(transaction)
        
        # Mettre à jour le solde
        if id_membre not in self.soldes:
            self.soldes[id_membre] = 0.0
        
        self.soldes[id_membre] -= montant
        if penalite > 0:
            self.soldes[id_membre] -= penalite
        
        self.sauvegarder_donnees()
        
        print(f"\n✅ Cotisation enregistrée! Transaction ID: {id_transaction}")
        if penalite > 0:
            print(f"   Montant: {montant} FCFA + Pénalité: {penalite:.2f} FCFA")
            print(f"   Total débité: {montant + penalite:.2f} FCFA")
    
    def verifier_retards(self) -> None:
        """Vérifie et affiche les retards de paiement"""
        afficher_titre("VÉRIFICATION DES RETARDS")
        
        cycle = self.gestionnaire_cycles.obtenir_cycle_actif()
        if not cycle:
            print("❌ Aucun cycle actif.")
            return
        
        print(f"Cycle: {cycle.id_cycle}")
        print(f"Mois actuel: {cycle.mois_actuel + 1}/{cycle.duree_mois}")
        print(f"Montant attendu: {cycle.montant_cotisation} FCFA\n")
        
        print("-" * 80)
        print(f"{'Membre':<30} {'Statut':<20} {'Montant dû':<15}")
        print("-" * 80)
        
        retards_trouves = False
        
        for membre_id in cycle.membres_ids:
            membre = self.gestionnaire_membres.obtenir_membre(membre_id)
            if not membre:
                continue
            
            # Vérifier si payé ce mois
            transactions_mois = [
                t for t in self.transactions
                if t.id_membre == membre_id and
                   t.id_cycle == cycle.id_cycle and
                   t.mois == cycle.mois_actuel and
                   t.type_transaction == "cotisation"
            ]
            
            if not transactions_mois:
                statut = "❌ Non payé"
                montant_du = cycle.montant_cotisation
                retards_trouves = True
            elif sum(t.montant for t in transactions_mois) < cycle.montant_cotisation:
                statut = "⚠️  Paiement partiel"
                montant_du = cycle.montant_cotisation - sum(t.montant for t in transactions_mois)
                retards_trouves = True
            else:
                statut = "✓ Payé"
                montant_du = 0.0
            
            nom_complet = f"{membre.prenom} {membre.nom} ({membre_id})"
            print(f"{nom_complet:<30} {statut:<20} {montant_du:>12.2f} FCFA")
        
        print("-" * 80)
        
        if not retards_trouves:
            print("\n✅ Tous les membres sont à jour!")
    
    def afficher_solde_membre(self) -> None:
        """Affiche le solde d'un membre spécifique"""
        afficher_titre("SOLDE D'UN MEMBRE")
        
        if not self.gestionnaire_membres.membres:
            print("❌ Aucun membre enregistré.")
            return
        
        print("Membres disponibles:")
        for membre in self.gestionnaire_membres.membres.values():
            print(f"  - {membre.id_membre}: {membre.prenom} {membre.nom}")
        
        id_membre = input("\nID du membre: ").strip().upper()
        
        membre = self.gestionnaire_membres.obtenir_membre(id_membre)
        if not membre:
            print("❌ Membre introuvable.")
            return
        
        solde = self.soldes.get(id_membre, 0.0)
        
        print("\n" + "="*60)
        print(f"Membre: {membre.prenom} {membre.nom} ({id_membre})")
        print(f"Solde actuel: {solde:.2f} FCFA")
        
        if solde < 0:
            print("Statut: ⚠️  Débiteur")
        elif solde > 0:
            print("Statut: ✓ Créditeur")
        else:
            print("Statut: ✓ À jour")
        
        print("="*60)
    
    def afficher_tous_soldes(self) -> None:
        """Affiche les soldes de tous les membres"""
        afficher_titre("SOLDES DE TOUS LES MEMBRES")
        
        if not self.gestionnaire_membres.membres:
            print("❌ Aucun membre enregistré.")
            return
        
        print("-" * 70)
        print(f"{'Membre':<35} {'Solde (FCFA)':<20} {'Statut':<15}")
        print("-" * 70)
        
        for membre_id, membre in sorted(self.gestionnaire_membres.membres.items()):
            solde = self.soldes.get(membre_id, 0.0)
            nom_complet = f"{membre.prenom} {membre.nom} ({membre_id})"
            
            if solde < 0:
                statut = "⚠️  Débiteur"
            elif solde > 0:
                statut = "✓ Créditeur"
            else:
                statut = "✓ À jour"
            
            print(f"{nom_complet:<35} {solde:>15.2f} {statut:<15}")
        
        print("-" * 70)
    
    def afficher_historique(self) -> None:
        """Affiche l'historique des transactions"""
        afficher_titre("HISTORIQUE DES TRANSACTIONS")
        
        if not self.transactions:
            print("❌ Aucune transaction enregistrée.")
            return
        
        print(f"\nNombre total de transactions: {len(self.transactions)}\n")
        print("-" * 120)
        print(f"{'ID':<8} {'Date':<20} {'Membre':<12} {'Cycle':<8} {'Type':<15} {'Montant':<12} {'Pénalité':<12}")
        print("-" * 120)
        
        for transaction in sorted(self.transactions, 
                                 key=lambda t: t.date_transaction, 
                                 reverse=True):
            print(f"{transaction.id_transaction:<8} "
                  f"{transaction.date_transaction:<20} "
                  f"{transaction.id_membre:<12} "
                  f"{transaction.id_cycle:<8} "
                  f"{transaction.type_transaction:<15} "
                  f"{transaction.montant:>10.2f} "
                  f"{transaction.penalite:>10.2f}")
        
        print("-" * 120)
    
    def generer_rapport_mensuel(self) -> None:
        """Génère un rapport mensuel"""
        afficher_titre("RAPPORT MENSUEL")
        
        cycle = self.gestionnaire_cycles.obtenir_cycle_actif()
        if not cycle:
            print("❌ Aucun cycle actif.")
            return
        
        mois_actuel = cycle.mois_actuel
        
        # Transactions du mois
        transactions_mois = [
            t for t in self.transactions
            if t.id_cycle == cycle.id_cycle and t.mois == mois_actuel
        ]
        
        total_collecte = sum(t.montant for t in transactions_mois)
        total_penalites = sum(t.penalite for t in transactions_mois)
        nombre_cotisations = len(transactions_mois)
        
        print(f"\nCycle: {cycle.id_cycle}")
        print(f"Mois: {mois_actuel + 1}/{cycle.duree_mois}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        print("\n" + "="*60)
        print("RÉSUMÉ FINANCIER")
        print("="*60)
        print(f"Nombre de cotisations reçues: {nombre_cotisations}/{len(cycle.membres_ids)}")
        print(f"Montant total collecté: {total_collecte:.2f} FCFA")
        print(f"Total des pénalités: {total_penalites:.2f} FCFA")
        print(f"Montant attendu: {cycle.montant_cotisation * len(cycle.membres_ids):.2f} FCFA")
        
        manque = (cycle.montant_cotisation * len(cycle.membres_ids)) - total_collecte
        print(f"Manque à collecter: {manque:.2f} FCFA")
        
        beneficiaire_id = cycle.obtenir_beneficiaire_actuel()
        if beneficiaire_id:
            beneficiaire = self.gestionnaire_membres.obtenir_membre(beneficiaire_id)
            if beneficiaire:
                print(f"\nBénéficiaire du mois: {beneficiaire.prenom} {beneficiaire.nom} ({beneficiaire_id})")
                print(f"Montant à recevoir: {total_collecte:.2f} FCFA")
        
        print("="*60)
    
    def exporter_csv(self) -> None:
        """Exporte les données en fichiers CSV"""
        afficher_titre("EXPORT DES DONNÉES EN CSV")
        
        # Export des transactions
        fichier_transactions = "data/export_transactions.csv"
        try:
            with open(fichier_transactions, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID Transaction", "Date", "Membre", "Cycle", 
                    "Type", "Montant", "Pénalité"
                ])
                
                for t in self.transactions:
                    writer.writerow([
                        t.id_transaction,
                        t.date_transaction,
                        t.id_membre,
                        t.id_cycle,
                        t.type_transaction,
                        t.montant,
                        t.penalite
                    ])
            
            print(f"✅ Transactions exportées: {fichier_transactions}")
        except Exception as e:
            print(f"❌ Erreur lors de l'export des transactions: {e}")
        
        # Export des soldes
        fichier_soldes = "data/export_soldes.csv"
        try:
            with open(fichier_soldes, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID Membre", "Nom", "Prénom", "Solde"])
                
                for membre_id, solde in self.soldes.items():
                    membre = self.gestionnaire_membres.obtenir_membre(membre_id)
                    if membre:
                        writer.writerow([
                            membre_id,
                            membre.nom,
                            membre.prenom,
                            solde
                        ])
            
            print(f"✅ Soldes exportés: {fichier_soldes}")
        except Exception as e:
            print(f"❌ Erreur lors de l'export des soldes: {e}")
        
        print("\n📁 Fichiers disponibles dans le dossier 'data/'")