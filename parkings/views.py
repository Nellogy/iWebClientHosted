import json

import requests
from django.shortcuts import render, redirect

weatherURL = 'https://api.openweathermap.org/data/2.5/weather?id=2514256&appid=a616b07331d06ea639f3b99c87ef5830&units=metric&lang=es'
apiURL = 'https://ingenieriaweb-260616.appspot.com/api/v1/'
current_user_id = ''


def index(request):
    try:
        weatherResponse = requests.get(weatherURL)
        weatherData = weatherResponse.json()

        # TODO: user end point on AppEngine
        userResponse = requests.get(apiURL + 'users/byUserId/' + current_user_id)
        userData = userResponse.json()

        parkingsResponse = requests.get(apiURL + 'openData/parkings')
        parkingsData = parkingsResponse.json()

        locationsResponse = requests.get(apiURL + 'openData/locations')
        locationsData = json.dumps(locationsResponse.json()['features'])
        i = 1
        availableSpots = 0
        totalSpots = 0
        parkingList = []

        for item in parkingsData:
            aux = ''
            info = item['availableSpotNumber']['value']

            if info == str(-1) or info is None:
                aux = 'N/A'
            else:
                aux = info
                availableSpots += int(info)
                totalSpots += int(item['totalSpotNumber']['value'])

            parkingList.append({'id': i,
                                'parking': item['name']['value'],
                                'available': aux,
                                'address': item['description']['value'],
                                })
            i += 1

        context = {
                   'weather': weatherData['weather'][0]['description'],
                   'temperature': str(weatherData['main']['temp']) + 'ºC',
                   'humidity': str(weatherData['main']['humidity']) + '%',
                   'user_name': userData[0]['full_name'],
                   'parkingList': parkingList,
                   'counter': i - 1,
                   'totalSpots': totalSpots,
                   'availableSpots': availableSpots,
                   'locationsData': locationsData,
                   }

        return render(request, 'parking/parkingsPage.html', context)

    except Exception as e:
        print('not valid username')
        raise e


def details(request, idParking):
    try:
        weatherResponse = requests.get(weatherURL)
        weatherData = weatherResponse.json()

        # TODO: user end point on AppEngine
        userResponse = requests.get(apiURL + 'users/byUserId/' + current_user_id)
        userData = userResponse.json()

        parkingResponse = requests.get(apiURL + 'openData/parking/' + str(idParking))
        parkingData = parkingResponse.json()

        locationResponse = requests.get(apiURL + 'openData/location/' + str(idParking))
        locationData = locationResponse.json()

        context = {
            'weather': weatherData['weather'][0]['description'],
            'temperature': str(weatherData['main']['temp']) + 'ºC',
            'humidity': str(weatherData['main']['humidity']) + '%',
            'user_name': userData[0]['full_name'],
            'id': idParking,
            'name': parkingData['name']['value'],
            'requiredPermit': parkingData['requiredPermit']['value'],
            'allowedVehicleType': parkingData['allowedVehicleType']['value'],
            'availableSpotNumber': parkingData['availableSpotNumber']['value'],
            'totalSpotNumber': parkingData['totalSpotNumber']['value'],
            'description': parkingData['description']['value'],
            'longitude': locationData['geometry']['coordinates'][0],
            'latitude': locationData['geometry']['coordinates'][1],
        }
        return render(request, 'parking/parkingDetails.html', context)

    except Exception as e:
        print('not valid username')
        raise e


def startLogin(request, user_id):

    global current_user_id

    try:
        # TODO: user end point on AppEngine
        userResponse = requests.get(apiURL + 'users/byUserId/' + user_id)
        userData = userResponse.json()

        current_user_id = userData[0]['user_id']
        valid_user = current_user_id != ''

    except Exception as e:
        print('not valid login ID')
        raise e

    return redirect('https://iwebclient-host-16.herokuapp.com/parkings/')


def userInfo(request):
    try:
        # TODO: user end point on AppEngine
        userResponse = requests.get(apiURL + 'users/byUserId/' + current_user_id)
        userData = userResponse.json()

        context = {
            'user_id': userData[0]['user_id'],
            'user_name': userData[0]['full_name'],
        }

        return render(request, 'parking/userInfo.html', context)

    except Exception as e:
        print('not valid username')
        raise e


def logOut(request):
    global current_user_id
    current_user_id = ''
    return render(request, 'parking/mainView.html')
