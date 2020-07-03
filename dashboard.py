import streamlit as st
import glob
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from math import nan
import os
import json

from dataset_helper import records, sampling_frequency
from algo_helper import algorithms_list

'''
# Benchmark of QRS detectors
'''


def get_layout(title):
    return go.Layout(title=title, margin=dict(l=20, r=20, t=30, b=20))


applications = ['Comparison of different algorithms', 'Evaluation of one algorithm', 'Noise robustness']
application = st.sidebar.selectbox('What would you like to study ?', applications)


def print_error_no_evaluation(ds='"#check --help#"', alg='"#check --help#"', t='#int(ms)#'):
    st.write('The evaluation of your interest has not already being performed. You probably did not execute the '
             'evaluation. Please compute the following command :')
    st.write(f'\t make evaluation --DATASET="{ds}" --ALGO="{alg}" --TOLERANCE={t}')


datasets_list = ['mit-bih-arrhythmia', 'european-stt', 'mit-bih-supraventricular-arrhythmia', 'mit-bih-long-term-ecg']

colormap = {
    'Pan-Tompkins-ecg-detector': ['red', 'circle'],
    'Hamilton-ecg-detector': ['green', 'circle'],
    'Christov-ecg-detector': ['blue', 'circle'],
    'Engelse-Zeelenberg-ecg-detector': ['cyan', 'circle'],
    'SWT-ecg-detector': ['magenta', 'circle'],
    'Matched-filter-ecg-detector': ['yellow', 'circle'],
    'Two-average-ecg-detector': ['black', 'circle'],
    'Hamilton-biosppy': ['green', 'star-diamond'],
    'Christov-biosppy': ['red', 'star-diamond'],
    'Engelse-Zeelenberg-biosppy': ['blue', 'star-diamond'],
    'Gamboa-biosppy': ['black', 'star-diamond'],
    'mne-ecg': ['black', 'square-dot'],
    'heartpy': ['cyan', 'x'],
    'gqrs-wfdb': ['blue', 'star-triangle-up'],
    'xqrs-wfdb': ['red', 'star-triangle-up']
}

