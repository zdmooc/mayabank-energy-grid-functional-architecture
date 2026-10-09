# E2 — Processus BPMN, séquences UML et données
Statut : DOCUMENTED_SYNTHETIC / MODEL_IMPORT_NOT_TESTED.

## Processus métier (spécification BPMN 2.0)
Pool : **Exploitation réseau**. Lanes : Supervision ; Analyse ; Opérateur autorisé ; Coordination terrain.
- **Start message** : observation reçue
- T1 contrôler provenance/qualité ; **gateway exclusive G1** donnée recevable ?
- Si non : consigner anomalie et clôturer la branche
- Si oui : T2 corréler / qualifier ; T3 évaluer impact ; **gateway exclusive G2** intervention requise ?
- Si non : observation, suivi et clôture documentée
- Si oui : T4 requérir décision humaine ; **gateway G3** autorisée ?
- Si non : escalade vers responsable ; aucune action OT
- Si oui : T5 créer ordre d'intervention ; T6 recevoir compte rendu ; T7 valider restauration du service par source autorisée ; T8 clôturer et publier bilan ; **end event**
- Timer non interruptif : revue de dossier si l'attente terrain dépasse le SLA *hypothétique* ; pas d'automatisation de conduite.
- Idempotence à l'entrée par `source_event_id`, déduplication de décisions et ordres par `incident_id + action_type`.

## Séquence UML (Mermaid, illustratrice)
Voir [modèle](../models/incident-sequence.mmd). Elle démontre réception, déduplication, synchronisation données et publication asynchrone.

## MCD logique
| Entité | Identifiant | Attributs principaux | Relations |
|---|---|---|---|
| Observation | observation_id | source_event_id, observed_at, received_at, quality_code | n→1 incident facultatif |
| NetworkAsset | asset_id | asset_type, topology_version, status_as_reported | n↔n incident |
| Incident | incident_id | detected_at, status, severity, version | 1→n observations/assessments |
| ImpactAssessment | assessment_id | snapshot_version, evaluated_at, confidence | n→1 incident |
| HumanDecision | decision_id | incident_id, actor_role, approved_at, rationale | n→1 incident |
| WorkOrder | work_order_id | incident_id, assigned_at, status | n→1 incident |
| AuditEntry | audit_id | subject_id, action, actor, timestamp | append-only |

Contraintes : `source_event_id` unique par source ; les horodatages incluent une timezone UTC normalisée ; contrôle optimiste `incident.version` ; traçabilité complète sur incident/work order ; conservation à définir selon politique client.

## Contrats d'intégration (fictifs)
- `POST /v1/incidents` : `{sourceEventId, observedAt, assetRef, qualityCode, correlationId}` → `202 {incidentId, status}` ou `409` si conflit sémantique.
- `POST /v1/incidents/{id}/assessments` : évaluation calculée, snapshot versionnée.
- `POST /v1/incidents/{id}/decisions` : rôle habilité, motif, trace ; jamais de commande réseau.
- `POST /v1/work-orders` : `idempotencyKey`, incident, objectif ; décision humaine validée obligatoire.
- Event `IncidentQualified.v1` : `eventId, incidentId, occurredAt, correlationId, schemaVersion`.
- Event `WorkOrderClosed.v1` : `eventId, workOrderId, incidentId, outcome, occurredAt`.

## Exigences NFR
Disponibilité à définir ; résilience au replay, back-pressure Kafka, DLQ/quarantaine, chiffrement en transit et au repos, RBAC par privilège minimum, audit immuable logique, RPO/RTO à négocier, gestion de l'obsolescence des snapshots et opérabilité. Aucun chiffre de latence garanti sans banc d'essai.
