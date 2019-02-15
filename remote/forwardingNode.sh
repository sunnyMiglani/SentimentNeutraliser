computeIP=10.139.1.19
echo --- Forwarding node! $computeIP ---
ssh -N -4 -L 8082:localhost:8082 $computeIP
