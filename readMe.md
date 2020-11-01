# Covid attestation generator

## Description
Generate and send by email a PDF attestation required by french gov to go out during confinement.
(Example of generated attestation)[example.pdf]
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
### Launch 
python3 ./main.py

### Reasons
In the attestation you can choose between 9 possible reasons of getting out [see example.pdf](example.pdf)
You can choose multiple reasons when calling the app  
Reasons are identified by a number according to their position in the list.
Example: 
1.  Déplacements entre le domicile et le lieu d'exercice de l'activité professionnelle ou un établissement
d'enseignement ou de formation...

2. Déplacements pour effectuer des achats de fournitures nécessaires à l'activité professionnelle,
des achats de première nécessité(3) dans des établissements dont les activités demeurent
autorisées...
3. ...

### Http call
Possible query params:
- firstname: used in the attestation
- lastname: used in the attestation
- birthdate: used in the attestation
- place_birth: used in the attestation
- sign_place: used in the attestation
- address: used in the attestation
- receiver_email: Recipient address of the attestation
- reasons: reasons to checked in the attestation (see reasons paragraph).
  Example: 1,2

For any unused param, the default config will be used  
Example:  
``` shell script
curl -X GET \
  'http://localhost:5050/get-attestation?reasons=1,2&firstname=John&lastname=Die&birthdate=01/01/2000&place_birth=Bayonne&sign_place=Paris&address=1%20rue%20de%20l%27%C3%A9glise,%2075015,%20Paris&receiver_email=john.doe@gmail.com' 