#!/usr/bin/env python3

import json
from housepy import config, log, util
from lib import mturkcore

m = mturkcore.MechanicalTurk()
# m.create_request("GetAccountBalance")
# response = m.create_request('CreateHIT', {  'HITTypeId': util.timestamp(), 
#                                             'HITLayoutId': config['mturk']['layout_id'], 
#                                             'HITLayoutParameter': {'name': "link", 'value': "http://test.com"},
#                                             'LifetimeInSeconds': 5*60,                                
#                                             })

response = m.create_request('CreateHIT', {  'Title': "Transcribe 10 seconds of audio (WARNING: This HIT may contain adult content. Worker discretion is advised.)",
                                            'Description': "Listen to a 10 second audio clip and transcribe what is said.",
                                            'Reward': {'Amount': 0.05, 'CurrencyCode': "USD"},
                                            'AssignmentDurationInSeconds': 3*60,
                                            'LifetimeInSeconds': 5*60,                                                                            
                                            'HITLayoutId': config['mturk']['layout_id'], 
                                            'HITLayoutParameter': {'Name': "link", 'Value': "http://test.com"},
                                            })

print(json.dumps(response, indent=4))
if m.is_valid():
    print("--> success")    
else:
    print("failed")