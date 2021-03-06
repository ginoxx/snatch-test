# Snatch Test

Python, Flask, SQLite, Docker

# Requirements
[docker](https://www.docker.com/get-docker)

docker-compose

# Usage
Clone this repository
```
git clone https://github.com/ginoxx/snatch-test.git
cd snatch-test
```
Run docker-compose
```
docker-compose up --build
```

Test localhost app is working in browser by navigating to
```
http://localhost:5000/
```

# Test endpoints
Use curl or browser REST client (I use YARC Chrome extension)

Register user
```
curl -H "Content-Type: application/json" -X POST localhost:5000/users -d '{"username": "snatch", "email": "snatch@domain.com", "phone": "1111111111"}'
```

Update location

Assumption: Coordinates are passed as parameter, for a given user.

Coordinates are in decimal degrees (London, Tower Hill)
```
curl -H "Content-Type: application/json" -X POST localhost:5000/location -d '{"username": "snatch", "lat": "51.510153", "lon": "-0.076507"}'
```

List user details
```
curl -H "Content-Type: application/json" -X GET localhost:5000/users/snatch
```
