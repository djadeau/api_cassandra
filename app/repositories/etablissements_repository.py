from app.repositories.base_etablissements import BaseEtablissementsRepository
from app.repositories.base_etablissements import etablissements, periodes_etablissements, adresse_etablissements, adresse2_etablissements

class EtablissementsRepository(BaseEtablissementsRepository):

    _model = etablissements

class PeriodesEtablissementsRepository(BaseEtablissementsRepository):

    _model = periodes_etablissements

class AdresseEtablissementsRepository(BaseEtablissementsRepository):

    _model = adresse_etablissements

class Adresse2EtablissementsRepository(BaseEtablissementsRepository):

    _model = adresse2_etablissements