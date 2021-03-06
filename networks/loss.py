import tensorflow as tf


NUM_CLASSES = 2


def loss_def(model, _logits, _labels, _mask=None):
    if model != 'pixelwise':
        # logits = tf.reshape(_logits, [-1, NUM_CLASSES])
        # labels = tf.cast(tf.reshape(_labels, [-1]), tf.int32)

        mask = tf.cast(tf.reshape(_mask, [-1]), tf.bool)
        logits = tf.boolean_mask(tf.reshape(_logits, [-1, NUM_CLASSES]), mask)
        labels = tf.boolean_mask(tf.cast(tf.reshape(_labels, [-1]), tf.int64), mask)
    else:
        logits = _logits
        labels = _labels

    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels,
                                                                   name='cross_entropy_per_example')
    cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')
    tf.compat.v1.add_to_collection('losses', cross_entropy_mean)

    # The total loss is defined as the cross entropy loss plus all of the weight decay terms (L2 loss).
    return tf.add_n(tf.compat.v1.get_collection('losses'), name='total_loss')
