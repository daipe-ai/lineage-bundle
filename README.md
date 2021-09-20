# Lineage bundle

**This package is distributed under the "DataSentics SW packages Terms of Use." See [license](https://raw.githubusercontent.com/daipe-ai/lineage-bundle/master/LICENSE.txt)**

Lineage bundle allows you to generate and publish lineage of notebooks and notebook functions of your __Daipe__ project.

## Getting started

### Add _lineage-bundle_ to your project
```yaml
poetry add lineage-bundle --dev
```

### Generate and publish lineage to a static HTML
```bash
console lineage:publish:html
```

## Optional:

#### To use a databaase: add _sqlalchemybundle.yaml_ file to `[PROJECT_NAME]/_config/bundles/`
```yaml
parameters:
  sqlalchemybundle:
    connections:
      default:
        engine: mssql
        server: '%env(DB_HOST)%'
        database: '%env(DB_NAME)%'
        username: '%env(DB_USER)%'
        password: '%env(DB_PASS)%'
        driver: '{ODBC Driver 17 for SQL Server}'
```
#### In _.env_ in your Daipe project

```yaml
APP_ENV=dev

# Databricks
DBX_TOKEN=
# Lineage
DB_HOST=address.of.mssql.server.com
DB_NAME=db_name
DB_USER=username
DB_PASS=password
```

#### Initialize the database
```bash
console lineage:database:init
```

#### Generate and publish lineage to database
```bash
console lineage:publish:database
```

## Preview
### Pipelines lineage
![Example lineage](https://raw.githubusercontent.com/daipe-ai/lineage-bundle/master/static/lineage.png)
### Functions lineage
![Example lineage](https://raw.githubusercontent.com/daipe-ai/lineage-bundle/master/static/lineage-functions.png)
