# Attendance Processor
[![<Attendance Processor>](https://circleci.com/gh/circleci/circleci-docs.svg?style=shield)](https://app.circleci.com/pipelines/github/Silvian/attendance-processor)

Romanian SDA Church Harlesden attendance google forms gsheets processor.

### Installation Guide

1. Clone the project.
2. Create a python3 virtual environment: `python3 -m venv venv`
3. Install all requirements: `pip install -r requirements.txt`
4. Configure cron job to run: `python processor.py` and `python cleaner.py` as needed.

### Tests

To run tests: `pytest`
