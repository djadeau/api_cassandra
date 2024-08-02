import os
import abc
import math
import uuid
import inspect
from datetime import datetime
from app.responses.base_response import PaginationResponse

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# For model
from cassandra.cqlengine import columns, functions
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import register_connection, set_default_connection, dict_factory
from cassandra.util import Date, Time


KEYSPACE = "repertoire_national"
HOSTS = ['dockerv2']
CREDENTIAL = {'username': 'admin', 'password': 'admin'} 
AUTH_PROVIDER = PlainTextAuthProvider(username='admin', password='admin')

class etablissements(Model):
    __keyspace__ = 'repertoire_national'
    __connection__ = 'etablissements'
    siren                                          = columns.Text(required=True, index=True)
    nic                                            = columns.Text(required=True)
    siret                                          = columns.Text(primary_key=True)        
    statutDiffusionEtablissement                   = columns.Text(required=False)
    dateCreationEtablissement                      = columns.Date(required=False)
    trancheEffectifsEtablissement                  = columns.Text(required=False)
    anneeEffectifsEtablissement                    = columns.Integer(required=False)
    activitePrincipaleRegistreMetiersEtablissement = columns.Text(required=False)
    dateDernierTraitementEtablissement             = columns.DateTime(required=False)
    etablissementSiege                             = columns.Boolean(required=False)
    nombrePeriodesEtablissement                    = columns.Integer(required=False)
    hub_update_date                                = columns.Date()
    
class adresse_etablissements(Model):
    __keyspace__ = 'repertoire_national'
    __connection__ = 'etablissements'
    siret                                          = columns.Text(primary_key=True)        
    complementAdresseEtablissement                 = columns.Text(required=False)
    numeroVoieEtablissement                        = columns.Text(required=False)
    dernierNumeroVoieEtablissement                 = columns.Text(required=False)
    indiceRepetitionEtablissement                  = columns.Text(required=False)
    typeVoieEtablissement                          = columns.Text(required=False)
    indiceRepetitionDernierNumeroVoieEtablissement = columns.Text(required=False)
    libelleVoieEtablissement                       = columns.Text(required=False)
    codePostalEtablissement                        = columns.Text(required=False)
    libelleCommuneEtablissement                    = columns.Text(required=False)
    libelleCommuneEtrangerEtablissement            = columns.Text(required=False)
    distributionSpecialeEtablissement              = columns.Text(required=False)
    codeCommuneEtablissement                       = columns.Text(required=False)
    codeCedexEtablissement                         = columns.Text(required=False)
    libelleCedexEtablissement                      = columns.Text(required=False)
    codePaysEtrangerEtablissement                  = columns.Integer(required=False)
    libellePaysEtrangerEtablissement               = columns.Text(required=False)
    identifiantAdresseEtablissement                = columns.Text(required=False)
    coordonneeLambertAbscisseEtablissement         = columns.Text(required=False)
    coordonneeLambertOrdonneeEtablissement         = columns.Text(required=False)
    hub_update_date                                = columns.Date(required=True)

class adresse2_etablissements(Model):
    __keyspace__ = 'repertoire_national'
    __connection__ = 'etablissements'
    siret                                           = columns.Text(primary_key=True)        
    complementAdresse2Etablissement                 = columns.Text(required=False)
    numeroVoie2Etablissement                        = columns.Text(required=False)
    indiceRepetition2Etablissement                  = columns.Text(required=False)
    typeVoie2Etablissement                          = columns.Text(required=False)
    libelleVoie2Etablissement                       = columns.Text(required=False)
    codePostal2Etablissement                        = columns.Text(required=False)
    libelleCommune2Etablissement                    = columns.Text(required=False)
    libelleCommuneEtranger2Etablissement            = columns.Text(required=False)
    distributionSpeciale2Etablissement              = columns.Text(required=False)
    codeCommune2Etablissement                       = columns.Integer(required=False)
    codeCedex2Etablissement                         = columns.Text(required=False)
    libelleCedex2Etablissement                      = columns.Text(required=False)
    codePaysEtranger2Etablissement                  = columns.Integer(required=False)
    libellePaysEtranger2Etablissement               = columns.Text(required=False)
    hub_update_date                                 = columns.Date(required=True)

