# TGSIM Trajectory Visualization and Traffic Flow Analysis

This project is an interactive Streamlit app for exploring and analyzing the Third-Generation Simulation (TGSIM) I-90/I-94 trajectory dataset, specifically Run 1. It enables visualization of vehicle trajectories and computes key traffic flow metrics such as headways, speeds, flow, and density.

## Features

- Load and preprocess large-scale TGSIM trajectory data efficiently.
- Interactive visualization of vehicle trajectories with lane selection.
- Zoom and filter functionality to select specific time ranges.
- Analytical plots showing distributions of:
  - Headways (time differences between consecutive vehicles)
  - Speeds (individual vehicle speeds)
  - Space-mean speeds (mean speeds aggregated over lanes and time)
  - Flow (vehicles per unit time)
  - Density (vehicles per unit distance)
- Exploration of speed-density-flow fundamental relationships.

## How to Run

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Pandas
- Plotly
- NumPy

## Installation

#### Install required Python packages using pip (Can skip if you have already installed these packages):

```pip install streamlit pandas plotly numpy```

#### In the terminal again, cd into where your files are:

```cd "C:\Users\HaoDC\Documents\6. Fall 2025\CEE 416\MP1\Version 2"```

### Running the App

1. Download the TGSIM I-90/I-94 dataset CSV (Run 1) from the [U.S. Department of Transportation Data Portal](https://data.transportation.gov/Automobiles/Third-Generation-Simulation-Data-TGSIM-I-90-I-94-S/9uas-hf8b/about_data).

2. Save the dataset CSV locally, e.g., as `tgsim_run1.csv`.

3. Run the Streamlit app from the command line:

streamlit run app.py

4. In the app interface, enter the path to your saved dataset file.

5. Use the lane selection menu and time range slider to explore trajectories.

6. View the analytical plots below the trajectories to understand traffic flow metrics.

## Dataset Preprocessing

- The app filters the dataset to include only Run 1 trajectory data.
- Data is sorted by time and vehicle id for consistency.
- Time and space headways are calculated as differences between consecutive vehicles within each lane.
- Space-mean speeds, flow, and density are computed aggregated by lane and time or spatial bins.

## Interpretation of Analysis

- **Trajectory Plot**: Shows individual vehicle positions over time, color-coded by vehicle ID, filtered by lane and time.
- **Headways**: Time gaps between vehicles, important for safety and flow stability.
- **Speeds**: Distribution of vehicle speeds identifies traffic conditions.
- **Space-Mean Speeds**: Average speeds aggregated spatially to smooth and represent flow.
- **Flow**: Number of vehicles passing per unit time, indicative of road usage.
- **Density**: Number of vehicles per spatial unit on the road, indicating congestion.
- **Speed-Density-Flow Relationships**: Fundamental traffic flow diagrams that help relate these metrics to understand overall traffic dynamics.
