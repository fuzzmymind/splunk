# $SPLUNK_HOME/etc/apps/my_splunk_mi/bin/my_splunk_mi.py

import sys
import xml.dom.minidom, xml.sax.saxutils
import os
import json
import logging
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.modularinput import *

class MyScript(Script):

    def get_scheme(self):
        scheme = Scheme("mysplunkmi")
        scheme.description = "My splunk modular input."
        scheme.use_external_validation = True
        scheme.use_single_instance = False

        apikey_argument = Argument("apikey")
        apikey_argument.data_type = Argument.data_type_string
        apikey_argument.description = "The api key for coinmarketcap.com"
        apikey_argument.required_on_create = True
        scheme.add_argument(apikey_argument)

        return scheme

    def validate_input(self, validation_definition):
        apikey = str(validation_definition.parameters["apikey"])
        if len(apikey) != 36:
            raise ValueError("The apikey needs to be 36 character long!")


    def stream_events(self, inputs, ew):
        for input_name, input_item in inputs.inputs.iteritems():
            load_data(input_name, input_item, ew)


def load_data(input_name,input_item, ew):
    apikey = str(input_item["apikey"])
    url = 'your api url goes here'
    # add params and headers as needed.
    parameters = {}
    headers = {}
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # Loop through the response. this logic will change depending on your api response.
        for d in data["data"]:
            event = Event()
            event.data = json.dumps(d)
            ew.write_event(event)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

if __name__ == "__main__":
    sys.exit(MyScript().run(sys.argv))
