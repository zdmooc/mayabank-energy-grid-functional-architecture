# E3 — Dossier de choix d'architecture, trajectoire, gouvernance
Statut : REFERENCE_DECISION / NOT_CLIENT_APPROVED.

## Problème et exigences
Unifier la qualification d'incidents issus de signaux hétérogènes, exposer un dossier métier cohérent et sécuriser la coordination humaine/terrain sans intégrer de commandes au système OT. Traçabilité [CSV](TRACEABILITY.csv).

## Scénarios
| Option | Principe | Avantages | Risques |
|---|---|---|---|
| A | Application centrale et appels synchrones | Simplicité initiale | Couplage, charge, SPOF |
| B | Services délimités, bus événementiel, contrôle humain | Autonomie métier, replay contrôlé, audit | Gouvernance schémas, observabilité, consistance éventuelle |
| C | Plateforme OT directement couplée à chaque système métier | Accès direct supposé | Frontières de confiance fragiles, dépendance au fournisseur OT |

**Orientation de référence : B**, sous réserve d'audit du SI existant, exigences de sûreté de fonctionnement, politiques cybersécurité et coût global réel. Ce n'est pas un arbitrage d'Enedis.

## Trajectoire incrémentale
1. M0 cartographier capacités, applications, flux, contrats, propriétaires de données, homologations OT.
2. M1 mettre en place une façade d'observation **read-only** sur données synthétiques puis valider sémantique/provenance.
3. M2 brancher IncidentManagement et ImpactAssessment, tester rejouabilité et doublons.
4. M3 introduire processus de décision humaine + FieldWork, audit et scénarios négatifs.
5. M4 migrer les consommateurs, observer KPIs et définir rollback, sans coupure des applications existantes.

## Architecture Board : décisions demandées
- Validation des capacités et ownership métier ;
- qualification de la frontière OT/IT et des autorisations ;
- arbitrage B vs A avec coûts, risques et contraintes de conformité ;
- seuils de performance/résilience réels et modalités de preuve ;
- responsable de chaque risque et critères Go/No-Go.

## Risques et parades
R1 signaux ambigus → provenance, qualité, quarantaine ; R2 double intervention → idempotency key ; R3 incohérence topologique → snapshot versionné ; R4 indisponibilité du bus → outbox + replay sous contrôle ; R5 escalade non traitée → SLA d'alerte à définir ; R6 confusion preuve démonstration / production → étiquettes explicites.
