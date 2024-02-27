from typing import Any, Mapping
from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
import flask
import functions_framework
import json
import re
import collectionClass
import newHire_dialogs
import newHire_messages

db = firestore.Client(project = "eott-chat-app")
users_ref = db.collection("users")
accesses_db = db.collection("accesses")

@functions_framework.http # decorators: a powerful and versatile tool in Python that allow you to modify the behavior of functions without changing their source code. They add functionality to existing functions, wrap them in additional operations, and can be used for various purposes like logging, caching, authentication, and more.


def edit(event: Mapping[str, Any]) -> Mapping[str, Any]:
  parameters = event.get('common').get('parameters')
  employeeID = parameters['employeeID']
  edit_dialog = newHire_dialogs.editEmployeeResponse(employeeID)
  return edit_dialog

def editReceiveDialog(event: Mapping[str, Any]) -> Mapping[str, Any]:
  parameters = event.get('common').get('parameters')
  employeeID = parameters['employeeID']
  editFormInputs = event.get('common').get('formInputs')
  newHireFirstName = editFormInputs.get('newHireFirst').get('stringInputs').get('value')[0]
  newHireLastName = editFormInputs.get('newHireLast').get('stringInputs').get('value')[0]
  newHireDealership = editFormInputs.get('newHireDealership').get('stringInputs').get('value')[0]
  newHireDepartment = editFormInputs.get('newHireDepartment').get('stringInputs').get('value')[0]
  newHireHiringManager = editFormInputs.get('newHireHiringManager').get('stringInputs').get('value')[0]
  
  # TODO: Verify newHireHiringManager (email-address) exists and has permissions (also in receiveDialog)
  
  users_ref.document(employeeID).update({
    "first": newHireFirstName,
    "last": newHireLastName,
    "dealership": newHireDealership,
    "department": newHireDepartment,
    "hiringManager": newHireHiringManager
  })

  doc_ref = users_ref.document(employeeID)
  doc = doc_ref.get()
  data = doc.to_dict()
  if data['status'] == "I_inprogress":
    edit_access_dialog = newHire_dialogs.editAccessDialog(employeeID)
    return edit_access_dialog

  return newHire_messages.valid_message
  
# TODO: include tags indicating if a checked box is True or inprogress  
def editAccessReceiveDialog(event: Mapping[str, Any]) -> Mapping[str, Any]:
  parameters = event.get('common').get('parameters')
  employeeID = parameters['employeeID']
  accesses_db_ref = accesses_db.stream()
  editAccessFormInputs = event.get('common').get('formInputs') # editAccessFormInputs = None, if none of the checkboxes are checked
  
  for access_type_db in accesses_db_ref:
    access_type_user = users_ref.document(employeeID).collection("accesses").document(access_type_db.id)
    access_type_user_ref = access_type_user.get().to_dict()
    try:
      access_type_formInput = editAccessFormInputs.get(access_type_db.id).get('stringInputs').get('value')
    except:
      try:
        access_type_user.update({key: False for key in access_type_db.to_dict().keys()})
      except Exception as e:
        print("ERROR: ",e)
      continue
    for key in access_type_db.to_dict().keys():
      if key in access_type_formInput and (access_type_user_ref[key] == True or access_type_user_ref[key] == "inprogress"):
        pass
      elif key not in access_type_formInput and (access_type_user_ref[key] == False):
        pass
      elif key not in access_type_formInput and (access_type_user_ref[key] == True):
        print(f"{key}: True => False")
        access_type_user.update({key: False})
      elif key not in access_type_formInput and (access_type_user_ref[key] == "inprogress"):
        print(f"{key}: inprogress => False")
        access_type_user.update({key: False})
      elif key in access_type_formInput and (access_type_user_ref[key] == False):
        print(f"{key}: False => inprogress")
        access_type_user.update({key: "inprogress"})
      else:
        print("ERROR: EDITACCESSRECEIVEDIALOG CHECKBOX IF STATEMENT SHOULD NOT REACH HERE.")

  return newHire_messages.valid_message
  
