#!/bin/sh
{
    HEROKU_CLIENT_URL="https://s3.amazonaws.com/assets.heroku.com/heroku-client/heroku-client.tgz"

    echo "This script requires superuser access to install software."
    echo "You will be prompted for your password by sudo."

    # clear any previous sudo permission
    sudo -k

    # run inside sudo
    sudo sh <<SCRIPT

  # download and extract the client tarball
  rm -rf /home/niranj/django-projects/onlinechess-project/venv/heroku
  mkdir -p /home/niranj/django-projects/onlinechess-project/venv/heroku
  cd /home/niranj/django-projects/onlinechess-project/venv/heroku

  if [ -z "$(which wget)" ]; then
    curl -s $HEROKU_CLIENT_URL | tar xz
  else
    wget -qO- $HEROKU_CLIENT_URL | tar xz
  fi

  mv heroku-client/* .
  rmdir heroku-client

SCRIPT
}
