"""
Copyright 2023 MSOE DISE Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import pprint

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from ringling_lib.param_set import ParameterSet
from ringling_lib.ringling_db import RinglingDBSession
from .response_handling import handle_create
from .response_handling import handle_get
from .response_handling import handle_modify
from .response_handling import perform_list
from .response_handling import connection_error



def get_url(base_url):
    """
    Get the URL for interacting with parameter sets
    :return: The parameter set URL
    """
    return base_url + "/v1/parameter_sets"


def create_param_set(session, project_id, training_params, is_active, metadata):
    """
    Create a parameter set on the Ringling service
    :param base_url: The URL of the Ringling Service
    :param project_id: The ID of the project that the parameter set belongs to
    :param training_params: The parameters of the parameter set
    :param is_active: If the parameter set is active or inactive
    :return: None
    """
    param = ParameterSet(project_id, training_params, is_active, metadata)
    cur_id = session.create_param_set(param)
    print(f"Parameter Set created with ID {cur_id}")


def get_param_set(session, param_set_id):
    """
    Get a parameter set given an ID
    :param base_url: The URL of the Ringling Service
    :param param_set_id: The ID of the parameter set
    :return: None
    """
    pprint.pprint(session.get_param_set_json(param_set_id))


def modify_param_set(base_url, param_set_id, is_active):
    """
    Modify the activity status of a parameter set
    :param base_url: The URL of the Ringling Service
    :param param_set_id: The ID of the parameter set
    :param is_active: If the parameter set should be set to active or inactive
    :return: None
    """
    url = get_url(base_url) + "/" + str(param_set_id)
    update = {"is_active": is_active}
    try:
        response = requests.patch(url, json=update, timeout=5)
        if handle_modify(response, "Parameter Set", param_set_id):
            print("Parameter Set", param_set_id, "active status changed to", is_active)
    except RequestsConnectionError:
        connection_error()


def list_param_sets(session):
    """
    List all the parameter sets in the Ringling Service
    :param base_url: The URL of the Ringling Service
    :return: None
    """
    pprint.pprint(session.list_param_sets_json())
