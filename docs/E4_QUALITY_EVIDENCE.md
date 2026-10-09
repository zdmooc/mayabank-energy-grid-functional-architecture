# E4 — Plan de revue qualité et preuves
**Statut : REVIEW_PLAN_READY / EXTERNAL_VALIDATION_PENDING.** Ne pas marquer E4 CLOSED par la seule création documentaire.

## Contrôles de cohérence à exécuter
- Vérifier les liens README et les 6 lignes FR-01…FR-06 de traçabilité ; confirmer chaque capacité/app/data dans E1/E2.
- Rendre les deux diagrammes Mermaid et vérifier erreurs et labels avec un renderer externe.
- Transcrire le processus E2 en BPMN 2.0 XML, valider XSD et import via bpmn.io/Camunda Modeler ; contrôler lanes, flux, gateways, conditions et end events.
- Construire des vues ArchiMate dans un outil compatible et vérifier l'export Open Group ArchiMate Exchange ; ne pas revendiquer de validation avant import réussi.
- Vérifier le modèle conceptuel avec un outil de modélisation et un expert métier industriel.
- Cas de non-régression contractuels : event dupliqué, event tardif, données obsolètes, absence d'approbation, indisponibilité Kafka, échec de replay, work order idempotent, audit incomplet.
- Faire relire dossier E3 par un Architecture Board simulé ; noter objections, arbitrages, risques résiduels.
- Revoir références publiques et limites de leur applicabilité au client.

## Définitions de statut
E1–E3 : DOCUMENTED_SYNTHETIC, **aucune exécution, import, homol­ogation ou validation client**.
E4 : OPEN tant que les contrôles ne sont pas matérialisés par preuves (outil, version, date, résultat, artefact, commit).
