"""E4 — structural/model gates and bounded synthetic behavioral contracts."""
from pathlib import Path
import csv
import unittest
import xml.etree.ElementTree as ET
from reference.incident_contract import IncidentLedger, ContractViolation

ROOT = Path(__file__).resolve().parents[1]
BPMN = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
BPMNDI = "{http://www.omg.org/spec/BPMN/20100524/DI}"
AM = "{http://www.opengroup.org/xsd/archimate/3.0/}"

class ModelGates(unittest.TestCase):
    def test_bpmn_flow_graph_and_di(self):
        doc = ET.parse(ROOT / "models/incident-lifecycle.bpmn").getroot()
        process = doc.find(BPMN + "process")
        self.assertIsNotNone(process)
        self.assertEqual(process.attrib["isExecutable"], "false")
        kinds = {"task", "startEvent", "endEvent", "exclusiveGateway"}
        nodes = {n.get("id"): n for n in process if n.tag.split("}")[-1] in kinds}
        flows = list(process.findall(BPMN + "sequenceFlow"))
        self.assertGreaterEqual(len(nodes), 15)
        self.assertGreaterEqual(len(flows), 15)
        self.assertEqual(len(nodes), len(set(nodes)))
        for f in flows:
            self.assertIn(f.get("sourceRef"), nodes)
            self.assertIn(f.get("targetRef"), nodes)
        outgoing = {name: set() for name in nodes}
        incoming = {name: set() for name in nodes}
        for f in flows:
            outgoing[f.get("sourceRef")].add(f.get("id"))
            incoming[f.get("targetRef")].add(f.get("id"))
        for name, n in nodes.items():
            self.assertEqual(set(x.text for x in n.findall(BPMN + "outgoing")), outgoing[name], name)
            self.assertEqual(set(x.text for x in n.findall(BPMN + "incoming")), incoming[name], name)
            if n.tag == BPMN + "exclusiveGateway":
                self.assertEqual(len(outgoing[name]), 2)
        shapes = {n.get("bpmnElement") for n in doc.iter(BPMNDI + "BPMNShape")}
        edges = {n.get("bpmnElement") for n in doc.iter(BPMNDI + "BPMNEdge")}
        self.assertEqual(shapes, set(nodes))
        self.assertEqual(edges, {f.get("id") for f in flows})
        self.assertEqual(len([n for n in nodes.values() if n.tag == BPMN + "startEvent"]), 1)
        self.assertGreaterEqual(len([n for n in nodes.values() if n.tag == BPMN + "endEvent"]), 3)
        start = next(name for name,n in nodes.items() if n.tag == BPMN + "startEvent")
        reachable = {start}
        change = True
        while change:
            before = len(reachable)
            reachable |= {f.get("targetRef") for f in flows if f.get("sourceRef") in reachable}
            change = len(reachable) > before
        self.assertEqual(reachable, set(nodes), "unreachable BPMN node")

    def test_archimate_identifiers_and_relationships(self):
        root = ET.parse(ROOT / "models/energy-grid-archimate.xml").getroot()
        self.assertEqual(root.tag, AM + "model")
        self.assertEqual(root.get("version"), "3.1")
        elements = root.findall(".//" + AM + "element")
        relationships = root.findall(".//" + AM + "relationship")
        names = {n.get("identifier") for n in elements}
        self.assertEqual(len(names), len(elements))
        self.assertGreaterEqual(len(elements), 15)
        self.assertGreaterEqual(len(relationships), 15)
        self.assertTrue(any(n.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "Capability" for n in elements))
        for rel in relationships:
            self.assertIn(rel.get("source"), names)
            self.assertIn(rel.get("target"), names)

    def test_requirements_trace_to_docs(self):
        with (ROOT / "docs/TRACEABILITY.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["Requirement"] for row in rows], [f"FR-{i:02d}" for i in range(1, 7)])
        architecture = (ROOT / "docs/E1_BUSINESS_FUNCTIONAL_MODEL.md").read_text(encoding="utf-8")
        data = (ROOT / "docs/E2_PROCESS_DATA_INTEGRATION.md").read_text(encoding="utf-8")
        for row in rows:
            self.assertIn(row["Application"], architecture)
            self.assertIn(row["Data"], data)
            self.assertTrue(row["AcceptanceCriteria"])
        self.assertIn("sequenceDiagram", (ROOT / "models/incident-sequence.mmd").read_text(encoding="utf-8"))
        self.assertIn("flowchart", (ROOT / "models/ARCHIMATE_README.md").read_text(encoding="utf-8"))

class ContractCases(unittest.TestCase):
    def setUp(self):
        self.l = IncidentLedger()

    def test_missing_origin_rejected(self):
        with self.assertRaises(ContractViolation):
            self.l.observe("", "event-1", "topology-v1")

    def test_quality_rejected(self):
        with self.assertRaises(ContractViolation):
            self.l.observe("read-only-adapter", "event-1", "topology-v1", "INVALID")

    def test_duplicate_event_is_idempotent(self):
        one = self.l.observe("observation", "evt1", "v1")
        two = self.l.observe("observation", "evt1", "v1")
        self.assertIs(one, two)
        self.assertEqual(len(self.l.incidents), 1)

    def test_reject_unauthorized_role(self):
        item = self.l.observe("observation", "evt1", "v1")
        with self.assertRaises(ContractViolation):
            self.l.authorize_intervention(item.incident_id, "OBSERVER", "v1")

    def test_reject_stale_topology(self):
        item = self.l.observe("observation", "evt1", "v2")
        with self.assertRaises(ContractViolation):
            self.l.authorize_intervention(item.incident_id, "OPERATOR_AUTHORIZED", "v1")

    def test_workorder_requires_approval(self):
        item = self.l.observe("observation", "evt1", "v1")
        with self.assertRaises(ContractViolation):
            self.l.request_work_order(item.incident_id, "retry-1")

    def test_workorder_idempotency(self):
        item = self.l.observe("observation", "evt1", "v1")
        self.l.authorize_intervention(item.incident_id, "OPERATOR_AUTHORIZED", "v1")
        a = self.l.request_work_order(item.incident_id, "retry-1")
        b = self.l.request_work_order(item.incident_id, "retry-1")
        self.assertEqual(a, b)
        self.assertEqual(item.audit.count("WORK_ORDER_CREATED"), 1)

    def test_prevent_second_workorder_with_distinct_key(self):
        item = self.l.observe("observation", "evt1", "v1")
        self.l.authorize_intervention(item.incident_id, "OPERATOR_AUTHORIZED", "v1")
        self.l.request_work_order(item.incident_id, "retry-1")
        with self.assertRaises(ContractViolation):
            self.l.request_work_order(item.incident_id, "retry-2")

    def test_restoration_required_and_audited(self):
        item = self.l.observe("observation", "evt1", "v1")
        self.l.authorize_intervention(item.incident_id, "OPERATOR_AUTHORIZED", "v1")
        self.l.request_work_order(item.incident_id, "retry-1")
        with self.assertRaises(ContractViolation):
            self.l.close_after_restoration(item.incident_id, False)
        closed = self.l.close_after_restoration(item.incident_id, True)
        self.assertEqual(closed.status, "CLOSED")
        self.assertIn("HUMAN_APPROVAL", closed.audit)
        self.assertIn("INCIDENT_CLOSED", closed.audit)

if __name__ == "__main__":
    unittest.main()
