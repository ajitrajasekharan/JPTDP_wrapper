pip install cython numpy
pip install dynet==2.0.3
pip install gdown
echo "Fetching model"
./fetch_model.sh
echo "Run run_server.sh to start service"

echo "In a new shell, Change directory to POS_wrappaer to run_server.sh to also  start service required for NER"

