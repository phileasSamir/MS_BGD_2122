# tp-hadoop-1, 2, 5, 6, 7, 21
# penser à autoriser l'execution du fichier :
# chmod +x cassandra-install.sh

cd

# installation de python et java version 8
sudo apt install -y python
sudo apt install -y openjdk-8-jdk

# téléchargement du fichier d'installation depuis le répo officiel
wget https://downloads.apache.org/cassandra/debian/pool/main/c/cassandra/cassandra_3.11.11_all.deb 

# installation du packet
sudo dpkg -i cassandra_3.11.11_all.deb

# suppression du fichier d'installation
rm cassandra_3.11.11_all.deb

# il reste encore à éditer le fichier cassandra.yaml
#sudo vim /etc/cassandra/cassandra.yaml

# puis lancer le script cassandra-config.sh
