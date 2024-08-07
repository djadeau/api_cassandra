import requests
from pytest_schema import schema, Or


API_ROOT = 'http://api/organizations'


expected_oganization_list = {
    "message": str,
    "success": bool,
    "data": {
        "total": int,
        "limit": int,
        "offset": Or(None, str),
        "last_page": Or(None, int),
        "next_page_link": Or(None, str),
        "data": Or(None, list)
    }
}

expected_oganization_detail = {
    "message": str,
    "success": bool,
    "data": {
        "organization_id": str,
        "user_id": int,
        "name": str,
        "alias": str,
        "logo": Or(None, str),
    }
}

class TestEtablissementsApi:

    results = []
    siret = ''

    def test_get_detail(self):
        url = f'{API_ROOT}/{siret}'
        print(url)
        
        response = requests.get(url=url)
        result = response.json()
        assert response.status_code == 200
        assert schema(expected_oganization_detail) == result

    # def test_get_list_and_detail(self):
    #     # Case 1: get list with pagination
    #     url = f'{API_ROOT}'
    #     response = requests.get(url=url)
    #     result = response.json()

    #     if result['data'] is not None and len(result['data']) > 0:
    #         print(result['data']['data'])
    #         self.organization_id = result['data']['data'][0]['organization_id']

    #     assert response.status_code == 200
    #     assert schema(expected_oganization_list) == result

    #     # Case 2: Get detail by id 
    #     url = f'{API_ROOT}/{self.organization_id}'
    #     print(url)
        
    #     response = requests.get(url=url)
    #     result = response.json()
    #     assert response.status_code == 200
    #     assert schema(expected_oganization_detail) == result