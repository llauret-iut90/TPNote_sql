DROP TABLE IF EXISTS emprunt;
DROP TABLE IF EXISTS exemplaire;
DROP TABLE IF EXISTS oeuvre;
DROP TABLE IF EXISTS auteur;
DROP TABLE IF EXISTS adherent;


CREATE TABLE adherent
(
    id_adherent   INT NOT NULL AUTO_INCREMENT,
    nom           VARCHAR(50),
    adresse       VARCHAR(50),
    date_paiement DATE,
    PRIMARY KEY (Id_adherent)
);

CREATE TABLE auteur
(
    id_auteur INT NOT NULL AUTO_INCREMENT,
    nom       VARCHAR(50),
    prenom    VARCHAR(50),
    PRIMARY KEY (id_auteur)
);

CREATE TABLE oeuvre
(
    id_oeuvre     INT NOT NULL AUTO_INCREMENT,
    titre         VARCHAR(255),
    date_parution DATE,
    photo         VARCHAR(50),
    auteur_id     INT NOT NULL,
    PRIMARY KEY (id_oeuvre),
    FOREIGN KEY (auteur_id) REFERENCES auteur (id_auteur)
);

CREATE TABLE exemplaire
(
    id_exemplaire INT NOT NULL AUTO_INCREMENT,
    etat          VARCHAR(50),
    date_achat    DATE,
    prix          VARCHAR(50),
    oeuvre_id     INT NOT NULL,
    PRIMARY KEY (id_exemplaire),
    FOREIGN KEY (oeuvre_id) REFERENCES oeuvre (id_oeuvre)
);

CREATE TABLE emprunt
(
    adherent_id   INT,
    exemplaire_id INT,
    date_emprunt  DATE,
    date_retour   DATE,
    PRIMARY KEY (adherent_id, exemplaire_id, date_emprunt),
    FOREIGN KEY (adherent_id) REFERENCES adherent (id_adherent),
    FOREIGN KEY (exemplaire_id) REFERENCES exemplaire (id_exemplaire)
);

INSERT INTO auteur (id_auteur, nom, prenom)
VALUES (1, 'Christie', 'Agatha'),
       (2, 'Chateaubriand', 'François-René'),
       (3, 'Flaubert', 'Gustave'),
       (4, 'Prévert', 'Jacques'),
       (5, 'De La Fontaine', 'Jean'),
       (6, 'Daudet', 'Alphonse'),
       (7, 'Hugo', 'Victor'),
       (8, 'Kessel', 'Joseph'),
       (9, 'Duras', 'Marguerite'),
       (10, 'Proust', 'Marcel'),
       (11, 'Zola', 'Émile'),
       (12, 'Highsmith', 'Patricia'),
       (13, 'Kipling', 'Rudyard'),
       (14, 'Azimov', 'Isaac'),
       (15, 'Baudelaire', 'Charles');
INSERT INTO auteur (id_auteur, nom, prenom) VALUE
    (16, 'Moliere', 'Jean-Baptiste Poquelin');

/* 23 oeuvres */
/* pas de 5*/
INSERT INTO oeuvre (id_oeuvre, titre, date_parution, photo, auteur_id)
VALUES (1, 'le retour de Poirot', '1960-02-12', 'leRetourDePoirot.jpg', 1);
INSERT INTO oeuvre (id_oeuvre, titre, date_parution, photo, auteur_id)
VALUES (2, 'Poirot quitte la scène', '1975-05-01', '', 1);
INSERT INTO oeuvre (id_oeuvre, titre, date_parution, photo, auteur_id)
VALUES (3, 'dix brèves rencontres', '1982-10-01', 'dixBrevesRencontres.jpg', 1),
       (4, 'le miroir de la mort', '1961-01-01', 'leMiroirDuMort.jpeg', 1),
       (6, 'une créature de rêve', '1992-02-01', '', 12),
       (7, 'mémoire d\'outre-tombe', '1949-01-01', '', 2),
       (8, 'Madame de Bovary', '1956-12-15', '', 3);
INSERT INTO oeuvre (id_oeuvre, titre, date_parution, photo, auteur_id)
VALUES (9, 'un amour de swam', '2004-06-01', 'unAmourDeSwann.jpeg', 9),
       (10, 'les femmes savantes', '1672-03-16', '', 16),
       (11, 'le misanthrope', '1666-01-01', '', 16),
       (12, 'Les fleurs du mal', '1957-06-25', 'lesFleursDuMal.jpg', 15),
       (13, 'petits poèmes en prose', '1969-01-01', NULL, 15),
       (14, 'les mondes perdus', '1980-05-06', 'lesMondesPerdus.jpg', 14),
       (15, 'La guerre des mondes', '1970-03-15', '', 14),
       (16, 'spectacles', '1948-05-12', '', 4),
       (17, 'Les fables', '1694-01-01', '', 5);
