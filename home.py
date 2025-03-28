import datetime
import os

import pandas
import plotly
import streamlit

import utils


def main() -> None:
    streamlit.set_page_config(
        page_title="Pandas Viewer", layout="wide", page_icon="🐼"
    )
    streamlit.subheader("Pandas Plot Viewer", divider=True)
    streamlit.success(
        "Welcome to the Pandas Viewer! Upload a CSV file to get started."
    )
    streamlit.caption(
        "This is a simple Streamlit app that allows you to upload a \
            CSV file and view the data in a Pandas DataFrame."
    )
    streamlit.subheader("File Upload", divider=True)
    with streamlit.form("Upload a CSV data file", clear_on_submit=True):
        file = streamlit.file_uploader(
            "Upload a CSV data file", type=["csv"], accept_multiple_files=False
        )
        if streamlit.form_submit_button("Upload File"):
            if not file:
                streamlit.warning("Please select a file to upload.")
            else:
                utils.save_file(file)

    streamlit.subheader("File Information", divider=True)
    file_info_df = pandas.DataFrame({"File": os.listdir(utils.get_data_dir())})
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
    streamlit.dataframe(file_info_df, use_container_width=True)

    if streamlit.button("Delete File"):
        utils.delete_file()
        streamlit.success("File deleted successfully")
        streamlit.dataframe(file_info_df, use_container_width=True)

    streamlit.subheader("Data Preview", divider=True)
    df = None
    with streamlit.expander("Raw Data", expanded=True):
        try:
            df = utils.load_data()
            df.head()
            streamlit.dataframe(df, use_container_width=True)
        except Exception:
            streamlit.warning("No data available. Please upload a CSV file.")

    with streamlit.expander("Plot Data", expanded=True):
        if df is None or df.empty:
            streamlit.warning("No data available. Please upload a CSV file.")
        else:
            x = list(df.columns)[0:]
            y = list(df.columns)[0:]
            graph_type = streamlit.sidebar.selectbox(
                "Select your Graph Type:", ("Scatter", "Bar"), index=0
            )
            x_choice = streamlit.sidebar.selectbox(
                "Select your X-Axis:", x, index=0
            )
            y_choice = streamlit.sidebar.selectbox(
                "Select your Y-Axis:", y, index=len(y) - 1
            )
            category = streamlit.sidebar.text_input(
                "Enter Category", value=f"{y_choice} over {x_choice}"
            )
            graph_type_selected = None
            if graph_type == "Scatter":
                graph_type_selected = plotly.graph_objects.Scatter(
                    x=df[x_choice],
                    y=df[y_choice],
                    name=category or "Share Prices (in USD)",
                )
            elif graph_type == "Bar":
                graph_type_selected = plotly.graph_objects.Bar(
                    x=df[x_choice],
                    y=df[y_choice],
                    name=category or "Share Prices (in USD)",
                )
            fig = plotly.graph_objects.Figure(graph_type_selected)
            fig.update_layout(
                title=dict(text="Apple Share Prices over time (2014)"),
                plot_bgcolor="rgb(230, 230,230)",
                showlegend=True,
            )
            streamlit.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
