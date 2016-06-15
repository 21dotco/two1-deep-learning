# A tutorial for using 21 with Django and Heroku

See the tutorial at [https://21.co/learn/django-heroku/](https://21.co/learn/django-heroku/)

## Quick deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/21dotco/two1-django-heroku/tree/master)

If you clone this repository directly (and don't use one of the tagged
releases) note that `ALLOWED_HOSTS` is set to a wildcard to enable the
quick-deploy button above. For security purposes you should change this to your
specific domain, and note that it's only enforced when DEBUG mode is off.
