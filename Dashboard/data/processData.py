import subprocess
import torch

"""
This file is used to process the data from the database and return it in a format that can be used by the front end.
Specifically, here we run the DeepCASE algorithm on the uploaded data and return the specific steps
"""

main_file_path = '../../DeepCase/deepcase/__main__.py'


def create_sequences(file):
    """
    Create sequences from the uploaded file
    :param file: the uploaded file
    """

    # the command to run it is:
    # python3 -m deepcase sequence --csv alerts.csv --save-sequences sequences.save

    arguments = ['sequence', '--csv', file, '--save-sequences', 'sequences.save']
    command = ['python3', main_file_path] + arguments
    subprocess.run(command, check=True)

    with open('sequences.save', 'rb') as infile:
        # Load data
        data = torch.load(infile)
        # Extract data
        events = data["events"]
        context = data["context"]
        labels = data["labels"]
        mapping = data["mapping"]

    # write the sequences to a .csv file
    with open("sequences.csv", "w") as result_file:
        result_file.write("Context,Event,Label\n")
        for i in range(len(context)):
            result_file.write(f'"{context[i]}",{events[i]},{labels[i]}\n')

    # add the mapping to mapping.csv
    with open("mapping.csv", "w") as mapping_file:
        mapping_file.write("Key,Value\n")
        for key, value in mapping.items():
            mapping_file.write(f"{key},{value}\n")

    #TODO: maybe add a return True here, so that the server knows that the file was processed correctly?


def train_context_builder():
    """
    Train the context builder on the uploaded file
    """

    # the command to run it is:
    # python3 -m deepcase train --load-sequences sequences.save --save-builder builder.save
    arguments = ['train', '--load-sequences', 'sequences.save', '--save-builder', 'builder.save']
    command = ['python3', main_file_path] + arguments
    subprocess.run(command, check=True)
    # TODO: the result is an ordered dict of weights so I don't know how do we convert it to .csv to make it make sense


def create_interpreter_clusters():
    """
    Create the interpreter clusters from the uploaded file
    """

    # the command to run it is:
    # python3 -m deepcase cluster --load-sequences sequences.save --load-builder builder.save
    #                                                   --save-interpreter interpreter.save --save-clusters clusters.csv

    arguments = ['cluster', '--load-sequences', 'sequences.save', '--load-builder', 'builder.save',
                 '--save-interpreter',
                 'interpreter.save', '--save-clusters', 'clusters.csv']
    command = ['python3', main_file_path] + arguments
    subprocess.run(command, check=True)


def manual_mode():
    """
    Run the deepcase algorithm in manual mode
    """

    # the command to run it is:
    # python3 -m deepcase manual --load-sequences sequences.save --load-builder builder.save
    # --load-interpreter interpreter.save --load-clusters clusters.csv --save-interpreter interpreter_fitted.save
    arguments = ['manual', '--load-sequences', 'sequences.save', '--load-builder', 'builder.save',
                 '--load-interpreter', 'interpreter.save', '--load-clusters', 'clusters.csv', '--save-interpreter',
                 'interpreter_fitted.save']
    command = ['python3', main_file_path] + arguments
    subprocess.run(command, check=True)

    #TODO: open the interpreter_fitted.save and get the clusters and scores to store in the .csv file


def automatic_mode(printing = False):
    """
    Run the deepcase algorithm in automatic mode
    """

    # the command to run it is:
    # python3 -m deepcase automatic --load-sequences sequences.save --load-builder builder.save
    #                                      --load-interpreter interpreter_fitted.save --save-prediction prediction.csv
    arguments = ['automatic', '--load-sequences', 'sequences.save', '--load-builder', 'builder.save',
                 '--load-interpreter', 'interpreter.save', '--save-prediction', 'prediction.csv']
    command = ['python3', main_file_path] + arguments
    subprocess.run(command, check=True)
    #TODO: this is for some reason, not the result we get if we run all this in the command line. We need to check why


create_sequences("alerts.csv")
train_context_builder()
create_interpreter_clusters()
manual_mode()
automatic_mode()
