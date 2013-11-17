import os
import sys
repo_path = '/opt/datakind/dlovell_ctl/'
sys.path.append(repo_path)

import numpy
import pylab
pylab.ion()
pylab.show()
import matplotlib.gridspec as gridspec
#
import munging.ctl_utils as cu
import munging.file_utils as fu
import munging.sdl_utils as su


# import the data
data_path = os.path.join(repo_path, 'data')
#
conversation_filename = os.path.join(data_path, 'dk_conversation_level_1311114.csv')
conversations = fu.process_or_unpickle(conversation_filename, cu.parse_conversations) 
conversation_ids = conversations.c_id.values
#
message_filename = os.path.join(data_path, 'dk_message_level_131114.csv')
messages = fu.process_or_unpickle(message_filename, cu.parse_messages)
teen_messages = su.filter_dataframe_rows(messages, su.is_teen)
counselor_messages = su.filter_dataframe_rows(messages, su.is_counselor)


# verify message, conversation ids increment sanely
pylab.figure()
messages.c_id.plot()
#
pylab.figure()
messages.m_id.map(numpy.float).plot()
#
pylab.figure()
messages.m_id.map(numpy.float).plot(linestyle='', marker='x', markersize=3)
pylab.xlim(42000, 45000)
pylab.ylim(45000, 48001)
#
pylab.figure()
is_teen = messages.actor_type == 'MobileMessenger'
messages.m_id[is_teen].map(numpy.float).plot(linestyle='', marker='x', markersize=3)
pylab.xlim(42000, 45000)
pylab.ylim(45000, 48001)


# generate top level message lengths
truncate_conversation_to = 20
conversation_message_lengths = su.generate_conversation_message_lengths(
        messages, conversation_ids, truncate_conversation_to)
teen_conversation_message_lengths = su.generate_conversation_message_lengths(
        teen_messages, conversation_ids, truncate_conversation_to)
counselor_conversation_message_lengths = su.generate_conversation_message_lengths(
        counselor_messages, conversation_ids, truncate_conversation_to)


# plot some conversation metrics
pylab.figure()
gs = gridspec.GridSpec(2,4)
#
ax1 = pylab.subplot(gs[0, 1:-1])
ax1.boxplot(conversation_message_lengths)
pylab.title('all message lengths')
#
ax2 = pylab.subplot(gs[1,:2])
ax2.boxplot(teen_conversation_message_lengths)
pylab.title('teen message lengths')
#
ax3 = pylab.subplot(gs[1,2:])
ax3.boxplot(counselor_conversation_message_lengths)
pylab.title('counselor message lengths')


