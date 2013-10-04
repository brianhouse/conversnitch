#!/usr/bin/env python3

import json, xmltodict
from housepy import config, log, util, strings
from lib import mturkcore

m = mturkcore.MechanicalTurk()

def create_hit(link):
    log.info("Creating HIT...")
    response = m.create_request('CreateHIT', {  'Title': "Transcribe 10 seconds of audio (WARNING: This HIT may contain adult content. Worker discretion is advised.)",
                                                'Description': "Listen to a 10 second audio clip and transcribe what is said.",
                                                'Reward': {'Amount': config['mturk']['payout'], 'CurrencyCode': "USD"},
                                                'AssignmentDurationInSeconds': config['lag'],
                                                'LifetimeInSeconds': config['lag'],
                                                'HITLayoutId': config['mturk']['layout_id'], 
                                                'HITLayoutParameter': {'Name': "link", 'Value': link},
                                                'AutoApprovalDelayInSeconds': 3600,
                                                })
    if not m.is_valid():
        log.error("--> failed: %s" % json.dumps(response, indent=4))
        return False
    try:
        hit_id = response['CreateHITResponse']['HIT']['HITId']
        log.info("--> created HIT %s" % hit_id)
        return hit_id
    except Exception as e:
        log.error(log.exc(e))
        return False


def retrieve_result(hit_id):
    response = m.create_request('GetAssignmentsForHIT', {'HITId': hit_id})
    if not m.is_valid():
        log.error("Request failed: %s" % response)
        return None
    try:
        answer = response['GetAssignmentsForHITResponse']['GetAssignmentsForHITResult']        
        if 'Assignment' not in answer:
            log.info("--> not answered yet")
            return None
        answer = xmltodict.parse(answer['Assignment']['Answer'])
        answer = answer['QuestionFormAnswers']['Answer']
        struct = {}
        for part in answer:
            if part['FreeText'] is None:
                continue
            struct[part['QuestionIdentifier']] = part['FreeText'].strip().replace("&#13;", "").replace('"', "").replace("&lt;", "<").replace("&gt;", ">")
        return struct
    except Exception as e:
        log.error("Response malformed: (%s) %s" % (log.exc(e), json.dumps(response, indent=4)))
        return None


if __name__ == "__main__":
    # hit_id = create_hit("http://google.com")
    # print(hit_id)
    struct = retrieve_result("2YYYQ4J3NAB9ZQFXU3PYLT1TUPMQD3")
    print(struct)


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


"""

