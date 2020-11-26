# Lethe Setup
Clone the project and install dependencies
```bash
git clone os.path.dirname(
pipenv install --dev
```

Run the web server
```bash
pipenv run ./manage.py runserver
```
Navigate to http://localhost:5000/ to check everything is working.

## Docker Configuration

### Environment Variables

- `LETHE_DEBUG`
  - Bool Value, `"True"` or `"False"`, sets up Flask debugger
- `HERMES_URL`
  - String Value, Hermes URL
- `LETHE_URL`
  - String Value, Lethe URL
- `EXTERNAL_SERVER_NAME`
  - String value, URL to use when generating URLs
- `EXTERNAL_SERVER_NAME`
  - String value, URL to use when generating URLs
- `SENTRY_DSN`
  - String value, Sentry DSN, automatically read by Sentry
- `SENTRY_ENVIRONMENT`
  - String value, Sentry environment, automatically read by Sentry
