set -x

sudo apt update

sudo apt install python-pip python3-venv

pushd ../

python3 -m venv converter-venv

popd

. ena.sh

pushd ../

pip install -r requirements.txt

popd

set +x
