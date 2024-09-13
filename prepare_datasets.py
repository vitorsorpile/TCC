from argparse import ArgumentParser
from pathlib import Path
import re
import pandas


def match_column_header(column):
    return re.match(
        r"^Timestamp|\w+Accelerometer|\w+AngularVelocity|Subject|Activity|Trial|Tag",
        column,
    )


def parse_args():
    arg_parser = ArgumentParser()

    arg_parser.add_argument("--csv_file", type=Path, required=True)

    return arg_parser.parse_args()


args = parse_args()

data = pandas.read_csv(args.csv_file, skiprows=1, usecols=match_column_header)

positions = ["Ankle", "Belt", "Neck", "RightPocket", "Wrist"]

frequency_features = [
    "Mean Frequency",
    "Median Frequency",
    "Entropy",
    "Energy",
    "Principal Frequency",
    "Spectral Centroid",
]

common_columns = ["Timestamp", "Subject", "Activity", "Trial", "Tag"]

for position in positions:
    headers = data.columns
    position_columns = common_columns + [
        column for column in headers if position in column
    ]

    position_df = data[position_columns]
    position_df.to_csv(f"{position}_dataset.csv", index=False)
    print(f"{position} -> {position_df.shape}")

    frequency_domain_columns = common_columns + [
        column
        for column in position_columns
        if any(feature in column for feature in frequency_features)
    ]
    position_frequency_domain_df = position_df[frequency_domain_columns]

    position_frequency_domain_df.to_csv(
        f"{position}_frequency_dataset.csv", index=False
    )
    print(f"{position}_frequency -> {position_frequency_domain_df.shape}")

    time_domain_columns = common_columns + list(
        set(position_columns) - set(frequency_domain_columns)
    )

    position_time_df = position_df[time_domain_columns]

    position_time_df.to_csv(f"{position}_time_dataset.csv", index=False)
    print(f"{position}_time -> {position_time_df.shape}")

data.to_csv("full_dataset.csv", index=False)
