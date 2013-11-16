import datetime
#
import numpy
import pylab
pylab.ion()
pylab.show()
#
import ctl_utils as cu


# import the ata
conversations = cu.parse_conversations('../data/dk_conversation_level_1311114.csv')
messages = cu.parse_messages('../data/dk_message_level_131114.csv')

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
messages.m_id.map(numpy.float).plot(linestyle='', marker='x', markersize=3)
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

conversation_ids = conversations.c_id.values
conversation_characters_per_message_over_messages = []
# conversation_characters_per_message_over_time = []
for conversation_id in conversation_ids:
    num_chars_list = get_conversation_num_chars_per_message(messages,
            conversation_id)
    if num_chars_list is None:
        continue
    conversation_characters_per_message_over_messages.append(num_chars_list)

num_chars_l = transpose_ragged_list(conversation_characters_per_message_over_messages, 20)
pylab.figure()
boxplot_fh = pylab.boxplot(num_chars_l)

