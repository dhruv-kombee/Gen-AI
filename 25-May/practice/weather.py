import requests
cityn=input("Enter the City name : ")
cityname=cityn.lower()


try:
    res=requests.get(f"https://wttr.in/{cityname}?format=j1")
    code=res.status_code
    if code==200:
        data=res.json()
        temp=int(data["current_condition"][0]["temp_C"])
        desc=data["current_condition"][0]["weatherDesc"][0]["value"]
        humidity=data["current_condition"][0]["humidity"]
        def get_temperature(temp):
            if temp<=15:
                return "Cold Environment"
            elif temp>15 and temp<=30:
                return "Warm Environment"
            elif temp>30:
                return "Hot Environment"
            else:
                return "Unable to find the Environment"
        print("\n------ Weather Report ------")
        print(f"City: {cityname}")
        print(f"Temperature: {temp}°C")
        print(f"Environment: {get_temperature(temp)}")
        print(f"Weather: {desc}")
        print(f"Humidity: {humidity}%")
    elif code==404:
        print("There is no city with that name")
    else:
        print("Error in the API")

except requests.exceptions.RequestException:
    print("Internet connection or request error")
    
except Exception as e:
    print("Something went wrong:",e)