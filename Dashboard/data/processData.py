import os
from deepcase.preprocessing.preprocessor import Preprocessor # potentially change all this to use the deepcase module
from deepcase.context_builder.context_builder import ContextBuilder

import torch

"""
This file is used to process the data from the database and return it in a format that can be used by the front end.
Specifically, here we run the DeepCASE algorithm on the uploaded data and return the specific steps
"""

def create_sequences(file):
    """
    Create sequences from the uploaded file
    :param file: the uploaded file
    :return: the sequences
    """

    # the command to run it is:
    # python3 -m deepcase sequence --csv alerts.csv --save-sequences sequences.save

    # Create preprocessor
    preprocessor = Preprocessor(
        length=10,  # 10 events in context
        timeout=86400,  # Ignore events older than 1 day (60*60*24 = 86400 seconds)
    )

    # Load data from file
    context, events, labels, mapping = preprocessor.csv(
        file, verbose=True
    )

    # Save sequences if necessary
    with open("sequences.save", 'wb') as outfile:
        result = {
            "events": events,
            "context": context,
            "labels": labels,
            "mapping": mapping,
        }
        torch.save(result, outfile)

    print(result)
    # convert context to list
    context = context.tolist()
    # convert events to list
    events = events.tolist()
    # convert labels to list
    labels = labels.tolist()

    with open("sequences.csv", "w") as result_file:
        result_file.write("Context,Event,Label\n")
        for i in range(len(context)):
            result_file.write(f"{context[i]},{events[i]},{labels[i]}\n")

    # add the mapping to mapping.csv
    with open("mapping.csv", "w") as mapping_file:
        mapping_file.write("Key,Value\n")
        for key, value in mapping.items():
            mapping_file.write(f"{key},{value}\n")


def train_context_builder(file):
    """
    Train the context builder on the uploaded file
    :param file: the uploaded file
    :return: the trained context builder
    """

    # the command to run it is:
    # python3 -m deepcase train --load-sequences sequences.save --save-builder builder.save





create_sequences("alerts.csv")