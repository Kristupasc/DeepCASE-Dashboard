import os
from deepcase.preprocessing.preprocessor import Preprocessor  # potentially change all this to use the deepcase module
from deepcase.context_builder.context_builder import ContextBuilder
from deepcase.interpreter.interpreter import Interpreter
import pandas as pd

import torch

"""
This file is used to process the data from the database and return it in a format that can be used by the front end.
Specifically, here we run the DeepCASE algorithm on the uploaded data and return the specific steps
"""


def create_sequences(file):
    """
    Create sequences from the uploaded file
    :param file: the uploaded file
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


def train_context_builder():
    """
    Train the context builder on the uploaded file
    """

    # the command to run it is:
    # python3 -m deepcase train --load-sequences sequences.save --save-builder builder.save

    # Load labels from the mapping.csv into a dict (Inefficient)
    mapping = {}
    with open("mapping.csv", "r") as mapping_file:
        next(mapping_file)
        for line in mapping_file:
            key, value = line.strip().split(',')
            mapping[key] = value

    events = len(mapping)

    context_builder = ContextBuilder(
        input_size=events,
        output_size=events,
        hidden_size=128,  # default value
        num_layers=1,
        max_length=10,  # default value
        bidirectional=False,
        LSTM=False,
    )

    with open("sequences.save", 'rb') as infile:
        sequences = torch.load(infile)
        context = sequences["context"]
        events = sequences["events"]
        labels = sequences["labels"]

    # Train the ContextBuilder
    context_builder.fit(
        X=context,
        y=events.reshape(-1, 1),
        epochs=10,  # default value
        batch_size=128,  # default value
        learning_rate=0.01,
        teach_ratio=0.5,
        verbose=True,
    )

    # Save the builder
    context_builder.save("builder.save")
    # TODO: the result is an ordered dict of weights so I don't know how do we convert it to .csv to make it make sense


def create_interpreter_clusters():
    """
    Create the interpreter clusters from the uploaded file
    """

    # the command to run it is:
    # python3 -m deepcase cluster --load-sequences sequences.save --load-builder builder.save
    #                                                   --save-interpreter interpreter.save --save-clusters clusters.csv

    # Load sequences
    with open("sequences.save", 'rb') as infile:
        sequences = torch.load(infile)
        context = sequences["context"]
        events = sequences["events"]
        labels = sequences["labels"]

    # Load context builder
    context_builder = ContextBuilder.load("builder.save")
    # with open("builder.save", 'rb') as infile:
    #     context_builder = torch.load(infile)

    # load labels from the mapping.csv into a dict (Inefficient)
    mapping = {}
    with open("mapping.csv", "r") as mapping_file:
        next(mapping_file)
        for line in mapping_file:
            key, value = line.strip().split(',')
            mapping[key] = value

    # Create Interpreter
    interpreter = Interpreter(
        context_builder=context_builder,
        features=len(mapping),
        eps=0.1,  # default value
        min_samples=5,  # default value
        threshold=0.2,  # default value
    )

    # Cluster samples with the interpreter
    clusters = interpreter.cluster(
        X=context,
        y=events.reshape(-1, 1),
        iterations=100,
        batch_size=1024,
        verbose=True,
    )

    # Save to file
    pd.DataFrame({
        'clusters': clusters,
        'labels': labels,
    }).to_csv("clusters.csv", index=False)

    # Save the interpreter
    interpreter.save("interpreter.save")


def manual_mode():
    """
    Run the deepcase algorithm in manual mode
    """

    # the command to run it is:
    # python3 -m deepcase manual --load-sequences sequences.save --load-builder builder.save
    # --load-interpreter interpreter.save --load-clusters clusters.csv --save-interpreter interpreter_fitted.save

    device = "cuda" if torch.cuda.is_available() else "cpu"

    context_builder = ContextBuilder.load("builder.save", device)

    interpreter = Interpreter.load(
        "interpreter.save",
        context_builder=context_builder,
    )

    # Load labels from csv file
    labels = pd.read_csv(
        "clusters.csv",
        index_col=False,
    )['labels'].values

    # Use given labels to compute score for each cluster
    scores = interpreter.score_clusters(labels, strategy="max")
    # Manually assign computed scores
    interpreter.score(scores, verbose=True)
    interpreter.save("interpreter_fitted.save")

    #TODO: open the interpreter_fitted.save and get the clusters and scores to store in the .csv file


def automatic_mode():
    """
    Run the deepcase algorithm in automatic mode
    """

    # the command to run it is:
    # python3 -m deepcase automatic --load-sequences sequences.save --load-builder builder.save
    #                                      --load-interpreter interpreter_fitted.save --save-prediction prediction.csv

    device = "cuda" if torch.cuda.is_available() else "cpu"

    context_builder = ContextBuilder.load("builder.save", device)

    interpreter = Interpreter.load(
        "interpreter.save",
        context_builder=context_builder,
    )

    with open("sequences.save", 'rb') as infile:
        sequences = torch.load(infile)
        context = sequences["context"]
        events = sequences["events"]

    # Compute predicted scores
    prediction = interpreter.predict(
        X=context,
        y=events.reshape(-1, 1),
        iterations=100,
        batch_size=1024,
        verbose=True,
    )

    # Save to file
    pd.DataFrame({
        'labels': prediction,
    }).to_csv("prediction.csv", index=False)

    #TODO: this is for some reason, not the result we get if we run all this in the command line. We need to check why


create_sequences("alerts.csv")
train_context_builder()
create_interpreter_clusters()
manual_mode()
automatic_mode()
