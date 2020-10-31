# Covid attestation generator

## Description
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

## Usage
### Http call
Possible query params:
- firstname: used in the attestation
- lastname: used in the attestation
- birthdate: used in the attestation
- place_birth: used in the attestation
- sign_place: used in the attestation
- address: used in the attestation
- receiver_email: Recipient address of the attestation

For any unused param, the default config will be used  
Example:  
``` shell script
curl -X GET \
  'http://localhost:5050/get-attestation?firstname=John&lastname=Die&birthdate=01/01/2000&place_birth=Bayonne&sign_place=Paris&address=1%20rue%20de%20l%27%C3%A9glise,%2075015,%20Paris&receiver_email=john.doe@gmail.com'