import json
import datetime
import os
from urllib.parse import urlparse
import requests

def rHandle(s, b):
  return json.dumps({
    "statusCode": s,
    "body": {
      "message": b
    }
  })

def action_list(request):
	r = request.get_json()
    
	response = """
        {
       	"integrations": [{
       		"name": "beeceptortester",
          "label": "Beeceptor Tester",
       		"description": "everything to beeceptor endpoint for testing",
       		"supported_action_types": ["query","cell","dashboard"],
       		"url": "https://us-central1-graphic-theory-197904.cloudfunctions.net/beeceptor-action-hub/execute",
       		"form_url": "https://us-central1-graphic-theory-197904.cloudfunctions.net/beeceptor-action-hub/action_form",
          "icon_data_uri": "data:image/png;base64,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",
        	"required_fields": [{"tag": "beeceptor-test"}],
          "params": [{
       			"name": "testuser",
       			"label": "User Attribute Test",
       			"required": true
       		}]
       	}]
       }
	"""
	return response

def action_form(request):
  request_json = request.json
  form = {
    "name": "endpoint",
    "label": "Beeceptor Endpoint",
    "description": "Type the beeceptor endpoint you would like to test. e.g, https://action-testing.free.beeceptor.com",
    "type": "text",
    "required": True
  }
  return json.dumps([form])

def execute_action(r):
  request_json = r.json
  if r.path == '/action_list':
    return action_list(r)
  elif r.path == '/action_form':
    return action_form(r)
  else:
    endpoint = request_json['form_params']['endpoint']
    req = requests.post(endpoint, json=request_json)
    return rHandle(200,"ok")
