portID=8082
echo "--- Connecting to BlueCrystal 3's port $portID ---"

ssh -N -L $portID:localhost:$portID bc3
