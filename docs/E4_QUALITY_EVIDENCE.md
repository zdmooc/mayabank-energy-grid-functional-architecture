# E4 — Revue qualité, gates et registre de preuves

**Date :** 2026-10-09  
**Statut :** `E4_AUTOMATED_SYNTHETIC_GATE_CLOSED / EXTERNAL_IMPORT_AND_INDUSTRIAL_REVIEW_OPEN`  
**Frontière :** étude pédagogique fictive d'architecture fonctionnelle. Pas d'approbation Enedis, pas de systèmes réels, aucune commande OT ni preuve de comportement industriel.

## E4-A — Modélisations produites

| Artefact | Format | Contenu | Vérification disponible |
|---|---|---|---|
| [incident-lifecycle.bpmn](../models/incident-lifecycle.bpmn) | BPMN 2.0 XML + DI | 19 flow nodes, 18 sequence flows, 4 lanes logiques ; exceptions et fins distinctes | XML bien formé, références des flux/nodes, gateways à 2 sorties, DI, atteignabilité et couverture lanes via tests CI |
| [energy-grid-archimate.xml](../models/energy-grid-archimate.xml) | ArchiMate Model Exchange XML 3.1 | 21 éléments métier/applicatif/data/capacités, 22 relations | XML bien formé, unicité identifiants et endpoints via tests CI |
| [incident-sequence.mmd](../models/incident-sequence.mmd) | Mermaid sequence UML-inspired | corrélation, impact, décision humaine, ordre de travail | présence statique + revue du contenu |
| [incident-domain-class.mmd](../models/incident-domain-class.mmd) | Mermaid class UML-inspired | 7 entités conceptuelles / cardinalités illustratives | présence statique des entités |
| [TRACEABILITY.csv](TRACEABILITY.csv) | CSV | FR-01…FR-06 → capacités/processus/applications/données/critères | unicité, couverture noms application/data et critères non vides |

**Important :** la conformité au schéma XSD officiel (OMG BPMN20.xsd / The Open Group ArchiMate 3.1), le rendu graphique Mermaid et l'import dans un outil BPMN ou ArchiMate **ne sont pas démontrés** par ces contrôles Python. Les lanes sont définies sémantiquement en XML, sans BPMN DI de couloirs certifiée.

## E4-B — Tests d'invariants et CI

- Référence synthétique `reference/incident_contract.py`, **in-memory**, sans intégration SCADA, Kafka ni réseau.
- Contrôles négatifs : source manquante, qualité rejetée, doublon, rôle non habilité, topologie obsolète, ordre sans décision, seconde commande d'ordre, clôture sans confirmation de restauration.
- Contrôles positifs : replay idempotent de création d'ordre et audit de la clôture.
- Tests : `python -m unittest discover -s tests -v` ; `python -m compileall -q reference tests` en CI.
- **Preuve GitHub CI confirmée :** [run 37980944735](https://github.com/zdmooc/mayabank-energy-grid-functional-architecture/actions/runs/37980944735) — `SUCCESS`, commit `6aff9c2716b7daf351facb552d11ec0f5fa38a34`, **12 tests, OK** ; contient modèle XML, lanes, ArchiMate, class UML et contrôles testés à cet état.

## Revue d'architecture simulée

La [soutenance E4](E4_ARCHITECTURE_BOARD_REHEARSAL.md) formalise sept objections : sécurité OT/IT, déduplication, snapshot, habilitations, Kafka, résilience et import modèles. Option B (services bornés, workflow humain, bus d'événements) reste **orientation fictive**, non arbitrage client.

## Gates externes non bloquants pour la clôture du portfolio

| Gate | Responsable externe / contexte | Statut |
|---|---|---|
| XSD OMG + import BPMN Camunda Modeler / bpmn.io | outil compatible, preuve d'import + version | PENDING |
| XSD The Open Group + import Archi (ou outil compatible) | outil compatible, preuve d'import + version | PENDING |
| Rendu Mermaid et revue visuelle de diagrammes | moteur Mermaid/éditeur | PENDING |
| Revue métier énergétique, sécurité/sûreté et interactions OT | expert métier habilité, équipe OT/architecture | PENDING |
| Validation Architecture Board et paramétrage SLA/SLO/RTO/RPO | client réel / mandat | NOT CLAIMED |
| Essais CI/CD de véritables API/services et Kafka sur runtime | projet ultérieur explicitement autorisé | OUT_OF_SCOPE |

## Conclusion et labels

Le périmètre **portfolio automatisé synthétique** est clôturable dès que le dernier commit `main` a sa CI verte. Les contrôles CI sont des **tests de structure de modèles et de contrats in-memory**, pas une certification BPMN/ArchiMate ou un POC industriel. Toute affirmation de validation métier externe exige sa propre preuve nominative/datée.

Références normatives : [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2) ; [The Open Group — ArchiMate Exchange File Format](https://www.opengroup.org/open-group-archimate-model-exchange-file-format).
