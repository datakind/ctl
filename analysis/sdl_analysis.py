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
import crisis.constants as C


# import the data
conversation_filename = os.path.join(C.this_repo_dir, C.CONVERSATION_DATA_FILENAME)
conversations = fu.process_or_unpickle(conversation_filename, cu.parse_conversations) 
conversation_ids = conversations.c_id.values
#
message_filename = os.path.join(C.this_repo_dir, C.MESSAGE_DATA_FILENAME)
messages = fu.process_or_unpickle(message_filename, cu.parse_messages)
teen_messages = su.filter_dataframe_rows(messages, su.is_teen)
counselor_messages = su.filter_dataframe_rows(messages, su.is_counselor)
#
teen_good_messages = su.filter_dataframe_rows(teen_messages, su.is_good)
teen_bad_messages = su.filter_dataframe_rows(teen_messages, su.is_bad)
teen_unrated_messages = su.filter_dataframe_rows(teen_messages, su.is_unrated)
#
counselor_good_messages = su.filter_dataframe_rows(counselor_messages, su.is_good)
counselor_bad_messages = su.filter_dataframe_rows(counselor_messages, su.is_bad)
counselor_unrated_messages = su.filter_dataframe_rows(counselor_messages, su.is_unrated)


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
# generate teen level message lengths
teen_good_conversation_message_lengths = su.generate_conversation_message_lengths(
        teen_good_messages, conversation_ids, truncate_conversation_to)
teen_bad_conversation_message_lengths = su.generate_conversation_message_lengths(
        teen_bad_messages, conversation_ids, truncate_conversation_to)
teen_unrated_conversation_message_lengths = su.generate_conversation_message_lengths(
        teen_unrated_messages, conversation_ids, truncate_conversation_to)
# generate counselor level message lengths
counselor_good_conversation_message_lengths = su.generate_conversation_message_lengths(
        counselor_good_messages, conversation_ids, truncate_conversation_to)
counselor_bad_conversation_message_lengths = su.generate_conversation_message_lengths(
        counselor_bad_messages, conversation_ids, truncate_conversation_to)
counselor_unrated_conversation_message_lengths = su.generate_conversation_message_lengths(
        counselor_unrated_messages, conversation_ids, truncate_conversation_to)


# plot some conversation metrics

# {all, teen, counselor} conversations
pylab.figure()
gs = gridspec.GridSpec(2,2)
#
ax0 = pylab.subplot(gs[0, 0])
bp_fh = ax0.boxplot(conversation_message_lengths)
t_fh = pylab.title('all message lengths')
#
ax2 = pylab.subplot(gs[1,0])
bp_fh = ax2.boxplot(teen_conversation_message_lengths)
t_fh = pylab.title('teen message lengths')
#
ax3 = pylab.subplot(gs[1,1])
bp_fh = ax3.boxplot(counselor_conversation_message_lengths)
t_fh = pylab.title('counselor message lengths')

# teen {good, bad} conversations
pylab.figure()
gs = gridspec.GridSpec(2,2)
#
ax0 = pylab.subplot(gs[0, 0])
bp_fh = ax0.boxplot(teen_conversation_message_lengths)
ax0.set_ylim((0, 300))
t_fh = pylab.title('teen message lengths')
#
ax1 = pylab.subplot(gs[0, 1])
bp_fh = ax1.boxplot(teen_unrated_conversation_message_lengths)
ax1.set_ylim((0, 300))
t_fh = pylab.title('teen unrated message lengths')
#
ax2 = pylab.subplot(gs[1, 0])
bp_fh = ax2.boxplot(teen_good_conversation_message_lengths)
ax2.set_ylim((0, 300))
pylab.title('teen good message lengths')
#
ax3 = pylab.subplot(gs[1, 1])
bp_fh = ax3.boxplot(teen_bad_conversation_message_lengths)
ax3.set_ylim((0, 300))
t_fh = pylab.title('teen bad message lengths')

# counselor {good, bad} conversations
pylab.figure()
gs = gridspec.GridSpec(2,2)
#
ax0 = pylab.subplot(gs[0, 0])
bp_fh = ax0.boxplot(counselor_conversation_message_lengths)
ax0.set_ylim((0, 300))
t_fh = pylab.title('counselor message lengths')
#
ax1 = pylab.subplot(gs[0, 1])
bp_fh = ax1.boxplot(counselor_unrated_conversation_message_lengths)
ax1.set_ylim((0, 300))
t_fh = pylab.title('counselor unrated message lengths')
#
ax2 = pylab.subplot(gs[1, 0])
bp_fh = ax2.boxplot(counselor_good_conversation_message_lengths)
ax2.set_ylim((0, 300))
t_fh = pylab.title('counselor good message lengths')
#
ax3 = pylab.subplot(gs[1, 1])
bp_fh = ax3.boxplot(counselor_bad_conversation_message_lengths)
ax3.set_ylim((0, 300))
t_fh = pylab.title('counselor bad message lengths')

