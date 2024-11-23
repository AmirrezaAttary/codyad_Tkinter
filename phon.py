# from kavenegar import *
# api = KavenegarAPI('3936466A51684633482B34396E5541532F66585A455958385036674E54796A52694530396A48766E6574413D')
# params = { 'sender' : '1000689696', 'receptor': '09330570810', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
# response = api.sms_send(params)

import kavenegar

api = kavenegar.KavenegarAPI("3936466A51684633482B34396E5541532F66585A455958385036674E54796A52694530396A48766E6574413D") # Replace with your API key

try:
  params = {
    'receptor': '09330570810', #Recipient phone number
    'sender': '1000689696',    # Your Kavenegar sender ID
    'message': 'Test message',
  }
  response = api.sms_send(params)
  print(response) # Check the response from the API
except kavenegar.APIException as e:
  print(f"Error: {e}")
except Exception as e:
  print(f"An unexpected error occurred: {e}")

