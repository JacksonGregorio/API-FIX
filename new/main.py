import time

from fix_api_client import FixApiClient

if __name__ == '__main__':
  fix_api_client = FixApiClient()

  print(f"Logon {fix_api_client.logon()}")

  time.sleep(.5)

  print(f"heartbeat: {fix_api_client.heartbeat()}")

  time.sleep(.5)

  print(f"test_request: {fix_api_client.test_request()}")

  time.sleep(.5)

  print(f"resend_request: {fix_api_client.resend_request()}")

  # time.sleep(.5)

  # print(f"reject: {fix_api_client.reject()}")

  time.sleep(.5)

  print(f"sequence_reset: {fix_api_client.sequence_reset()}")
  
  time.sleep(.5)

  print(f"logout: {fix_api_client.logout()}")
