import json
from time import time
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Response, status

from app.repositories.base_unites_legales import unites_legales, periodes_unites_legales
from app.repositories.base_etablissements import etablissements, periodes_etablissements, adresse_etablissements, adresse2_etablissements
from app.repositories.unites_legales_repository import UnitesLegalesRepository, PeriodesUnitesLegalesRepository
from app.repositories.etablissements_repository import EtablissementsRepository, PeriodesEtablissementsRepository, AdresseEtablissementsRepository, Adresse2EtablissementsRepository
from app.responses.unites_legales_response import ( 
    SuccessUnitesLegalesPaginationResponse,
    SuccessUnitesLegalesDetailResponse,
)
from app.responses.etablissements_response import ( 
    SuccessEtablissementsPaginationResponse,
    SuccessEtablissementsDetailResponse,
)

from cassandra.cqlengine.management import sync_table

# Initial Application
app = FastAPI(title="let's gooo")
router = APIRouter()

'''
@app.on_event("startup")
async def startup_event():
    sync_table(unites_legales)
    sync_table(periodes_unites_legales)
'''

# API endpoints
@router.get("/check")
async def health_check():
    response={}
    start_time = time()
    cass_stats=UnitesLegalesRepository().find_one("821398013")
    duration_time_unites_legales = time() - start_time
    start_time = time()
    cass_stats=EtablissementsRepository().find_one("81035280700020")
    duration_time_etablissements = time() - start_time
    return {
        'unites_legales' : duration_time_unites_legales,
        'etablissements' : duration_time_etablissements
    }

@router.get("/unites_legales/{id}", response_model=SuccessUnitesLegalesDetailResponse)
async def unites_legales_detail(id: str):
    unites_legales = UnitesLegalesRepository().find_one(id)
    if unites_legales is not None:
        periodes_unites_legales = PeriodesUnitesLegalesRepository().find_all(id)   

        '''
        print("------------------------------")
        print(unites_legales)
        print(periodes_unites_legales)
        print("------------------------------")
        '''

        unites_legales["periodes_unites_legales"]=periodes_unites_legales
        return {
            'header' : {
                'status': 200,
                'message': 'ok'
            },
            'uniteLegale': unites_legales,
        }
    else:
        return {
            'header' : {
                'status': 404,
                'message': 'Aucun élément trouvé pour le siren ' + id
            }
        }

'''
@router.get("/", response_model=SuccessPaginationResponse)
async def paginate(limit: int=10, offset: str = None, search: str=''):
    organizations = OrganizationRepository().paginate(limit, offset, search)
    return {
        'message': 'Retrieve organizations successfully', 
        'data': organizations,
    }
'''

@router.get("/etablissements/{id}", response_model=SuccessEtablissementsDetailResponse)
async def etablissements_detail(id: str):
    etablissements = EtablissementsRepository().find_one(id)
    if etablissements is not None:
        periodes_etablissements = PeriodesEtablissementsRepository().find_all(id)   
        adresse = AdresseEtablissementsRepository().find_one(id)
        adresse2 = Adresse2EtablissementsRepository().find_one(id)
        unites_legales=UnitesLegalesRepository().find_one(etablissements["siren"])
        periodes_unites_legales= PeriodesUnitesLegalesRepository().find_all(etablissements["siren"])
        '''
        print("------------------------------")
        print(unites_legales)
        print(periodes_unites_legales)
        print("------------------------------")
        '''
        etablissements["uniteLegale"]=None
        etablissements["periodesEtablissement"]=periodes_etablissements
        etablissements["adresseEtablissement"]=adresse
        etablissements["adresse2Etablissement"]=adresse2
        return {
            'header' : {
                'status': 200,
                'message': 'ok'
            },
            'etablissement': etablissements,
        }
    else:
        return {
            'header' : {
                'status': 404,
                'message': 'Aucun élément trouvé pour le siret ' + id
            }
        }


# API Multiple Routers
app.include_router(router, prefix="/api/v1", tags=["siren"])