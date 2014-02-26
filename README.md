ponysynth
=========

A web synthetizer based on PySynth, Flask and Google App Engine
Boilerplate via github.com/kamalgill/flask-appengine-template

Setup
-------------------
1. Set the application id in `src/app.yaml`
2. Add the secret keys for CSRF protection by running the `generate_keys.py`
   script at `application/generate_keys.py`, which will generate the
   secret keys module at application/secret_keys.py
3. Install python dependancies: pip install -r requirements_dev.txt
4. Run the app: dev_appserver.py .
5. Test: export FLASK_CONF=TEST then python tests/apptest.py .
6. Deploy: appcfg.py update .

