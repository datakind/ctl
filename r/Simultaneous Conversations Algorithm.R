# Frank Firke
# ffirke@gmail.com
# DataKind Datadive (11/16/2013)

# Rough Algorithm to Quantify the Number of Messages Sent/Received
# And Other Conversations Engaged In During Given Conversation

# Creates Dataframe with All Conversations, each with a measure of overlapping 
# conversations, overlapping outgoing messages, and overlapping incoming messages

# Things that could be tweaked to improve methodological framework:
# 1) Length of Gap Time
# 2) Is simple average over all messages right?
# 3) Are There Other Metrics for Engagement (e.g. relative message length in 
# conversations, relative number of messages sent)

# Currently handles ~ 30 conversations/second--probably could be made faster

# ----------------------------------



# Reads in the data and converts it to convenient time format
# Requires nicely formatted date input (someone did it in Python)

# Fix file path

mess<-read.csv("C:\\Users\\Frank\\Documents\\DataDive\\Data\\messages_cleaned.csv",stringsAsFactors=FALSE)

# Converts to the appropriate time--the format may need to be changed

mess$time<-as.POSIXct(mess$msg_time,format="%Y-%m-%d %H:%M:%S")

mess<-mess[c("time","c_id","specialist_id","area_code")]

# List of specialists to iterate over

start<-Sys.time()

ids<-unique(mess$specialist_id)
convs<-unique(mess$c_id)
leng<-length(convs)

# This is the amount of time around a message that is treated as relevant
# i.e., a message within five minutes of another message will be considered
# overlapping

gaptime<-5

c_id<-numeric(leng)
otherconvers<-numeric(leng)
otheroutmessages<-numeric(leng)
otherinmessages<-numeric(leng)

count=1

#for (i in 1:5) {
for (i in 1:length(ids)) {  
  # Starts by subsetting to only conversations with one specialist and
  # Iterating through each of their conversations
  
  temp<-mess[mess$specialist_id==ids[i],]
  convos<-unique(temp$c_id)
  for (j in 1:length(convos)) {
    tempconv<-temp[temp$c_id==convos[j],]
    
    # Subsets to only messages that were sent by the same counselor in a 
    # different conversation that fall in the interval 
    # (beginning of conversation - 5 minutes, beginning of conversation + 5 minutes)
    
    min<-min(tempconv$time)-gaptime*60
    max<-max(tempconv$time)+gaptime*60
    base<-temp[temp$c_id!=convos[j]&(temp$time>=min)&(temp$time<=max),]
    
    tempotheroutmess<-numeric(nrow(tempconv))
    tempotherinmess<-numeric(nrow(tempconv))
    tempotherconv<-numeric(nrow(tempconv))
    
    # For each message in the conversation, calculate 3 things:
    # 1) Number of Other Conversations Counselor Participating in W/ In 5 Minutes of Message
    # 2) Number of Incoming Messages Counselor Receives in Other Conversations
    # 3) Number of Outgoing Messages Counselor Sends in Other Conversations
    
    for (k in 1:nrow(tempconv)) {
      
      # Subsets to other messages sent/received w/ in 5 minutes
      
      base$diff<-abs(as.numeric(difftime(base$time,tempconv$time[k],units="mins")))
      nearby<-base[base$diff<=gaptime,]

      # Number of outgoing, incoming, and conversations within that 5 minute window
      
      tempotheroutmess[k]<-nrow(nearby[nearby$area_code=="int",])
      tempotherinmess[k]<-nrow(nearby[nearby$area_code!="int",])
      tempotherconv[k]<-length(unique(nearby$c_id))
    }
    
    # Takes averages over conversations and adds to vectors
    
    c_id[count]<-convos[j]
    otherconvers[count]<-mean(tempotherconv)
    otheroutmessages[count]<-mean(tempotheroutmess)
    otherinmessages[count]<-mean(tempotherinmess)
    count=count+1
  }
  
}

# Collects into dataframe

outdata<-data.frame(c_id,otherconvers,otheroutmessages,otherinmessages)

Sys.time()-start