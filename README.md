# Silent Disco
Through our app, we are solving a very important issue - when people want to have a party but they cannot play loud music for some reason.

With Silent Disco, they will all be able to sync their devices and listen to the exact same song at the same time, on their own headphones - essentially permitting them to have a silent disco wherever they are.

[Test Here!](https://silent-disco-intensive.herokuapp.com)

## To Run
```bash
$ git clone https://www.github.com/omarsagoo/silent-disco-v1
$ cd silent-disco-v1
$ pip install -r requirements.txt
$ flask run
```
navigate to localhost:5000

## To Run with Docker
```bash
$ git clone https://www.github.com/omarsagoo/silent-disco-v1
$ docker build -t silent-disco-image .
$ docker run -p 5000:5000 --rm --name silent-disco-container silent-disco-image
```
navigate to localhost:5000
