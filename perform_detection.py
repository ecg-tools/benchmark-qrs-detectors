import os
import json
import click
from dataset_helper import *
from algo_helper import *


# write json file
def write_detections_json(dataset, algorithm, dict_detections):
    os.makedirs(f'output/frames', exist_ok=True)
    with open(f'output/frames/{algorithm}_{dataset}.json', 'w') as outfile:
        json.dump(dict_detections, outfile)


# parse arguments/parameters
@click.command()
@click.option('--data', required=True, type=click.Choice(datasets_list, case_sensitive=False), help='dataset')
@click.option('--algo', required=True, type=click.Choice(algorithms_list, case_sensitive=True), help='algorithm')
def main(data, algo):
    dataset = data
    algorithm = algo
    data_generator = dataset_generators[dataset]
    records_dict = records[dataset]

    detections_dict = {}
    counter = 0
    print(f'Detection with {algorithm} on dataset {dataset} is running....')
    while True:
        try:
            record_id, record_sigs = next(data_generator)
            sig_names = records_dict[str(record_id)]
            detections_rec_dict = {}
            for id_sig in range(len(sig_names)):
                qrs_frames = run_algo(algorithm, record_sigs[sig_names[id_sig]], sampling_frequency[dataset])
                detections_rec_dict[sig_names[id_sig]] = qrs_frames
            detections_dict[record_id] = detections_rec_dict
            counter += 1
            print(f'{counter}/{len(records_dict.keys())}')
        except StopIteration:
            write_detections_json(dataset, algorithm, detections_dict)
            print(f'Detection with {algorithm} on dataset {dataset} was successful....')
            break


main()
