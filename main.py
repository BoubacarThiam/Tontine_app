
"""
Système de Gestion de Tontine Numérique
Point d'entrée principal de l'application
"""

import os
import sys
from typing import Optional

from membres import GestionnaireMembres
from cycles import GestionnaireCycles
from finances import GestionnaireFinances
from utils import afficher_titre, afficher_menu, effacer_ecran, pause, valider_choix


class ApplicationTontine:
    """Classe principale gérant l'application de tontine"""
    
    def __init__(self):
        """Initialise les gestionnaires de l'application"""
        self.gestionnaire_membres = GestionnaireMembres()
        self.gestionnaire_cycles = GestionnaireCycles(self.gestionnaire_membres)
        self.gestionnaire_finances = GestionnaireFinances(
            self.gestionnaire_membres,
            self.gestionnaire_cycles
        )
    
    def menu_principal(self) -> None:
        """Affiche et gère le menu principal"""
        while True:
            effacer_ecran()
            afficher_titre("SYSTÈME DE GESTION DE TONTINE")
            
            options = [
                "Gestion des Membres",
                "Gestion des Cycles",
                "Gestion des Cotisations",
                "Historique et Rapports",
                "Quitter"
            ]
            
            afficher_menu(options)
            choix = valider_choix(1, len(options))
            
            if choix == 1:
                self.menu_membres()
            elif choix == 2:
                self.menu_cycles()
            elif choix == 3:
                self.menu_cotisations()
            elif choix == 4:
                self.menu_rapports()
            elif choix == 5:
                self.quitter()
                break
    
    def menu_membres(self) -> None:
        """Menu de gestion des membres"""
        while True:
            effacer_ecran()
            afficher_titre("GESTION DES MEMBRES")
            
            options = [
                "Ajouter un membre",
                "Modifier un membre",
                "Supprimer un membre",
                "Activer/Désactiver un membre",
                "Afficher tous les membres",
                "Retour au menu principal"
            ]
            
            afficher_menu(options)
            choix = valider_choix(1, len(options))
            
            if choix == 1:
                self.gestionnaire_membres.ajouter_membre()
            elif choix == 2:
                self.gestionnaire_membres.modifier_membre()
            elif choix == 3:
                self.gestionnaire_membres.supprimer_membre()
            elif choix == 4:
                self.gestionnaire_membres.toggle_statut_membre()
            elif choix == 5:
                self.gestionnaire_membres.afficher_membres()
            elif choix == 6:
                break
            
            if choix != 6:
                pause()
    
    def menu_cycles(self) -> None:
        """Menu de gestion des cycles"""
        while True:
            effacer_ecran()
            afficher_titre("GESTION DES CYCLES")
            
            options = [
                "Créer un nouveau cycle",
                "Afficher le cycle actif",
                "Afficher tous les cycles",
                "Terminer le cycle actif",
                "Retour au menu principal"
            ]
            
            afficher_menu(options)
            choix = valider_choix(1, len(options))
            
            if choix == 1:
                self.gestionnaire_cycles.creer_cycle()
            elif choix == 2:
                self.gestionnaire_cycles.afficher_cycle_actif()
            elif choix == 3:
                self.gestionnaire_cycles.afficher_tous_cycles()
            elif choix == 4:
                self.gestionnaire_cycles.terminer_cycle()
            elif choix == 5:
                break
            
            if choix != 5:
                pause()
    
    def menu_cotisations(self) -> None:
        """Menu de gestion des cotisations"""
        while True:
            effacer_ecran()
            afficher_titre("GESTION DES COTISATIONS")
            
            options = [
                "Enregistrer une cotisation",
                "Vérifier les retards de paiement",
                "Afficher le solde d'un membre",
                "Afficher tous les soldes",
                "Retour au menu principal"
            ]
            
            afficher_menu(options)
            choix = valider_choix(1, len(options))
            
            if choix == 1:
                self.gestionnaire_finances.enregistrer_cotisation()
            elif choix == 2:
                self.gestionnaire_finances.verifier_retards()
            elif choix == 3:
                self.gestionnaire_finances.afficher_solde_membre()
            elif choix == 4:
                self.gestionnaire_finances.afficher_tous_soldes()
            elif choix == 5:
                break
            
            if choix != 5:
                pause()
    
    def menu_rapports(self) -> None:
        """Menu des historiques et rapports"""
        while True:
            effacer_ecran()
            afficher_titre("HISTORIQUE ET RAPPORTS")
            
            options = [
                "Afficher l'historique des transactions",
                "Générer un rapport mensuel",
                "Exporter les données en CSV",
                "Retour au menu principal"
            ]
            
            afficher_menu(options)
            choix = valider_choix(1, len(options))
            
            if choix == 1:
                self.gestionnaire_finances.afficher_historique()
            elif choix == 2:
                self.gestionnaire_finances.generer_rapport_mensuel()
            elif choix == 3:
                self.gestionnaire_finances.exporter_csv()
            elif choix == 4:
                break
            
            if choix != 4:
                pause()
    
    def quitter(self) -> None:
        """Quitte l'application proprement"""
        effacer_ecran()
        print("\n" + "="*50)
        print("Merci d'avoir utilisé le Système de Gestion de Tontine")
        print("Toutes les données ont été sauvegardées.")
        print("="*50 + "\n")


def main():
    """Fonction principale"""
    try:
        app = ApplicationTontine()
        app.menu_principal()
    except KeyboardInterrupt:
        print("\n\nArrêt de l'application...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nErreur critique: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()