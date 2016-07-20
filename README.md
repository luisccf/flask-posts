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
workon <name>
```
### Requirements
```
pip install -r requirements.txt
```
### Run application
```
python run.py
```
