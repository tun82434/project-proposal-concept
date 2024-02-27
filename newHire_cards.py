from typing import Any, Mapping
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter 
import flask
import functions_framework
import json
import re

help_card = {
  'cardsV2': [
    {
      'cardId': 'helpCard',
      'card': {
        'header': {
            'title': 'HR Bot',
            'subtitle': 'Bobby Rahal HR Google Chat Bot'
        },
        'sections': [
          { 
            'header': 'Available Commands',
            'collapsible': False,
            'widgets': [
              {
                'decoratedText': {
                  'text': '/newHire',
                  'bottomLabel': '/newHire Description',
                  'button': {
                    'text': 'Try it',
                    'onClick': {
                      'action': {
                        'function': 'newHireOpenDialog',
                        'interaction': 'OPEN_DIALOG'
                      }
                    }
                  }
                }
              },
              {
                'divider': {}
              },
              {
                'decoratedText': {
                  'text': '/newHireAccess',
                  'bottomLabel': '/newHireAccess Description',
                  'button': {
                    'text': 'Try it',
                    'onClick': {
                      'action': {
                        'function': 'newHireAccess',
                        'interaction': 'OPEN_DIALOG'
                      }
                    }
                  }
                }
              },
              {
                'divider': {}
              },
              {
                'decoratedText': {
                  'text': '/newHireProgress',
                  'bottomLabel': '/newHireProgress Description',
                  'button': {
                    'text': 'Try it',
                    'onClick': {
                      'action': {
                        'function': 'newHireProgress',
                        'interaction': 'OPEN_DIALOG'
                      }
                    }
                  }
                }
              },
              {
                'divider': {}
              }
            ]
          }
        ]
      }
    }
  ]
}
