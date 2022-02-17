## Pour l'installation de Cassandra :
1. Lancer le script ```cassandra-install.sh```
2. Configurer le fichier ```cassandra.yaml``` *
3. Lancer le script ```cassandra-config.sh```

Le fichier ```cassandra.yaml``` correspond au fichier founi par défaut lors de l'installation de Cassandra dont les lignes suivantes ont été éditées :
```
# ligne 11 : nom du cluster
cluster_name: 'Cluster Group 2'

# ligne 426 : les noeuds graines. Les 3 première machines dans l'ordre numérique ont été utilisées
```seed_provider:
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
        - seeds: tp-hadoop-1, tp-hadoop-2, tp-hadoop-5


# ligne 613 : remplacer x par le numéro de la machine correspondante
listen_address: tp-hadoop-x

# ligne 690 : remplacer x par le numéro de la machine correspondante
rpc_address: tp-hadoop-x

# ligne 962 : la politique Snitch utilisée
endpoint_snitch: GossipingPropertyFileSnitch

```

## Pour l'installation de Spark :
1. Lancer le script ```spark-install.sh```
2. Lancer Spark depuis le master ```tp-hadoop-1``` :
```
start-master.sh
start-workers.sh 
```
3. Editer le fichier ```/opt/spark/conf/workers``` sur le master :
```
tp-hadoop-1
tp-hadoop-2
tp-hadoop-5
tp-hadoop-6
tp-hadoop-7
tp-hadoop-21
```
4. Pour lancer une shell Spark ou Pyspark, depuis n'importe quelle machine lancer la commande :
```
# pyspark
pyspark --deploy-mode client --master spark://tp-hadoop-1:7077 --conf spark.cassandra.connection.host=tp-hadoop-1 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 --conf spark.cassandra.input.consistency.level=ONE --conf spark.cassandra.output.consistency.level=ONE

# spark shell
spark-shell --deploy-mode client --master spark://tp-hadoop-1:7077 --conf spark.cassandra.connection.host=tp-hadoop-1 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 --conf spark.cassandra.input.consistency.level=ONE --conf spark.cassandra.output.consistency.level=ONE
```

## Pour l'installation de HADOOP/HDFS :
1. Lancer le script ```hadoop-install.sh```
2. Editer le fichier ```/opt/hadoop/etc/workers``` sur le master :
```
tp-hadoop-1
tp-hadoop-2
tp-hadoop-5
tp-hadoop-6
tp-hadoop-7
tp-hadoop-21
```
3. Modifier les fichiers de configuration sur toutes les machines :
   1. editer le fichier ```/opt/hadoop/etc/hadoop/hadoop-env.sh```:
   ```
   # ligne 55 : JAVA_HOME
   export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre

   # ligne 59 : HADOOP_HOME
   export HADOOP_HOME=/opt/hadoop

   # ligne 69 : HADOOP_CONF_DIR
   export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
   ```
   2. editer le fichier ```/opt/hadoop/etc/hadoop/core-site.xml```:
   ```
   <!-- à la fin du fichier -->
   <configuration>
     <property>
       <name>fs.defaultFS</name>
       <value>hdfs://tp-hadoop-1:9000</value>
     </property>
   </configuration>
   ```
   3. editer le fichier ```/opt/hadoop/etc/hadoop/hdfs-site.xml```:
   ```
   <!-- à la fin du fichier -->
   <configuration>
     <property>
       <name>dfs.namenode.name.dir</name>
       <value>file:///home/ubuntu/hadoop/data/namenode</value>
     </property>
     <property>
       <name>dfs.datanode.data.dir</name>
       <value>file:///home/ubuntu/hadoop/data/datanode</value>
     </property>
     <property>
       <name>dfs.replication</name>
       <value>2</value>
     </property>
   </configuration>
   ```
4. Formater HDFS et lancer le service depuis le master :
```
/opt/hadoop/bin/hdfs namenode -format
/opt/hadoop/sbin/start-dfs.sh
```
