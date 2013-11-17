import os
#
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
conversations = fu.process_or_read_hdf(conversation_filename, cu.parse_conversations, 'conversations')
message_filename = os.path.join(C.this_repo_dir, C.MESSAGE_DATA_FILENAME)
messages = fu.process_or_read_hdf(message_filename, cu.parse_messages, 'messages')


# subset the data
conversation_ids = conversations.c_id.values
#
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
fh = pylab.figure()
messages.c_id.plot()
pylab.xlabel('message index')
pylab.ylabel('conversation id')
pylab.title('conversation id is monotonically increasing\nrows must be stored in conversation order')
pylab.savefig('conversation_ids')
#
pylab.figure()
messages.m_id.map(numpy.float).plot()
pylab.xlabel('message index')
pylab.ylabel('message id')
pylab.title('message ids not monotonic')
pylab.savefig('message_ids')
#
pylab.figure()
messages.m_id.map(numpy.float).plot(linestyle='', marker='x', markersize=3)
pylab.xlim(42000, 45000)
pylab.ylim(45000, 48001)
pylab.xlabel('message index')
pylab.ylabel('message id')
pylab.title('zoom in to get a sense for conversation overlaps')
pylab.savefig('conversation_overlap')


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
pylab.savefig('all_teen_counselor_conversation_message_length_boxplots')

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
pylab.savefig('teen_unrated_good_bad_message_length_boxplots')

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
pylab.savefig('counselor_unrated_good_bad_message_length_boxplots')

