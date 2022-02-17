-- Requêtes SQL de mise en forme des tables Cassandra
-- table_ab
SELECT event.event_id, pays, langue, annee_event, mois_event, jour_event, annee_mention, mois_mention, jour_mention, COUNT(*) AS total
FROM event, mentions
WHERE event.event_id = mentions.event_id
GROUP BY event.event_id, pays, langue, annee_event, mois_event, jour_event, annee_mention, mois_mention, jour_mention

-- table_c
SELECT source, theme, personne, lieu, annee, mois, jour, SUM(total) as total, SUM(somme_ton) as somme_ton
FROM gkg_c
GROUP BY source, theme, personne, lieu, annee, mois, jour

-- table_d
SELECT lieu, langue, annee, mois, jour, SUM(total) as total, SUM(somme_ton) as somme_ton
FROM gkg_d
GROUP BY lieu, langue, annee, mois, jour

-- Requêtes CQL de creation des tables
CREATE KEYSPACE production WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};

-- table_ab
CREATE TABLE table_ab (
    pays text,
    event_id int,
    annee_event int,
    mois_event int,
    jour_event int,
    annee_mention int,
    mois_mention int,
    jour_mention int,
    langue text,
    total bigint,
    PRIMARY KEY ((pays), event_id, annee_event, mois_event, jour_event, annee_mention,  mois_mention, jour_mention)
);

-- table_c
CREATE TABLE table_c (
    source text,
    theme text,
    personne text,
    lieu text,
    annee int,
    mois int,
    jour int,
    somme_ton double,
    total bigint,
    PRIMARY KEY ((source), theme, personne, lieu, annee, mois, jour)
);

-- table_d
CREATE TABLE table_d (
    lieu text,
    langue text,
    annee int,
    mois int,
    jour int,
    somme_ton double,
    total bigint,
    PRIMARY KEY ((lieu, langue), annee, mois, jour)
);

-- Requêtes CQL de réponse aux questions
-- a
SELECT pays, jour_mention, langue, total FROM table_ab WHERE pays='FR';

-- b
SELECT event_id, SUM(total) as compte
FROM table_ab
WHERE pays = 'input'
GROUP BY event_id, annee_event, mois_event, jour_event;

-- c
SELECT source, theme, personne, lieu, SUM(total) AS somme_total, SUM(somme_ton) AS somme_ton, jour -- mois, annee
FROM table_c
WHERE source = 'input'
GROUP BY theme, personne, lieu, annee; -- mois, jour

-- d
SELECT langue, lieu, SUM(total) AS somme_total, SUM(somme_ton) AS somme_ton
FROM table_d
WHERE langue = 'input1' AND lieu = 'input2'
GROUP BY annee; -- mois, jour
