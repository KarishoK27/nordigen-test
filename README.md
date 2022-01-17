# Nordigen Python Developer Task

AIS API implementation

Solution developed using Django and other technologies I am familiar with.

## Getting started

Create `.env` file using `.env.dist` template. Replace required values with your own. File content should be similar to this example:

```
DEBUG=False
SECRET_KEY=1234
HOST_ADDRESS=http://localhost:8000
API_BASE_URL=https://ob.nordigen.com
API_SECRET_ID=1234567
API_SECRET_KEY=abcdefg
BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379
```

## Run using docker-compose


```
docker-compose up
```

## Check the solution

If docker container with app is running on your local machine, simply open [localhost:8000](http://localhost:8000)
