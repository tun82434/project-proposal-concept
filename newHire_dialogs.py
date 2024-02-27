from typing import Any, Mapping
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter 
import flask
import functions_framework
import json
import re

#TODO: last edited last changed last accessed etc etc
#TODO: change dialog button to be a fixedFooter for UX (same button placement)
#TODO: in editAccessDialog, I need to indicate whether something is inprogress or true.

db = firestore.Client(project = "eott-chat-app")
users_ref = db.collection("users")
accesses_db = db.collection("accesses")


def editEmployeeResponse(employeeID):
  doc_ref = users_ref.document(employeeID)
  doc = doc_ref.get()
  data = doc.to_dict()
  
  if data['status'] == "I_inprogress_na": #not given access 
    edit_dialog_noAccess = {
      'action_response': {
        'type': 'DIALOG',
        'dialog_action': {
          'dialog': {
            'body': {
              'sections': [
                {
                  'header': f"Employee ID: {doc.id}",
                  'widgets': [
                    {
                      'textInput': {
                        'label': 'First Name',
                        'type': 'SINGLE_LINE',
                        'name': 'newHireFirst',
                        'value': data['first']
                      }
                    },
                    {
                      'textInput': {
                        'label': 'Last Name',
                        'type': 'SINGLE_LINE',
                        'name': 'newHireLast',
                        'value': data['last']
                      }
                    },
                    {
                      'selectionInput': {
                        'type': "DROPDOWN",
                        'label': 'newHireDropDownDealership label',
                        'name': 'newHireDealership',
                        'items': [
                          {
                            'text': 'Select a Dealership',
                            'value': 'default',
                            'selected': data['dealership'] == 'default'
                          },
                          {
                            'text': 'Honda',
                            'value': 'honda',
                            'selected': data['dealership'] == 'honda'
                          },
                          {
                            'text': 'Toyota',
                            'value': 'toyota',
                            'selected': data['dealership'] == 'toyota'
                          },
                          {
                            'text': 'Acura',
                            'value': 'acura',
                            'selected': data['dealership'] == 'acura'
                          },
                          {
                            'text': 'Lexus',
                            'value': 'lexus',
                            'selected': data['dealership'] == 'lexus'
                          }
                        ]
                      }
                    },
                    {
                      'selectionInput': {
                        'type': "DROPDOWN",
                        'label': 'newHireDropDownDepartment label',
                        'name': 'newHireDepartment',
                        'items': [
                          {
                            'text': 'Select a Department',
                            'value': 'default',
                            'selected': data['department'] == 'default'
                          },
                          {
                            'text': 'Sales',
                            'value': 'sales',
                            'selected': data['department'] == 'sales'
                          },
                          {
                            'text': 'Parts',
                            'value': 'parts',
                            'selected': data['department'] == 'parts'
                          },
                          {
                            'text': 'Service',
                            'value': 'service',
                            'selected': data['department'] == 'service'
                          },
                          {
                            'text': 'Accounting',
                            'value': 'accounting',
                            'selected': data['department'] == 'accounting'
                          }
                        ]
                      }
                    },
                    {
                      'textInput': {
                        'label': 'Hiring Manager',
                        'type': 'SINGLE_LINE',
                        'name': 'newHireHiringManager',
                        'value': data['hiringManager']
                      }
                    },
                  ]
                }
              ],
              'fixedFooter': {
                'primaryButton': {
                  'text': 'Submit',
                  'color': {
                    'red': 0,
                    'green': 0.5,
                    'blue': 1,
                    'alpha': 1
                  },
                  'onClick': {
                    'action': {
                      'function': 'editReceiveDialog',
                      'parameters': [
                        {
                          'key': 'employeeID',
                          'value': employeeID
                        }
                      ]
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    return edit_dialog_noAccess
  
  else:
    # might need to make a sequential dialog because of the access portion
    
    edit_dialog = { # with access given
      'action_response': {
        'type': 'DIALOG',
        'dialog_action': {
          'dialog': {
            'body': {
              'sections': [
                {
                  'header': f"WITH ACCESS Employee ID: {doc.id}",
                  'widgets': [
                    {
                      'textInput': {
                        'label': 'First Name',
                        'type': 'SINGLE_LINE',
                        'name': 'newHireFirst',
                        'value': data['first']
                      }
                    },
                    {
                      'textInput': {
                        'label': 'Last Name',
                        'type': 'SINGLE_LINE',
                        'name': 'newHireLast',
                        'value': data['last']
                      }
                    },
                    {
                      'selectionInput': {
                        'type': "DROPDOWN",
                        'label': 'newHireDropDownDealership label',
                        'name': 'newHireDealership',
                        'items': [
                          {
                            'text': 'Select a Dealership',
                            'value': 'default',
                            'selected': data['dealership'] == 'default'
                          },
                          {
                            'text': 'Honda',
                            'value': 'honda',
                            'selected': data['dealership'] == 'honda'
                          },
                          {
                            'text': 'Toyota',
                            'value': 'toyota',
                            'selected': data['dealership'] == 'toyota'
                          },
                          {
                            'text': 'Acura',
                            'value': 'acura',
                            'selected': data['dealership'] == 'acura'
                          },
                          {
                            'text': 'Lexus',
                            'value': 'lexus',
                            'selected': data['dealership'] == 'lexus'
                          }
                        ]
                      }
                    },
                    {
                      'selectionInput': {
                        'type': "DROPDOWN",
                        'label': 'newHireDropDownDepartment label',
                        'name': 'newHireDepartment',
                        'items': [
                          {
                            'text': 'Select a Department',
                            'value': 'default',
                            'selected': data['department'] == 'default'
                          },
                          {
                            'text': 'Sales',
                            'value': 'sales',
                            'selected': data['department'] == 'sales'
                          },
                          {
                            'text': 'Parts',
                            'value': 'parts',
                            'selected': data['department'] == 'parts'
                          },
                          {
                            'text': 'Service',
                            'value': 'service',
                            'selected': data['department'] == 'service'
                          },
                          {
                            'text': 'Accounting',
                            'value': 'accounting',
                            'selected': data['department'] == 'accounting'
                          }
                        ]
                      }
                    },
                    {
                      'textInput': {
                        'label': 'Hiring Manager',
                        'type': 'SINGLE_LINE',
                        'name': 'newHireHiringManager',
                        'value': data['hiringManager']
                      }
                    },
                  ]
                }
              ],
              'fixedFooter': {
                'primaryButton': { # send to a receiveDialog for checking and send a sequential dialog or make it so that they scroll
                  'text': 'Next',
                  'color': {
                    'red': 0,
                    'green': 0.5,
                    'blue': 1,
                    'alpha': 1
                  },
                  'onClick': {
                    'action': {
                      'function': 'editReceiveDialog',
                      'parameters': [
                        {
                          'key': 'employeeID',
                          'value': employeeID
                        }
                      ]
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    return edit_dialog
  
def editAccessDialog(employeeID):
  edit_access_dialog = {
    'action_response': {
      'type': 'DIALOG',
      'dialog_action': {
        'dialog': {
          'body': {
            'sections': [],
            'fixedFooter': {
              'primaryButton': {
                'text': 'Submit',
                'color': {
                  'red': 0,
                  'green': 0.5,
                  'blue': 1,
                  'alpha': 1
                },
                'onClick': {
                  'action': {
                    'function': 'editAccessReceiveDialog',
                    'parameters': [
                      {
                        'key': 'employeeID',
                        'value': employeeID
                      }
                    ]
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  accesses_db_ref = accesses_db.stream()
  for access_type_db in accesses_db_ref:
    
    section = {
      'header': access_type_db.id,
      'widgets': [
        {
          'selectionInput': {
            'name': access_type_db.id,
            'label': f'{access_type_db.id} accesses:',
            'type': 'CHECK_BOX',
            'items': []
          }
        }
      ]
    }
    for access in access_type_db.to_dict().keys():
      access_type_user = users_ref.document(employeeID).collection('accesses').document(access_type_db.id).get().to_dict()
      try:
        if access_type_user[access] == "inprogress" or access_type_user[access] == True:
          item = {
            'text': access,
            'value': access,
            'selected': True
          }
          section['widgets'][0]['selectionInput']['items'].append(item)
        else:
          item = {
            'text': access,
            'value': access,
            'selected': False
          }
          section['widgets'][0]['selectionInput']['items'].append(item)
      except:
        try:
          item = {
            'text': access,
            'value': access,
            'selected': False
          }
          section['widgets'][0]['selectionInput']['items'].append(item)
        except Exception as e:
          print("ERROR: ",e)

    edit_access_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)
  return edit_access_dialog

def accessResponse(docs, queryNum):
  access_dialog = {
    'action_response': {
      'type': 'DIALOG',
      'dialog_action': {
        'dialog': {
          'body': {
            'sections': []
          }
        }
      }
    }
  }
  #TODO: Make UI Better
  if queryNum == 0:
    section = {
      'header': 'no result header',
      'widgets': [
        {
          'textParagraph': {
            'text': 'No current inprogress employees to give access to'
          }
        }
      ]
    }
    access_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)
    return access_dialog
  
  for doc in docs:
    data = doc.to_dict()
    name = f"{data['first']} {data['last']}"
    id = f"ID: {doc.id}"
    dealership =f"{data['dealership']}"
    department = f"{data['department']}"
    section = {
      'header': name,
      'widgets': [
        {
          'decoratedText': {
            'icon': {
              'iconUrl': 'https://raw.githubusercontent.com/google/material-design-icons/master/png/social/person/materialicons/24dp/1x/baseline_person_black_24dp.png',
              'altText': 'person_icon',
              'imageType': 'CIRCLE'   
            },
            'topLabel': dealership,
            'text': id,
            'bottomLabel': department,
            'button': {
              'icon': {
                'iconUrl': 'https://raw.githubusercontent.com/google/material-design-icons/master/png/editor/edit_note/materialiconsoutlined/24dp/1x/outline_edit_note_black_24dp.png',
                'altText': 'Click to edit employee.',
                'imageType': 'CIRCLE'
              },
              'text': 'Add Accesses',
              'onClick': {
                'action': {
                  'function': 'openAccessDialog',
                  'interaction': 'OPEN_DIALOG',
                  'parameters': [
                    {
                      'key': 'employeeID',
                      'value': doc.id
                    }
                  ]
                }
              }
            }
          }
        }
      ]
    }
    access_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)

  return access_dialog  

def openAccessDialog(employeeID):
  open_access_dialog = {
    'action_response': {
      'type': 'DIALOG',
      'dialog_action': {
        'dialog': {
          'body': {
            'sections': []
          }
        }
      }
    }
  }

  accesses = accesses_db.stream()
  for access_type in accesses:
    section = {
      'header': access_type.id,
      'widgets': [
        {
          'selectionInput': {
            'name': access_type.id,
            'label': f'{access_type.id} accesses:',
            'type': 'CHECK_BOX',
            'items': []
          }
        }
      ]
    }
    for access in access_type.to_dict().keys():
      item = {
        'text': access,
        'value': access,
        'selected': False
      }
      section['widgets'][0]['selectionInput']['items'].append(item)      
    open_access_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)
  section = {
    'buttonList': {
      'buttons': [
        {
          'text': 'Submit',
          'onClick': {
            'action': {
              'function': 'accessReceiveDialog',
              'parameters': [
                {
                  'key': 'receiveDialog',
                  'value': 'receiveDialog'
                }
              ]
            }
          }
        }
      ]
    }
  }
  open_access_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)
  return open_access_dialog

def progressResponse(docs, queryNum): #progress of all of users i_inprogress
  progress_dialog = {
    'action_response': {
      'type': 'DIALOG',
      'dialog_action': {
        'dialog': {
          'body': {
            'sections': []
          }
        }
      }
    }
  }
  # TODO: Make UI Better
  if queryNum == 0:
    section = {
      'header': 'no result header',
      'widgets': [
        {
          'textParagraph': {
            'text': 'No current inprogress employees to give access to'
          }
        }
      ]
    }
    progress_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)
    return progress_dialog
  

  
  for doc in docs:
    data = doc.to_dict()
    name = f"{data['first']} {data['last']}"
    id = f"ID: {doc.id}"
    dealership =f"{data['dealership']}"
    department = f"{data['department']}"
    docs_ref = users_ref.document(doc.id).collection('accesses').stream()
    accesses_text =""
    for doc_ref in docs_ref:
      access_text = f"{doc.id} {doc_ref.id} => {doc_ref.to_dict()}\n" # 1 DealerDaily => {'access2': False, 'access3': False, 'access1': False}
      accesses_text += access_text #TODO: Use HTML to make this look better.
    section = {
      'header': name,
      'collapsible': True,
      'uncollapsibleWidgetsCount': 1,
      'widgets': [
        {
          'decoratedText': {
            'icon': {
              'iconUrl': 'https://raw.githubusercontent.com/google/material-design-icons/master/png/social/person/materialicons/24dp/1x/baseline_person_black_24dp.png',
              'altText': 'person_icon',
              'imageType': 'CIRCLE'   
            },
            'topLabel': dealership,
            'text': id,
            'bottomLabel': department,
            'button': {
              'icon': {
                'iconUrl': 'https://raw.githubusercontent.com/google/material-design-icons/master/png/editor/edit_note/materialiconsoutlined/24dp/1x/outline_edit_note_black_24dp.png',
                'altText': 'Click to edit employee.',
                'imageType': 'CIRCLE'
              },
              'text': 'Edit',
              'onClick': {
                'action': {
                  'function': 'newHireEdit',
                  'interaction': 'OPEN_DIALOG',
                  'parameters': [
                    {
                      'key': 'employeeID',
                      'value': doc.id
                    }
                  ]
                }
              }
            }
          }
        },
        {
          'textParagraph': {
            'text': accesses_text
          }
        }
      ]
    }
    progress_dialog['action_response']['dialog_action']['dialog']['body']['sections'].append(section)

  return progress_dialog  

open_dialog = {
  'action_response': {
    'type': 'DIALOG',
    'dialog_action': {
      'dialog': {
        'body': {
          'sections': [
            {
              'header': 'newHireHeader',
              'widgets': [
                {
                  'textInput': {
                      'label': 'Employee ID',
                      'type': 'SINGLE_LINE',
                      'name': 'newHireID'
                  }
                },
                {
                  'textInput': {
                    'label': 'First Name',
                    'type': 'SINGLE_LINE',
                    'name': 'newHireFirst'
                  }
                },
                {
                  'textInput': {
                    'label': 'Last Name',
                    'type': 'SINGLE_LINE',
                    'name': 'newHireLast'
                  }
                },
                {
                  'selectionInput': {
                    'type': "DROPDOWN",
                    'label': 'newHireDropDownDealership label',
                    'name': 'newHireDealership',
                    'items': [
                      {
                        'text': 'Select a Dealership',
                        'value': 'default',
                        'selected': True
                      },
                      {
                        'text': 'Honda',
                        'value': 'honda',
                        'selected': False
                      },
                      {
                        'text': 'Toyota',
                        'value': 'toyota',
                        'selected': False
                      },
                      {
                        'text': 'Acura',
                        'value': 'acura',
                        'selected': False
                      },
                      {
                        'text': 'Lexus',
                        'value': 'lexus',
                        'selected': False
                      }
                    ]
                  }
                },
                {
                  'selectionInput': {
                    'type': "DROPDOWN",
                    'label': 'newHireDropDownDepartment label',
                    'name': 'newHireDepartment',
                    'items': [
                      {
                        'text': 'Select a Department',
                        'value': 'default',
                        'selected': True
                      },
                      {
                        'text': 'Sales',
                        'value': 'sales',
                        'selected': False
                      },
                      {
                        'text': 'Parts',
                        'value': 'parts',
                        'selected': False
                      },
                      {
                        'text': 'Service',
                        'value': 'service',
                        'selected': False
                      },
                      {
                        'text': 'Accounting',
                        'value': 'accounting',
                        'selected': False
                      }
                    ]
                  }
                },
                {
                  'textInput': {
                    'label': 'Hiring Manager',
                    'type': 'SINGLE_LINE',
                    'name': 'newHireHiringManager'
                  }
                },
                {
                  'buttonList': {
                    'buttons': [
                      {
                        'text': 'Submit',
                        'onClick': {
                          'action': {
                            'function': 'newHireReceiveDialog',
                            'parameters': [
                              {
                                'key': 'receiveDialog',
                                'value': 'receiveDialog'
                              }
                            ]
                          }
                        }
                      }
                    ]
                  }
                }
              ]
            }
          ]
        }
      }
    }
  }
}

def receiveInvalidResponse(newHireID, newHireFirstName, newHireLastName, newHireDealership, newHireDepartment, newHireHiringManager):
  return {
    'action_response': {
      'type': 'DIALOG',
      'dialog_action': {
        'dialog': {
          'body': {
            'sections': [
              {
                'header': 'newHireHeader',
                'widgets': [
                  {
                    'decoratedText': {
                      'startIcon': {
                        'knownIcon': 'STAR'
                      },
                      'text': '<font color=\"#FE0000\">MISSING FIELDS</font>'
                    }
                  },
                  {
                    'textInput': {
                      'label': 'Employee ID',
                      'type': 'SINGLE_LINE',
                      'name': 'newHireID',
                      'value': newHireID
                    }
                  },
                  {
                    'textInput': {
                      'label': 'First Name',
                      'type': 'SINGLE_LINE',
                      'name': 'newHireFirst',
                      'value': newHireFirstName
                    }
                  },
                  {
                    'textInput': {
                      'label': 'Last Name',
                      'type': 'SINGLE_LINE',
                      'name': 'newHireLast',
                      'value': newHireLastName
                    }
                  },
                  {
                    'selectionInput': {
                      'type': "DROPDOWN",
                      'label': 'newHireDropDownDealership label',
                      'name': 'newHireDealership',
                      'items': [
                        {
                          'text': 'Select a Dealership',
                          'value': 'default',
                          'selected': newHireDealership == 'default'
                        },
                        {
                          'text': 'Honda',
                          'value': 'honda',
                          'selected': newHireDealership == 'honda'
                        },
                        {
                          'text': 'Toyota',
                          'value': 'toyota',
                          'selected': newHireDealership == 'toyota'
                        },
                        {
                          'text': 'Acura',
                          'value': 'acura',
                          'selected': newHireDealership == 'acura'
                        },
                        {
                          'text': 'Lexus',
                          'value': 'lexus',
                          'selected': newHireDealership == 'lexus'
                        }
                      ]
                    }
                  },
                  {
                    'selectionInput': {
                      'type': "DROPDOWN",
                      'label': 'newHireDropDownDepartment label',
                      'name': 'newHireDepartment',
                      'items': [
                        {
                          'text': 'Select a Department',
                          'value': 'default',
                          'selected': newHireDepartment == 'default'
                        },
                        {
                          'text': 'Sales',
                          'value': 'sales',
                          'selected': newHireDepartment == 'sales'
                        },
                        {
                          'text': 'Parts',
                          'value': 'parts',
                          'selected': newHireDepartment == 'parts'
                        },
                        {
                          'text': 'Service',
                          'value': 'service',
                          'selected': newHireDepartment == 'service'
                        },
                        {
                          'text': 'Accounting',
                          'value': 'accounting',
                          'selected': newHireDepartment == 'accounting'
                        }
                      ]
                    }
                  },
                  {
                    'textInput': {
                      'label': 'Hiring Manager',
                      'type': 'SINGLE_LINE',
                      'name': 'newHireHiringManager',
                      'value': newHireHiringManager
                    }
                  },
                  {
                    'buttonList': {
                      'buttons': [
                        {
                          'text': 'Submit',
                          'onClick': {
                            'action': {
                              'function': 'newHireTestReceiveDialog',
                              'parameters': [
                                {
                                  'key': 'receiveDialog',
                                  'value': 'receiveDialog'
                                }
                              ]
                            }
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            ]
          }
        }
      }
    }
  }
