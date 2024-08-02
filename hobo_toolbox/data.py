from pandas import to_datetime, MultiIndex
from logging import getLogger

logger = getLogger(__name__)

def read_timezone(data_df):
    """
    Read timezone from the 'Date Time GMT+HH:MM' column header
    :param data_df: pd.DataFrame(); containing the original header
    :return tz_offset: float; decimal time offset
    """
    for col_name in data_df.columns:
        if 'Date Time' in col_name:
            tz_offset = col_name.split('GMT+')[-1]
            try:
                tz_offset = int(tz_offset.split(':')[0]) + int(tz_offset.split(':')[1]) / 60
            except ValueError:
                tz_offset = None
            else:
                pass
    return tz_offset


def parse_header(data_df):
    """
    Reformat raw header with multiindex containing measurement name and units

    :param data_df: pd.DataFrame(); containing the selected columns of the raw data
    :return data_df: pd.DataFrame(); containing the dataframe with formatted columns (name, unit)
    """
    from pint import UnitRegistry
    ureg = UnitRegistry()

    tuple_cols = []
    for col_name in data_df.columns:
        new_name = col_name.split(', ')[0]
        if new_name == 'Date Time':
            unit = ureg.Unit('')
        else:
            if 'LBL' in col_name:
                sensor_name = col_name.split('LBL: ')[-1].split(')')[0]
                new_name = f"{new_name} ({sensor_name})"
            else:
                new_name = f"{new_name}"
            unit = col_name.split(', ')[1].split(' ')[0]
            unit = ureg.Unit(unit)
        tuple_cols.append((new_name, unit))

    # rename columns with multindex
    data_df.columns = MultiIndex.from_tuples(tuple_cols, names=['name', 'unit'])
    return data_df


def parse_date(data_df, preserve_original=False):
    """
    Format datetime columns to ISO 8601 format (YYYY-MM-DD HH:MM:SS)

    :param data_df: pd.DataFrame(); containing the data with formatted header (name, unit)
    :param preserve_original: boolean; if True, copy original datetimestamp to "Date Time (Original)" columns
    :return data_df: pd.DataFrame(); containing the data with formatted datetime stamp.
    """

    if preserve_original:
        data_df['Date Time (Original)'] = data_df['Date Time']
    data_df['Date Time'] = to_datetime(data_df['Date Time'], format='mixed')
    return data_df
