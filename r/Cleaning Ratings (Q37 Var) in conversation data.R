conversation=read.csv("./dk_conversation_level_1311114.csv",sep=",")
 
label_con <-conversation[1,]
conversation=conversation[-1,]

#CLEAN UP Q37 (ratings variable) - If Q37 vars should be in Q36 it fixes that
#Also makes numbers from the Q37 number/comments combined
#Q37_numeric is the cleaned numeric ratings var
#Q37_character is the cleaned Q36  comment var

conversation$q37_cleaning<-as.character(conversation$Q37_counselor_feeling2)
conversation$q37_cleaning<-ifelse(regexpr(",",conversation$q37_cleaning,fixed=T)<0,conversation$q37_cleaning,substr(conversation$q37_cleaning,1,regexpr(",",conversation$q37_cleaning,fixed=T)-1))
conversation$q37_cleaning<-ifelse(regexpr(" ",conversation$q37_cleaning,fixed=T)<0,conversation$q37_cleaning,substr(conversation$q37_cleaning,1,regexpr(" ",conversation$q37_cleaning,fixed=T)-1))
conversation$q37_numeric=as.numeric(conversation$q37_cleaning)
conversation$q36_cleaning<-as.character(ifelse(is.na(conversation$q37_numeric) & conversation$Q36_visitor_feeling=="",as.character(conversation$Q37_counselor_feeling2),as.character(conversation$Q36_visitor_feeling)))

