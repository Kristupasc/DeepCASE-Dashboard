class csv_file_manager(object):
    def __init__(self):
        super(csv_file_manager, self).__init__()

    def save_sequencing_results(self, context, events, labels, mapping):
        # write the sequences to a .csv file
        with open("sequences.csv", "w") as result_file:
            result_file.write("Context,Event,Label\n")
            for i in range(len(context)):
                result_file.write(f'"{context[i].tolist()}",{events[i]},{labels[i]}\n')

        # add the mapping to mapping.csv
        with open("mapping.csv", "w") as mapping_file:
            mapping_file.write("Key,Value\n")
            for key, value in mapping.items():
                mapping_file.write(f'{key},"{value}"\n')

        # TODO: maybe add a return True here, so that the server knows that the file was processed correctly?

    def save_clustering_results(self, clusters):
        with open("clusters.csv", "w") as result_file:
            result_file.write("Clusters,Labels\n")
            for i in range(len(clusters)):
                result_file.write(f'{clusters[i]}\n')

    def save_prediction_results(self, prediction):

        with open("prediction.csv", "w") as result_file:
            result_file.write("Labels\n")
            for i in range(len(prediction)):
                result_file.write(f'{prediction[i]}\n')
