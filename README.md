### 1. 准备数据库

```
sudo apt install postgresql

sudo su postgres
psql
create user lean with password '123456';
create database blog owner lean;
grant all on database blog to lean;
\q
```

### 2. 准备环境

```
pipenv install
pipenv shell
python manage.py db upgrade
python manage.py shell

# python
u = User()
u.email = '565743040@qq.com'
u.password = '123456'
u.nickname = 'lean'
db.session.add(u)
db.session.commit()
exit()
```

### 3. 准备nginx

```
sudo apt install nginx
sudo cp conf/nginx.conf /etc/nginx/sites-enabled/lean.code-my.life
sudo nginx -s reload
```

### 4. 运行app

```
pipenv run gunicorn -c conf/gunicorn.py app:app
```