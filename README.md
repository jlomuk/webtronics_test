# Poster backend service

### 1. Docker installation

- **Clone repo**

```sh
git clone https://github.com/jlomuk/webtronics_test
```

- **Move in directory "webtronics_test"**

```sh
cd webtronics_test
```

- **Copy .env file from .env.example in root directory**

```sh
cp .env.example .env
```

- **Start docker-compose**

```sh
docker-compose -f ./docker-compose.yaml up
```
*****
> ***After start docker containers, the site will be available on http://127.0.0.1:8000*** <br>
> ***Api documentation available on http://127.0.0.1:8000/docs*** <br>
> ***User service available on http://127.0.0.1:8000/api/v1/auth/*** <br>
> ***Post service available on http://127.0.0.1:8000/api/v1/post/*** <br> 

#
### 2. POSTMAN COLLECTION:

*Import and use [postman collections](https://www.postman.com/) for testing api*

```sh
webtronics_test/poster.postman_collection.json
```
