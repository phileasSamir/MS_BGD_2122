# depuis sa machine en état connecté au réseau de l'école
ssh -L 8080:localhost:8088 ubuntu@137.194.211.146

# depuis le bridge, remplace -21 par la machine souhaitée
ssh -L 8088:localhost:8888 ubuntu@tp-hadoop-21

# sur la machine de tp
jupyter notebook

# sur sa machine
firefox http://localhost:8080
