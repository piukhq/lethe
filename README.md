# Lethe Setup
Clone the project and install dependencies
```
$ git clone git@gitlab.loyaltyangels.local:Olympus/lethe.git
$ virtualenv lethe_env
$ . ./lethe_env/bin/activate
$ pip install -r requirements.txt
```

Run the web server
```
$ ./manage.py runserver
```
Navigate to http://localhost:5000/ to check everything is working.

## Docker Configuration

### Environment Variables


- `HERMES_URL`
  - String Value, Hermes URL
- `LETHE_URL`
  - String Value, Lethe URL
