:: Lint the whole App
@echo off
cls

pylint pricedb --output-format=colorized

::pause