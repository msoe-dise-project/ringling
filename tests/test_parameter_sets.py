import argparse
import datetime as dt
import os
import sys
import unittest

import requests

BASE_URL_KEY = "BASE_URL"

class ParameterSetsTests(unittest.TestCase):
    def get_url(self):
        return os.path.join(os.environ[BASE_URL_KEY], "v1/parameter_sets")

    def test_create_success(self):
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "minimum_software_version" : 3,
                "active_from" : dt.datetime.now().isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)
        
    def test_create_success_no_end(self):
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "minimum_software_version" : 3,
                "active_from" : (dt.datetime.now() - dt.timedelta(days=1)).isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)
        
    def test_list_params(self):
        param_ids = set()
        
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "minimum_software_version" : 3,
                "active_from" : dt.datetime.now().isoformat() }
                
        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])
                
        obj = { "project_id" : 6,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "minimum_software_version" : 3,
                "active_from" : dt.datetime.now().isoformat(),
                "active_until" : (dt.datetime.now() + dt.timedelta(days=3)).isoformat() }
                
        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])
                
        obj = { "project_id" : 7,
                "minimum_software_version" : 3,
                "training_parameters" : { "param1" : 1, "param2" : "2" } }
                
        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        param_ids.add(json_response["parameter_set_id"])

        response = requests.get(self.get_url())

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn("parameter_sets", json_response)
        
        observed_param_ids = set([obj["parameter_set_id"] for obj in json_response["parameter_sets"]])
        
        # check that param_ids is a proper subset of observed_param_ids
        self.assertEqual(param_ids, observed_param_ids.intersection(param_ids))
    
    def test_get_by_id(self):
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "minimum_software_version" : 1,
                "active_from" : dt.datetime.now().isoformat(),
                "active_until" : (dt.datetime.now() + dt.timedelta(days=3)).isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response2["parameter_set_id"], json_response["parameter_set_id"])
        self.assertEqual(obj["project_id"], json_response2["project_id"])
        self.assertEqual(obj["training_parameters"], json_response2["training_parameters"])
        self.assertEqual(obj["active_from"], json_response2["active_from"])
        self.assertEqual(obj["active_until"], json_response2["active_until"])
        
    def test_get_by_id_no_end(self):
        obj = { "project_id" : 5,
                "minimum_software_version" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "active_from" : dt.datetime.now().isoformat() }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertIn("parameter_set_id", json_response)
        self.assertIsInstance(json_response["parameter_set_id"], int)

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response2["parameter_set_id"], json_response["parameter_set_id"])
        self.assertEqual(obj["project_id"], json_response2["project_id"])
        self.assertEqual(obj["training_parameters"], json_response2["training_parameters"])
        self.assertEqual(obj["active_from"], json_response2["active_from"])
        
    def test_update_active_interval(self):
        _from = (dt.datetime.now() - dt.timedelta(days=1)).isoformat()
        _until = dt.datetime.now().isoformat()
        obj = { "project_id" : 5,
                "training_parameters" : { "param1" : 1, "param2" : "2" },
                "minimum_software_version" : 3,
                "active_from" : _from }

        response = requests.post(self.get_url(),
                            json=obj)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        url = os.path.join(self.get_url(), str(json_response["parameter_set_id"]))
        
        update = { "active_from" : _from,
                   "active_until" : _until }
        
        response = requests.put(url, json=update)

        self.assertEqual(response.status_code, 200)

        json_response2 = response.json()
        self.assertIn("parameter_set_id", json_response2)
        self.assertEqual(json_response["parameter_set_id"], json_response2["parameter_set_id"])
        self.assertEqual(obj["active_from"], json_response2["active_from"])
        self.assertIsNotNone(json_response2["active_until"])

if __name__ == "__main__":
    if BASE_URL_KEY not in os.environ:
        print("Must define the base URL using the {} environment variable".format(BASE_URL_KEY))
        sys.exit(1)

    unittest.main()
