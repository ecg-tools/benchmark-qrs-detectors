#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script gets chosen algorithm and dataset to perform detection thanks to methods from algo_helper and
dataset_helper modules. Obtained results (localisations of QRS for each channel of the entire dataset) are saved in json
 files."""

import os
import json
import click
from dataset_helper import *
from algo_helper import *


def write_detections_json(dataset: str, algorithm: str, dict_detections: Dict[str, Dict[str, List[int]]]) -> None:
    """
    write results of QRS detection from a dictionary in a json file.

    :param dataset: name of the studied dataset
    :type dataset: str
    :param algorithm: name of the used method for QRS detection
    :type algorithm: str
    :param dict_detections: results of QRS detections (localisations) for each record and each channel
    :type dict_detections: dict(str, dict(str, list(int)))
    """
    os.makedirs(f'output/frames', exist_ok=True)
    with open(f'output/frames/{algorithm}_{dataset}.json', 'w') as outfile:
        json.dump(dict_detections, outfile)


# parse arguments
@click.command()
@click.option('--data', required=True, type=click.Choice(datasets_list, case_sensitive=False), help='dataset')
@click.option('--algo', required=True, type=click.Choice(algorithms_list, case_sensitive=True), help='algorithm')
def main(data: str, algo: str) -> None:
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
