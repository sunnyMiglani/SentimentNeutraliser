portID=8082
echo "--- Connecting to Jupyter Notebook port $portID ---"

ssh -N -L $portID:localhost:$portID oracle
