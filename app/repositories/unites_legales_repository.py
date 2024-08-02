from app.repositories.base_unites_legales import BaseUnitesLegalesRepository
from app.repositories.base_unites_legales import unites_legales, periodes_unites_legales

class UnitesLegalesRepository(BaseUnitesLegalesRepository):

    _model = unites_legales

class PeriodesUnitesLegalesRepository(BaseUnitesLegalesRepository):

    _model = periodes_unites_legales