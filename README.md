# Store
Online store - test project

## Setup the project locally

Create env
```bash
python3 -m venv venv
```

Activate environment
```bash
. venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

Create DB
```bash
touch db.sqlite3
```

Apply migrations
```bash
./manage.py migrate
```

Run project
```bash
./manage.py runserver
```


## Curl request examples

Create products:
- products can only be created by superuser through admin page

Register new user
```bash
curl -XPOST -H "Content-type: application/json" -d '{
"email": "test@ex.com",
"password": "Qwerty@123"
}' 'http://127.0.0.1:8000/authentication/signup/'
```

Login (save token from response to use in another requests)
```bash
curl -XPOST -H "Content-type: application/json" -d '{
"email": "test@ex.com",
"password": "Qwerty@123"
}' 'http://127.0.0.1:8000/authentication/login/'
```

Get list of products
```bash
curl -XGET -H 'Authorization: Token {{token}}' -H "Content-type: application/json" 'http://127.0.0.1:8000/product/'
```

Create order
```bash
curl -XPOST -H 'Authorization: Token {{token}}' -H "Content-type: application/json" -d '{"product": 1}' 'http://127.0.0.1:8000/order/'
```

Pay for order
```bash
curl -XPOST -H 'Authorization: Token {{token}}' -H "Content-type: application/json" 'http://127.0.0.1:8000/order/{{order_id}}/pay/'
```
