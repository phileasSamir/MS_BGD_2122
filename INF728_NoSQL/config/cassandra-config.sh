# cassandra-config.sh
cd

# avant toutes choses on stoppe le process
sudo service cassandra stop

# on on supprime les anciennes données
sudo rm -rf /var/lib/cassandra/data/system/*

# on sauvegarde l'ancienne config puis on copie la nouvelle
sudo mv /etc/cassandra/cassandra.yaml /etc/cassandra/cassandra.yaml.backup
sudo cp cassandra.yaml /etc/cassandra/cassandra.yaml

# on supprime l'ancienne topologie, cela ne sert que pour PropertyFileSnitch
sudo rm /etc/cassandra/cassandra-topology.properties

# on redémarre cassandra
sudo service cassandra start
