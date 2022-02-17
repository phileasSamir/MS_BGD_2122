# tp-hadoop-1, 2, 5, 6, 7, 21
# penser à autoriser l'execution du fichier :
# chmod +x spark-install.sh

cd

# téléchargement du fichier d'installation depuis le site officiel
wget https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz

# décompression de l'archive
tar -xvzf spark-3.2.0-bin-hadoop3.2.tgz

# suppression du fichier
rm spark-3.2.0-bin-hadoop3.2.tgz
sudo mv spark-3.2.0-bin-hadoop3.2 /opt/spark

# mise à jour du ~/.profile pour avoir les bonnes variables d'environnement
echo "export SPARK_HOME=/opt/spark" >> ~/.profile
echo "export PATH=$PATH:/opt/spark/bin:/opt/spark/sbin" >> ~/.profile
echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.profile
source ~/.profile

# définition du master
cp /opt/spark/conf/spark-env.sh.template /opt/spark/conf/spark-env.sh
echo "SPARK_MASTER_HOST=tp-hadoop-1" >> /opt/spark/conf/spark-env.sh

# editer la liste des workers sur le master
# vim /opt/spark/conf/workers

# démarer spark sur le master uniquement :
# start-master.sh
# start-workers.sh 

# pour lancer une shell pyspark
# pyspark --deploy-mode client --master spark://tp-hadoop-1:7077 --conf spark.cassandra.connection.host=tp-hadoop-1 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 --conf spark.cassandra.input.consistency.level=ONE --conf spark.cassandra.output.consistency.level=ONE
