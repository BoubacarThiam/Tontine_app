# 🏦 Système de Gestion de Tontine Numérique



## 🎯 Contexte du projet

Une **tontine** est un système d'épargne rotatif traditionnel largement utilisé en Afrique et dans d'autres régions du monde. Les membres cotisent régulièrement un montant fixe, et chaque mois, un membre différent reçoit la totalité de la cagnotte.

Ce projet vise à **digitaliser** ce processus en offrant :
- Une gestion transparente des membres et des cotisations
- Un suivi rigoureux des paiements et des retards
- Une automatisation du calcul des pénalités
- Un historique complet des transactions
- Des rapports mensuels détaillés

### Objectifs pédagogiques
- Maîtrise de la **Programmation Orientée Objet (POO)** en Python
- Gestion de la **persistance des données** avec JSON
- Développement d'une **interface CLI** professionnelle
- Application des **bonnes pratiques** de développement
- Projet valorisable sur un **CV** ou un portfolio GitHub

## ✨ Fonctionnalités

### 1. Gestion des Membres
- ➕ Ajouter un nouveau membre avec ses informations (nom, prénom, email, téléphone)
- ✏️ Modifier les informations d'un membre existant
- 🗑️ Supprimer un membre
- 🔄 Activer ou désactiver un membre
- 📋 Afficher la liste complète des membres

### 2. Gestion des Cycles
- 🔁 Créer un nouveau cycle avec :
  - Montant de cotisation mensuelle
  - Durée en mois
  - Date de début
  - Sélection des membres participants
- 🎲 Génération automatique de l'ordre de passage aléatoire
- 📊 Affichage de l'état du cycle en cours
- 📜 Consultation de l'historique de tous les cycles
- ✔️ Terminer manuellement un cycle

### 3. Gestion des Cotisations
- 💰 Enregistrement des cotisations mensuelles
- ⏰ Vérification automatique des retards de paiement
- ⚠️ Application automatique de pénalités (10% du montant manquant)
- 💳 Calcul et affichage du solde de chaque membre
- 📈 Tableau récapitulatif des soldes

### 4. Historique et Rapports
- 📝 Historique complet de toutes les transactions
- 📊 Génération de rapports mensuels détaillés
- 📤 Export des données en format CSV
- 📉 Suivi de la progression du cycle

## 🏗️ Architecture

```
tontine_app/
│
├── main.py                 # Point d'entrée principal (menus CLI)
├── membres.py              # Gestion des membres (classe Membre + GestionnaireMembres)
├── cycles.py               # Gestion des cycles (classe Cycle + GestionnaireCycles)
├── finances.py             # Gestion des finances (Transaction + GestionnaireFinances)
├── utils.py                # Fonctions utilitaires (affichage, validation, etc.)
│
├── data/
│   ├── tontine.json        # Base de données JSON (persistance)
│   ├── export_transactions.csv  # Export des transactions
│   └── export_soldes.csv        # Export des soldes
│
└── README.md               # Documentation complète
```

### Classes principales

**Membre** : Représente un membre de la tontine avec ses informations personnelles et son statut

**Cycle** : Représente un cycle de tontine avec montant, durée, participants et ordre de passage

**Transaction** : Représente une opération financière (cotisation, pénalité, distribution)

**Gestionnaires** : Classes responsables de la logique métier et de la persistance des données

## 📦 Prérequis

- **Python 3.8 ou supérieur**
- Aucune bibliothèque externe requise (uniquement modules standards)

## 🚀 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-username/tontine-app.git
cd tontine-app
```

2. **Vérifier la version de Python**
```bash
python --version
# ou
python3 --version
```

3. **Créer le dossier de données** (automatique au premier lancement)
```bash
mkdir -p data
```

## 💻 Utilisation

### Lancement de l'application

```bash
python main.py
# ou
python3 main.py
```

### Navigation dans les menus

L'application propose une interface CLI intuitive avec des menus numérotés :

```
==============================================================================
                    SYSTÈME DE GESTION DE TONTINE
==============================================================================

1. Gestion des Membres
2. Gestion des Cycles
3. Gestion des Cotisations
4. Historique et Rapports
5. Quitter

Votre choix (1-5):
```

Entrez simplement le numéro correspondant à l'action souhaitée.

### Workflow typique

1. **Ajouter des membres** (minimum 2)
2. **Créer un cycle** avec montant et durée
3. **Enregistrer les cotisations** mensuelles
4. **Vérifier les retards** et pénalités
5. **Consulter les rapports** et l'historique

## 📊 Structure des données

### Format JSON (data/tontine.json)

```json
{
    "membres": {
        "M001": {
            "id_membre": "M001",
            "nom": "DIOP",
            "prenom": "Amadou",
            "email": "amadou.diop@email.com",
            "telephone": "+221771234567",
            "actif": true,
            "date_inscription": "2024-01-15 10:30:00"
        }
    },
    "cycles": {
        "C001": {
            "id_cycle": "C001",
            "montant_cotisation": 10000,
            "duree_mois": 12,
            "date_debut": "2024-01-01",
            "membres_ids": ["M001", "M002", "M003"],
            "ordre_passage": ["M002", "M001", "M003"],
            "mois_actuel": 0,
            "termine": false
        }
    },
    "transactions": [
        {
            "id_transaction": "T0001",
            "id_membre": "M001",
            "id_cycle": "C001",
            "montant": 10000,
            "type_transaction": "cotisation",
            "mois": 0,
            "penalite": 0,
            "date_transaction": "2024-01-15 14:20:00"
        }
    ],
    "soldes": {
        "M001": -10000,
        "M002": 0,
        "M003": -10000
    }
}
```

## 🎮 Exemples d'utilisation

### Exemple 1 : Créer une tontine de 5 personnes

1. Ajouter 5 membres avec leurs informations
2. Créer un cycle :
   - Montant : 50 000 FCFA
   - Durée : 5 mois
   - Tous les membres actifs
3. L'ordre de passage est généré automatiquement
4. Chaque mois, les membres cotisent 50 000 FCFA
5. Le bénéficiaire du mois reçoit 250 000 FCFA (5 × 50 000)

### Exemple 2 : Gérer les retards

1. Vérifier les retards du mois en cours
2. Le système identifie automatiquement les membres n'ayant pas cotisé
3. Pour les paiements partiels, une pénalité de 10% est appliquée
4. Le solde du membre est mis à jour automatiquement

### Exemple 3 : Exporter les données

1. Générer un rapport mensuel
2. Exporter les transactions en CSV
3. Exporter les soldes en CSV
4. Analyser les données dans Excel ou LibreOffice


## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité (`git checkout -b feature/NouvelleFonctionnalite`)
3. **Committez** vos changements (`git commit -m 'Ajout de NouvelleFonctionnalite'`)
4. **Pushez** vers la branche (`git push origin feature/NouvelleFonctionnalite`)
5. Ouvrez une **Pull Request**

### Standards de code
- Respecter **PEP 8** (style Python)
- Documenter les fonctions avec des **docstrings**
- Ajouter des **tests unitaires** si possible
- Commenter les parties complexes du code

## 📝 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Votre Nom**
- GitHub: [Boubacar Thiam](https://github.com/BoubacarThiam)
- Email: boubacarthiam005@icloud.com
- num : 784061791


- Inspiration : Systèmes de tontine traditionnels africains


**⭐ Si ce projet vous est utile, n'oubliez pas de lui donner une étoile sur GitHub !**

**📚 Conçu avec ❤️ pour l'apprentissage et le développement de compétences professionnelles**