if application == 'Comparison of different algorithms':
    st.write('\n\n')
    '''
    ## Comparison of performances of some algorithms on a dataset
    '''
    st.write('\n\n')

    dataset = st.selectbox('Please choose a dataset:', datasets_list)
    csv_files_dataset = glob.glob(f'output/perf/*_{dataset}_*.csv')
    tolerance_list = []
    for file in csv_files_dataset:
        eval_tolerance = file[:-4].split('_')[-1]
        tolerance_list.append(eval_tolerance)
    tolerance = st.selectbox('Please choose tolerance of the evaluation (in ms):', list(set(tolerance_list)))
    csv_files = [csv_file for csv_file in csv_files_dataset if csv_file[:-4].split('_')[-1] == tolerance]

    if len(csv_files) == 0:
        print_error_no_evaluation(ds=dataset)
    else:
        comparison_df = pd.DataFrame(columns=['FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
        number_of_beats = ''
        st.write('Please select algorithms you would like to compare:')
        if st.checkbox('Pan-Tompkins-ecg-detector'):
            if not os.path.exists(f'output/perf/Pan-Tompkins-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Pan-Tompkins-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Pan-Tompkins-ecg-detector_{dataset}_{tolerance}.csv',
                                         delimiter=',', index_col=0)
                results_df.iloc[-1, :].name = 'Pan-Tompkins-ecg-detector'
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Pan-Tompkins-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Hamilton-ecg-detector'):
            if not os.path.exists(f'output/perf/Hamilton-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Hamilton-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Hamilton-ecg-detector_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Hamilton-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Christov-ecg-detector'):
            if not os.path.exists(f'output/perf/Christov-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Christov-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Christov-ecg-detector_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Christov-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Engelse-Zeelenberg-ecg-detector'):
            if not os.path.exists(f'output/perf/Engelse-Zeelenberg-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Engelse-Zeelenberg-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Engelse-Zeelenberg-ecg-detector_{dataset}_{tolerance}.csv',
                                         delimiter=',', index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Engelse-Zeelenberg-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('SWT-ecg-detector'):
            if not os.path.exists(f'output/perf/SWT-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='SWT-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/SWT-ecg-detector_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'SWT-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Matched-filter-ecg-detector'):
            if not os.path.exists(f'output/perf/Matched-filter-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Matched-filter-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Matched-filter-ecg-detector_{dataset}_{tolerance}.csv',
                                         delimiter=',', index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Matched-filter-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Two-average-ecg-detector'):
            if not os.path.exists(f'output/perf/Two-average-ecg-detector_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Two-average-ecg-detector', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Two-average-ecg-detector_{dataset}_{tolerance}.csv',
                                         delimiter=',', index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Two-average-ecg-detector'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Hamilton-biosppy'):
            if not os.path.exists(f'output/perf/Hamilton-biosppy_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Hamilton-biosppy', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Hamilton-biosppy_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Hamilton-biosppy'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Christov-biosppy'):
            if not os.path.exists(f'output/perf/Christov-biosppy_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Christov-biosppy', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Christov-biosppy_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Christov-biosppy'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Engelse-Zeelenberg-biosppy'):
            if not os.path.exists(f'output/perf/Engelse-Zeelenberg-biosppy_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Engelse-Zeelenberg-biosppy', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Engelse-Zeelenberg-biosppy_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Engelse-Zeelenberg-biosppy'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('Gamboa-biosppy'):
            if not os.path.exists(f'output/perf/Gamboa-biosppy_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='Gamboa-biosppy', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/Gamboa-biosppy_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'Gamboa-biosppy'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('mne-ecg'):
            if not os.path.exists(f'output/perf/mne-ecg_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='mne-ecg', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/mne-ecg_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'mne-ecg'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('heartpy'):
            if not os.path.exists(f'output/perf/heartpy_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='heartpy', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/heartpy_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'heartpy'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('gqrs-wfdb'):
            if not os.path.exists(f'output/perf/gqrs-wfdb_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='gqrs-wfdb', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/gqrs-wfdb_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'gqrs-wfdb'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        if st.checkbox('xqrs-wfdb'):
            if not os.path.exists(f'output/perf/xqrs-wfdb_{dataset}_{tolerance}.csv'):
                print_error_no_evaluation(ds=dataset, alg='xqrs-wfdb', t=tolerance)
            else:
                results_df = pd.read_csv(f'output/perf/xqrs-wfdb_{dataset}_{tolerance}.csv', delimiter=',',
                                         index_col=0)
                global_eval = results_df.iloc[-1, 1:]
                global_eval.name = 'xqrs-wfdb'
                comparison_df = comparison_df.append(global_eval)
                number_of_beats = results_df.iloc[-1, 0]
        st.write(f"Comparative table of global performances: ")
        st.write(comparison_df)
        st.write(f'Total number of beats for this dataset is : {number_of_beats}')

        '''
        ## Comparison of performances of algorithms on different datasets
        '''
        tol = 50
        results_F1 = pd.DataFrame(columns=datasets_list, index=algorithms_list)
        results_Fp = pd.DataFrame(columns=datasets_list, index=algorithms_list)
        for algo in algorithms_list:
            for dataset in datasets_list:
                if os.path.exists(f'output/perf/{algo}_{dataset}_50.csv'):
                    results_df = pd.read_csv(f'output/perf/{algo}_{dataset}_50.csv', delimiter=',')
                    results_F1.loc[algo, dataset] = results_df.iloc[-1, -1]
                    results_Fp.loc[algo, dataset] = results_df.iloc[-1, 5]
                else:
                    results_F1.loc[algo, dataset] = nan
                    results_Fp.loc[algo, dataset] = nan
        fig_F1 = go.Figure(layout=get_layout('F1 score of every algorithms for each dataset (tolerance=50ms)'))
        fig_Fp = go.Figure(layout=get_layout('Rate of detection failure of every algorithms for each dataset '
                                             '(tolerance=50ms)'))
        for algo in algorithms_list:
            F1_algo = results_F1.loc[algo, :]
            Fp_algo = results_Fp.loc[algo, :]
            fig_F1.add_trace(go.Scatter(x=datasets_list,
                                        y=F1_algo,
                                        mode='lines+markers',
                                        marker=dict(size=10, color=colormap[algo][0], symbol=colormap[algo][1]),
                                        name=algo))
            fig_Fp.add_trace(go.Scatter(x=datasets_list,
                                        y=Fp_algo,
                                        mode='lines+markers',
                                        marker=dict(size=10, color=colormap[algo][0], symbol=colormap[algo][1]),
                                        name=algo))
            fig_F1.update_layout(autosize=False,
                                 width=800,
                                 height=600)
            fig_Fp.update_layout(autosize=False,
                                 width=800,
                                 height=600)
        st.plotly_chart(fig_F1)
        st.plotly_chart(fig_Fp)


elif application == 'Evaluation of one algorithm':
    st.write('\n\n')
    '''
    ## Complete evaluation of an algorithm on a dataset
    '''
    st.write('\n\n')

    dataset = st.selectbox('Please choose a dataset:', datasets_list)
    algorithm = st.selectbox('Please choose an algorithm:', algorithms_list)

    csv_files = glob.glob(f'output/perf/{algorithm}_{dataset}_*.csv')
    json_files = glob.glob(f'output/perf/{algorithm}_{dataset}_*.json')

    if len(csv_files) == 0 or len(json_files) == 0:
        print_error_no_evaluation(ds=dataset, alg=algorithm)
    else:
        if st.checkbox("Display performances' scores"):
            for file in csv_files:
                results_df = pd.read_csv(file, delimiter=',', index_col=0)
                tolerance = file[:-4].split('_')[-1]
                st.write(f"Evaluation's results for a tolerance of {tolerance} ms: ")
                st.write(results_df)
        if st.checkbox("Display delays' plots"):
            freq_sampling = sampling_frequency[dataset]
            st.write(f'Signals of this dataset ({dataset}) was sampled at {freq_sampling}Hz. It means that 1 second of '
                     f'recording corresponds to {freq_sampling} frames.')
            id_records = list(records[dataset].keys())
            record_id = st.selectbox('Please choose the record', id_records)
            for file in json_files:
                with open(file) as json_delays:
                    dict_delays = json.load(json_delays)
                    tolerance = int(file[:-5].split('_')[-1])
                    tolerance_fr = int((tolerance * 360 / 1000))
                    plt.hist(dict_delays[record_id], range=(-tolerance_fr, tolerance_fr + 1), bins=2 * tolerance_fr,
                             label=f'tolerance : {tolerance}ms')
                    plt.xlabel('delay (nb of frames)')
                    plt.ylabel('count of annotations detected with each delay')
                    plt.title(f'Distribution of Delays for Record {record_id}')
                    plt.legend()
                    st.pyplot()

elif application == 'Noise robustness':
    st.write('\n\n')
    '''
    ## Comparison of performances of one algorithm for different SNRs
    '''
    st.write('\n\n')
    st.write('Impact of the electrode motion artefact')

    algorithm = st.selectbox('Please choose an algorithm:', algorithms_list)
    csv_files_noise_stress = glob.glob(f'output/perf/{algorithm}_mit-bih-noise-stress-test-*_*.csv')
    tolerance_list = []
    for file in csv_files_noise_stress:
        eval_tolerance = file[:-4].split('_')[-1]
        tolerance_list.append(eval_tolerance)
    tolerance = st.selectbox('Please choose tolerance of the evaluation (in ms):', list(set(tolerance_list)))
    csv_files = [csv_file for csv_file in csv_files_noise_stress if csv_file[:-4].split('_')[-1] == tolerance]

    st.write('Indexes (IDeSNR) correspond to the ID of the record and its SNR during the "noisy segments" in dB. The '
             'record without added noise belongs to the MIT-BIH arrhythmia database.'
             'Available SNRs with the MIT-BIH noise stress test are -6, 0, 6, 12, 18, 24. If one or more are missing, '
             'it means the evaluation has not already being performed. You probably did not execute the evaluation. '
             'Please compute the following command :')
    st.write(f'\t make evaluation --DATASET="mit-bih-noise-stress-test-e#SNR" --ALGO="{algorithm}" '
             f'--TOLERANCE={tolerance}')
    comparison_df_118 = pd.DataFrame(columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    comparison_df_119 = pd.DataFrame(columns=['nbofbeats', 'FP', 'FN', 'F', 'F(%)', 'P+(%)', 'Se(%)', 'F1(%)'])
    if os.path.exists(f'output/perf/{algorithm}_mit-bih-arrhythmia_{tolerance}.csv'):
        df_without_noise = pd.read_csv(f'output/perf/{algorithm}_mit-bih-arrhythmia_{tolerance}.csv', delimiter=',',
                                       index_col=0)
        comparison_df_118 = comparison_df_118.append(df_without_noise.loc['118', :])
        comparison_df_119 = comparison_df_119.append(df_without_noise.loc['119', :])
    for csv_file in csv_files:
        results_df = pd.read_csv(csv_file, delimiter=',', index_col=0)
        comparison_df_118 = comparison_df_118.append(results_df.iloc[0, :])
        comparison_df_119 = comparison_df_119.append(results_df.iloc[1, :])
    st.write(comparison_df_118)
    st.write(comparison_df_119)

    tol = 50
    SNR_list = ['_6', '00', '06', '12', '18', '24']
    results_F1 = pd.DataFrame(columns=SNR_list, index=algorithms_list)
    results_Fp = pd.DataFrame(columns=SNR_list, index=algorithms_list)
    for algo in algorithms_list:
        for snr in SNR_list:
            dataset = f"mit-bih-noise-stress-test-e{snr}"
            if os.path.exists(f'output/perf/{algo}_{dataset}_50.csv'):
                results_df = pd.read_csv(f'output/perf/{algo}_{dataset}_50.csv', delimiter=',')
                results_F1.loc[algo, snr] = results_df.iloc[-1, -1]
                results_Fp.loc[algo, snr] = results_df.iloc[-1, 5]
            else:
                results_F1.loc[algo, snr] = nan
                results_Fp.loc[algo, snr] = nan
    fig_F1 = go.Figure(layout=get_layout('F1 score of every algorithms for each value of SNR (tolerance=50ms)'))
    fig_Fp = go.Figure(layout=get_layout('Rate of detection failure of every algorithms for each value of SNR'
                                         '(tolerance=50ms)'))
    for algo in algorithms_list:
        F1_algo = results_F1.loc[algo, :]
        Fp_algo = results_Fp.loc[algo, :]
        fig_F1.add_trace(go.Scatter(x=SNR_list,
                                    y=F1_algo,
                                    mode='lines+markers',
                                    marker=dict(size=10, color=colormap[algo][0], symbol=colormap[algo][1]),
                                    name=algo))
        fig_Fp.add_trace(go.Scatter(x=SNR_list,
                                    y=Fp_algo,
                                    mode='lines+markers',
                                    marker=dict(size=10, color=colormap[algo][0], symbol=colormap[algo][1]),
                                    name=algo))
        fig_F1.update_layout(autosize=False,
                             xaxis_type='category',
                             xaxis_title="SNR (dB)",
                             width=800,
                             height=600)
        fig_Fp.update_layout(autosize=False,
                             xaxis_type='category',
                             xaxis_title="SNR (dB)",
                             width=800,
                             height=600)
    st.plotly_chart(fig_F1)
    st.plotly_chart(fig_Fp)
