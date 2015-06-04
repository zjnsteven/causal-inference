library(pcalg)
library(maptools)
arbitraryShapeFile <- readShapePoly("/home/vinay/Downloads/KFW_newNDVI.shp")
dataFrame_from_Shp <- arbitraryShapeFile@data
newy=dataFrame_from_Shp[which(dataFrame_from_Shp$demend_y>0),]
newtest=newy[,c(4,7,8,10:12,13:815)]
#########
test=newtest
suffStat=list(C=cor(test),n=nrow(test))
test.gmG=pc(suffStat, indepTest = gaussCItest, p= ncol(test),alpha = 0.01)
idaFast(3,c(73:138),cov(test),test.gmG@graph)

######
##new varibale
newtest1=cbind(test[,c(1:6)],test$Slope,test$Elevation,test$UrbTravTim,test$Riv_Dist,test$Road_dist,test$MeanN_2000-test$MeanN_1982, test$MaxN_2000-test$MaxN_1982, test$MeanL_2000-test$MeanL_1982,test$MaxL_2000-test$MaxL_1982,test$MeanT_2000-test$MeanT_1982,test$MaxT_2000-test$MaxT_1982,test$MinT_2000-test$MinT_1982,test$MeanP_2000-test$MeanP_1982,test$MaxP_2000-test$MaxP_1982,test$MinP_2000-test$MinP_1982)
test=newtest1
colnames(test)=c("terrai_are","pop","demend_y","pop1990","pop1995","pop2000","slope","elevation","urbtravtim","riv_dist","road_dist","newmeanN","newmaxN","newmeanL","newmaxL","newmeanT","newmaxT","newminT","newmeanP","newmaxP","newminP")
suffStat=list(C=cor(test),n=nrow(test))
test.gmG=pc(suffStat, indepTest = gaussCItest, p= ncol(test),alpha = 0.01)
idaFast(3,c(14,15),cov(test),test.gmG@graph)
plot(test.gmG, main = "")
########
#move demand to last column
suffStat=list(C=cor(test1),n=nrow(test1))
test1.gmG=pc(suffStat, indepTest = gaussCItest, p= ncol(test1),alpha = 0.01)
idaFast(21,c(13,14),cov(test1),test.gmG@graph)
plot(test1.gmG, main = "")

#####

#ges
score = new("GaussL0penObsScore", as.matrix(test))
ges.fit = ges(ncol(test), score)
plot(ges.fit$essgraph, main = "")


#rfci
suffStat1 <- list(C = cor(test), n = nrow(test))
pag.est <- rfci(suffStat1, indepTest = gaussCItest,
                  p = ncol(test), alpha = 0.01, labels = as.character(2:5))

#bianry
# V <- colnames(test)
# suffStat <- list(dm = test, adaptDF = FALSE)
# fit=pc(suffStat, indepTest = binCItest, labels=V,alpha = 0.01)


#pc,idaFast result
# 73  -7.746614e-04
# 74  -1.288536e-03
# 75  -1.822316e-03
# 76  -1.683020e-03
# 77  -1.439520e-03
# 78  -1.591028e-03
# 79  -1.515819e-03
# 80  -1.380201e-03
# 81  -8.696733e-04
# 82  -7.262308e-04
# 83  -1.334015e-03
# 84  -1.527412e-03
# 85  -1.559211e-03
# 86  -5.878188e-04
# 87  -2.940973e-04
# 88  -7.195301e-04
# 89  -1.508692e-03
# 90  -9.929905e-04
# 91  -1.452951e-03
# 92  -1.042023e-03
# 93  -5.018879e-04
# 94  -4.978452e-04
# 95  -1.992665e-04
# 96  -1.062493e-03
# 97  -9.101664e-04
# 98  -9.260982e-04
# 99  -1.149705e-04
# 100 -9.383646e-05
# 101 -1.011481e-03
# 102 -5.186374e-04
# 103 -1.130038e-03
# 104 -1.683488e-03
# 105 -1.549119e-03
# 106  4.189877e-05
# 107 -2.474288e-03
# 108 -2.320050e-03
# 109  3.561833e-04
# 110 -3.751600e-03
# 111 -1.037384e-03
# 112 -1.345925e-03
# 113 -3.809279e-03
# 114 -3.442826e-03
# 115  1.235247e-04
# 116 -3.643686e-03
# 117 -2.425443e-03
# 118  5.851583e-03
# 119 -2.618242e-03
# 120  6.764950e-06
# 121  5.461047e-04
# 122 -4.212645e-03
# 123 -1.101947e-03
# 124 -1.443751e-03
# 125 -3.232932e-03
# 126  6.691456e-04
# 127 -1.351329e-03
# 128 -1.090741e-03
# 129 -2.562552e-03
# 130 -2.156661e-03
# 131 -2.202218e-03
# 132 -8.207211e-04
# 133 -2.874629e-03
# 134 -4.818367e-03
# 135 -1.794543e-03
# 136 -2.600868e-03
# 137 -2.513817e-03
# 138  1.811701e-04