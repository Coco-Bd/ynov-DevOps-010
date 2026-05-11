# Projet DevOps : Déploiement K8s & Observabilité via AWX

## 👤 Auteur
- **Étudiant :** Corentin BEDO
---

## 📝 Présentation du Projet
L'objectif de ce projet est de monter de A à Z une infrastructure automatisée sur un VPS OVH. On y déploie une application web conteneurisée sur un cluster Kubernetes (K3s), et tout le processus de déploiement est piloté par AWX.

> **Note sur le code applicatif :** Mon but ici est de faire de l'infrastructure (système, réseau, automatisation, IaC). N'étant pas développeur de formation, le code Python/Flask a été généré avec l'aide d'une IA.

---

## 🤝 Qui fait quoi ? (Le contexte du projet)
Ce repo fait partie d'un projet de groupe orienté SRE où l'on sépare la création de l'app, la collecte des métriques, et l'analyse des logs. Voici la répartition :

* **Mon rôle (Production des données & Déploiement) :** 
  J'ai préparé l'application Flask pour qu'elle génère de la donnée propre et instrumentée :
  - Création d'un `request_id` unique (UUID) à chaque requête.
  - Mise en place de compteurs Prometheus pour tracker les codes HTTP (200, 500).
  - Formatage des logs en JSON incluant le `request_id` pour faciliter la recherche.
  Ensuite, je me suis occupé de dockeriser l'app, de préparer les manifestes K8s, et de configurer le déploiement automatisé via AWX.

* **L'Ops (JB) :** 
  Son rôle est de configurer le *Service Discovery* de Prometheus pour venir "aspirer" automatiquement les métriques que j'expose sur mon cluster.

* **L'Analyste (Enzo) :** 
  Il gère la stack Loki/Promtail pour récupérer mes logs JSON, extraire facilement les `request_id`, et permettre de faire des corrélations dans Grafana.

---

## 🏗️ Architecture Technique
- **App :** Python Flask avec l'exportateur Prometheus.
- **Conteneur :** Docker (image légère `python:3.12-slim`).
- **Orchestrateur :** Kubernetes (K3s) sur une VM Ubuntu.
- **Automatisation :** Ansible via AWX, avec un *Execution Environment* (EE) sur mesure.
- **Réseau :** Service K8s exposé en **NodePort** sur le port public **31000**.

---

## 📂 Structure du Repo

```text
coco-bd-ynov-devops-010/
├── app.py                # L'app Flask (génère les logs JSON + métriques)
├── Dockerfile            # Pour build l'image de l'app
├── requirements.txt      # Dépendances Python
├── k8s-flask.yml         # Manifestes Kubernetes (Deployment & Service)
├── ansible/
│   └── app.yml           # Le playbook de déploiement lu par AWX
└── ee/                   # L'environnement d'exécution pour AWX
    ├── Dockerfile        # Image custom pour AWX
    └── requirements.yml  # Dépendances Ansible (ex: community.docker)
```

### Le flux AWX
Plutôt que d'exécuter Ansible localement, le cycle de vie est géré par l'interface AWX. Celui-ci synchronise ce dépôt Git et utilise l'image construite à partir du dossier `ee/` (l'Execution Environment) contenant toutes les dépendances Python et Kubernetes nécessaires pour communiquer de manière sécurisée avec le cluster K3s.

### 🚀 Utilisation de la Web App
L'application est accessible directement via l'adresse IP publique du VPS sur le port configuré :

**WEBAPP URL :** `http://57.128.51.49:31000/`
**AWX URL :** `http://57.128.51.49:31358/`

Pour tester le bon fonctionnement et la production des données, 4 endpoints sont disponibles :

* `GET /` : Page d'accueil classique avec les infos de l'app.
* `GET /ok` : Simule un succès (HTTP 200) -> incrémente le compteur Prometheus et génère un log JSON.
* `GET /error` : Simule une panne (HTTP 500) -> incrémente le compteur d'erreur et génère un log JSON.
* `GET /metrics` : L'endpoint brut où Prometheus vient scraper les données.

PS : L'utilisation de AWX ici n'est pas specialement necessaire car on fait tout sur du localhost. Neanmoins, c'est une techno que je voulais decouvrir, et qui a un interet particulier en entreprise. AWX facilite le travail des equipes DevOps en centralisant l'automatisation et le suivi des deploiements. En effet, il permet de stocker de maniere sécurisée les credentials (ex: login/mdp des serveurs), de gérer les droits (qui peut lancer quel playbook), et d'avoir un historique clair des actions menées sur l'infrastructure. On peut aussi mettre en place des alertes et des notifications pour être informé en temps réel des problèmes rencontrés.