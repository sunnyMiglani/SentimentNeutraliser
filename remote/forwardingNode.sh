computeIP=$1
echo --- Forwarding node! $computeIP ---
ssh -N -4 -L 8082:localhost:8082 $computeIP
