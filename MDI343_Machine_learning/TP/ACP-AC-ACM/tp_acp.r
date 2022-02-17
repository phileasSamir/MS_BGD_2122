library(ade4)
library(FactoMineR)

#' ### Températures
temperature <-
  read.table("http://factominer.free.fr/book/temperature.csv",
             header=TRUE,sep=";",dec=".",row.names=1)

class(temperature)
names(temperature)
rownames(temperature)
dim(temperature)
plot(as.numeric(temperature[1,1:12]), ylim= range(temperature[,1:12]))
lines(as.numeric(temperature[2,1:12]))
lines(as.numeric(temperature[3,1:12]), col="red")
lines(as.numeric(temperature[4,1:12]), col="blue")
res <- PCA(temperature,ind.sup=24:35,quanti.sup=13:16,quali.sup=17)
plot.PCA(res,choix="ind",habillage=17)
#' L'axe 1 semble représenter l'axe nord/sud, tandis que l'axe 2 représente plutôt un axe est/ouest.
dimdesc(res)
#' Les variables les plus corrélées à la composante 1 sont les températures annuelles, de septembre et d'octobre.
#' Les variables les plus corrélées à la composante 2 sont l'amplitude des températures, la longitude et le mois de juin.
res$eig
#' Les deux premières composantes expliquent plus de 98% de la variance des données (resp. 83, 15).
#' On peut donc ignorer les axes suivants.
plot.PCA(res, choix = c("ind"),
         invisible=c("ind.sup", "quali", "quanti.sup"))
#' Deux capitales représentatives de l'axe 1, resp. valeur minimale et maximale : Reykjavik et Athènes.
#' Deux capitales représentatives de l'axe 2, resp. valeur minimale et maximale : Reykjavik et Moscou.
plot.PCA(res, choix = c("ind"), invisible = c("ind"))
res$ind.sup
#' Deux villes n'étant pas des capitales représentatives de l'axe 1 : Saint-Pétersbourg et Séville.
#' Deux villes n'étant pas des capitales représentatives de l'axe 2 : Saint-Pétersbourg et Édimbourg.
plot.PCA(res, choix = "var")
res$var
#' Les mois qui contribuent le plus à l'inertie de l'axe 1 : octobre, septembre, avril.
#' Les mois qui contribuent le plus à l'inertie de l'axe 2 : juin, janvier, juillet.
res$quanti.sup
#' Les variables "annual" et "latitude" peuvent être rattachées à l'axe 1.
#' Les variables "amplitude" et "longitude" peuvent être rattachées à l'axe 2.
res$quali.sup
plot.PCA(res, choix = "ind", invisible = c("ind", "ind.sup"))
#' La catégorie "East" est plus corrélée à la composante 2 qu'à la composante 1. Cette corrélation est positive.
#' En se basant sur les composantes de l'ACP, on peut prédire que janvier sera négativement corrélé avec amplitude.   
#' Typologie sommaire des températures en Europe :   
#' - Au nord, il fait froid ; au sud, il fait chaud.  
#' - Certaines villes subissent une plus grande amplitude de températures, càd des températures très froides en hiver et très chaudes en été.
#' Ces villes ont tendance à se situer à l'est, tandis que les villes occidentales ont des amplitudes de températures moindres.   
#' ### Jeux olympiques
data(JO)
apply(JO, 1, sum)
resJO <- CA(JO)
summary(resJO)
## profils lignes
rowprof <- JO / apply(JO, 1, sum)
apply(rowprof,1,sum)
## profils colonnes
colprof <- t(t(JO) / apply(JO, 2, sum)) #t() : transposee
apply(colprof,2,sum)
round(resJO$eig,1)
#' Il faudrait garder 6 dimensions pour expliquer plus de 50% de la variance (54.7%)
chisq.test(JO)
#' ???
resJO$row$coord
n <- sum(JO)
rowW <- apply(JO,1,sum)/n
rowW
colW <- apply(JO,2,sum)/n
colW
sum(resJO$row$coord[,"Dim 1"]*rowW)
sum(resJO$row$coord[,"Dim 2"]*rowW)
#' Le barycentre des projections des profils lignes sur les deux premiers axes est le vecteur nul.
var(resJO$row$coord[,"Dim 1"]) == resJO$eig["dim 1", "eigenvalue"]
#' La variance pondérée des coordonnées des lignes sur le premier axe est égal à la première valeur propre.
cor(resJO$row$coord[,"Dim 1"],resJO$row$coord[,"Dim 2"])
#' Justification théorique du résultat
resJO$row$contrib[,1] == resJO$row$coord[,"Dim 1"]*rowW*resJO$eig["dim 1", "eigenvalue"]
#' On retrouve la contribution.
plot.CA(resJO, invisible="col")
#' L'axe 1 semble représenter les épreuves d'endurance (valeurs négatives -> épreuves longues, valeurs positives -> épreuves rapides), à l'exception des épreuves 20 et 50 km
#' L'axe 2 semble représenter la "partie du corps" impliquée dans les épreuves (valeurs positives -> bras, valeurs négatives -> jambes), à l'exception à nouveau des épreuves 20 et 50 km
plot.CA(resJO)
contr <- resJO$col$contrib[,1]
contr[rev(order(contr))]
#' Les 5 pays contribuant le plus à l'inertie sur l'axe 1 sont : le Kenya, l'Éthiopie, le Maroc, les États-Unis, le Royaume-Uni
resJO$col$coord["usa","Dim 1"]
#' Les États-Unis se situent du côté positif de l'axe endurance (valeurs positives -> faible endurance).  
#'  ### ACM
data(banque)
dim(banque)
names(banque)
head(banque)
# par(mfrow=c(5,1))
ids <- c(4,5,6,12,13)
# for(id in ids)
# {
#     barplot(banque[,id])
# }
idSup <- setdiff(1:21, ids )
tabdisj <- tab.disjonctif(banque[,ids])
colnames(tabdisj)
head(tabdisj)
#' La somme de chaque ligne est de 5 (le nombre de colonnes sélectionnées). La somme totale est donc de 810*5 = 4050.
colSums(tabdisj)
resMCA <- MCA(banque[,ids])
#' Le premier plot représente les modalités des colonnes sur les axes de la MCA.
#' Le deuxième représente les individus sur les axes de la MCA.
#' Le troisième représente les colonnes sur les axes de la MCA.
resMCA$eig
chisq.test(tabdisj)
ctrs <- resMCA$var$contrib[,1]
ctrs
#' Les trois modalités qui contribuent le plus à l'axe 1 sont la présence d'un crédit habitation, d'être dans la première tranche d'âge et d'être une femme.
ctrs <- resMCA$var$contrib[,2]
ctrs
#' Les trois modalités qui contribuent le plus à l'axe 2 sont le fait d'être interdit bancaire, et le fait d'appartenir à la deuxième ou à la dernière tranche d'âge.
resMCA <- MCA(banque, quali.sup = idSup)
graphics.off()
plot.MCA(resMCA, choix = "ind", invisible = "ind", selectMod = "cos2 30",
         unselect = "gray50")
