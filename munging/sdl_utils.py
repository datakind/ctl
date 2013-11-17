import os
import datetime
#
import numpy


def minimalist_xldate_as_datetime(xldate, datemode):
    # datemode: 0 for 1900-based, 1 for 1904-based
    base = datetime.datetime(1899, 12, 30)
    additional = datetime.timedelta(days=xldate + 1462 * datemode)
    return base + additional

def convert_datestr(datestr):
    return datetime.datetime.strptime(datestr, '%m/%d/%Y %H:%M')

def convert_msg_time(datestr):
    date = None
    try:
        date = convert_datestr(datestr)
    except Exception, e:
        date = minimalist_xldate_as_datetime(float(datestr), 0)
    return date

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

def get_conversation_msg_lengths(conversation):
    values = conversation.msg_chars.values
    return numpy.array(values, dtype=int)

def get_conversation_num_chars_per_message(messages, conversation_id):
    num_chars_list = None
    try:
        messages_i = get_conversation_messages(messages, conversation_id)
        msg_times = messages_i.msg_time.map(convert_msg_time).values
        assert(is_sorted(msg_times))
        values = messages_i.msg_chars.values
        values = numpy.array(values, dtype=int)
        num_chars_list = values
    except Exception, e:
        pass
    return num_chars_list

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
    conversation_message_lengths = []
    for conversation_id in conversation_ids:
        num_chars_list = get_conversation_num_chars_per_message(messages,
                conversation_id)
        if num_chars_list is None:
            continue
        conversation_message_lengths.append(num_chars_list)
    conversation_message_lengths = transpose_ragged_list(conversation_message_lengths, max_length)
    return conversation_message_lengths

is_teen = lambda message: message['actor_type'] == 'MobileMessenger'
is_counselor = lambda message: message['actor_type'] == 'Internal'

def filter_dataframe_rows(dataframe, func):
    return dataframe[dataframe.apply(func, axis=1)]
