from fhir.resources.coverage import Coverage
from fhir.resources.organization import Organization


# Crear la Organization que actúa como aseguradora / obra social (payor)
def create_organization_resource(name):
    return Organization(**{"name": name, "active": True})


# Crear el recurso FHIR Coverage (cobertura de salud del paciente)
def create_coverage_resource(patient_id, payor_id, subscriber_id=None,
                             plan_name=None, start_date=None, end_date=None,
                             status="active"):
    data = {
        "status": status,                                       # obligatorio (1..1)
        "beneficiary": {"reference": f"Patient/{patient_id}"},  # obligatorio: quién recibe la cobertura
        "payor": [{"reference": f"Organization/{payor_id}"}],   # obligatorio: quién paga (obra social)
        "type": {                                               # tipo de cobertura
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "HIP",
                "display": "health insurance plan policy"
            }]
        },
        "relationship": {                                       # relación del beneficiario con el titular
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/subscriber-relationship",
                "code": "self"
            }]
        },
    }

    if subscriber_id:
        data["subscriberId"] = str(subscriber_id)                      # nº de afiliado
        data["subscriber"] = {"reference": f"Patient/{patient_id}"}    # titular
    if plan_name:
        data["class"] = [{
            "type": {"coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
                "code": "plan"
            }]},
            "value": plan_name,
            "name": plan_name
        }]
    if start_date or end_date:
        period = {}
        if start_date:
            period["start"] = start_date
        if end_date:
            period["end"] = end_date
        data["period"] = period

    return Coverage(**data)