def access(request: Mapping[str, Any]) -> Mapping[str, Any]: 
  docs = (
    users_ref
    .where(filter = FieldFilter("status", "==", "I_inprogress_na"))
  )

  aggregate_query = aggregation.AggregationQuery(docs)
  aggregate_query.count(alias="all")
  results = aggregate_query.get()
  queryNum = int (results[0][0].value)
  access_dialog = newHire_dialogs.accessResponse(docs.stream(), queryNum)

  return access_dialog

def openAccessDialog(event: Mapping[str, Any]) -> Mapping[str, Any]:
  parameters = event.get('common').get('parameters') 
  return newHire_dialogs.openAccessDialog(parameters['employeeID'])
  
# TODO: Optimize setting values in db similar to editAccessReceiveDialog


def accessReceiveDialog(event: Mapping[str, Any]) -> Mapping[str, Any]:
  parameters = event.get('common').get('parameters')
  employeeID = parameters['employeeID'] 
  accessesFormInputs = event.get('common').get('formInputs')
  for accessType in accessesFormInputs:
    accessTypeFormInputs = accessesFormInputs.get(accessType).get('stringInputs').get('value')
    accesses_ref = users_ref.document(employeeID).collection("accesses")
    accesses_ref.set(collectionClass.access(False))
    accessType_ref = accesses_ref.document(accessType)
    for access in accessTypeFormInputs:
      accessType_ref.set({access: "inprogress"})
  users_ref.document(employeeID).update({"status": "I_inprogress"})
  return newHire_messages.valid_message
  
  

def progress(request: Mapping[str, Any]) -> Mapping[str, Any]: #TODO better UI in newHire_dialogs.py
  docs = (
    users_ref
    .where(filter = FieldFilter("status", "in", ["I_inprogress_na", "I_inprogress"]))
  )

  aggregate_query = aggregation.AggregationQuery(docs)
  aggregate_query.count(alias="all")
  results = aggregate_query.get()
  queryNum = int (results[0][0].value)
  progress_dialog = newHire_dialogs.progressResponse(docs.stream(), queryNum)

  return progress_dialog

def openDialog(request: Mapping[str, Any]) -> Mapping[str, Any]:
  return newHire_dialogs.open_dialog

def receiveDialog(event: Mapping[str, Any]) -> Mapping[str, Any]:
  newHireFormInputs = event.get('common').get('formInputs')
  newHireID = newHireFormInputs.get('newHireID').get('stringInputs').get('value')[0]
  newHireFirstName = newHireFormInputs.get('newHireFirst').get('stringInputs').get('value')[0]
  newHireLastName = newHireFormInputs.get('newHireLast').get('stringInputs').get('value')[0]
  newHireDealership = newHireFormInputs.get('newHireDealership').get('stringInputs').get('value')[0]
  newHireDepartment = newHireFormInputs.get('newHireDepartment').get('stringInputs').get('value')[0]
  newHireHiringManager = newHireFormInputs.get('newHireHiringManager').get('stringInputs').get('value')[0]
  
  allowedCharacterName = r"^[a-zA-Z.']+$"
  allowedCharacterEmail = r"^[a-zA-z.'@]+$"
  allowedDomains = ["bobbyrahal.com", "bobbyrahaltoyota.com", "bobbyrahallexus.com", 'bobbyrahalacura.com']
  
  # TODO: Verify newHireHiringManager (email) is a valid email address
  
  if not re.match(allowedCharacterName, newHireFirstName) or not re.match(allowedCharacterName, newHireLastName) or not re.match(allowedCharacterEmail, newHireHiringManager):
    return newHire_messages.invalidNumeric_message
  
  doc_ref = users_ref.document(newHireID)
  doc = doc_ref.get()
  
  if not newHireID or not newHireFirstName or not newHireLastName or newHireDealership == 'default' or newHireDepartment == 'default' or not newHireHiringManager:
    receiveInvalid_dialog = newHire_dialogs.receiveInvalidResponse(newHireID, newHireFirstName, newHireLastName, newHireDealership, newHireDepartment, newHireHiringManager)
    return receiveInvalid_dialog
  
  
  elif doc.exists:
    return newHire_messages.invalidExist_message

  users_ref.document(newHireID).set(collectionClass.newHireData(newHireFirstName, newHireLastName, 
                                                newHireDealership, newHireDepartment, 
                                                newHireHiringManager, "I_inprogress_na").to_dict())
  
  return newHire_messages.valid_message


    
  
