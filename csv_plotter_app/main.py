import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sys
import os
import platform
from importlib import resources
from typing import Optional


def get_icon_path() -> Optional[str]:
    try:
        with resources.path("csv_plotter_app", "icon.ico") as p:
            return str(p)
    except Exception:
        return None

def run_streamlit():
    """Entry-point script registered in pyproject."""
    script_path = os.path.abspath(__file__)
    os.system(f"{sys.executable} -m streamlit run {script_path}")


def create_shortcut():
    """Create a desktop shortcut on Windows to launch the app.

    The shortcut launches: python -m streamlit run <this_file>
    Requires pywin32 on Windows.
    """
    if platform.system() != "Windows":
        print("Shortcut creation only supported on Windows.")
        return
    try:
        import win32com.client  # type: ignore
    except ImportError:
        print("pywin32 not installed. Install with: pip install pywin32")
        return

    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    if not os.path.isdir(desktop):
        print("Could not locate Desktop folder.")
        return
    shortcut_path = os.path.join(desktop, "CSV Plotter App.lnk")
    target = sys.executable
    module_path = os.path.abspath(__file__)
    arguments = f"-m streamlit run \"{module_path}\""
    icon_path = get_icon_path()

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = os.path.dirname(module_path)
    if icon_path:
        shortcut.IconLocation = icon_path
    shortcut.Description = "CSV Plotter App"
    shortcut.Save()
    print(f"Desktop shortcut created: {shortcut_path}")

def main():
    if "_page_config_set" not in st.session_state:
        icon_path = get_icon_path()
        st.set_page_config(layout="wide", page_title="CSV Plotter App", page_icon=icon_path)
        st.session_state["_page_config_set"] = True

    st.title("CSV Plotter App")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.header("Data Preview")
        st.dataframe(df)

        st.sidebar.header("Plotting Options")
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        all_cols = df.columns.tolist()
        plot_type = st.sidebar.selectbox(
            "Plot Type", ["Line", "Scatter", "Bar", "Area", "Histogram", "Box"], index=0
        )
        # X-axis only needed for some plot types
        requires_x = plot_type in {"Line", "Scatter", "Bar", "Area"}
        if requires_x:
            x_axis = st.sidebar.selectbox("Select X-axis", all_cols)
        else:
            x_axis = None
        y_axes = st.sidebar.multiselect(
            "Select Y-axis" if requires_x else "Select Columns", numeric_cols if numeric_cols else all_cols
        )

        secondary_y_axis = None
        if requires_x and len(y_axes) > 1 and plot_type in {"Line", "Scatter", "Area"}:
            secondary_y_axis = st.sidebar.multiselect("Secondary Y-axis", y_axes)

        use_subplots = False
        if len(y_axes) > 1 and plot_type not in {"Histogram", "Box"}:
            use_subplots = st.sidebar.checkbox("Create subplots (rows)")

        if st.sidebar.button("Generate Plot"):
            if not y_axes:
                st.warning("Please select at least one column to plot.")
            else:
                st.header("Generated Plot")
                # Distribution plots (Histogram / Box)
                if plot_type in {"Histogram", "Box"}:
                    fig = go.Figure()
                    for col in y_axes:
                        if plot_type == "Histogram":
                            fig.add_trace(go.Histogram(x=df[col], name=col, opacity=0.75))
                        else:
                            fig.add_trace(go.Box(y=df[col], name=col))
                    if plot_type == "Histogram":
                        fig.update_layout(barmode="overlay")
                    fig.update_layout(title=f"{plot_type} Plot", legend_title="Columns")
                    st.plotly_chart(fig, use_container_width=True)
                elif use_subplots:
                    fig = make_subplots(rows=len(y_axes), cols=1, shared_xaxes=True, vertical_spacing=0.05)
                    for i, y_axis in enumerate(y_axes):
                        trace_args = dict(x=df[x_axis], y=df[y_axis], name=y_axis)
                        if plot_type == "Line":
                            trace = go.Scatter(**trace_args, mode="lines")
                        elif plot_type == "Scatter":
                            trace = go.Scatter(**trace_args, mode="markers")
                        elif plot_type == "Area":
                            trace = go.Scatter(**trace_args, mode="lines", fill="tozeroy")
                        elif plot_type == "Bar":
                            trace = go.Bar(x=df[x_axis], y=df[y_axis], name=y_axis)
                        else:
                            trace = go.Scatter(**trace_args)
                        fig.add_trace(trace, row=i + 1, col=1)
                    fig.update_layout(height=300 * len(y_axes), title_text="Subplots")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = go.Figure()
                    for y_axis in y_axes:
                        if plot_type == "Line":
                            base = dict(x=df[x_axis], y=df[y_axis], name=y_axis, mode="lines")
                            trace = go.Scatter(**base, yaxis="y2" if secondary_y_axis and y_axis in secondary_y_axis else "y")
                        elif plot_type == "Scatter":
                            base = dict(x=df[x_axis], y=df[y_axis], name=y_axis, mode="markers")
                            trace = go.Scatter(**base, yaxis="y2" if secondary_y_axis and y_axis in secondary_y_axis else "y")
                        elif plot_type == "Area":
                            base = dict(x=df[x_axis], y=df[y_axis], name=y_axis, mode="lines", fill="tozeroy")
                            trace = go.Scatter(**base, yaxis="y2" if secondary_y_axis and y_axis in secondary_y_axis else "y")
                        elif plot_type == "Bar":
                            trace = go.Bar(x=df[x_axis], y=df[y_axis], name=y_axis)
                        else:
                            trace = go.Scatter(x=df[x_axis], y=df[y_axis], name=y_axis)
                        fig.add_trace(trace)

                    layout_kwargs = dict(
                        title=f"{plot_type} Plot",
                        xaxis_title=x_axis,
                    )
                    if secondary_y_axis:
                        layout_kwargs.update(
                            yaxis=dict(title="Primary"),
                            yaxis2=dict(title="Secondary", overlaying="y", side="right"),
                        )
                    fig.update_layout(**layout_kwargs)
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()