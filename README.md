# magdatacloud

## Installing dependencies

```shell
$ pip install -r requirements.txt
```

## How to run import_csv

You just need to call the management command we created in `import_csv.py`.  You do that by running:

1. Activate virtualenv in VS Code Terminal
2. `python manage.py import_csv --file-type=CUSTOMERS my_csv_file.csv`

And that will call `management/commands/import_csv.py` for you.