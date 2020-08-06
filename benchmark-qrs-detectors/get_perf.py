#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script compares QRS detections of an algorithm and beat annotations of specialists, in order to evaluate
performances of the chosen method in function of a tolerance's value. For that, it computes a confusion matrix with
criteria of interest, to calculate with those, different scores of performances. It studies also delays between
annotations and correct detections. Obtained results are saved in csv files (criteria & scores) and json files (delays).
"""

import numpy as np
import os
import click
import json
from dataset_helper import *
from algo_helper import *


def compute_confusion_matrix_and_delays(frames_detections: List[int], frames_annotations: List[int],
                                        tolerance_frames: int) -> Tuple[List[int], List[int]]:
    """
    compute the confusion matrix of the evaluation. For each annotation, consider a interval of tolerance around it, and
    check if there is a detection. If Yes : correct detection (TP) and the delays between the corresponding annotation
    and it is measured, if No : missed complex (FN). Every detections which were not in a tolerance interval around an
    annotation is a false detection (FP).

    :param frames_detections: list of QRS detections (localisations) of the chosen algorithm
    :type frames_detections: list(int)
    :param frames_annotations: list of beat annotations (localisations)
    :type frames_annotations: list(int)
    :param tolerance_frames: number of frames corresponding to the value of the tolerance in milliseconds
    :type tolerance_frames: int
    :return: list of calculated criteria and the list of delays between annotations and their corresponding correct
    detections
    :rtype: tuple(list(int),list(int))
    """
    true_pos = 0
    false_neg = 0
    delays = []
    for fr in frames_annotations:
        interval = range(fr - tolerance_frames, fr + tolerance_frames + 1)
        corresponding_detections_frame = list(set(interval).intersection(frames_detections))
        if len(corresponding_detections_frame) > 0:
            true_pos += 1
            delays.append(corresponding_detections_frame[0] - fr)
        else:
            false_neg += 1
    false_pos = len(frames_detections) - true_pos
    return [true_pos, false_pos, false_neg], [delays]


def get_scores(true_pos: int, false_pos: int, false_neg: int) -> List[float]:
    """
    calculate scores of performances with criteria of the computed confusion matrix : precision, recall or sensibility
    and F1-score.

    :param true_pos: number of correct detections
    :type true_pos: int
    :param false_pos: number of false detections
    :type false_pos: int
    :param false_neg: number of missed QRS complex
    :type false_neg: int
    :return: list of calculated scores : precision, recall or sensibility and F1-score
    :rtype: list(float)
    """
    positive_predictivity = round(100 * true_pos / (true_pos + false_pos), 2)
    recall = round(100 * true_pos / (true_pos + false_neg), 2)
    f1_score = round(100 * 2 * true_pos / ((2 * true_pos) + false_pos + false_neg), 2)
    return [positive_predictivity, recall, f1_score]


def get_perf_dataset(records_dict: Dict[str, List[str]], detections_dict: Dict[str, Dict[str, List[int]]],
                     annotations_dict: Dict[str, List[int]], tolerance: int, tolerance_sup1: int, tolerance_sup2: int) \
                    -> Generator[Tuple[str, List[int], List[int], List[pd.DataFrame]], None, None]:
    """
    get performances of the chosen algorithm for each record thanks to compute_confusion_matrix_and_delays and
    get_scores for 3 tolerance's values.

    :param records_dict: names of the record and its channel(s)
    :type records_dict: dict(str, list(str))
    :param detections_dict: QRS detections (localisations) of the chosen algorithm for each record
    :type detections_dict: dict(str, dict(str,list(int)))
    :param annotations_dict: list of beat annotations (localisations) for each record
    :type annotations_dict: dict(str, list(int))
    :param tolerance: accepted number of frames before and after an annotation to consider a detection as correct.
    It corresponds to the value of the tolerance in milliseconds (given as argument)
    :type tolerance: int
    :param tolerance_sup1: number of frames corresponding to the value of the tolerance in milliseconds (fixed in main())
    :type tolerance_sup1: int
    :param tolerance_sup2: number of frames corresponding to the value of the tolerance in milliseconds (fixed in main())
    :type tolerance_sup2: int
    :return: results of evaluation for each record: number of correct detections, delays between annotations and their
    corresponding correct detections and Series with criteria and scores of interest (number of annotations, number of
    false detections, number of missed QRS complexes, number of errors (FP+FN), rate of detection error, precision,
    recall or sensibility and F1-score)
    :rtype: tuple(str, list(int), list(int), list(DataFrame))
    """
    for id_rec in list(records_dict.keys()):
        number_beats = len(annotations_dict[id_rec])
        sig_name = records_dict[str(id_rec)][0]
        # given tolerance
        [true_pos_tol, false_pos_tol, false_neg_tol], delays_tol = compute_confusion_matrix_and_delays(
            detections_dict[str(id_rec)][sig_name], annotations_dict[id_rec], tolerance)
        false_tol = false_pos_tol + false_neg_tol
        false_per_tol = round(100 * false_tol / number_beats, 2)
        pos_predict_tol, recall_tol, f1_tol = get_scores(true_pos_tol, false_pos_tol, false_neg_tol)
        # first additional tolerance
        [true_pos_sup1, false_pos_sup1, false_neg_sup1], delays_sup1 = compute_confusion_matrix_and_delays(
            detections_dict[str(id_rec)][sig_name], annotations_dict[id_rec], tolerance_sup1)
        false_sup1 = false_pos_sup1 + false_neg_sup1
        false_per_sup1 = round(100 * false_sup1 / number_beats, 2)
        pos_predict_sup1, recall_sup1, f1_sup1 = get_scores(true_pos_sup1, false_pos_sup1, false_neg_sup1)
        # second additional tolerance
        [true_pos_sup2, false_pos_sup2, false_neg_sup2], delays_sup2 = compute_confusion_matrix_and_delays(
            detections_dict[str(id_rec)][sig_name], annotations_dict[id_rec], tolerance_sup2)
        false_sup2 = false_pos_sup2 + false_neg_sup2
        false_per_sup2 = round(100 * false_sup2 / number_beats, 2)
        pos_predict_sup2, recall_sup2, f1_sup2 = get_scores(true_pos_sup2, false_pos_sup2, false_neg_sup2)
        # lists to yield
        list_true_pos = [true_pos_tol, true_pos_sup1, true_pos_sup2]
        list_delays = [delays_tol, delays_sup1, delays_sup2]
        list_df = [pd.DataFrame([[int(number_beats), int(false_pos_tol), int(false_neg_tol), int(false_tol),
                                  false_per_tol, pos_predict_tol, recall_tol, f1_tol]], index=[id_rec],
                                columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)']),
                   pd.DataFrame([[int(number_beats), int(false_pos_sup1), int(false_neg_sup1), int(false_sup1),
                                  false_per_sup1, pos_predict_sup1, recall_sup1, f1_sup1]], index=[id_rec],
                                columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)']),
                   pd.DataFrame([[int(number_beats), int(false_pos_sup2), int(false_neg_sup2), int(false_sup2),
                                  false_per_sup2, pos_predict_sup2, recall_sup2, f1_sup2]], index=[id_rec],
                                columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
                   ]
        yield id_rec, list_true_pos, list_delays, list_df


def add_eval_global_line(performances_df: pd.DataFrame, nb_of_records: int, total_true_pos: int) -> pd.DataFrame:
    """
    get and calculate global criteria and scores on the entire dataset with those calculated for each record. Obtained
    results are added at the end of the global DataFrame (with performances for each record).

    :param performances_df: criteria and scores for each record
    :type performances_df: DataFrame
    :param nb_of_records: number of records in the studied dataset
    :type nb_of_records: int
    :param total_true_pos: number of correct detections in the entire dataset (sum of number of correct detections for
    each record)
    :type total_true_pos: int
    :return: criteria and scores for each record and for the entire dataset
    :rtype: DataFrame
    """
    total_beats = np.sum(performances_df.iloc[:nb_of_records, 0])
    total_false_pos = np.sum(performances_df.iloc[:nb_of_records, 1])
    total_false_neg = np.sum(performances_df.iloc[:nb_of_records, 2])
    glob_pos_predict, glob_recall, glob_f1 = get_scores(total_true_pos, total_false_pos, total_false_neg)
    global_perf = pd.DataFrame(
        [[total_beats, total_false_pos, total_false_neg, (total_false_pos + total_false_neg),
          round((100 * (total_false_pos + total_false_neg) / total_beats), 2), glob_pos_predict,
          glob_recall, glob_f1]],
        index=['global'],
        columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    blanks = pd.DataFrame([['_____', '_____', '_____', '_____', '_____', '_____', '_____', '_____']],
                          index=['_____'],
                          columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    performances_df = performances_df.append(blanks, ignore_index=False)
    final_performances_df = performances_df.append(global_perf, ignore_index=False)
    return final_performances_df


def write_delays_json(algorithm: str, dataset: str, tolerance_ms: int, delays_dict: Dict[str, List[int]]) -> None:
    """
    write delays between annotations and their corresponding correct detections for each record of the dataset from a
    dictionary in a json file.

    :param algorithm: name of the used method for QRS detection
    :type algorithm: str
    :param dataset: name of the studied dataset
    :type dataset: str
    :param tolerance_ms: accepted time before and after an annotation to consider a detection as correct
    :type tolerance_ms: int
    :param delays_dict: values of delays between annotations and their corresponding correct detections for each record
    :type delays_dict: dict(str, dict(str, list(int)))
    """
    os.makedirs(f'output/perf', exist_ok=True)
    with open(f'output/perf/{algorithm}_{dataset}_{tolerance_ms}.json', 'w') as outfile:
        json.dump(delays_dict, outfile)


def write_perf_csv(algorithm: str, dataset: str, tolerance_ms: int, perf_df: pd.DataFrame) -> None:
    """
    write criteria and scores calculated for each record and the entire dataset from a DataFrame with all results in a
    csv file.

    :param algorithm: name of the used method for QRS detection
    :type algorithm: str
    :param dataset: name of the studied dataset
    :type dataset: str
    :param tolerance_ms: accepted time before and after an annotation to consider a detection as correct
    :type tolerance_ms: int
    :param perf_df: results of evaluation (criteria and scores)
    :type perf_df: DataFrame
    """
    os.makedirs(f'output/perf', exist_ok=True)
    perf_df.to_csv(f'output/perf/{algorithm}_{dataset}_{tolerance_ms}' + '.csv', sep=',', index=True)


# parse arguments
@click.command()
@click.option('--data', required=True, type=click.Choice(datasets_list, case_sensitive=False), help='dataset')
@click.option('--algo', required=True, type=click.Choice(algorithms_list, case_sensitive=True), help='algorithm')
@click.option('--tol', required=True, type=click.IntRange(0, 1000, clamp=True),
              help='tolerance of the evaluation (in ms), type=int')
def main(data: str, algo: str, tol: int) -> None:
    dataset = data
    algorithm = algo
    fs = sampling_frequency[dataset]
    tol_sup1 = 25
    tol_sup2 = 50
    tolerances_fr = [int((tol * fs) / 1000), int((tol_sup1 * fs) / 1000), int((tol_sup2 * fs) / 1000)]
    records_dict = records[dataset]
    nb_of_records = len(records_dict.keys())

    with open(f'output/frames/{algorithm}_{dataset}.json') as detections_json:
        detections_dict = json.load(detections_json)
    with open(f'output/annotations/{dataset}.json') as annotations_json:
        annotations_dict = json.load(annotations_json)
    perf_generator = get_perf_dataset(records_dict, detections_dict, annotations_dict, tolerances_fr[0],
                                      tolerances_fr[1], tolerances_fr[2])

    total_true_pos_tol = 0
    total_true_pos_sup1 = 0
    total_true_pos_sup2 = 0
    delays_dict_tol = {}
    delays_dict_sup1 = {}
    delays_dict_sup2 = {}
    performances_tol = pd.DataFrame(columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    performances_sup1 = pd.DataFrame(columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    performances_sup2 = pd.DataFrame(columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    counter = 0
    print(f'Evaluation of performances of {algorithm} on dataset {dataset} is running....')
    while True:
        try:
            id_rec, list_true_pos, list_delays, list_performance = next(perf_generator)
            total_true_pos_tol += list_true_pos[0]
            total_true_pos_sup1 += list_true_pos[1]
            total_true_pos_sup2 += list_true_pos[2]
            delays_dict_tol[id_rec] = list_delays[0]
            delays_dict_sup1[id_rec] = list_delays[1]
            delays_dict_sup2[id_rec] = list_delays[2]
            performances_tol = performances_tol.append(list_performance[0], ignore_index=False)
            performances_sup1 = performances_sup1.append(list_performance[1], ignore_index=False)
            performances_sup2 = performances_sup2.append(list_performance[2], ignore_index=False)
            counter += 1
            print(f'{counter}/{nb_of_records}')
        except StopIteration:
            final_performances_tol = add_eval_global_line(performances_tol, nb_of_records, total_true_pos_tol)
            final_performances_sup1 = add_eval_global_line(performances_sup1, nb_of_records, total_true_pos_sup1)
            final_performances_sup2 = add_eval_global_line(performances_sup2, nb_of_records, total_true_pos_sup2)
            write_delays_json(algorithm, dataset, tol, delays_dict_tol)
            write_delays_json(algorithm, dataset, tol_sup1, delays_dict_sup1)
            write_delays_json(algorithm, dataset, tol_sup2, delays_dict_sup2)
            write_perf_csv(algorithm, dataset, int(tol), final_performances_tol)
            write_perf_csv(algorithm, dataset, tol_sup1, final_performances_sup1)
            write_perf_csv(algorithm, dataset, tol_sup2, final_performances_sup2)
            print(f'Evaluation of performances of {algorithm} on dataset {dataset} was successful....')
            break


main()
