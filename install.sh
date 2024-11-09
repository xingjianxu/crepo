#! /bin/sh

echo "Installing crepo..."
CREPO_HOME=/opt/crepo
sudo mkdir -p $CREPO_HOME
sudo chown -R `whoami` $CREPO_HOME
git clone https://github.com/xingjianxu/crepo $CREPO_HOME
sudo ln -s $CREPO_HOME/bin/crepo /usr/bin/crepo

echo "Installing config-repo..."
CREPO_REPO=/.config-repo
sudo mkdir -p $CREPO_REPO
sudo chown -R `whoami` $CREPO_REPO
if [ -z "$1" ]; then
  git clone https://github.com/$1 $CREPO_REPO
fi

echo "Successfully installed crepo!"