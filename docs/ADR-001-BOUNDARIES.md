# ADR-001 — Séparer l'observation réseau, la décision humaine et les interventions
**État :** ACCEPTED_FOR_SYNTHETIC_REFERENCE (not client approved) — 2026-10-09

## Contexte
La chaîne métier doit être compréhensible, résiliente au rejeu et auditable sans inventer le fonctionnement interne des systèmes de conduite d'un exploitant.

## Décision
Maintenir l'interface OT en lecture seule ; isoler Observation, Incident, Impact, Decision et FieldWork ; requérir validation par un opérateur habilité avant toute intervention ; publier des événements via outbox transactionnelle et des consommateurs idempotents ; aucune télécommande OT n'est exposée.

## Alternatives
- Couplage synchrone monolithique : facile à tracer au départ, faible découplage et résilience.
- Tout événementiel sans contrôle humain : interdiction dans ce scénario pour la conduite et les actions sensibles.
- Événementiel borné + workflow humain (**retenu comme référence**) : compromis découplage, audit, coût opérationnel.

## Conséquences
Gestion des versions de schémas, corrélation, sémantique d'au-moins-une-fois, reconciliation, cas de DLQ et procédures de reprise nécessaires. Une analyse de sécurité OT indépendante est obligatoire pour un véritable projet.
