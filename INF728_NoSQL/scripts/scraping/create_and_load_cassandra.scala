import org.apache.spark.sql.cassandra._
import com.datastax.spark.connector._
import com.datastax.spark.connector.cql.CassandraConnector
import java.io.FileWriter
import java.text.SimpleDateFormat
import java.util.Calendar

// définition du répertoire de stockage des données
val path = "hdfs://tp-hadoop-1:9000/data/"

// définition d'une fonction pour logger les évènements
val date_format = new SimpleDateFormat("[yyyy-MM-dd HH:mm:ss] ")
def now() :String = {date_format.format(Calendar.getInstance().getTime)}
def write_log(str:String) =  {
    val log = new FileWriter("cassandra_loading.log", true)
    println(now + str)
    log.write(now + str + "\n")
    log.close
}

write_log("started script on path " + path)

// chargement des fichiers dans des DF
write_log("loading table events ...")
val event = spark.read.format("csv").options(Map("header"->"true", "delimiter" -> "\t", "encoding" -> "ISO-8859-1", "inferSchema" -> "true")).load(path+"*.export.CSV.gz")
write_log("table events loaded")
write_log("loading table mentions ...")
val mentions = spark.read.format("csv").options(Map("header"->"true", "delimiter" -> "\t", "encoding" -> "ISO-8859-1", "inferSchema" -> "true")).load(path+"*.mentions.CSV.gz")
write_log("table mentions loaded")
write_log("loading table gkg_c ...")
val gkg_c = spark.read.format("csv").options(Map("header"->"true", "delimiter" -> "\t", "encoding" -> "ISO-8859-1", "inferSchema" -> "true")).load(path+"*.gkg.csv.gz")
write_log("table gkg_c loaded")
write_log("loading gkg_d  ...")
val gkg_d = spark.read.format("csv").options(Map("header"->"true", "delimiter" -> "\t", "encoding" -> "ISO-8859-1", "inferSchema" -> "true")).load(path+"*.gkg_d.csv.gz")
write_log("table gkg_d loaded")

// créationde vues pour interragir en SQL
write_log("creating SQL views ...")
event.createOrReplaceTempView("event")
mentions.createOrReplaceTempView("mentions")
gkg_c.createOrReplaceTempView("gkg_c")
gkg_d.createOrReplaceTempView("gkg_d")
write_log("SQL views created")

// définition de la requête SQL table_ab
val req_table_ab = """
SELECT event.event_id, pays, langue, annee_event, mois_event, jour_event, annee_mention, mois_mention, jour_mention, COUNT(*) AS total
FROM event, mentions
WHERE event.event_id = mentions.event_id
GROUP BY event.event_id, pays, langue, annee_event, mois_event, jour_event, annee_mention, mois_mention, jour_mention
"""

// execution de la requête sur le DF
val table_ab = spark.sql(req_table_ab)

// affichage de la table
//table_ab.show()

// creation de la nouvelle table
write_log("creating table table_ab ...")
table_ab.createCassandraTable("production", "table_ab", partitionKeyColumns = Some(Seq("pays")), clusteringKeyColumns = Some(Seq("event_id", "annee_event", "mois_event", "jour_event", "annee_mention", "mois_mention", "jour_mention")))
write_log("table table_ab created")

// insertion des valeurs dans la nouvelle table
write_log("inserting table table_ab ...")
table_ab.write.cassandraFormat("table_ab", "production", "").mode("append").save()
write_log("table table_ab inserted")

// définition de la requête SQL table_c
val req_table_c = """
SELECT source, theme, personne, lieu, annee, mois, jour, SUM(total) as total, SUM(somme_ton) as somme_ton
FROM gkg_c
GROUP BY source, theme, personne, lieu, annee, mois, jour
"""

// execution de la requête sur le DF
val table_c = spark.sql(req_table_c)

// creation de la nouvelle table
write_log("creating table table_c ...")
table_c.createCassandraTable("production", "table_c", partitionKeyColumns = Some(Seq("source")), clusteringKeyColumns = Some(Seq("theme", "personne", "lieu", "annee", "mois", "jour")))
write_log("table table_c created")

// insertion des valeurs dans la nouvelle table
write_log("inserting table table_c ...")
table_c.write.cassandraFormat("table_c", "production", "").mode("append").save()
write_log("table table_c inserted")

// définition de la requête SQL table_d
val req_table_d = """
SELECT lieu, langue, annee, mois, jour, SUM(total) as total, SUM(somme_ton) as somme_ton
FROM gkg_d
GROUP BY lieu, langue, annee, mois, jour
"""

// execution de la requête sur le DF
val table_d = spark.sql(req_table_d)

// creation de la nouvelle table
write_log("creating table table_d ...")
table_d.createCassandraTable("production", "table_d", partitionKeyColumns = Some(Seq("lieu", "langue")), clusteringKeyColumns = Some(Seq("annee", "mois", "jour")))
write_log("table table_d created")

// insertion des valeurs dans la nouvelle table
write_log("inserting table table_d ...")
table_d.write.cassandraFormat("table_d", "production", "").mode("append").save()
write_log("table table_d inserted")