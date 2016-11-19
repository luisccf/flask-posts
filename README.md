# flask-posts
### MySQL Server
```
mysql.server start
```
If there is an error regarding updating PID files, run
```
chmod -R 777 /usr/local/var/mysql/
```
to change read and write permissions.
### Virtual Environment
With virtualenvwrapper installed, run
```
mkvirtualenv <name>
```
### Environment variables
Add env variables to ```$HOME/.virtualenvs/<env-name>/bin/activate```
```
FP_DATABASE_URI='mysql+pymysql://<db-user>:<db-password>@localhost/<db-schema>'
export FP_DATABASE_URI

FP_SECRET_KEY=<secret-key>
export FP_SECRET_KEY
```
Then reactivate the virtual environment
### Requirements
```
pip install -r requirements.txt
```
### Run application
```
python run.py
```
