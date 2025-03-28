import datetime
import os

import pandas as pd
import plotly.express as px
import streamlit as st

import utils


def main() -> None:
    st.set_page_config(
        page_title="Pandas Viewer", layout="wide", page_icon="🐼"
    )
    st.subheader("Pandas Plot Viewer", divider=True)
    st.success(
        "Welcome to the Pandas Viewer! Upload a CSV file to get started."
    )
    st.caption(
        "This is a simple Streamlit app that allows you to upload a \
            CSV file and view the data in a Pandas DataFrame."
    )
    st.subheader("File Upload", divider=True)
    with st.form("Upload a CSV data file", clear_on_submit=True):
        file = st.file_uploader(
            "Upload a CSV data file", type=["csv"], accept_multiple_files=False
        )
        if st.form_submit_button("Upload File"):
            if not file:
                st.warning("Please select a file to upload.")
            else:
                utils.save_file(file)

    st.subheader("File Information", divider=True)
    file_info_df = pd.DataFrame({"File": os.listdir(utils.get_data_dir())})
    file_info_df["Creation Time"] = file_info_df["File"].apply(
        lambda x: datetime.datetime.fromtimestamp(
            os.path.getctime(os.path.join(utils.get_data_dir(), x))
        )
    )
    file_info_df["Last Modified Time"] = file_info_df["File"].apply(
        lambda x: datetime.datetime.fromtimestamp(
            os.path.getmtime(os.path.join(utils.get_data_dir(), x))
        )
    )
    file_info_df["Size (bytes)"] = file_info_df["File"].apply(
        lambda x: os.path.getsize(os.path.join(utils.get_data_dir(), x))
    )

    file_info_df.sort_values("Creation Time", ascending=False, inplace=True)
    st.dataframe(file_info_df, use_container_width=True)

    if st.button("Delete File"):
        utils.delete_file()
        st.success("File deleted successfully")
        st.dataframe(file_info_df, use_container_width=True)

    st.subheader("Data Preview", divider=True)
    df = None
    with st.expander("Raw Data", expanded=True):
        try:
            df = utils.load_data()
            df.head()
            st.dataframe(df, use_container_width=True)
        except Exception:
            st.warning("No data available. Please upload a CSV file.")

    with st.expander("Plot Data", expanded=True):
        if df is None or df.empty:
            st.warning("No data available. Please upload a CSV file.")
        else:
            columns = list(df.columns)[0:]
            x_choice = st.sidebar.selectbox("X-Axis:", columns, index=0)
            y_choice = st.sidebar.selectbox(
                "Y-Axis:", columns, index=len(columns) - 1
            )
            color = st.sidebar.selectbox(
                "Color:", columns, index=len(columns) - 1
            )
            fig = px.line(
                df,
                x=x_choice,
                y=y_choice,
                color=color,
                markers=True,
            )
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
