import ghasedak_sms
sms_api = ghasedak_sms.Ghasedak('1db7668768563cfeab73d905e36f5b665fdf18cca3588a53ab401f76fc89b312eNDxttZcHSLBg8az')
response = sms_api.send_single_sms({'message':'hello, world!', 'receptor':'09330570810', 'linenumber':'09330570810'})
print(response)