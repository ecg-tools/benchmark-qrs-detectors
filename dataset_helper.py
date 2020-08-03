import wfdb
import pandas as pd
from typing import  Generator, Dict, Tuple
data_path = 'data'

# list all dataset
datasets_list = ['mit-bih-arrhythmia', 'mit-bih-noise-stress-test-e24', 'mit-bih-noise-stress-test-e18',
                 'mit-bih-noise-stress-test-e12', 'mit-bih-noise-stress-test-e06', 'mit-bih-noise-stress-test-e00',
                 'mit-bih-noise-stress-test-e_6', 'european-stt', 'mit-bih-supraventricular-arrhythmia',
                 'mit-bih-long-term-ecg']

# MIT-BIH Arrhythmia Database
# records
mit_bih_arrhythmia = {
    '100': ['MLII', 'V5'],
    '101': ['MLII', 'V1'],
    '102': ['V5', 'V2'],
    '103': ['MLII', 'V2'],
    '104': ['V5', 'V2'],
    '105': ['MLII', 'V1'],
    '106': ['MLII', 'V1'],
    '107': ['MLII', 'V1'],
    '108': ['MLII', 'V1'],
    '109': ['MLII', 'V1'],
    '111': ['MLII', 'V1'],
    '112': ['MLII', 'V1'],
    '113': ['MLII', 'V1'],
    '114': ['MLII', 'V5'],
    '115': ['MLII', 'V1'],
    '116': ['MLII', 'V1'],
    '117': ['MLII', 'V2'],
    '118': ['MLII', 'V1'],
    '119': ['MLII', 'V1'],
    '121': ['MLII', 'V1'],
    '122': ['MLII', 'V1'],
    '123': ['MLII', 'V5'],
    '124': ['MLII', 'V4'],
    '200': ['MLII', 'V1'],
    '201': ['MLII', 'V1'],
    '202': ['MLII', 'V1'],
    '203': ['MLII', 'V1'],
    '205': ['MLII', 'V1'],
    '207': ['MLII', 'V1'],
    '208': ['MLII', 'V1'],
    '209': ['MLII', 'V1'],
    '210': ['MLII', 'V1'],
    '212': ['MLII', 'V1'],
    '213': ['MLII', 'V1'],
    '214': ['MLII', 'V1'],
    '215': ['MLII', 'V1'],
    '217': ['MLII', 'V1'],
    '219': ['MLII', 'V1'],
    '220': ['MLII', 'V1'],
    '221': ['MLII', 'V1'],
    '222': ['MLII', 'V1'],
    '223': ['MLII', 'V1'],
    '228': ['MLII', 'V1'],
    '230': ['MLII', 'V1'],
    '231': ['MLII', 'V1'],
    '232': ['MLII', 'V1'],
    '233': ['MLII', 'V1'],
    '234': ['MLII', 'V1']
}


