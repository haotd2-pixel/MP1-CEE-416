import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Dataset loading and preprocessing
@st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath)
    # Filter for Run 1 only
    df = df[df['run_index'] == 1]
    # Sort by time and vehicle id for analysis
    df = df.sort_values(['time', 'id']).reset_index(drop=True)
    return df

# 2. Compute key traffic flow metrics
def compute_metrics(df):
    # Headways: time difference between consecutive vehicles at the same lane
    df['time_diff'] = df.groupby('lane_kf')['time'].diff()
    df['space_diff'] = df.groupby('lane_kf')['xloc_kf'].diff()
    
    # Speeds are already in speed_kf (in some units)
    
    # Space-mean speed per lane per time window (aggregated mean)
    space_mean_speed = df.groupby(['lane_kf', 'time'])['speed_kf'].mean().reset_index(name='space_mean_speed')
    
    # Flow: count vehicles per lane per time unit
    flow = df.groupby(['lane_kf', 'time']).size().reset_index(name='flow')
    
    # Density: number of vehicles per spatial distance unit (approximate)
    density = df.groupby(['lane_kf', 'xloc_kf']).size().reset_index(name='density')
    
    return df, space_mean_speed, flow, density

# 3. Streamlit app UI and plotting
def main():
    st.title("TGSIM Trajectory Visualization and Traffic Flow Analysis")

    # File uploader or path input
    filepath = st.text_input("Enter path to TGSIM dataset CSV file:", "tgsim_run1.csv")
    
    if filepath:
        with st.spinner("Loading data..."):
            df = load_data(filepath)

        # Lane selection dropdown
        lanes = sorted(df['lane_kf'].unique())
        selected_lane = st.selectbox("Select lane:", lanes)
        
        # Filter data by selected lane for visualization
        lane_df = df[df['lane_kf'] == selected_lane]
        
        # Time range slider for zooming in time dimension
        time_min, time_max = int(lane_df['time'].min()), int(lane_df['time'].max())
        time_range = st.slider("Select time range to zoom:", time_min, time_max, (time_min, time_max))
        lane_df = lane_df[(lane_df['time'] >= time_range[0]) & (lane_df['time'] <= time_range[1])]
        
        # Plot trajectories: xloc (space) vs time, color by vehicle id
        fig_traj = px.scatter(lane_df, x='xloc_kf', y='time', color='id',
                              labels={'xloc_kf': 'Position on Road (xloc_kf)', 'time': 'Time'},
                              title=f"Trajectories of Vehicles in Lane {selected_lane}")
        fig_traj.update_yaxes(autorange='reversed')  # Show early time at top
        
        st.plotly_chart(fig_traj, use_container_width=True)
        
        # Compute metrics
        df_metrics, space_mean_speed, flow, density = compute_metrics(df)

        st.subheader("Traffic Flow Analysis")

        # Plot Headways distribution (time headways)
        headways = df_metrics['time_diff'].dropna()
        fig_headways = px.histogram(headways, nbins=50, labels={'value': 'Time Headway (s)'},
                                   title="Distribution of Time Headways")
        st.plotly_chart(fig_headways, use_container_width=True)

        # Plot Speeds distribution
        fig_speeds = px.histogram(df['speed_kf'], nbins=50, labels={'value': 'Speed (units)'},
                                  title="Distribution of Speeds")
        st.plotly_chart(fig_speeds, use_container_width=True)

        # Plot Space-mean Speeds over time for selected lane
        sm_speed_lane = space_mean_speed[space_mean_speed['lane_kf'] == selected_lane]
        fig_sms = px.line(sm_speed_lane, x='time', y='space_mean_speed',
                          title="Space-Mean Speed Over Time")
        st.plotly_chart(fig_sms, use_container_width=True)

        # Plot Flow over time for selected lane
        flow_lane = flow[flow['lane_kf'] == selected_lane]
        fig_flow = px.line(flow_lane, x='time', y='flow', title="Flow Over Time (vehicles/time)")
        st.plotly_chart(fig_flow, use_container_width=True)

        # Plot Density along the road for selected lane (spatial density)
        density_lane = density[density['lane_kf'] == selected_lane]
        fig_density = px.scatter(density_lane, x='xloc_kf', y='density',
                                 title="Density Along Road (vehicles per position)",
                                 labels={'xloc_kf': 'Position on Road', 'density': 'Density'})
        st.plotly_chart(fig_density, use_container_width=True)

        st.subheader("Speed-Density-Flow Relationships")

        # Merge mean speed, density and flow approximations by lane and spatial/time bins if needed (simplified)
        # This is a complex analysis; here, display illustrative scatter plots:
        fig_sd = px.scatter(density_lane, x='xloc_kf', y='density', title='Density along road')
        st.plotly_chart(fig_sd, use_container_width=True)

        # Future extensions: compute and plot fundamental diagrams (flow vs density, speed vs density)

if __name__ == "__main__":
    main()