class periodes_etablissements(Model):
    __keyspace__ = 'repertoire_national'
    __connection__ = 'etablissements'
    id                                          = columns.Text(primary_key=True)
    siret                                       = columns.Text(index=True, required=True)  
    dateDebut                                   = columns.Date(required=False)
    dateFin                                     = columns.Date(required=False)
    etatAdministratifEtablissement              = columns.Text(required=False)
    changementEtatAdministratifEtablissement    = columns.Boolean(required=False)
    enseigne1Etablissement                      = columns.Text(required=False)
    enseigne2Etablissement                      = columns.Text(required=False)
    enseigne3Etablissement                      = columns.Text(required=False)
    changementEnseigneEtablissement             = columns.Boolean(required=False)
    denominationUsuelleEtablissement            = columns.Text(required=False)
    changementDenominationUsuelleEtablissement  = columns.Boolean(required=False)
    activitePrincipaleEtablissement             = columns.Text(required=False)
    changementActivitePrincipaleEtablissement   = columns.Boolean(required=False)
    nomenclatureActivitePrincipaleEtablissement = columns.Text(required=False)
    caractereEmployeurEtablissement             = columns.Text(required=False)
    changementCaractereEmployeurEtablissement   = columns.Boolean(required=False)
    hub_update_date                             = columns.Date(required=True)



def cassandra_session_factory():
    HOSTS=[os.environ["CASSANDRA_HOST"]]
    CREDENTIAL = {'username': os.environ["CASSANDRA_USER"], 'password': os.environ["CASSANDRA_PASSWORD"]} 
    AUTH_PROVIDER = PlainTextAuthProvider(username=CREDENTIAL["username"], password=CREDENTIAL['password'])
    cluster = Cluster(HOSTS, auth_provider=AUTH_PROVIDER)
    session = cluster.connect()

    log.info("Creating keyspace...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % KEYSPACE
    )

    log.info("Setting keyspace...")
    session.set_keyspace(KEYSPACE)

    session.row_factory = dict_factory
    session.execute("USE {}".format(KEYSPACE))

    return session


_session = cassandra_session_factory()
register_connection("etablissements", session=_session)
set_default_connection('etablissements')

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def to_dict(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def to_list(self, l):
        raise NotImplementedError

class BaseEtablissementsRepository(AbstractRepository):

    _model = None

    def __init__(self):
        self.session = _session

    def count(self):
        return self._model.objects.count()

    def to_dict(self, obj):
        if obj is not None:
            return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
        else:
            return {}

    def to_list(self, _list):
        if isinstance(_list, list) and len(_list):
            output = []
            for item in _list:
                output.append(self.to_dict(item))
            return output
        else:
            print("A list is reuired!")
            return []

    def _is_empty(self, value):
        if value is None:
            return True
        elif isinstance(value, str) and value.strip() == '':
            return True
        return False

    def find_one(self, id: str):
        items = self._model.objects(siret=id)
        if len(items)!=0:
            result=dict(items[0])
            cleaned_result=result.copy()
            for elem in result:
                if result[elem]==None:
                    del cleaned_result[elem]
                elif "date" in elem:
                    cleaned_result[elem]=str(result[elem])
            return cleaned_result
        return None    
    
    def find_all(self, id: str):
        items = self._model.objects(siret=id)
        item_list=[]
        if len(items)!=0:
            for item in items:
                result=dict(item)
                cleaned_result=result.copy()
                for elem in result:
                    if result[elem]==None:
                        del cleaned_result[elem]
                    elif "date" in elem:
                        cleaned_result[elem]=str(result[elem])
                item_list.append(cleaned_result)
        return item_list    

    def paginate(self, limit: int, offset: str = None, search: str = ''):
        total = self._model.objects.count()
        last_page = math.ceil(total / limit) if total > 0 else 1
        next_page = None
        data = []
        
        if total > 0:
            query = self._model.objects.all().limit(limit)
            
            if offset is not None:
                query = query.filter(pk__token__gt=functions.Token(offset))

            data = list(query)

            if len(data) > 0:
                last = data[-1]
                next_page = f'?limit={limit}&offset={last.pk}&search={search}'
        
        return PaginationResponse(
            total=total,
            limit=limit,
            offset=offset,
            last_page=last_page,
            next_page_link=next_page,
            data=data
        )