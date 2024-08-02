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

class unites_legales(Model):
    __keyspace__ = 'repertoire_national'
    __connection__ = 'unites_legales'
    siren                               = columns.Text(primary_key=True)
    anneeCategorieEntreprise            = columns.Integer(required=False)
    anneeEffectifsUniteLegale           = columns.Integer(required=False)        
    categorieEntreprise                 = columns.Text(required=False)
    dateCreationUniteLegale             = columns.Date(required=False)
    dateDernierTraitementUniteLegale    = columns.DateTime(required=False)
    identifiantAssociationUniteLegale   = columns.Text(required=False)
    nombrePeriodesUniteLegale           = columns.Integer(required=False)
    prenom1UniteLegale                  = columns.Text(required=False)
    prenom2UniteLegale                  = columns.Text(required=False)
    prenom3UniteLegale                  = columns.Text(required=False)
    prenom4UniteLegale                  = columns.Text(required=False)
    prenomUsuelUniteLegale              = columns.Text(required=False)
    pseudonymeUniteLegale               = columns.Text(required=False)
    sexeUniteLegale                     = columns.Text(required=False)
    sigleUniteLegale                    = columns.Text(required=False)
    statutDiffusionUniteLegale          = columns.Text(required=False)
    trancheEffectifsUniteLegale         = columns.Text(required=False)
    hub_update_date                     = columns.Date()

class periodes_unites_legales(Model):
    __keyspace__ = 'repertoire_national'
    __connection__ = 'unites_legales'
    id                                              = columns.Text(primary_key=True)
    siren                                           = columns.Text(index=True, required=True)
    activitePrincipaleUniteLegale                   = columns.Text(required=False) 
    caractereEmployeurUniteLegale                   = columns.Text(required=False) 
    categorieJuridiqueUniteLegale                   = columns.Text(required=False) 
    changementActivitePrincipaleUniteLegale         = columns.Boolean(required=False) 
    changementCaractereEmployeurUniteLegale         = columns.Boolean(required=False) 
    changementCategorieJuridiqueUniteLegale         = columns.Boolean(required=False) 
    changementDenominationUniteLegale               = columns.Boolean(required=False) 
    changementDenominationUsuelleUniteLegale        = columns.Boolean(required=False) 
    changementEconomieSocialeSolidaireUniteLegale   = columns.Boolean(required=False) 
    changementEtatAdministratifUniteLegale          = columns.Boolean(required=False) 
    changementNicSiegeUniteLegale                   = columns.Boolean(required=False) 
    changementNomUniteLegale                        = columns.Boolean(required=False) 
    changementNomUsageUniteLegale                   = columns.Boolean(required=False) 
    changementSocieteMissionUniteLegale             = columns.Boolean(required=False) 
    dateDebut                                       = columns.Date(required=False) 
    dateFin                                         = columns.Date(required=False) 
    denominationUniteLegale                         = columns.Text(required=False) 
    denominationUsuelle1UniteLegale                 = columns.Text(required=False) 
    denominationUsuelle2UniteLegale                 = columns.Text(required=False) 
    denominationUsuelle3UniteLegale                 = columns.Text(required=False) 
    economieSocialeSolidaireUniteLegale             = columns.Text(required=False) 
    etatAdministratifUniteLegale                    = columns.Text(required=False) 
    nicSiegeUniteLegale                             = columns.Text(required=False) 
    nomenclatureActivitePrincipaleUniteLegale       = columns.Text(required=False) 
    nomUniteLegale                                  = columns.Text(required=False) 
    nomUsageUniteLegale                             = columns.Text(required=False) 
    societeMissionUniteLegale                       = columns.Text(required=False) 
    hub_update_date                                 = columns.Date()



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
register_connection("unites_legales", session=_session)
set_default_connection('unites_legales')

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def to_dict(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def to_list(self, l):
        raise NotImplementedError

class BaseUnitesLegalesRepository(AbstractRepository):

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
        items = self._model.objects(siren=id)
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
        items = self._model.objects(siren=id)
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