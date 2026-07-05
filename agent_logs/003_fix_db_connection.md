# Task: Fix Database Connection

## Files Modified

### `docker-compose.yml`

- Changed the port mapping from `"5432:5432"` to `"5433:5432"`.

```diff
-      - "5432:5432"
+      - "5433:5432"
```

### `config/settings.py`

- Updated the `DATABASES` dictionary to use port `5433`.

```diff
-             'PORT': '5432',
+             'PORT': '5433',
```

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
docker-compose down
docker-compose up -d
Start-Sleep -s 5
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
