# Covid attestation generator
Generate and send by email a PDF attestation required by french gov to go out during confinement.

Can be used through:
- http call
- Raspberry pin (soon)

## Requirements
### Dependency:
 - Python3
 - virtualenv (not mandatory but helpful)
### Mail setup
This app was mainly tested with gmail address

1. Create a gmail account (better to not use your usual one)
2. Allow external systems to use this address: [here](https://myaccount.google.com/lesssecureapps)
 
## Installation
```shell script
# create venv
virtualenv -p python3 .venv
# activate venv
source ./.venv/bin/activate
# install dependencies
pip install -r requirements.txt
```

## Config
Config is made through the file [config.yaml](config.yaml)  
You can either modify it or copy paste it and put the name of the new one in the env var `COVID_ATTEST_CONF_FILE`