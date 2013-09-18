#!/usr/bin/env python3

import json, xmltodict
from housepy import config, log, util, strings
from lib import mturkcore

m = mturkcore.MechanicalTurk()

def create_hit():
    response = m.create_request('CreateHIT', {  'Title': "Transcribe 10 seconds of audio (WARNING: This HIT may contain adult content. Worker discretion is advised.)",
                                                'Description': "Listen to a 10 second audio clip and transcribe what is said.",
                                                'Reward': {'Amount': 0.05, 'CurrencyCode': "USD"},
                                                'AssignmentDurationInSeconds': 3*60,
                                                'LifetimeInSeconds': 5*60,                                                                            
                                                'HITLayoutId': config['mturk']['layout_id'], 
                                                'HITLayoutParameter': {'Name': "link", 'Value': "http://test.com"},
                                                })
    if not m.is_valid():
        log.error("Request failed: %s" % response)
        return    
    print(json.dumps(response, indent=4))
    # retrieve hit
    if m.is_valid():
        print("--> success")    
    else:
        print("failed")


def retrieve_result():
    response = m.create_request('GetAssignmentsForHIT', {'HITId': "2ACHYW2GTP9RA5UWMPS6CYSOP30SN4"})
    if not m.is_valid():
        log.error("Request failed: %s" % response)
        return
    try:
        answer = response['GetAssignmentsForHITResponse']['GetAssignmentsForHITResult']['Assignment']['Answer']
        tokens = strings.strip_html(answer).split('\n')
        for token in tokens:
            if len(token) == 0 or token == "summary":
                continue
            answer = token
            break
        print(answer)
    except Exception as e:
        log.error("Response malformed: (%s) %s" % (log.exc(e), response))


retrieve_result()

"""
{
    "CreateHITResponse": {
        "OperationRequest": {
            "RequestId": "38c6e751-ce27-4126-8d97-0a7202d35905"
        }, 
        "HIT": {
            "Request": {
                "IsValid": "True"
            }, 
            "HITId": "2ACHYW2GTP9RA5UWMPS6CYSOP30SN4", 
            "HITTypeId": "2IIC6SK9RJ85OXKQ4KDADPMOOE64S7"
        }
    }
}

{
    "GetAssignmentsForHITResponse": {
        "OperationRequest": {
            "RequestId": "8b22554e-386c-4297-81f2-3e8ded87f40f"
        }, 
        "GetAssignmentsForHITResult": {
            "Request": {
                "IsValid": "True"
            }, 
            "NumResults": "1", 
            "TotalNumResults": "1", 
            "PageNumber": "1", 
            "Assignment": {
                "AssignmentId": "2DGH1XERSQV66PNG7LK3KVWAW1G08S", 
                "WorkerId": "A2TM28MRAA0LLD", 
                "HITId": "2ACHYW2GTP9RA5UWMPS6CYSOP30SN4", 
                "AssignmentStatus": "Submitted", 
                "AutoApprovalTime": "2013-10-18T04:22:35Z", 
                "AcceptTime": "2013-09-18T04:22:27Z", 
                "SubmitTime": "2013-09-18T04:22:35Z", 
                "Answer": "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<QuestionFormAnswers xmlns=\"http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd\">\n<Answer>\n<QuestionIdentifier>summary</QuestionIdentifier>\n<FreeText>This is my transcription, which involves elephants and shaving cream.</FreeText>\n</Answer>\n</QuestionFormAnswers>"
            }
        }
    }
}



Retrieve the HITId, then we need to check up on it later.

Make sure hits are automatically accepted and paid within the same interval as the expiration. This will then essentially be the lag time.

"""

