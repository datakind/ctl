#Frank FIrke
#This does some basic summary statistics of ratings by center

#Read the dataset in; sub in your own filepath

conv<-read.csv("C:\\Users\\Frank\\Documents\\DataDive\\Data\\dk_conversation_level_1311114.csv")

#Subsets to crisis and conversation and junks the weird ones with wrong crisis center numbers

crisis<-conv[conv$Q2_conv_type %in% c("crisis","conversation") & conv$crisis_center_id %in% c(1,4,5),]
crisis$unrated<-crisis$conv_rating==""
crisis$poor<-crisis$conv_rating==-1

#Prints datasets with percentages of unrated and rated poor conversations

aggregate(unrated ~ crisis_center_id,data=crisis,mean)
aggregate(poor ~ crisis_center_id,data=crisis,mean)

#Subsets to rated conversations, looks at percentage rated poor

crated<-crisis[crisis$conv_rating %in% c(-1,1,2),]
aggregate(poor~crisis_center_id,data=crated,mean)