INSERT INTO oeuvre (id_oeuvre, titre, date_parution, photo, auteur_id)
VALUES (18, 'Le triomphe de l\'amour', '1980-05-06', '', 5),
       (19, 'le livre de la jungle', '1968-12-11', '', 13),
       (20, 'kim', '1901-07-01', '', 13),
       (21, 'le marin de Gibraltar', '1952-07-12', '', 9),
       (22, 'l’assommoir', '1976-01-01', '', 11),
       (23, 'j\'accuse', '1898-01-13', '', 11),
       (24, 'la terre', '1887-01-01', '', 11);


INSERT INTO exemplaire (id_exemplaire, etat, date_achat, prix, oeuvre_id)
VALUES (1, 'BON', '2022-08-25', '13.50', 1),
       (2, 'MOYEN', '2015-09-28', '12.50', 1),
       (3, 'MOYEN', '2022-05-26', '12.00', 1),
       (4, 'BON', '2015-01-11', '10.00', 1),
       (5, 'MAUVAIS', '2021-10-29', '13.00', 2),
       (6, 'NEUF', '2022-10-29', '20.00', 2),
       (7, 'BON', '2021-12-27', '7.00', 3),
       (8, 'MOYEN', '2021-09-25', '13.00', 3),
       (9, 'NEUF', '2015-12-29', '18.00', 4),
       (10, 'NEUF', '2015-12-29', '21.00', 4),
       (11, 'BON', '2015-04-29', '26.00', 4),
       (12, 'BON', '2022-01-24', '22.00', 6),
       (13, 'BON', '2022-01-24', '22.00', 6),
       (14, 'BON', '2022-05-01', '28.00', 7),
       (15, 'MAUVAIS', '2022-01-26', '28.00', 7),
       (16, 'BON', '2022-01-24', '30.00', 8),
       (17, 'BON', '2022-01-23', '32.00', 9),
       (18, 'MAUVAIS', '2015-01-29', '17.00', 10),
       (19, 'BON', '2021-10-29', '18.00', 10),
       (20, 'BON', '2021-10-29', '18.00', 10),
       (21, 'BON', '2021-10-29', '19.00', 10),
       (22, 'BON', '2022-01-26', '20.00', 11),
       (23, 'BON', '2022-10-29', '21.50', 12),
       (24, 'MAUVAIS', '2022-01-24', '22.00', 13),
       (25, 'BON', '2015-01-28', '22.00', 13),
       (26, 'MAUVAIS', '2022-01-23', '26.00', 14),
       (27, 'MOYEN', '2015-12-26', '13.00', 14),
       (28, 'BON', '2022-02-23', '12.00', 15),
       (29, 'BON', '2022-10-29', '15.00', 15),
       (30, 'MAUVAIS', '2022-01-26', '32.00', 16),
       (31, 'BON', '2022-01-23', '19.00', 17),
       (32, 'MAUVAIS', '2017-10-29', '19.00', 17),
       (33, 'BON', '2021-01-23', '20.00', 19),
       (34, 'BON', '2022-01-25', '11.00', 19),
       (35, 'MAUVAIS', '2021-10-29', '15.00', 19),
       (36, 'NEUF', '2022-10-29', '18.00', 19),
       (37, 'BON', '2022-01-23', '8.00', 19),
       (38, 'MAUVAIS', '2021-09-28', '18.00', 20),
       (39, 'BON', '2021-12-26', '18.00', 20),
       (40, 'BON', '2022-01-23', '11.00', 20);


INSERT INTO adherent (id_adherent, nom, adresse, date_paiement)
VALUES (1, 'billot', 'Montbeliard', '2022-11-03'),
       (2, 'lauvernay', 'sevenans', '2022-06-13'),
       (3, 'axelrad', 'sevenans', '2022-01-12'),
       (4, 'bedez', 'hericourt', '2022-04-17'),
       (5, 'berger', 'les glacis', '2013-11-03'),
       (6, 'cambot', 'sevenans', '2022-12-15'),
       (7, 'bonilla', 'sochaux', '2022-02-17'),
       (8, 'asproitis', 'grenoble', '2022-12-04'),
       (9, 'pereira', 'danjoutin', '2022-11-03'),
       (10, 'dupont', 'grenoble', '2022-03-14'),
       (11, 'durant', 'belfort', '2022-12-16'),
       (12, 'piton', 'belfort', '2022-11-03');

