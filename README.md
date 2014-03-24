# H2H Fantasy on sports.ru #

## Build & Run ##

```sh
$ sbt
> container:start
> browse
```

If `browse` doesn't launch your browser, manually open [http://localhost:8080/](http://localhost:8080/) in your browser.

## Deploy on Heroku ##

```sh
$ sbt package
> heroku deploy:war --war target/${SCALA_VERSION}/${APP_NAME}.war
 --app ${HEROKU_APP_NAME}
```