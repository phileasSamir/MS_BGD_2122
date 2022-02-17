# démarer spark sur le master uniquement :
# start-master.sh
# start-workers.sh 

# pour lancer une shell spark
spark-shell --deploy-mode client --master spark://tp-hadoop-1:7077 --conf spark.cassandra.connection.host=tp-hadoop-1 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 --conf spark.cassandra.input.consistency.level=ONE --conf spark.cassandra.output.consistency.level=ONE

