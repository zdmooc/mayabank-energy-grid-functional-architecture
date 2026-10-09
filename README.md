# MayaBank Energy Grid — Functional Architecture Reference

**Statut :** CASE_STUDY / SYNTHETIC_DESIGN / NOT_ENEDIS_INTERNAL / NO_RUNTIME_CLAIM  
**Date :** 2026-10-09 · **Domaine :** conduite du réseau public de distribution HTA/BT, qualification d'incident, intervention et rétablissement.

## Objectif
Portefeuille démonstratif pour mission d'architecte fonctionnel à Courbevoie : relier exigences et capacités métier, bounded contexts DDD, processus BPMN 2.0, séquences UML, données, contrats d'intégration, vues ArchiMate, dossier de choix et preuves vérifiables.

**Limites impératives :** modèle fictif et données synthétiques. Aucun schéma interne Enedis, aucun accès SCADA, aucune automatisation de manœuvre électrique, aucun claim production ou temps réel garanti. Toute opération de conduite reste sous contrôle d'opérateurs habilités et des systèmes OT autorisés. Les intitulés industriels publics ne valent pas validation métier du client.

## Parcours
- [E1 — capacités, frontières DDD, contexte](docs/E1_BUSINESS_FUNCTIONAL_MODEL.md)
- [E2 — BPMN, UML, données et intégration](docs/E2_PROCESS_DATA_INTEGRATION.md)
- [E3 — dossier de choix et trajectoire](docs/E3_ARCHITECTURE_DECISION.md)
- [E4 — revue et matrice de preuves](docs/E4_QUALITY_EVIDENCE.md)
- [Décisions](docs/ADR-001-BOUNDARIES.md), [registre de traçabilité](docs/TRACEABILITY.csv), [modèles Mermaid](models/incident-sequence.mmd)

## Réutilisation sans duplication
Méthode d'urbanisation et BPMN : `hopex-aquila-enterprise-architecture-masterbook`; patterns d'exigences Soluxan : `mayabank-customer-identity-kyc-digital-banking-architecture`; Kafka/DDD : `mayabank-kafka-ddd-openshift`. Aucun impact sur D-091/D-099/D-100 ni le runtime CRC.

## Definition of Done
Documentation E1–E3 contrôlable dans Git ; E4 à clore uniquement après vérifications externes des modèles (BPMN/ArchiMate/UML, liens, cohérence) et simulation d'Architecture Board. Les supports Mermaid sont des diagrammes textuels, pas un export ArchiMate validé.
