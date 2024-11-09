#! /bin/sh

echo "Installing crepo..."
CREPO_HOME=/opt/crepo
sudo mkdir -p $CREPO_HOME
sudo chown -R `whoami` $CREPO_HOME
git clone https://gitee.com/xingjianxu/crepo $CREPO_HOME
sudo ln -s $CREPO_HOME/bin/crepo /usr/bin/crepo

echo "Installing config-repo..."
CREPO_REPO=/.config-repo
sudo mkdir -p $CREPO_REPO
sudo chown -R `whoami` $CREPO_REPO
cd $CREPO_REPO
if [ -v CREPO_REPO_URL_GITHUB ]; then
  git clone https://github.com/$CREPO_REPO_URL_GITHUB $CREPO_REPO
elif [ -v CREPO_REPO_URL_GITEE ]; then
  git clone https://gitee.com/$CREPO_REPO_URL_GITEE $CREPO_REPO
elif [ -v CREPO_REPO_URL ]; then
  git clone $CREPO_REPO_URL $CREPO_REPO
else
  git init
fi
git config --global credential.helper store

echo "Successfully installed crepo!"