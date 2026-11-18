from patient import create_patient_resource
from coverage_resource import create_organization_resource, create_coverage_resource
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir, search_patient_by_document

if __name__ == "__main__":
    dni = "44642149"  

    # 3.a Crear el paciente con DNI y leerlo
    patient = create_patient_resource("Mastantuono", "Franco", "2007-08-14", "male", None, dni)
    patient_id = send_resource_to_hapi_fhir(patient, 'Patient')
    if patient_id:
        get_resource_from_hapi_fhir(patient_id, 'Patient')

        # 3.b Buscar por documento y comprobar que aparece el creado
        encontrados = search_patient_by_document(dni)
        print("¿Está el paciente creado?", any(p["id"] == patient_id for p in encontrados))

        # 3.c Coverage (Grupo 3): primero la Organization (obra social), después la Coverage
        org = create_organization_resource("Obra Social River Plate")
        org_id = send_resource_to_hapi_fhir(org, 'Organization')
        if org_id:
            coverage = create_coverage_resource(
                patient_id, org_id, subscriber_id="91218",
                plan_name="El Mas Grande", start_date="2018-12-09")
            coverage_id = send_resource_to_hapi_fhir(coverage, 'Coverage')
            if coverage_id:
                get_resource_from_hapi_fhir(coverage_id, 'Coverage')
