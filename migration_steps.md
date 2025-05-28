## Step 1: Create a new database for leases licensing

```
CREATE DATABASE leaseslicensing_dev;
CREATE USER leaseslicensing_dev WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE "leaseslicensing_dev" to leaseslicensing_dev;
\c leaseslicensing_dev
CREATE EXTENSION postgis;
GRANT ALL ON ALL TABLES IN SCHEMA public TO leaseslicensing_dev;
GRANT ALL ON SCHEMA public TO leaseslicensing_dev;
\q
```

## Step 2: Migrate the auth and ledger api client apps

```
./manage.sh migrate auth &&
./manage.sh migrate ledger_api_client
```

## Step 2: Apply the admin migration patch

```
export virtual_env_path=$(poetry env info -p) &&
export python_version=$(python -c 'import sys; print(str(sys.version_info[0])+"."+str(sys.version_info[1]))') &&
patch $virtual_env_path/lib/python$python_version/site-packages/django/contrib/admin/migrations/0001_initial.py 0001_initial.py.patch
```

_Note: this step creates two environment variables which are used in subsequent steps_

## Step 3: Migrate the admin app

```
./manage.sh migrate admin
```

## Step 4: Reverse the admin migration patch

```
patch -R $virtual_env_path/lib/python$python_version/site-packages/django/contrib/admin/migrations/0001_initial.py 0001_initial.py.patch
```

## Step 5: Apply the reversion migration patch

```
patch $virtual_env_path/lib/python$python_version/site-packages/reversion/migrations/0001_squashed_0004_auto_20160611_1202.py 0001_squashed_0004_auto_20160611_1202.py.patch

```

## Step 6: Migrate the reversion app

```
./manage.sh migrate reversion

```

## Step 7: Reverse the reversion migration patch

```
patch -R $virtual_env_path/lib/python$python_version/site-packages/reversion/migrations/0001_squashed_0004_auto_20160611_1202.py 0001_squashed_0004_auto_20160611_1202.py.patch

```

## Step 8: Run the rest of the migrations

```
./manage.sh migrate

```

## Step 9 Apply required fixtures

```
./manage.sh loaddata \
    approvaltype.json \
    approvaltypedocumenttype.json \
    approvaltypedocumenttypeonapprovaltype.json \
    default_standard_requirements.json \
    details_text.json \
    groups.json \
    lgas.json \
    regions.json \
    districts.json

```
