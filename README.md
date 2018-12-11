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
u.email = '15622342848@163.com'
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

### 4. 线上运行app

```
pipenv shell
export BLOG_ENV='production'
python manage.py shell

# 创建用户用于登录编辑器
u = User()
u.email = '15622342848@163.com'
u.password = '123456'
u.nickname = 'lean'
db.session.add(u)
db.session.commit()
exit()

pipenv run gunicorn -c conf/gunicorn.py app:app
```
