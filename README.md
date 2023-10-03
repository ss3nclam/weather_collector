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
2. Configure the file **config.conf**:
    * Setup all the parts where have "change_me"
    * Change **time_delta** parameter if you need another time delta for refreshing weather (in hours)
    * Change **logs_to_file** on **false** if you don't need to write logs to logs' folder
3. Use **migration.py** for configure your database:
```
python migration.py
```

# Using
Use this command for start app:
```
python app.py
```


# Have a good day!