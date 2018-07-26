## Documentation

 Its simple currency exchange apps with 2 model Currecny & Echange models.
 
#### 1. Requirements for this projects:  

 1. Docker
 2. Django 1.11
 3. Python 3.4.3
 


#### 2. Running projects:

 1. fist run `$docker build .` 	on command line
 2. After finish all pull and download, run `docker-compose run web python manage.py migrate`
 3. After finish all migrations, let's create superuser admin to access admin dashboard with run command: `$docker-compose run web python manage.py createsuperuser`
 4.  Then run `$docker-compose up` and apps will be running on host `0.0.0.0:8000/`
 5. Go to django admin on `http://0.0.0.0:8000/admin`, to create API Authentication with fill username & API Key here : `http://0.0.0.0:8000/admin/tastypie/apikey/add/`, this is for auth API


#### 3. API  
List all exchange with average for past week:

host : `localhost:8000/api/v1/`
username : {your_username}
apikey : {your_api_key}

##1. GET all exchange: 
Url: `localhost:8000/api/v1/exchange/?username={your_username}&api_key={your_api_key}`

Its will return data like this:


````
{
    "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 2
    },
    "objects": [
        {
            "average_rate": 2000,
            "currency_from": "1",
            "currency_to": "2",
            "date": "2018-09-28",
            "rate": "2000.00000000",
            "resource_uri": "/api/v1/exchange/1/"
        },
        {
            "average_rate": 0.0005,
            "currency_from": "2",
            "currency_to": "1",
            "date": "2018-09-28",
            "rate": "0.00050000",
            "resource_uri": "/api/v1/exchange/2/"
        }
    ]
}
````
Field Description:

1. `average_rate` : rate avegrage for past week
2. `currency_from` : currency origin
3. `currency_to` : currencey exchange
4. `rate` : rate for now


##2. [POST] Exchange:
url : `localhost:8000/api/v1/create-exchange/?username={your_username}&api_key={your_api_key}`

Example body post :

````
{
	"date": "2018-09-28",
	"currency_from": "USD",
	"currency_to": "EUR",
	"rate": 2000
}

````
Field Description:

1. `date`: date,
2. `currency_from`: For this field will automatically add to database currency if it's not exist before
3. `currency_to`: For this field will automatically add to database currency if it's not exist before
4. `rate`: will automatically calculate swap of currency exchange


