from typing import Any, Mapping
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter 
import flask
import functions_framework
import json
import re

invalidNumeric_message = {
  'actionResponse': {
    'type': 'NEW_MESSAGE',
  },
  'text': 'Error: FIELDS HAS NUMERICAL VALUES. Form has not been submitted. TODO: incorporate as an error in invalidResponse'
}

invalidExist_message = {
  'actionResponse': {
    'type': 'NEW_MESSAGE',
  },
  'text': 'Error: USER ALREADY EXISTS. Form has not been submitted. TODO: incorporate as an error in invalidResponse'
}

valid_message = {
  'actionResponse': {
    'type': 'NEW_MESSAGE',
  },
  'text': 'Form has been sucessfully submitted. TODO: Make cleaner UI or conformation card/dialog'
}
