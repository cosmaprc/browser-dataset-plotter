# Browser Dataset Plotter

Browser Dataset Plotter is an example of using [Streamlit](https://docs.streamlit.io/), [Pandas](https://pandas.pydata.org/) and [Plotly](https://plotly.com/) libraries to plot and vizualize local dataset files as graphs directly in your web browser.

# Install
```
make install
```

# Run
```
streamlit run home.py
```

Sample test files can be found in `tests/datasets` directory. Or use samples from https://github.com/plotly/datasets .

# Test (uses pytest-selenium)

```
streamlit run home.py
pytest -v
```
