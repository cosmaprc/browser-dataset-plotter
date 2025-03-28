import os
import pathlib

import pandas


def get_data_dir():
    data_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


def set_session_state(streamlit_session_state):
    for k, v in streamlit_session_state.items():
        streamlit_session_state.session_state[k] = v


def save_file(file):
    data_dir = get_data_dir()

    with open(os.path.join(data_dir, file.name), "wb") as data_file:
        data_file.write(file.getvalue())


def load_data():
    data_dir = get_data_dir()
    for file in os.listdir(data_dir):
        return pandas.read_csv(os.path.join(data_dir, file))


def delete_file():
    data_dir = get_data_dir()
    for file in os.listdir(data_dir):
        os.remove(os.path.join(data_dir, file))
