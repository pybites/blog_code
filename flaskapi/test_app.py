from copy import deepcopy
from pprint import pprint as pp
import unittest
import json

import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/items'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.backup_items = deepcopy(app.items)  # no references!
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['items']), 3)

    def test_get_one(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['items'][0]['name'], 'laptop')

    def test_item_not_exist(self):
        response = self.app.get(BAD_ITEM_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # val is string = bad
        item = {"name": "screen", "value": 'string'}
        response = self.app.post(BASE_URL, 
				data=json.dumps(item),
				content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # good one
        item = {"name": "screen", "value": 200}
        response = self.app.post(BASE_URL, 
				data=json.dumps(item),
				content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['item']['id'], 4)
        self.assertEqual(data['item']['name'], 'screen')
        # cannot insert again
        item = {"name": "screen", "value": 200}
        response = self.app.post(BASE_URL, 
				data=json.dumps(item),
				content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        item = {"value": 30}
        response = self.app.put(GOOD_ITEM_URL, 
				data=json.dumps(item),
				content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['item']['value'], 30)

    def test_update_error(self):
        # non existing endpoint
        item = {"value": 30}
        response = self.app.put(BAD_ITEM_URL, 
				data=json.dumps(item),
				content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # val is string = bad
        item = {"value": 'string'}
        response = self.app.put(GOOD_ITEM_URL, 
				data=json.dumps(item),
				content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        response = self.app.delete(GOOD_ITEM_URL) 
        self.assertEqual(response.status_code, 204)
        # non existing endpoint
        response = self.app.delete(BAD_ITEM_URL) 
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        app.items = self.backup_items 


if __name__ == "__main__":
    unittest.main()
