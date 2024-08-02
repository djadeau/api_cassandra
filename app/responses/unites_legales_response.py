from typing import List, Optional
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel
from app.responses.base_response import PaginationResponse, HeaderResponse


class PeriodesUnitesLegalesResponse(BaseModel):
    activitePrincipaleUniteLegale                   : str
    caractereEmployeurUniteLegale                   : str
    categorieJuridiqueUniteLegale                   : str
    changementActivitePrincipaleUniteLegale         : bool
    changementCaractereEmployeurUniteLegale         : bool
    changementCategorieJuridiqueUniteLegale         : bool
    changementDenominationUniteLegale               : bool
    changementDenominationUsuelleUniteLegale        : bool
    changementEconomieSocialeSolidaireUniteLegale   : bool
    changementEtatAdministratifUniteLegale          : bool
    changementNicSiegeUniteLegale                   : bool
    changementNomUniteLegale                        : bool
    changementNomUsageUniteLegale                   : bool
    changementSocieteMissionUniteLegale             : bool
    dateDebut                                       : date
    dateFin                                         : date
    denominationUniteLegale                         : str
    denominationUsuelle1UniteLegale                 : str
    denominationUsuelle2UniteLegale                 : str
    denominationUsuelle3UniteLegale                 : str
    economieSocialeSolidaireUniteLegale             : str
    etatAdministratifUniteLegale                    : str
    nicSiegeUniteLegale                             : str
    nomenclatureActivitePrincipaleUniteLegale       : str
    nomUniteLegale                                  : str
    nomUsageUniteLegale                             : str
    societeMissionUniteLegale                       : str

class UnitesLegalesResponse(BaseModel):
    siren                               : str
    anneeCategorieEntreprise            : int = None
    anneeEffectifsUniteLegale           : int = None
    categorieEntreprise                 : str = None
    dateCreationUniteLegale             : date = None
    dateDernierTraitementUniteLegale    : datetime = None
    identifiantAssociationUniteLegale   : str = None
    nombrePeriodesUniteLegale           : int = None
    prenom1UniteLegale                  : str = None
    prenom2UniteLegale                  : str = None
    prenom3UniteLegale                  : str = None
    prenom4UniteLegale                  : str = None
    prenomUsuelUniteLegale              : str = None
    pseudonymeUniteLegale               : str = None
    sexeUniteLegale                     : str = None
    sigleUniteLegale                    : str = None
    statutDiffusionUniteLegale          : str = None
    trancheEffectifsUniteLegale         : str = None
    periodes_unites_legales             : List[PeriodesUnitesLegalesResponse] = []


class UnitesLegalesPaginationResponse(PaginationResponse):
    data: List[UnitesLegalesResponse] = []


class SuccessUnitesLegalesDetailResponse(BaseModel):
    header: HeaderResponse
    uniteLegale: Optional[UnitesLegalesResponse] = None


class SuccessUnitesLegalesPaginationResponse(BaseModel):
    header: HeaderResponse
    data: Optional[UnitesLegalesPaginationResponse] = None


class SuccessUnitesLegalesListResponse(BaseModel):
    header: HeaderResponse
    data: List[UnitesLegalesResponse] = None