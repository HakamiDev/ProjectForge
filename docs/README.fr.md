<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · **Français** · [Español](README.es.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Македонски](README.mk.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [中文](README.zh.md) · [日本語](README.ja.md)

</p>

**Un système d'exploitation pour une équipe d'agents IA.** Une seule commande transforme un simple dossier en bureau structuré : un tableau unique sur lequel travaillent tous les agents, quelle que soit la plateforme ; une porte qualité indépendante ; une gouvernance des décisions ; une piste d'audit complète ; des indicateurs de performance exportables vers Power BI ; et un site de gestion qui fonctionne à partir d'un seul fichier HTML.

Python 3.9 ou version ultérieure, aucune dépendance, aucun serveur. Open source, sous licence MIT.

Site web : https://hakamidev.github.io/ProjectForge/

## Installation

Une seule ligne, à coller dans un terminal. Elle télécharge l'outil, l'exécute, pose quatre questions, puis ouvre votre site de gestion.

macOS et Linux (Terminal) :

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell) :

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Le site vous permet aussi de choisir d'abord votre plateforme et votre langue préférée ; les deux sont intégrées à la commande d'installation et présélectionnées dans l'assistant.

## Ce que l'outil résout

- **Les conversations oublient.** Les règles et les fiches de rôle résident dans le dossier, et non dans la mémoire des conversations ; n'importe quelle conversation peut donc reprendre le travail.
- **Les agents entrent en collision.** Un tableau numéroté unique ; le statut « en cours » verrouille une ligne ; une garde par somme de contrôle empêche les écritures conflictuelles.
- **Des livrables non vérifiés.** Un responsable de l'assurance qualité statue sur la réussite ou l'échec avant que quoi que ce soit n'atteigne le propriétaire.
- **Des décisions bloquées.** Cinq décisions ouvertes au maximum, et une règle des 48 heures à l'issue de laquelle la recommandation s'applique.
- **Rien n'est mesuré.** `report` fournit le taux de livraison, le délai de traitement, le taux de réussite QA et la charge par rôle ; `export` écrit des fichiers CSV pour Power BI.
- **Aucune responsabilité tracée.** Chaque écriture sur le tableau est consignée : qui, quand et quoi.
- **Des données sensibles dans des outils externes.** Une politique de données contraignante, avec classification et outils approuvés.

## Ce que vous obtenez

- **80 spécialisations** (stratégie, restauration, immobilier, logiciel, RH, éducation et bien d'autres) avec plus de 330 rôles prêts à l'emploi que vous ajoutez en un clic.
- **130 compétences prêtes à l'emploi réparties en 18 groupes.** Une compétence est un court fichier qui décrit quand l'utiliser, ses étapes, son résultat et son critère d'acceptation, afin qu'un employé l'applique au lieu d'improviser.
- **Quatre plateformes :** Claude, ChatGPT, Grok et Gemini. Chaque employé peut travailler sur une plateforme différente.
- **13 langues d'interface** sur le site web et dans l'assistant. La langue préférée est celle de la gestion de l'ensemble du système et celle utilisée avec les employés.
- **Un site de gestion** à partir d'un seul fichier HTML : tableau, équipe, décisions, indicateurs, une bibliothèque de commandes prêtes à l'emploi, et un moteur d'attention qui signale ce qui est en retard ou en attente de votre part.

## Commandes

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Plateformes

| Plateforme | Mise en place de l'équipe |
| --- | --- |
| Claude | Créez un projet portant le nom de votre projet et ajoutez le dossier généré. |
| ChatGPT | Créez un projet et téléversez les fichiers du dossier. |
| Grok | Créez un projet, collez la commande Compass dans ses instructions et ajoutez les fichiers. |
| Gemini | Créez un Gem par employé, collez sa commande dans les instructions et ajoutez les fichiers sous Knowledge. |

Téléversez les fichiers depuis le dossier du projet à son emplacement d'origine, et téléversez de nouveau ce qui change. À notre connaissance, Grok et Gemini n'écrivent pas directement dans le dossier ; déplacez donc vous-même leurs productions dans le dossier. Les étapes suivent la documentation publique au moment de la rédaction ; les interfaces et les limites sont définies par ces plateformes et peuvent évoluer.

## Limites actuelles

- L'assistant et le site web sont disponibles en 13 langues, mais les fichiers générés du projet (règles, fiches de rôle, tableau) et le site de gestion sont pour l'instant rédigés en arabe. Les employés reçoivent la consigne de la langue de travail et vous répondent dans cette langue.
- Les noms de fichiers, les commandes et les termes de statut du tableau restent en arabe, car l'outil les lit littéralement.
- L'installation sous Windows n'a pas encore été testée sur une machine réelle.

## Pour les développeurs

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Le code source se trouve dans `forge/` ; `tools/build-single.py` produit l'outil en fichier unique dans `dist/`. Les modèles sont dans `forge/templates/`, le site public dans `site/`.

## Licence

MIT.
