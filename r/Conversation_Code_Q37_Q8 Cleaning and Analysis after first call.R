
conversation<-read.csv("./DATADIVE/dk_conversation_level_131114_clean.csv",stringsAsFactors=FALSE)

conversation$time<-as.POSIXct(conversation$conv_start,format="%m/%d/%y %H:%M")
 
label_con <-conversation[1,]
#conversation=conversation[-1,]

#CLEAN UP Q37 (ratings) - If Q37 vars should be in Q36 it fixes that
#Also makes numbers from the Q37 number/comments combined
#Q37_numberic is the cleaned numeric ratings var
#Q37_character is the cleaned Q36  comment var

conversation$q37_cleaning<-as.character(conversation$Q37_counselor_feeling2)
conversation$q37_cleaning<-ifelse(regexpr(",",conversation$q37_cleaning,fixed=T)<0,conversation$q37_cleaning,substr(conversation$q37_cleaning,1,regexpr(",",conversation$q37_cleaning,fixed=T)-1))
conversation$q37_cleaning<-ifelse(regexpr(" ",conversation$q37_cleaning,fixed=T)<0,conversation$q37_cleaning,substr(conversation$q37_cleaning,1,regexpr(" ",conversation$q37_cleaning,fixed=T)-1))
conversation$q37_numeric<-as.numeric(conversation$q37_cleaning)
conversation$q36_cleaning<-as.character(ifelse(is.na(conversation$q37_numeric) & conversation$Q36_visitor_feeling=="",as.character(conversation$Q37_counselor_feeling2),as.character(conversation$Q36_visitor_feeling)))

conversation$q37_cleaning<-NULL

#Create Conversation Q8 Mod
#Change Q8 (conv_resolution) to "exitedqueue" if silence/hangup in "Q3"
#Changed regardless of whether Q8 says (most of these are blank)
conversation$q8_mod<-(ifelse(regexpr("silence",as.character(conversation$Q3_conv_type),fixed=T)>0 |regexpr("hangup",as.character(conversation$Q3_conv_type),fixed=T)>0,"exitedqueue",as.character(conversation$Q8_conv_resolution)))

sum(ifelse(as.character(conversation$q36_cleaning)=="",0,1))
sum(ifelse(is.na(conversation$q37_numeric)==T,0,1))
sum(ifelse(as.character(conversation$Q8_conv_resolution)=="" &conversation$q8_mod=="exitedqueue",1,0))
sum(ifelse(conversation$q8_mod=="exitedqueue",1,0))

#Dropping conversations that are survey/test/inappropriate

require(sqldf)
conversation2<-sqldf('select * from conversation where Q3_conv_type !="survey" & Q3_conv_type !="test" & Q3_conv_type !="inappropriate"')
conversation2<-sqldf('select * from conversation where Q3_conv_type !="survey"')
conversation2<-sqldf('select * from conversation2 where Q3_conv_type !="inappropriate"')
conversation2<-sqldf('select * from conversation2 where Q3_conv_type !="test"')

#LOOK AT RESPONSE VS RATING
conversations2$freq<-(ifelse(q2_conv_type)!=""

conversation2$conv_ratings_text<-ifelse(conversation2$conv_rating==-1,"Bad",ifelse(conversation2$conv_rating==1,"Good",ifelse(conversation2$conv_rating==2,"Great","")))
conversation2$conv_ratings_text<-ifelse(is.na(conversation2$conv_ratings_text),"No Response",conversation2$conv_ratings_text)
conversation2$q8_mod2<-ifelse(conversation2$q8_mod=="","No Data",conversation2$q8_mod)
conv_ratings<-table(conversation2$q8_mod2,conversation2$conv_ratings_text)
ftable(conv_ratings)



#Find texters who have more than one conversation
conversation3<-sqldf('select texter_id, count(*) total from conversation2 group by texter_id')
conversation3<-sqldf('select texter_id, total from conversation3 where total>1 group by texter_id')

conversation4<-merge(conversation3, conversation2, by.conversation3="texter_id", by.conversation2="texter_id")

#Find Distribution of Outcomes after the first "postive" outcome -- we classify those as referral/assisted/transfered
conversation4$pos_var<-as.numeric(ifelse(conversation4$q8_mod=="assisted",1,ifelse(conversation4$q8_mod=="referral",1,ifelse(conversation4$q8_mod=="transferred",1,0))))

conversation4<-conversation4[order(conversation4$texter_id,conversation4$time),]
i<-1
conversation4$pos_var2<-0
for(i in 1:NROW(conversation4$pos_var)){
	if (conversation4$pos_var[i]==1) {
		conversation4$pos_var2[i]<-as.numeric(1)
		}
	else {
	if (i>1) {
		if(conversation4$texter_id[i]==conversation4$texter_id[i-1]){
			conversation4$pos_var2[i]<-conversation4$pos_var2[i-1]
		}
	else {conversation4$pos_var2[i]<-0
		}
		}
		}
	i<-i+1
}
		
#Limit Data to only those after first "postive" outcome		
conversation5<-subset(conversation4,conversation4$pos_var2==1)
conversation5$count_var <- ave(as.numeric(conversation5$texter_id), conversation5$texter_id,   
FUN=seq_along)

#CHART Distribution of outcomes vs. number of conversations
con_chart<-subset(conversation5,conversation5$count_var !=1)
con_chart$count_var <- ave(as.numeric(con_chart$texter_id), con_chart$texter_id,   
FUN=seq_along)
con_chart$q8_marker<-ifelse(con_chart$pos_var==1,"Referral/Transfer/Assisted",ifelse(con_chart$q8_mod=="","",ifelse(con_chart$q8_mod=="rescue","Rescue","Disengaged/Exited Queue/Other")))

require(ggplot2)

e<-ggplot(con_chart, aes(con_chart$count_var, fill=con_chart$q8_marker, colour=con_chart$q8_marker))
e+geom_bar(binwidth=1)+xlab("Conversations Since First Referral/Transfer/Assist")+ ggtitle("Outcomes After Interaction With Referral/Transfer/Assist")+scale_fill_discrete(name="Outcome")+scale_colour_discrete(name="Outcome")

#UNUSED CHARTS -- THESE BREAK DOWN BY Q8 RATHER THAN GROUPS 
#d<-ggplot(con_chart, aes(con_chart$count_var, fill=con_chart$q8_mod, colour=con_chart$q8_mod))
#d+geom_bar(binwidth=1) +xlab("Conversations Since First Referral/Transfer/Assist")+ ggtitle("Outcomes After First #Sucessful Interaction")+scale_fill_discrete(name="Outcome")+scale_colour_discrete(name="Outcome")
#d+geom_freqpoly(binwidth=1)+xlab("Conversations Since First Referral/Transfer/Assist")+ ggtitle("Outcomes After #First Sucessful Interaction")+scale_fill_discrete(name="Outcome")+scale_colour_discrete(name="Outcome")
#e+geom_freqpoly(binwidth=1)+xlab("Conversations Since First Referral/Transfer/Assist")+ ggtitle("Outcomes After #First Sucessful Interaction")+scale_fill_discrete(name="Outcome")+scale_colour_discrete(name="Outcome")

rescue<-subset(con_chart,con_chart$q8_marker=="Rescue")
View(rescue)






 
