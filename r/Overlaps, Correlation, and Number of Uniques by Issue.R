#Frank Firke
#Looks at how issues cluster with each other

#Fix the filename--this relies on its being Arun's output file

convissues<-read.csv("C:\\Users\\Frank\\Documents\\DataDive\\Data\\conversations_w_issues.csv",stringsAsFactors=FALSE)

#Drops the issues that seem like fake issues

drops<-c("teen","the","what","nan","mention","mica","did","issues")
vars<-names(convissues) %in% drops
convissues<-convissues[!vars]

#Loop to look at pairwise clustering of issues--looks at what fraction of one overlaps with the other

name1<-character(0)
name2<-character(0)
count1<-numeric(0)
count2<-numeric(0)
overlap<-numeric(0)
overlapfrac1<-numeric(0)
overlapfrac2<-numeric(0)

names<-colnames(convissues)

for (i in 30:55) {
  for (j in (i+1):56)
  {
    name1<-c(name1,names[i])
    name2<-c(name2,names[j])
    count1<-c(count1,sum(convissues[i]))
    count2<-c(count2,sum(convissues[j]))
    overlap<-c(overlap,sum(convissues[i]*convissues[j]))
    
  }
}

overlaps<-data.frame(name1,name2,count1,count2,overlap)
overlaps$frac1<-overlaps$overlap/overlaps$count1
overlaps$frac2<-overlaps$overlap/overlaps$count2

#Exports

#write.csv(overlaps,"C:\\Users\\Frank\\Documents\\DataDive\\Data\\Out\\Overlapping Issues.csv")

#Makes a correlation matrix for the issues--don't think this is useful, but as database grows probably
#worth looking at

corr<-cor(convissues[30:56])

#For digging purposes, shows large overlap percentages

order1<-overlaps[order(-overlaps$frac1),]
order2<-overlaps[order(-overlaps$frac2),]

#Loop to pull the number of conversations that mention only one issue

name<-character(0)
unique<-numeric(0)
total<-numeric(0)

for (i in 30:56) {
  name<-c(name,names[i])
  unique<-c(unique,nrow(convissues[convissues$Q13_issues==names[i],]))
  total<-c(total,sum(convissues[i]))
}

uniques<-data.frame(name,unique,total)
uniques$frac<-uniques$unique/uniques$total