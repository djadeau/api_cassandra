from typing import List, Optional
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel
from app.responses.base_response import PaginationResponse, HeaderResponse
from app.responses.unites_legales_response import UnitesLegalesResponse


class PeriodesEtablissementsResponse(BaseModel):
    dateDebut                                   : date = None
    dateFin                                     : date = None
    etatAdministratifEtablissement              : str = None
    changementEtatAdministratifEtablissement    : bool = None
    enseigne1Etablissement                      : str = None
    enseigne2Etablissement                      : str = None
    enseigne3Etablissement                      : str = None
    changementEnseigneEtablissement             : bool = None
    denominationUsuelleEtablissement            : str = None
    changementDenominationUsuelleEtablissement  : bool = None
    activitePrincipaleEtablissement             : str = None
    changementActivitePrincipaleEtablissement   : bool = None
    nomenclatureActivitePrincipaleEtablissement : str = None
    caractereEmployeurEtablissement             : str = None
    changementCaractereEmployeurEtablissement   : bool = None

class AdresseEtablissementsResponse(BaseModel):
    complementAdresseEtablissement                 : str = None
    numeroVoieEtablissement                        : str = None
    dernierNumeroVoieEtablissement                 : str = None
    indiceRepetitionEtablissement                  : str = None
    typeVoieEtablissement                          : str = None
    indiceRepetitionDernierNumeroVoieEtablissement : str = None
    libelleVoieEtablissement                       : str = None
    codePostalEtablissement                        : str = None
    libelleCommuneEtablissement                    : str = None
    libelleCommuneEtrangerEtablissement            : str = None
    distributionSpecialeEtablissement              : str = None
    codeCommuneEtablissement                       : str = None
    codeCedexEtablissement                         : str = None
    libelleCedexEtablissement                      : str = None
    codePaysEtrangerEtablissement                  : int = None
    libellePaysEtrangerEtablissement               : str = None
    identifiantAdresseEtablissement                : str = None
    coordonneeLambertAbscisseEtablissement         : str = None
    coordonneeLambertOrdonneeEtablissement         : str = None

class Adresse2EtablissementsResponse(BaseModel):
    complementAdresse2Etablissement                 : str = None
    numeroVoie2Etablissement                        : str = None
    indiceRepetition2Etablissement                  : str = None
    typeVoie2Etablissement                          : str = None
    libelleVoie2Etablissement                       : str = None
    codePostal2Etablissement                        : str = None
    libelleCommune2Etablissement                    : str = None
    libelleCommuneEtranger2Etablissement            : str = None
    distributionSpeciale2Etablissement              : str = None
    codeCommune2Etablissement                       : int = None
    codeCedex2Etablissement                         : str = None
    libelleCedex2Etablissement                      : str = None
    codePaysEtranger2Etablissement                  : int = None
    libellePaysEtranger2Etablissement               : str = None

class EtablissementsResponse(BaseModel):
    siren                                          : str
    nic                                            : str = None
    siret                                          : str = None
    statutDiffusionEtablissement                   : str = None
    dateCreationEtablissement                      : date = None
    trancheEffectifsEtablissement                  : str = None
    anneeEffectifsEtablissement                    : int = None
    activitePrincipaleRegistreMetiersEtablissement : str = None
    dateDernierTraitementEtablissement             : datetime = None
    etablissementSiege                             : bool = None
    nombrePeriodesEtablissement                    : int = None
    adresseEtablissement                           : AdresseEtablissementsResponse = None
    adresse2Etablissement                          : Adresse2EtablissementsResponse = None
    uniteLegale                                    : None
    periodesEtablissement             : List[PeriodesEtablissementsResponse] = []


class EtablissementsPaginationResponse(PaginationResponse):
    data: List[EtablissementsResponse] = []


class SuccessEtablissementsDetailResponse(BaseModel):
    header: HeaderResponse
    etablissement: Optional[EtablissementsResponse] = None


class SuccessEtablissementsPaginationResponse(BaseModel):
    header: HeaderResponse
    data: Optional[EtablissementsPaginationResponse] = None


class SuccessEtablissementsListResponse(BaseModel):
    header: HeaderResponse
    data: List[EtablissementsResponse] = None