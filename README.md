# Installation
## Requirements
### Python
For stable working need **version 3.11.5**

### Packages
Use **requirements.txt** for fast installation:
```
pip install -r requirements.txt
```

## Setting up the app
1. Remove **_example_** prefix from the name of the file **example_config.conf**
2. Into **config.conf** setup all the parts where have "change_me"
3. Change **time_delta** parameter if you need another time delta for refreshing weather (in hours)
4. Use **migration.py** for configure your database:
```
python migration.py
```

# Using
Use this command for start app:
```
python app.py
```


# Have a good day!