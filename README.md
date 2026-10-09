# MayaBank Energy Grid — Functional Architecture Reference

**Statut :** CASE_STUDY / E1-E3_DOCUMENTED / E4_STATIC_GATES_IMPLEMENTED / SYNTHETIC_ONLY / NO_INDUSTRIAL_VALIDATION  
**Date :** 2026-10-09 · **Domaine :** conduite du réseau public de distribution HTA/BT, qualification d'incident, intervention et rétablissement.

## Objectif
Portefeuille démonstratif pour mission d'architecte fonctionnel à Courbevoie : relier exigences et capacités métier, bounded contexts DDD, processus BPMN 2.0, séquences UML, données, contrats d'intégration, vues ArchiMate, dossier de choix et preuves vérifiables.

**Limites impératives :** modèle fictif et données synthétiques. Aucun schéma interne Enedis, aucun accès SCADA, aucune automatisation de manœuvre électrique, aucun claim production ou temps réel garanti. Toute opération de conduite reste sous contrôle d'opérateurs habilités et des systèmes OT autorisés. Les intitulés industriels publics ne valent pas validation métier du client.

## Parcours
- [E1 — capacités, frontières DDD, contexte](docs/E1_BUSINESS_FUNCTIONAL_MODEL.md)
- [E2 — BPMN, UML, données et intégration](docs/E2_PROCESS_DATA_INTEGRATION.md)
- [E3 — dossier de choix et trajectoire](docs/E3_ARCHITECTURE_DECISION.md)
- [E4 — revue et matrice de preuves](docs/E4_QUALITY_EVIDENCE.md)
- [E4 — soutenance Architecture Board simulée](docs/E4_ARCHITECTURE_BOARD_REHEARSAL.md)
- [BPMN 2.0 XML](models/incident-lifecycle.bpmn), [ArchiMate Exchange XML](models/energy-grid-archimate.xml), [UML séquence](models/incident-sequence.mmd) et [modèle conceptuel](models/incident-domain-class.mmd)
- [CI GitHub Actions](.github/workflows/architecture-validation.yml) et [tests de non-régression](tests/test_architecture.py)
- [Décisions](docs/ADR-001-BOUNDARIES.md), [registre de traçabilité](docs/TRACEABILITY.csv), [modèles Mermaid](models/incident-sequence.mmd)

## Réutilisation sans duplication
Méthode d'urbanisation et BPMN : `hopex-aquila-enterprise-architecture-masterbook`; patterns d'exigences Soluxan : `mayabank-customer-identity-kyc-digital-banking-architecture`; Kafka/DDD : `mayabank-kafka-ddd-openshift`. Aucun impact sur D-091/D-099/D-100 ni le runtime CRC.

## Definition of Done
Le périmètre **portfolio synthétique E4** est atteint seulement avec CI GitHub Actions verte sur le commit concerné : XML bien formé, cohérence des identifiants/gateways/lanes/flux/DI, traçabilité FR, tests négatifs du modèle contractuel mémoire et revue contradictoire **simulée**. Les fichiers XML sont des **candidats à l'import** et non une preuve d'import ni de conformité XSD officielle. Les imports BPMN/ArchiMate avec outils externes, XSD officiels, revue métier/OT et validation client sont des gates distincts toujours ouverts. Aucun runtime industriel, réseau réel ni Enedis interne.


## Test automatisé (sans dépendances tierces)
```sh
python -m unittest discover -s tests -v
```
La CI exécute ces tests et `compileall` ; les scénarios Python sont des contrats **in-memory**, pas des simulateurs de protection, SCADA ou télécommande.
