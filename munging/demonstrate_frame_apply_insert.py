import os
#
import munging.ctl_utils as cu
import munging.file_utils as fu
import munging.sdl_utils as su
import crisis.constants as C


# import the data
conversation_filename = os.path.join(C.this_repo_dir, C.CONVERSATION_DATA_FILENAME)
conversations = fu.process_or_read_hdf(conversation_filename, cu.parse_conversations, 'conversations')
message_filename = os.path.join(C.this_repo_dir, C.MESSAGE_DATA_FILENAME)
messages = fu.process_or_read_hdf(message_filename, cu.parse_messages, 'messages')


def get_conversation_num_messages(conversation_series):
    # messages taken from enclosing environment
    conversation_id = conversation_series['c_id']
    conversation_messages = su.get_conversation_messages(messages, conversation_id)
    return len(conversation_messages)

def get_conversation_duration(conversation_series):
    return conversation_series['conv_end'] - conversation_series['conv_start']


func_name_tuples = [
        (get_conversation_num_messages, 'num_messages'),
        (get_conversation_duration, 'conversation_duration'),
        ]


columns_truncated = conversations.columns[:11]
conversations_truncated = conversations[:11].reindex(columns=columns_truncated)
#
print conversations_truncated
conversations_truncated.to_csv('before.csv')
#
for (func, name) in func_name_tuples:
    su.frame_apply_insert(conversations_truncated, func, name)
#
print conversations_truncated
conversations_truncated.to_csv('after.csv')