# load data
def read_mit_bih_arrhythmia() -> Generator[Tuple[int, Dict], None, None]:
    records_list = pd.read_csv(f'{data_path}/mit-bih-arrhythmia-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-arrhythmia-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


# MIT-BIH Noise stress test Database
# records
mit_bih_noise_stress_test_e24 = {
    '118e24': ['MLII', 'V1'],
    '119e24': ['MLII', 'V1']
}

mit_bih_noise_stress_test_e18 = {
    '118e18': ['MLII', 'V1'],
    '119e18': ['MLII', 'V1']
}

mit_bih_noise_stress_test_e12 = {
    '118e12': ['MLII', 'V1'],
    '119e12': ['MLII', 'V1']
}

mit_bih_noise_stress_test_e06 = {
    '118e06': ['MLII', 'V1'],
    '119e06': ['MLII', 'V1']
}

mit_bih_noise_stress_test_e00 = {
    '118e00': ['MLII', 'V1'],
    '119e00': ['MLII', 'V1']
}

mit_bih_noise_stress_test_e_6 = {
    '118e_6': ['MLII', 'V1'],
    '119e_6': ['MLII', 'V1']
}


# load data
def read_mit_bih_noise_e24() -> Generator[Tuple[int, Dict], None, None]:
    rec_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    records_list = [record_id for record_id in rec_list['id'] if record_id.find('e24') != -1]
    for record_id in records_list:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


def read_mit_bih_noise_e18() -> Generator[Tuple[int, Dict], None, None]:
    rec_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    records_list = [record_id for record_id in rec_list['id'] if record_id.find('e18') != -1]
    for record_id in records_list:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


def read_mit_bih_noise_e12() -> Generator[Tuple[int, Dict], None, None]:
    rec_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    records_list = [record_id for record_id in rec_list['id'] if record_id.find('e12') != -1]
    for record_id in records_list:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


def read_mit_bih_noise_e06() -> Generator[Tuple[int, Dict], None, None]:
    rec_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    records_list = [record_id for record_id in rec_list['id'] if record_id.find('e06') != -1]
    for record_id in records_list:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


def read_mit_bih_noise_e00() -> Generator[Tuple[int, Dict], None, None]:
    rec_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    records_list = [record_id for record_id in rec_list['id'] if record_id.find('e00') != -1]
    for record_id in records_list:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


def read_mit_bih_noise_e_6() -> Generator[Tuple[int, Dict], None, None]:
    rec_list = pd.read_csv(f'{data_path}/mit-bih-noise-stress-test-database/RECORDS', names=['id'])
    records_list = [record_id for record_id in rec_list['id'] if record_id.find('e_6') != -1]
    for record_id in records_list:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-noise-stress-test-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


# European ST-T Database
# records
european_stt = {
    'e0103': ['V4', 'MLIII'],
    'e0104': ['MLIII', 'V4'],
    'e0105': ['MLIII', 'V4'],
    'e0106': ['MLIII', 'V3'],
    'e0107': ['D3', 'V4'],
    'e0108': ['V4', 'MLIII'],
    'e0110': ['V3', 'MLIII'],
    'e0111': ['MLIII', 'V4'],
    'e0112': ['MLIII', 'V4'],
    'e0113': ['MLIII', 'V4'],
    'e0114': ['MLIII', 'V4'],
    'e0115': ['V5', 'MLIII'],
    'e0116': ['V4', 'MLIII'],
    'e0118': ['V4', 'MLIII'],
    'e0119': ['V4', 'MLIII'],
    'e0121': ['V4', 'MLIII'],
    'e0122': ['V4', 'MLIII'],
    'e0123': ['V4', 'MLIII'],
    'e0124': ['V4', 'MLIII'],
    'e0125': ['V4', 'MLIII'],
    'e0126': ['V4', 'MLIII'],
    'e0127': ['V4', 'MLIII'],
    'e0129': ['MLIII', 'V3'],
    'e0133': ['MLIII', 'V3'],
    'e0136': ['MLIII', 'V4'],
    'e0139': ['MLIII', 'V4'],
    'e0147': ['MLIII', 'V4'],
    'e0148': ['MLIII', 'V4'],
    'e0151': ['V3', 'MLIII'],
    'e0154': ['MLIII', 'V4'],
    'e0155': ['MLIII', 'V4'],
    'e0159': ['MLIII', 'V4'],
    'e0161': ['V4', 'MLIII'],
    'e0162': ['MLIII', 'V4'],
    'e0163': ['MLIII', 'V4'],
    'e0166': ['V4', 'MLIII'],
    'e0170': ['V4', 'MLIII'],
    'e0202': ['V5', 'MLI'],
    'e0203': ['V5', 'MLI'],
    'e0204': ['V5', 'MLI'],
    'e0205': ['V5', 'MLI'],
    'e0206': ['V5', 'MLI'],
    'e0207': ['V5', 'MLI'],
    'e0208': ['V5', 'MLI'],
    'e0210': ['V5', 'MLI'],
    'e0211': ['V5', 'MLI'],
    'e0212': ['V5', 'MLI'],
    'e0213': ['V5', 'MLI'],
    'e0302': ['V3', 'V5'],
    'e0303': ['V2', 'V5'],
    'e0304': ['V3', 'V5'],
    'e0305': ['V2', 'V5'],
    'e0306': ['V2', 'V5'],
    'e0403': ['V5', 'V1'],
    'e0404': ['V5', 'MLI'],
    'e0405': ['V5', 'V1'],
    'e0406': ['V5', 'MLI'],
    'e0408': ['V5', 'MLI'],
    'e0409': ['V5', 'MLI'],
    'e0410': ['V5', 'MLI'],
    'e0411': ['V5', 'MLI'],
    'e0413': ['V2', 'V5'],
    'e0415': ['V2', 'V5'],
    'e0417': ['V5', 'MLI'],
    'e0418': ['V5', 'MLI'],
    'e0501': ['V2', 'V4'],
    'e0509': ['V2', 'V4'],
    'e0515': ['V2', 'V5'],
    'e0601': ['V5', 'MLIII'],
    'e0602': ['V5', 'MLIII'],
    'e0603': ['V5', 'V2'],
    'e0604': ['V2', 'MLIII'],
    'e0605': ['V5', 'MLIII'],
    'e0606': ['V5', 'MLIII'],
    'e0607': ['V5', 'V4'],
    'e0609': ['V5', 'MLIII'],
    'e0610': ['V5', 'MLIII'],
    'e0611': ['V5', 'MLIII'],
    'e0612': ['V5', 'MLIII'],
    'e0613': ['V5', 'MLIII'],
    'e0614': ['V5', 'V1'],
    'e0615': ['V5', 'MLIII'],
    'e0704': ['V5', 'V1'],
    'e0801': ['V1', 'V5'],
    'e0808': ['V5', 'V1'],
    'e0817': ['V5', 'V1'],
    'e0818': ['V5', 'V1'],
    'e1301': ['V1', 'V5'],
    'e1302': ['V1', 'V5'],
    'e1304': ['V1', 'V5']
}


# load data
def read_european_stt() -> Generator[Tuple[int, Dict], None, None]:
    records_list = pd.read_csv(f'{data_path}/european-stt-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        record = wfdb.rdrecord(f'{data_path}/european-stt-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


# MIT-BIH Supraventricular Arrhythmia Database
# records
mit_bih_supraventricular_arrhythmia = {
    '800': ['ECG1', 'ECG2'],
    '801': ['ECG1', 'ECG2'],
    '802': ['ECG1', 'ECG2'],
    '803': ['ECG1', 'ECG2'],
    '804': ['ECG1', 'ECG2'],
    '805': ['ECG1', 'ECG2'],
    '806': ['ECG1', 'ECG2'],
    '807': ['ECG1', 'ECG2'],
    '808': ['ECG1', 'ECG2'],
    '809': ['ECG1', 'ECG2'],
    '810': ['ECG1', 'ECG2'],
    '811': ['ECG1', 'ECG2'],
    '812': ['ECG1', 'ECG2'],
    '820': ['ECG1', 'ECG2'],
    '821': ['ECG1', 'ECG2'],
    '822': ['ECG1', 'ECG2'],
    '823': ['ECG1', 'ECG2'],
    '824': ['ECG1', 'ECG2'],
    '825': ['ECG1', 'ECG2'],
    '826': ['ECG1', 'ECG2'],
    '827': ['ECG1', 'ECG2'],
    '828': ['ECG1', 'ECG2'],
    '829': ['ECG1', 'ECG2'],
    '840': ['ECG1', 'ECG2'],
    '841': ['ECG1', 'ECG2'],
    '842': ['ECG1', 'ECG2'],
    '843': ['ECG1', 'ECG2'],
    '844': ['ECG1', 'ECG2'],
    '845': ['ECG1', 'ECG2'],
    '846': ['ECG1', 'ECG2'],
    '847': ['ECG1', 'ECG2'],
    '848': ['ECG1', 'ECG2'],
    '849': ['ECG1', 'ECG2'],
    '850': ['ECG1', 'ECG2'],
    '851': ['ECG1', 'ECG2'],
    '852': ['ECG1', 'ECG2'],
    '853': ['ECG1', 'ECG2'],
    '854': ['ECG1', 'ECG2'],
    '855': ['ECG1', 'ECG2'],
    '856': ['ECG1', 'ECG2'],
    '857': ['ECG1', 'ECG2'],
    '858': ['ECG1', 'ECG2'],
    '859': ['ECG1', 'ECG2'],
    '860': ['ECG1', 'ECG2'],
    '861': ['ECG1', 'ECG2'],
    '862': ['ECG1', 'ECG2'],
    '863': ['ECG1', 'ECG2'],
    '864': ['ECG1', 'ECG2'],
    '865': ['ECG1', 'ECG2'],
    '866': ['ECG1', 'ECG2'],
    '867': ['ECG1', 'ECG2'],
    '868': ['ECG1', 'ECG2'],
    '869': ['ECG1', 'ECG2'],
    '870': ['ECG1', 'ECG2'],
    '871': ['ECG1', 'ECG2'],
    '872': ['ECG1', 'ECG2'],
    '873': ['ECG1', 'ECG2'],
    '874': ['ECG1', 'ECG2'],
    '875': ['ECG1', 'ECG2'],
    '876': ['ECG1', 'ECG2'],
    '877': ['ECG1', 'ECG2'],
    '878': ['ECG1', 'ECG2'],
    '879': ['ECG1', 'ECG2'],
    '880': ['ECG1', 'ECG2'],
    '881': ['ECG1', 'ECG2'],
    '882': ['ECG1', 'ECG2'],
    '883': ['ECG1', 'ECG2'],
    '884': ['ECG1', 'ECG2'],
    '885': ['ECG1', 'ECG2'],
    '886': ['ECG1', 'ECG2'],
    '887': ['ECG1', 'ECG2'],
    '888': ['ECG1', 'ECG2'],
    '889': ['ECG1', 'ECG2'],
    '890': ['ECG1', 'ECG2'],
    '891': ['ECG1', 'ECG2'],
    '892': ['ECG1', 'ECG2'],
    '893': ['ECG1', 'ECG2'],
    '894': ['ECG1', 'ECG2']
}


# load data
def read_mit_bih_supraventricular_arrhythmia() -> Generator[Tuple[int, Dict], None, None]:
    records_list = pd.read_csv(f'{data_path}/mit-bih-supraventricular-arrhythmia-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-supraventricular-arrhythmia-database/{record_id}')
        yield record_id, {
            record.sig_name[0]: record.p_signal[:, 0],
            record.sig_name[1]: record.p_signal[:, 1]
        }


# MIT-BIH Long Term Database
# records
mit_bih_long_term = {
    '14046': ['ECG1', 'ECG2'],
    '14134': ['ECG1', 'ECG2'],
    '14149': ['ECG1', 'ECG2'],
    '14157': ['ECG1', 'ECG2'],
    '14172': ['ECG1', 'ECG2'],
    '14184': ['ECG1', 'ECG2'],
    '15814': ['ECG1', 'ECG2', 'ECG3']
}


# load data
def read_mit_bih_long_term() -> Generator[Tuple[int, Dict], None, None]:
    records_list = pd.read_csv(f'{data_path}/mit-bih-long-term-ecg-database/RECORDS', names=['id'])
    for record_id in records_list['id']:
        record = wfdb.rdrecord(f'{data_path}/mit-bih-long-term-ecg-database/{record_id}')
        record_sigs = {}
        for id_sig in range(len(record.sig_name)):
            record_sigs[record.sig_name[id_sig]] = record.p_signal[:, id_sig]
        yield record_id, record_sigs


# generator for reading records
dataset_generators = {
    'mit-bih-arrhythmia': read_mit_bih_arrhythmia(),
    'mit-bih-noise-stress-test-e24': read_mit_bih_noise_e24(),
    'mit-bih-noise-stress-test-e18': read_mit_bih_noise_e18(),
    'mit-bih-noise-stress-test-e12': read_mit_bih_noise_e12(),
    'mit-bih-noise-stress-test-e06': read_mit_bih_noise_e06(),
    'mit-bih-noise-stress-test-e00': read_mit_bih_noise_e00(),
    'mit-bih-noise-stress-test-e_6': read_mit_bih_noise_e_6(),
    'european-stt': read_european_stt(),
    'mit-bih-supraventricular-arrhythmia': read_mit_bih_supraventricular_arrhythmia(),
    'mit-bih-long-term-ecg': read_mit_bih_long_term()
}

#generator for names of records and their channels
records = {
    'mit-bih-arrhythmia': mit_bih_arrhythmia,
    'mit-bih-noise-stress-test-e24': mit_bih_noise_stress_test_e24,
    'mit-bih-noise-stress-test-e18': mit_bih_noise_stress_test_e18,
    'mit-bih-noise-stress-test-e12': mit_bih_noise_stress_test_e12,
    'mit-bih-noise-stress-test-e06': mit_bih_noise_stress_test_e06,
    'mit-bih-noise-stress-test-e00': mit_bih_noise_stress_test_e00,
    'mit-bih-noise-stress-test-e_6': mit_bih_noise_stress_test_e_6,
    'european-stt': european_stt,
    'mit-bih-supraventricular-arrhythmia': mit_bih_supraventricular_arrhythmia,
    'mit-bih-long-term-ecg': mit_bih_long_term
}

#generator for value of sampling frequence
sampling_frequency = {
    'mit-bih-arrhythmia': 360,
    'mit-bih-noise-stress-test-e24': 360,
    'mit-bih-noise-stress-test-e18': 360,
    'mit-bih-noise-stress-test-e12': 360,
    'mit-bih-noise-stress-test-e06': 360,
    'mit-bih-noise-stress-test-e00': 360,
    'mit-bih-noise-stress-test-e_6': 360,
    'european-stt': 250,
    'mit-bih-supraventricular-arrhythmia': 128,
    'mit-bih-long-term-ecg': 128
}
