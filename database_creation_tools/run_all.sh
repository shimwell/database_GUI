
sudo mongod --fork --logpath $HOME/mongod.log

python3 database_creation_tools/rest_api_database_functions.py &

npm start

