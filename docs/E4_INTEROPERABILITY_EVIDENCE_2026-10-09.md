# E4+ — Preuves d'interopérabilité et de rendu (2026-10-09)

**Statut :** `XSD_MIRRORED_SCHEMAS_PASS / BPMN_MODDLE_IMPORT_ROUNDTRIP_PASS / MERMAID_SVG_PASS`  
**Résultat GitHub Actions :** [Energy Grid Interoperability Validation — run 37982045352](https://github.com/zdmooc/mayabank-energy-grid-functional-architecture/actions/runs/37982045352) — **3 jobs SUCCESS** au commit `42813108a9b600d6c79655df125b7ed66e344050`.

## Gates effectivement vérifiés

| Gate | Technologie / entrée | Résultat CI | Frontière exacte |
|---|---|---|---|
| XML Schema BPMN | lxml sur BPMN20.xsd + BPMNDI.xsd/DC.xsd/DI.xsd/Semantic.xsd ; version du référentiel bpmn-io verrouillée | **PASS** | validation XSD d'une copie tierce du schéma OMG, pas une certification OMG |
| XML Schema ArchiMate | lxml sur archimate3_Model.xsd 3.1, référentiel ISA ITB verrouillé + xml.xsd du W3C | **PASS** | structure Exchange Model, sans vue graphique native ; pas d'import dans Archi |
| Import modèle BPMN programmatique | bpmn-moddle@10.2.0, lecture `fromXML`, réécriture `toXML`, relecture et vérification warnings | **PASS** | importer/parsing en Node, pas Camunda Modeler ni bpmn.io GUI |
| Rendu Mermaid séquence | @mermaid-js/mermaid-cli@11.17.0 → SVG | **PASS** | visualisation Mermaid, pas UML formel certifié |
| Rendu Mermaid classes | @mermaid-js/mermaid-cli@11.17.0 → SVG | **PASS** | modèle de classes conceptuel illustratif |
| Rendu vue ArchiMate pédagogique | extraction Mermaid du guide → SVG | **PASS** | illustration et non diagramme ArchiMate issu d'un outil certifié |

**Artefacts de l'exécution :**
- `bpmn-moddle-roundtrip` : BPMN XML normalisé issu de l'import/réexport programmatique ;
- `mermaid-rendered-svg` : `incident-sequence.svg`, `incident-domain-class.svg`, `archimate-conceptual-view.svg`.

Ces fichiers sont disponibles dans les artefacts de la page du workflow GitHub. Ils ne sont pas enregistrés comme fichiers source dans le dépôt.

## Sources de validation et reproductibilité
- BPMN (OMG 2.0.2) : [machine-readable specification](https://www.omg.org/spec/BPMN/machine-readable) ; copie [bpmn-moddle](https://github.com/bpmn-io/bpmn-moddle/tree/f35959afc443444b706a4f39542530134233db07/resources/bpmn/xsd).
- ArchiMate 3.1 Exchange : [The Open Group](https://www.opengroup.org/xsd/archimate/) ; copie [ISAITB validator-resources-eira](https://github.com/ISAITB/validator-resources-eira/blob/91bb0754f38ea31bf8053e5281569f0e1bf9d3b6/resources/common/xsds/3.1/archimate3_Model.xsd).
- Le script `tools/validate_external_schemas.py` épingle les deux commits et imprime SHA-256 des XSD récupérés ; échec fermé en cas d'échec du téléchargement ou du contrôle.
- La CI `.github/workflows/interoperability-validation.yml` est déclenchée sur push / PR / manuel.

## Correction prouvée pendant la revue
Première exécution [37981938795](https://github.com/zdmooc/mayabank-energy-grid-functional-architecture/actions/runs/37981938795) : XSD et bpmn-moddle SUCCESS ; rendu Mermaid FAILED en raison d'un point-virgule interprété comme un séparateur dans `incident-sequence.mmd`. Correction du libellé au commit `42813108` et **rejeu complet PASS**. Le défaut est résolu par preuve de rendu réel, pas par une supposition.

## Gates qui restent EXTERNES / OPEN
- Import visuel du fichier BPMN dans bpmn.io/Camunda Modeler (et vérification disposition/rendu des lanes) : **NOT_EXECUTED**.
- Import ArchiMate dans Archi (outil GUI) et réalisation d'un diagramme Exchange View/Diagram natif : **NOT_EXECUTED**.
- Règles sémantiques de relation ArchiMate/TOGAF, revues par architectes expérimentés : **NOT_VERIFIED_BY_XSD**.
- Revue d'un professionnel de la conduite électrique, validation sûreté/cybersécurité OT, exigences réelles, comité de décision et approbation client : **NOT_EXECUTED**.
- Tests d'intégration sur véritables API, Kafka, SCADA, automatisme, topologie industrielle : **OUT_OF_SCOPE**, aucune production ni temps réel revendiqué.

## Verdict
E4+ est **clos pour les contrôles techniques reproductibles GitHub CI**, avec preuves positives.
Le **portfolio architecture fonctionnelle synthétique est prêt pour démonstration** ; les validations industrielles restent distinctes et ne sauraient être considérées fermées sans autorité compétente.
