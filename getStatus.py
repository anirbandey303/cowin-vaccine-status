from cowin_api import CoWinAPI
import json
import time
import requests

class Cowin:
  def notifyUsers(self):
    # will send notification to users that vaccine is available
    print("Vaccine Found!!!")
    with open("telegram.params", 'r') as file:
      data = file.read()
    text = "Vaccine Found!!!"
    base_url = data + '\"{}\"'.format(text)
    response = requests.get(base_url)
    return response

  def checkForVaccine(self):
    district_id = '725' # We can make it to pass it as parameters.
    date = '10-05-2021'  # Optional. Takes today's date by default
    min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit

    cowin = CoWinAPI()
    available_centers = cowin.get_availability_by_district(district_id, date, min_age_limit)
    
    # print(json.dumps(available_centers))
    #print(available_centers)
    #print(available_centers["centers"][0]["name"])
    #print(len(available_centers["centers"]))
    # print(len(available_centers["centers"][0]["sessions"]))
    # print(available_centers["centers"][0]["sessions"][3]["date"])
    # available_centers["centers"][0]["sessions"][1]["available_capacity"] = 1
    
    for i in range(len(available_centers["centers"])):
      print(available_centers["centers"][i]["name"]) # Prints the name of the hospital
      for j in range(len(available_centers["centers"][i]["sessions"])):
        print('\t',available_centers["centers"][i]["sessions"][j]["date"]) #Prints the date
        print('\t',available_centers["centers"][i]["sessions"][j]["available_capacity"],'\n') #Prints the quantity available
        available_capacity = available_centers["centers"][i]["sessions"][j]["available_capacity"] # assigning it to variable, it's too lang!

        if(available_capacity > 0):
          try:
            response = self.notifyUsers()
          except Exception as err:
            print(f'Some error while notifying users: {err}')

obj = Cowin()
while True:
  obj.checkForVaccine()
  named_tuple = time.localtime() # get struct_time
  time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
  print(time_string," : Press 'Ctrl + C' to exit...")
  time.sleep(30)
