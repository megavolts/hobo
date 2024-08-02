from pandas import read_csv, concat
from logging import getLogger

logger = getLogger(__name__)
def concatenate_files(filepaths, sort_time=True, duplicate=True):
    """
    Concatenate all files, if logger name in first row is identical
    :param filepaths: list of string, containing the filepath of files to concatenate
    :param sort_time: boolean, if True sort data according to timestamp
    :param duplicate: boolean; if False remove duplicate row
    :return : pd.DataFrame(), containing the concatenated files
    """
    for ii_f, fn in enumerate(filepaths):
        if ii_f == 0:
            with open(fn, 'r', encoding='utf-8') as f:
                h_lines = f.readlines()[:1]
            data = read_csv(fn, sep=',', header=1)
        else:
            with open(fn, 'r', encoding='utf-8') as f:
                c_lines = f.readlines()[:1]
            if c_lines == h_lines:
                data = concat([data, read_csv(fn, sep=',', header=1)])
            else:
                logger.warning(f"Can not concatenate {fn} due to mismatched hobo logger name")

    if not duplicate:
        data.drop_duplicates(axis=1, inplace=True)

    if not sort_time:
        for col in data.columns:
            if 'Date Time' in col:
                data.sort_values(by=col, inplace=True)
                break
    data.reset_index(drop=True, inplace=True)
    return data
