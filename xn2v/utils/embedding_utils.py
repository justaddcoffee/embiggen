#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Embedding Utility Functions.

Reads and Writes Embedding Data
* write_embeddings
* load_embeddings

manipulates or Processes Embeddings
* get_embedding

"""

# import needed libraries
import numpy as np
import os
import os.path
import tensorflow as tf

from typing import Dict, List, Union


# TODO: consider updating writes_embeddings to not require id2word when writing embedding data


def get_embedding(x: int, embedding: np.ndarray, device: str = 'cpu') -> Union[np.ndarray, tf.Tensor]:
    """Get the embedding corresponding to the data points in x. Note, we ensure that this code is carried out on
    the CPU because some ops are not compatible with the GPU.

    Args:
        x: A integer representing a node or word index.
        embedding: A 2D tensor with shape (samples, sequence_length), where each entry is a sequence of integers.
        device: A string that indicates whether to run computations on (default=cpu).

    Returns:
        embedding: Corresponding embeddings, with shape (batch_size, embedding_dimension).

    Raises:
        ValueError: If the embedding variable is None.
    """

    if embedding is None:
        raise ValueError('No embedding data found (i.e. embedding is None)')
    else:
        with tf.device(device):
            embedding = tf.nn.embedding_lookup(embedding, x)

            return embedding


def write_embeddings(out_file: str, embedding: np.ndarray, reverse_worddictionary: Dict, device: str = 'cpu') -> None:
    """Writes embedding data to a local directory. Data is written out in the following format, which is consistent
    with current standards:
        'ENSP00000371067' 0.6698335 , -0.83192813, -0.3676057 , ...,  0.9241863 , -2.1407487 , -0.6607736
        'ENSP00000374213' -0.6342755 , -2.0504158 , -1.169239  , ..., -0.8034669 , 0.5925971 , -0.00864262

    Args:
        out_file: A string containing a filepath for writing embedding data.
        embedding: A 2D tensor with shape (samples, sequence_length), where each entry is a sequence of integers.
        reverse_worddictionary: A dictionary where the keys are integers and values are the nodes represented by the
            integers.
        device: A string that indicates whether to run computations on (default=cpu).

    Returns:
        None.

    Raises:
        - ValueError: If the embedding attribute contains no data.
        - ValueError: If the node id to integer dictionary contains no data.
    """

    if embedding is None:
        raise ValueError('No embedding data found (i.e. embedding is None)')
    elif reverse_worddictionary is None:
        raise ValueError('No node to integer word mapping dictionary data found (i.e. reverse_worddictionary is None)')
    else:
        with tf.device(device):
            with open(out_file, 'w') as write_location:
                for x in sorted(list(reverse_worddictionary.keys())):
                    embed = get_embedding(x, embedding).numpy()
                    word = reverse_worddictionary[x]
                    write_location.write('{word} {embedding}\n'.format(word=word, embedding=' '.join(map(str, embed))))
            write_location.close()

    return None


def load_embeddings(file_name: str) -> Dict[Union[str, int], List[float]]:
    """Reads in embedding data from a file.

    Returns:
        embedding_data: A dictionary where keys are nodes and values are embedding vectors (i.e. list of floats).

    Raises:
        ValueError: If file_name does not contain a valid filepath.
        IOError: If the file_name file is empty.
        TypeError: If the file_name contains no data.
    """

    if file_name is None:
        raise ValueError('file_name must not contain a valid filepath')
    elif not os.path.exists(file_name):
        raise IOError('The {} file does not exist!'.format(file_name))
    elif os.stat(file_name).st_size == 0:
        raise TypeError('The input file: {} is empty'.format(file_name))
    else:
        n_lines, embedding_data = 0, {}

        with open(file_name, 'r') as input_file:
            for line in input_file:
                fields = line.split(' ')
                embedding_vector = [float(i) for i in fields[1:]]
                embedding_data.update({fields[0]: embedding_vector})
                n_lines += 1
        input_file.close()

        print('Finished ingesting {} lines (vectors) from {}'.format(n_lines, file_name))

    return embedding_data
