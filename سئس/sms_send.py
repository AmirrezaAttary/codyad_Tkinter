from kavenegar import *
try:
    api = KavenegarAPI('3936466A51684633482B34396E5541532F66585A455958385036674E54796A52694530396A48766E6574413D')
    params = {
        'sender': '2000500666',#optional
        'receptor': '09330570810',#multiple mobile number, split by comma
        'message':'دست خر',
    } 
    response = api.sms_send(params)
    print(response)
except APIException as e: 
    print(e)
except HTTPException as e: 
    print(e)