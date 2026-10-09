#!/usr/bin/env python3
"""XSD validation against pinned third-party copies of OMG BPMN and Open Group ArchiMate schemas.

Fail-closed: a failed fetch or XSD validation fails this script. Downloads only XSDs,
no client data or OT access. Do not confuse XSD validation with import into an editor.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen, Request
from urllib.error import URLError
import hashlib
import sys

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
BPMN_SHA = "f35959afc443444b706a4f39542530134233db07"
ARCHI_SHA = "91bb0754f38ea31bf8053e5281569f0e1bf9d3b6"
BPMN_BASE = f"https://raw.githubusercontent.com/bpmn-io/bpmn-moddle/{BPMN_SHA}/resources/bpmn/xsd"
ARCHI_BASE = f"https://raw.githubusercontent.com/ISAITB/validator-resources-eira/{ARCHI_SHA}/resources/common/xsds/3.1"

MANIFEST = {
    "bpmn/BPMN20.xsd": f"{BPMN_BASE}/BPMN20.xsd",
    "bpmn/BPMNDI.xsd": f"{BPMN_BASE}/BPMNDI.xsd",
    "bpmn/DC.xsd": f"{BPMN_BASE}/DC.xsd",
    "bpmn/DI.xsd": f"{BPMN_BASE}/DI.xsd",
    "bpmn/Semantic.xsd": f"{BPMN_BASE}/Semantic.xsd",
    "archimate/archimate3_Model.xsd": f"{ARCHI_BASE}/archimate3_Model.xsd",
    "archimate/xml.xsd": "https://www.w3.org/2001/xml.xsd",
}

class OfflineSchemaResolver(etree.Resolver):
    def __init__(self, xml_schema: Path):
        super().__init__()
        self.xml_schema = xml_schema

    def resolve(self, url, pubid, context):
        if url in {"http://www.w3.org/2001/xml.xsd", "https://www.w3.org/2001/xml.xsd"}:
            return self.resolve_filename(str(self.xml_schema), context)
        return None

def retrieve_schema(url, target):
    request = Request(url, headers={"User-Agent": "MayaBank-Energy-Grid-XSD-Validation/1.0"})
    with urlopen(request, timeout=45) as stream:
        data = stream.read()
    if len(data) < 100 or b"<" not in data[:100]:
        raise RuntimeError(f"not an XSD payload from {url}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(f"SCHEMA_SOURCE={url} SHA256={hashlib.sha256(data).hexdigest()}")

def check(model, schema_file, parser):
    schema_doc = etree.parse(str(schema_file), parser=parser)
    schema = etree.XMLSchema(schema_doc)
    target_doc = etree.parse(str(ROOT / model), parser=parser)
    if not schema.validate(target_doc):
        raise ValueError(f"{model}: " + "; ".join(str(error) for error in schema.error_log))
    print(f"XSD_VALIDATION=PASS MODEL={model} SCHEMA={schema_file.name}")

def main():
    with TemporaryDirectory(prefix="energy-grid-xsd-") as temp:
        temp_dir = Path(temp)
        for file, url in MANIFEST.items():
            retrieve_schema(url, temp_dir / file)
        parser = etree.XMLParser(no_network=True, resolve_entities=False)
        parser.resolvers.add(OfflineSchemaResolver(temp_dir / "archimate/xml.xsd"))
        check("models/incident-lifecycle.bpmn", temp_dir / "bpmn/BPMN20.xsd", parser)
        check("models/energy-grid-archimate.xml", temp_dir / "archimate/archimate3_Model.xsd", parser)
    print("XSD_GATE=PASS BPMN_OMG_MIRROR=PASS ARCHIMATE_3_1_MIRROR=PASS")

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, URLError, etree.XMLSyntaxError, etree.XMLSchemaParseError) as exc:
        print(f"XSD_GATE=FAIL ERROR={exc}", file=sys.stderr)
        sys.exit(1)
