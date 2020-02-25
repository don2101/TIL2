## docker nginx 환경에서 django 앱 연결

### 1. Python, pip 설치

```bash
apt-get update
apt-get install python3
apt-get install python3-pip
```



### 2. uwsgi 설치 및 설정

```bash
# pip가 python에서 제공하는 pip와 다를 수 있으므로 pyhton과 연동하여 pip 업그레이드
python3 -m pip install --upgrade pip
pip3 install uwsgi
```



#### uwsgi 설정파일

```ini
# uwsgi.ini

[uwsgi]
project = test_app
# uwsgi 실행할 유저
username= root
base    = /root

### django settings
# base directory. django 프로젝트의 manage.py가 위치하는 폴더
chdir = /usr/share/nginx/html

# venv path. 가상환경을 사용하지 않는다면 comment
; home  = /usr/bin

# wsgi.py path. wsgi.py의 application 실행
module = test_app.wsgi:application

# nginx를 쓰지 않는다면 comment 처리
# http = 0.0.0.0:8000

master = true
processes = 5

uid = root
gid = root
socket = /run/uwsgi/test_app.sock
chown-socket = root:root
chmod-socket = 666
vaccum = true

logto = /var/log/uwsgi/text_app.log
```

- socket: Nginx와 함께 사용하기 위해 network port가 아닌 unix socket사용
- `socket`과 `logto`는 미리 폴더를 생성해야 한다.
- master: 마스터 프로세스 사용 엽부
- chown-socket: 소켓 소유자 (유저:그룹)



#### uwsgi 실행

```bash
uwsgi -i <uwsgi.ini 위치>
```



### 3. nginx 설정

#### default.conf

```bash
server {
	# default port
	listen 80;
	server_name <docker ip address>;
	
	location / {
		uwsgi_pass unix:<socket path>;
		include uwsgi_params;
	}
}
```

- location: `/` 로 들어오는 모든 요청을 설정한 경로로 보낸다.
  - 위 경우에는 서버로 들어온 요청을 `uwsgi_pass`로 지정된 socket에게 건네준다.
  - 그리고 `uwsgi`가 해당 socket으로 들어온 요청을 받아 django app에 전달
- uwsgi_params: `uwsgi` 관련 설정을 import



#### nginx.conf에서 주의할 점

- nginx 실행 유저를 반드시 `uwsgi`의 `chown-socket`에서 소켓 소유자(유저)와 일치시켜야 한다.
- 그렇지 않으면 nginx가 소켓에 접근하지 못하고, 소켓에 요청을 전달할 수 없다.
- nginx 관련 설정 파일을 변경한 이후에 반드시 nginx를 stop한 후 다시 실행해야 한다.



### 4. mysql container와 연동

- mysql 컨테이너 설치 후 실행



#### my.cnf

```cnf
[mysqld]
default_authentication_plugin=mysql_native_password
```

- mysql 8.0 이상은 인증 방식이 바뀌었다.
- 때문에 어플리케이션에서 접속하여 사용하는 경우 인증 방식을 기존의 인증방식으로 바꿔 사용해야 된다.



#### default 유저 인증 방식 설정

```mysql
ALTER USER "username"@'ip_address' IDENTIFIED WITH mysql_native_password by "password";
```

- 해당 유저의 인증을 `mysql_native_password` 방식으로 `password`를 받아 인증
- `ip_address`를 `%`로 설정할 경우 모든 ip를 통해 들어오는 경우를 의미한다.





