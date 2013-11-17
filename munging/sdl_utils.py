import numpy


def is_sorted(in_list):
    return all(in_list[i] <= in_list[i+1] for i in xrange(len(in_list)-1))

def get_conversation_messages(messages, conversation_id):
    is_this_conversation = messages.c_id == conversation_id
    return messages[is_this_conversation]

def conversation_apply(messages, conversation_ids, func):
    conversation_values = []
    for conversation_id in conversation_ids:
        messages_i = get_conversation_messages(messages, conversation_id)
        conversation_value = func(messages_i)
        conversation_values.append(conversation_value)
    return conversation_values

def get_conversation_message_lengths(conversation):
    values = conversation.msg_chars.values
    return numpy.array(values, dtype=int)

def transpose_ragged_list(ragged_list, max_len):
    num_lists = len(ragged_list)
    arr = numpy.zeros((num_lists, max_len), dtype=numpy.float) * numpy.nan
    for list_idx, list in enumerate(ragged_list):
        num_list_elements = len(list[:max_len])
        arr[list_idx, :num_list_elements] = list[:max_len]
    arr = arr.T
    list_out = []
    for vector_idx, vector_i in enumerate(arr):
        vector_i = vector_i[~numpy.isnan(vector_i)]
        vector_i = vector_i.clip(-1, 300)
        list_out.append(vector_i)
    return list_out

def generate_conversation_message_lengths(messages, conversation_ids, max_length):
    conversation_message_lengths = conversation_apply(messages, conversation_ids, get_conversation_message_lengths)
    conversation_message_lengths = transpose_ragged_list(conversation_message_lengths, max_length)
    return conversation_message_lengths

is_teen = lambda message: message['actor_type'] == 'MobileMessenger'
is_counselor = lambda message: message['actor_type'] == 'Internal'
is_good = lambda message: message['conv_rating'] in set([2., 1.])
is_bad = lambda message: message['conv_rating'] == -1
is_unrated = lambda message: numpy.isnan(message['conv_rating'])

def filter_dataframe_rows(dataframe, func):
    return dataframe[dataframe.apply(func, axis=1)]
