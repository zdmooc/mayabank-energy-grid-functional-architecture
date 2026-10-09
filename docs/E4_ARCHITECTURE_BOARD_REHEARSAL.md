# E4 — Dossier de soutenance Architecture Board (simulation)

**Contexte** : candidat architecte fonctionnel SI, étude de cas fictive d'un gestionnaire de réseau électrique. **Aucun accès aux applications d'Enedis**. Les données, interfaces, rôles et hypothèses sont de démonstration.

## Trame 10 minutes
| Durée | Sujet | Livrables |
|---|---|---|
| 0–1 min | Demande métier et limites du périmètre | README |
| 1–3 min | Capacités, domaines, frontières OT/IT et ownership | E1, ArchiMate XML |
| 3–5 min | BPMN incident, branches d'exception, rôles et MCD | E2, BPMN XML |
| 5–7 min | API/événements, idempotence, absence de commande OT | E2, séquence UML |
| 7–9 min | Alternatives A/B/C, risques, stratégie progressive | E3, ADR |
| 9–10 min | Tests, état des preuves, points ouverts et décision sollicitée | E4 |

## Revue contradictoire simulée (objections et réponses)
| Objection | Réponse d'architecture | Contrôle |
|---|---|---|
| L'OT peut-il être piloté par une API ? | Non : read-only côté observation, séparation explicite OT/IT et décision humaine | revue d'interface OT + IAM |
| Le même événement peut-il produire deux incidents ? | Clé d'idempotence source/event + déduplication dans contrat synthétique | test duplicate |
| Quelle garantie si la topologie change ? | Évaluation associée à une version ; refuser une décision basée sur snapshot obsolète | test stale topology |
| Une personne non habilitée peut-elle ouvrir un ordre ? | Rejet sans rôle autorisé et décision humaine tracée | tests authorization |
| Kafka est-il une vérité métier ? | Non : état maîtrisé par service métier, événements via outbox puis consommateurs idempotents | preuve à construire pour runtime réel |
| Quelles garanties disponibilité/temps réel ? | Aucune revendiquée ; SLA, RTO, RPO et exigences OT à obtenir en cadrage | gate externe |
| Le format BPMN/ArchiMate est-il importé dans un outil métier ? | XML fourni et topologie contrôlée ; import logiciel non exécuté tant que preuve outillage absente | gate de validation externe |

## Décision simulée (non signée)
- Retenir **B comme option de référence** pour enrichir l'étude ; ne pas passer en delivery industriel.
- Prévoir un atelier de découverte SI et un examen sécurité OT avant tout raccordement.
- Prévoir import BPMN/ArchiMate, vérification d'un architecte fonctionnel/OT, chiffrage et validation de l'autorité compétente.
- Ne déclarer aucun avis positif de comité client ; décision **SIMULATED_ONLY**.

## Frontière preuve
Le succès CI valide uniquement la syntaxe XML et les invariants de graphe/idempotence du simulateur Python. Il ne valide ni XSD OMG/Open Group, ni le rendu Mermaid, ni import BPMN/ArchiMate dans un outil métier, ni sécurité OT, ni vérité métier Enedis, ni disponibilité industrielle.