INSERT INTO emprunt (adherent_id, exemplaire_id, date_emprunt, date_retour)
VALUES (6, 2, '2022-09-21', '2022-09-28'),
       (7, 2, '2022-10-21', '2022-10-28'),
       (8, 2, '2022-11-21', '2022-11-28'),
       (3, 3, '2022-09-13', NULL),
       (2, 4, '2022-12-01', NULL),
       (2, 5, '2022-08-23', '2022-09-23'),
       (2, 5, '2022-12-15', NULL),
       (3, 5, '2022-07-26', '2022-08-23'),
       (3, 5, '2022-11-23', '2022-12-24'),
       (4, 6, '2023-01-22', '2023-01-23'),
       (4, 6, '2023-01-25', NULL),
       (3, 7, '2023-02-22', '2023-03-29'),
       (2, 8, '2022-12-30', NULL),
       (3, 9, '2023-01-25', NULL),
       (8, 9, '2022-07-26', '2022-09-22'),
       (3, 11, '2023-01-26', '2023-02-21'),
       (3, 13, '2023-01-04', NULL),
       (6, 15, '2022-09-23', '2022-09-26'),
       (2, 18, '2022-09-23', '2022-10-28'),
       (2, 19, '2023-02-26', NULL),
       (4, 19, '2022-09-21', NULL),
       (4, 27, '2023-02-22', NULL),
       (3, 33, '2023-01-30', NULL),
       (4, 34, '2023-01-23', '2023-02-20'),
       (2, 35, '2022-07-13', '2022-09-21'),
       (2, 37, '2023-02-11', NULL),
       (7, 38, '2022-07-26', '2022-10-22'),
       (2, 40, '2023-01-23', '2023-02-23'),
       (3, 40, '2022-11-23', '2022-12-24'),
       (5, 40, '2022-07-25', '2022-09-22'),
       (9, 15, '2023-02-22', NULL),
       (9, 18, '2023-01-30', NULL);



# SELECT * FROM oeuvre;

# SELECT exemplaire.id_exemplaire AS noExemplaire, exemplaire.date_achat, exemplaire.etat, exemplaire.oeuvre_id, exemplaire.id_exemplaire, oeuvre.date_parution, exemplaire.prix
#     FROM exemplaire
#     LEFT JOIN emprunt ON exemplaire.id_exemplaire=emprunt.exemplaire_id
#     INNER JOIN oeuvre ON oeuvre.id_oeuvre=exemplaire.oeuvre_id
#     WHERE oeuvre_id=14

# SELECT oeuvre.id_oeuvre,
#        oeuvre.titre,
#        DATE_FORMAT(oeuvre.date_parution, '%d/%m/%Y') AS date_parution,
#        oeuvre.photo,
#        auteur.nom,
#        COUNT(exemplaire.id_exemplaire)               AS nbExemplaire,
#        COUNT(E2.id_exemplaire)                       AS nb_exemp_dispo
# FROM oeuvre
#          INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur
#          LEFT JOIN exemplaire ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
#          LEFT JOIN emprunt ON exemplaire.id_exemplaire = emprunt.exemplaire_id
#          LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = exemplaire.id_exemplaire
#     AND E2.id_exemplaire NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
# GROUP BY oeuvre.id_oeuvre, oeuvre.titre, oeuvre.date_parution, oeuvre.photo, auteur.nom
# ORDER BY auteur.nom

# SELECT oeuvre.id_oeuvre AS noOeuvre,
#        oeuvre.titre,
#        oeuvre.date_parution,
#        oeuvre.photo,
#        auteur.nom,
#        COUNT(exemplaire.id_exemplaire)               AS nb_exemplaire,
#        COUNT(E2.id_exemplaire)                       AS nb_exemp_dispo
# FROM oeuvre
#          INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur
#          LEFT JOIN exemplaire ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
#          LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = exemplaire.id_exemplaire
#     AND E2.id_exemplaire NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
# WHERE exemplaire.oeuvre_id = 1
# GROUP BY oeuvre.id_oeuvre, oeuvre.titre, oeuvre.date_parution, oeuvre.photo, auteur.nom
# ORDER BY auteur.nom;

# SELECT oeuvre.id_oeuvre AS noOeuvre, oeuvre.titre, oeuvre.date_parution, oeuvre.photo, auteur.nom, COUNT(exemplaire.id_exemplaire) AS nb_exemplaire, COUNT(emprunt.date_retour) AS nb_exemp_dispo
#     FROM oeuvre
#     INNER JOIN auteur ON oeuvre.auteur_id=auteur.id_auteur
#     INNER JOIN exemplaire ON oeuvre.id_oeuvre=exemplaire.oeuvre_id
#     LEFT JOIN emprunt ON exemplaire.id_exemplaire=emprunt.exemplaire_id
#     WHERE exemplaire.oeuvre_id=%s
#
#
# SELECT *
# FROM exemplaire;
#
# SELECT COUNT(exemplaire.id_exemplaire) AS nb_exemplaire FROM exemplaire WHERE oeuvre_id=1


