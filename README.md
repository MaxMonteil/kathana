# Kathana

Simple project using the Asana API to generate and send a progress report.

## Table of Contents

* [Getting Started](#getting-started)
	* [Prerequisites](#prerequisites)
	* [Installing](#installing)
* [Deployment](#deployment)
* [Built With](#built-with)
* [License](#license)

## Getting Started

### Prerequisites

To install it you will need to have [pipenv](https://pipenv.readthedocs.io/en/latest/) installed.

Additionally you are going to need a Personal Access Token from Asana. You can find out how to do that from their API quickstart page [here](https://asana.com/developers/documentation/getting-started/quick-start).

Once you have your PAT, create a copy of the env file named `.env` and add your token.

```
.env
ASANA_TOKEN=<your-asana-token>
```

### Installing

```
git clone git@github.com:MaxMonteil/kithana.git
cd kithana
pipenv install
```

Run the program with `pipenv run python kathana.py`

## Deployment

### Coming Soon

* [AWS Lambda](https://aws.amazon.com/lambda)

## Built With

* [python-asana](https://github.com/Asana/python-asana/)

### Coming Soon

* [Yagmail](https://github.com/kootenpv/yagmail)
* [Telegram Bot](https://core.telegram.org/bots/api)

## License

This project is licensed under the MIT License.
