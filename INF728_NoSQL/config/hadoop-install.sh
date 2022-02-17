# tp-hadoop-1, 2, 5, 6, 7, 21
# penser à autoriser l'execution du fichier :
# chmod +x hadoop-install.sh

cd

# téléchargement du fichier d'installation depuis le site officiel
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz

# décompression de l'archive
tar -xvzf hadoop-3.3.1.tar.gz

# suppression du fichier
rm hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /opt/hadoop

# mise à jour du /opt/hadoop/etc/hadoop/hadoop-env.sh
#vim /opt/hadoop/etc/hadoop/hadoop-env.sh

# mise à jour du /opt/hadoop/etc/hadoop/core-site.xml
#vim /opt/hadoop/etc/hadoop/core-site.xml

# mise à jour du /opt/hadoop/etc/hadoop/hdfs-site.xml
#vim /opt/hadoop/etc/hadoop/hdfs-site.xml

mkdir -p /home/ubuntu/hadoop/data

# sur le master uniquement :
# mise à jour du /opt/hadoop/etc/workers
#vim /opt/hadoop/etc/workers
#/opt/hadoop/bin/hdfs namenode -format
#/opt/hadoop/sbin/start-dfs.sh
#/opt/hadoop/bin/hdfs dfsadmin -report
