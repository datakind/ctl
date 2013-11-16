import os
import sys
repo_path = '/opt/datakind/dlovell_ctl/'
sys.path.append(repo_path)

import datetime
#
import numpy
import pylab
pylab.ion()
pylab.show()
#
import munging.ctl_utils as cu
import munging.file_utils as fu


# import the ata
data_path = os.path.join(repo_path, 'data')
#
conversation_filename = os.path.join(data_path, 'dk_conversation_level_1311114.csv')
conversation_pkl_filename = conversation_filename + '.pkl'
conversations = None
if os.path.isfile(conversation_pkl_filename):
    print "using pickled conversations"
    conversations = fu.unpickle(conversation_pkl_filename)
else:
    print "parsing and pickling conversations"
    conversations = cu.parse_conversations(conversation_filename)
    fu.pickle(conversations, conversation_pkl_filename)
#
message_filename = os.path.join(data_path, 'dk_message_level_131114.csv')
message_pkl_filename = message_filename + '.pkl'
messages = None
if os.path.isfile(message_pkl_filename):
    print "using pickled messages"
    messages = fu.unpickle(message_pkl_filename)
else:
    print "parsing and pickling messages"
    messages = cu.parse_messages(message_filename)
    fu.pickle(messages, message_pkl_filename)


# verify message, conversation ids increment sanely
pylab.figure()
messages.c_id.plot()

pylab.figure()
messages.m_id.map(numpy.float).plot()

pylab.figure()
messages.m_id.map(numpy.float).plot(linestyle='', marker='x', markersize=3)
pylab.xlim(42000, 45000)
pylab.ylim(45000, 48001)

pylab.figure()
is_teen = messages.actor_type == 'MobileMessenger'
messages.m_id[is_teen].map(numpy.float).plot(linestyle='', marker='x', markersize=3)
pylab.xlim(42000, 45000)
pylab.ylim(45000, 48001)


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

def generate_conversation_message_lengths(conversations, messages, max_length):
    conversation_ids = conversations.c_id.values
    conversation_message_lengths = []
    for conversation_id in conversation_ids:
        num_chars_list = get_conversation_num_chars_per_message(messages,
                conversation_id)
        if num_chars_list is None:
            continue
        conversation_message_lengths.append(num_chars_list)
    conversation_message_lengths = transpose_ragged_list(conversation_message_lengths, max_length)
    return conversation_message_lengths

    
conversation_message_length_filename = os.path.join(data_path, 'conversation_message_length.pkl.gz')
if os.path.isfile(conversation_message_length_filename):
    print "using pickled conversation_message_lengths"
    conversation_message_lengths = fu.unpickle(conversation_message_length_filename)
else:
    print "parsing and pickling conversation_message_lengths"
    conversation_message_lengths = generate_conversation_message_lengths(conversations, messages, 20)
    fu.pickle(conversation_message_lengths, conversation_message_length_filename)
pylab.figure()
boxplot_fh = pylab.boxplot(conversation_message_lengths)