-- A changer dans le code
# SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre, oeuvre.date_parution AS date_parution_iso
#         , COALESCE (oeuvre.photo, '') AS photo
#         , COUNT(E1.id_exemplaire) AS nb_exemplaire
#         , COUNT(E2.id_exemplaire) AS nb_exemp_dispo
#         , CONCAT(LPAD(CAST(DAY(oeuvre.date_parution)AS CHAR(2)),2,0),'/',LPAD(MONTH(oeuvre.date_parution), 2, '0'),'/', YEAR(oeuvre.date_parution))
#         AS date_parution
#         FROM oeuvre
#         JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
#         LEFT JOIN exemplaire AS E1 ON E1.oeuvre_id = oeuvre.id_oeuvre
#         LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = E1.id_exemplaire
#         AND E2.id_exemplaire
#         NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
#         WHERE oeuvre.id_oeuvre=%s
#         GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
#         ORDER BY auteur.nom ASC, oeuvre.titre ASC;
#
# -- ancien
# SELECT oeuvre.id_oeuvre,
#        oeuvre.titre,
#        DATE_FORMAT(oeuvre.date_parution, '%d/%m/%Y') AS date_parution,
#        oeuvre.photo,
#        auteur.nom,
#        COUNT(exemplaire.id_exemplaire)               AS nb_exemplaire,
#        COUNT(E2.id_exemplaire)                       AS nb_exemp_dispo
# FROM oeuvre
#          INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur
#          LEFT JOIN exemplaire ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
#          LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = exemplaire.id_exemplaire
#     AND E2.id_exemplaire NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
# GROUP BY oeuvre.id_oeuvre, oeuvre.titre, oeuvre.date_parution, oeuvre.photo, auteur.nom
# ORDER BY auteur.nom

# SELECT exemplaire.id_exemplaire,
#        exemplaire.date_achat,
#        exemplaire.etat,
#        exemplaire.oeuvre_id,
#        exemplaire.id_exemplaire,
#        oeuvre.date_parution,
#        exemplaire.prix,
#        COUNT(E1.id_exemplaire)                        AS ExemplaireDispo,
#        IF(E1.id_exemplaire IS NULL, 'abs', 'present') AS present
# FROM exemplaire
#          LEFT JOIN emprunt ON exemplaire.id_exemplaire = emprunt.exemplaire_id
#          INNER JOIN oeuvre ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
#          LEFT JOIN exemplaire AS E1 ON E1.id_exemplaire = exemplaire.id_exemplaire
#     AND E1.id_exemplaire
#                                            NOT IN
#         (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
# WHERE exemplaire.oeuvre_id = 1
# GROUP BY exemplaire.id_exemplaire, exemplaire.date_achat, exemplaire.etat, exemplaire.oeuvre_id,
#          exemplaire.id_exemplaire, oeuvre.date_parution, exemplaire.prix

# +--------------+-------+------------+-------+---------------------+----------+--------------+-----------------+---------+
# | noExemplaire | etat  | date_achat | prix  | titre               | noOeuvre | dateParution | ExemplaireDispo | present |
# +--------------+-------+------------+-------+---------------------+----------+--------------+-----------------+---------+
# |            2 | MOYEN | 2015-09-28 | 12.50 | le retour de Poirot |        1 | 1960-02-12   |               2 | present |
# |            1 | BON   | 2022-08-25 | 13.50 | le retour de Poirot |        1 | 1960-02-12   |               1 | present |
# |            4 | BON   | 2015-01-11 | 10.00 | le retour de Poirot |        1 | 1960-02-12   |            NULL | abs     |
# |            3 | MOYEN | 2022-05-26 | 12.00 | le retour de Poirot |        1 | 1960-02-12   |            NULL | abs     |
# +--------------+-------+------------+-------+---------------------+----------+--------------+-----------------+---------+

# SELECT exemplaire.id_exemplaire,
#        oeuvre.titre,
#        oeuvre.id_oeuvre,
#        exemplaire.date_achat,
#        exemplaire.etat,
#        exemplaire.oeuvre_id,
#        exemplaire.id_exemplaire,
#        oeuvre.date_parution,
#        exemplaire.prix,
#        COUNT(E1.id_exemplaire)                        AS ExemplaireDispo,
#        IF(COUNT(E1.id_exemplaire) IS NULL, 'abs', 'present') AS present
# FROM exemplaire
#          LEFT JOIN emprunt ON exemplaire.id_exemplaire = emprunt.exemplaire_id
#          INNER JOIN oeuvre ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
#          LEFT JOIN exemplaire AS E1 ON E1.id_exemplaire = exemplaire.id_exemplaire
#     AND E1.id_exemplaire
#                                            NOT IN
#         (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
# WHERE exemplaire.id_exemplaire = 45
# GROUP BY exemplaire.id_exemplaire, exemplaire.date_achat, exemplaire.etat, exemplaire.oeuvre_id,
#          exemplaire.id_exemplaire, oeuvre.date_parution, exemplaire.prix;

