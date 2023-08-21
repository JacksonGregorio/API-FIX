import time

from fix_api_client import FixApiClient

if __name__ == '__main__':
  fix_api_client = FixApiClient()

  print(fix_api_client.logon())

  time.sleep(.5)

  print(fix_api_client.heartbeat())

  time.sleep(.5)

  print(fix_api_client.test_request())

  time.sleep(.5)

  print(fix_api_client.resend_request())

  time.sleep(.5)

  print(fix_api_client.reject())

  time.sleep(.5)

  print(fix_api_client.sequence_reset())
  
  time.sleep(.5)

  print(fix_api_client.logout())
