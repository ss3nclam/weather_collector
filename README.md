# GUID

## Installation and setting up the app

1. You have to download and install [**Docker**](https://www.docker.com/get-started/).
2. Download the [**Project**](https://github.com/ss3nclam/ex_test).
3. Open the project's folder.
1. Remove **_example_** prefix from the name of the file **example_config.conf**
2. Configure the file **config.conf**:
    * Setup all the parts from section **DATABASE**
    * Repeat the previous settings for db in _docker-compose.yml_ file.
    * Copy your OpenWeather token to **appid** parameter from section **OPEN_WEATHER_API**
    * Change **scheduler_time_delta** parameter in section **APP** if you need another time delta for refreshing weather (in hours).
    * Change **cities_limit** parameter if you need another count of cities _(default: 50)_.
3. From project folder run command:


```
docker-compose build
```

## Using the app


From project folder run command:
```
docker-compose up
```


# Have a good day!