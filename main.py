from typing import Any, Mapping
from google.cloud import firestore
import flask
import functions_framework
import json
import newHire_main
import collectionClass
import newHire_cards

@functions_framework.http

# TODO: Confirm who is accessing the application and what permissions they have
# TODO: Implement Date/Time & Who: Created, Modified

# Note: Terminated employeeID is not reused. If a terminated employee is rehired in a different building, the employeeID is different.
# If a terminated employee is rehired in the same building, the employeeID is the same.

# Next Steps:
# - Clean up the code
# - Separate into files to prepare for transfer & termination
# - Optimize the code
# - Webhook with Zammad IT ticketing system.


def main(req: flask.Request) -> Mapping[str, Any]:
  if req.method == 'GET':
    return 'Sorry, this function must be called from a Google Chat.'

  request = req.get_json(silent=True)
  if request.get('type') == 'MESSAGE':
    if slash_command := request.get('message', dict()).get('slashCommand'):
      command_id = slash_command['commandId']
      if command_id == '1':
        return newHire_main.openDialog(request)
      elif command_id == '2':
        return newHire_main.access(request)
      elif command_id == '3':
        return newHire_main.progress(request)
    else:
      return newHire_cards.help_card
    
  elif request.get('type') == 'CARD_CLICKED':
    invoked_function = request.get('common', dict()).get('invokedFunction')
    if invoked_function == 'newHireOpenDialog':
      return newHire_main.openDialog(request)
    elif invoked_function == 'newHireReceiveDialog':
      return newHire_main.receiveDialog(request)
    elif invoked_function == 'newHireAccess': 
      return newHire_main.access(request)
    elif invoked_function == 'openAccessDialog':
      return newHire_main.openAccessDialog(request)
    elif invoked_function == 'accessReceiveDialog':
      return newHire_main.accessReceiveDialog(request)
    elif invoked_function == 'newHireProgress':
      return newHire_main.progress(request)
    elif invoked_function == 'newHireEdit':
      return newHire_main.edit(request)
    elif invoked_function == 'editReceiveDialog':
      return newHire_main.editReceiveDialog(request)
    elif invoked_function == 'editAccessReceiveDialog': 
      return newHire_main.editAccessReceiveDialog(request)
  




  



