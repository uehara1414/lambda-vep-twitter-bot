pip install -U -r requirements.txt -t ./vendor
zip -r lambda-package.zip *.py vendor client_secret.json
