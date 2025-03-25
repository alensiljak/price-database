# price-database

A simple Python library and a CLI for storage of prices

The purpose of this project is to provide a storage and means of accessing a price database. It can be reused among multiple projects.

The goal is very simple: separate a storage of prices of various elements (commodities) from other applications or components.

The Price object has several properties:

- unique identifier = uniquely identifies each record for ease of accessing
- namespace = distinguishes the namespace for the symbol. Often the exchange name.
- symbol = security/commodity symbol that identifies it within the namespace (exchange).
- date = The date of the price
- time = The time of the price
- value = Value in currency
- currency identifier = identifier for the currency. Can be anything the remote system is using.

With these, it should be possible to store prices for commodities used in GnuCash, GnuCash Portfolio, Asset Allocation and other similar financial packages.

## Installation

`pip install -e .`

Then manually copy the `data/prices-template.db` into `data/prices.db`.

## Running

`pricedb`

is a command-line interface to all the provided functionality.
Using Python, the PriceDbApplication class is the front-end, providing the same functionality through code.

Example:

`pricedb import data\AUD_2017-11-11_142445.csv AUD -v DEBUG`

## Logging

click-log package is used to provide log output. Simply enable by passing 

`-v LEVEL`

to the command line, where LEVEL is one of the logging levels. Use empty -v option for details.

## Distribution

Create .pypirc file in your profile directory, containing:

```
[distutils]
index-servers =
    pypi
    test

[pypi]
repository: https://upload.pypi.org/legacy/
username: ****
password: ****

[test]
repository: https://test.pypi.org/legacy/
username: ****
password: ****
```

### Test Site

```
python setup.py sdist upload -r test
```

### Production Site

```
python setup.py sdist upload -r pypi
```