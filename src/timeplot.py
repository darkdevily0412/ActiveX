import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
def line_plot_insights(df, y_axis):
    """
    Plots a line graph for each day of the week using the specified Y-axis column from the DataFrame.
    Includes all details in the hover information.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing data.
    - y_axis (str): The column name to be used for the Y-axis.

    Returns:
    - fig (go.Figure): The Plotly figure object.
    """
    # Ensure the specified Y-axis column exists in the DataFrame
    if y_axis not in df.columns:
        print(f"Column '{y_axis}' does not exist in the DataFrame.")
        return
    
    # Convert time intervals to just the start time in hours
    df['Time'] = pd.to_datetime(df['hourly_stats_aggregated_by_audience_time_zone'].str.split(' - ').str[0], format='%H:%M:%S').dt.hour
    
    # Sort DataFrame by Time
    df = df.sort_values(by=['Time'])
    
    # Days of the week and corresponding colors for differentiation
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'grey', 'pink']
    
    # Create the figure
    fig = go.Figure()
    
    # Loop through each day and add a line trace
    for day, color in zip(days_of_week, colors):
        # Filter data for the specific day
        day_data = df[df['day_of_week'] == day]
        
        # Add trace if data for the day exists
        if not day_data.empty:
            fig.add_trace(go.Scatter(
                x=day_data['Time'], 
                y=day_data[y_axis], 
                mode='lines+markers', 
                name=day,
                line=dict(color=color),
                hovertemplate=(
                    f"Hour: %{{x}}<br>"
                    f"{y_axis}: %{{y}}<br>"
                    f"Spend: $%{{customdata[0]:.2f}}<br>"
                    f"Impressions: %{{customdata[1]}}<br>"
                    f"Clicks: %{{customdata[2]}}<br>"
                    f"Leads: %{{customdata[3]}}<br>"
                    f"Link Clicks: %{{customdata[4]}}<br>"
                    f"Post Engagement: %{{customdata[5]}}<br>"
                    f"Page Engagement: %{{customdata[6]}}<br>"
                    f"Post Reaction: %{{customdata[7]}}"
                ),
                customdata=day_data[['spend', 'impressions', 'clicks', 'lead', 'link_click', 'post_engagement', 'page_engagement', 'post_reaction']].values
            ))
    
    # Update layout with titles and axis labels
    fig.update_layout(
        title=f'{y_axis} Over Hours for Each Day of the Week',
        xaxis_title='Hour of the Day',
        yaxis_title=y_axis,
         xaxis=dict(
            tickmode='linear',
            tickvals=list(range(24)),  # Assuming hours are from 0 to 23
            ticktext=[str(hour) for hour in range(24)]  # Labels for each hour
        ),
        template='plotly_white'
    )
    
    # Show the plot
    return fig
def bar_plot_insights(df, y_axis):
    """
    Plots a stacked bar chart for each day of the week using the specified Y-axis column from the DataFrame.
    Includes all details in the hover information.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing data.
    - y_axis (str): The column name to be used for the Y-axis.

    Returns:
    - fig (go.Figure): The Plotly figure object.
    """
    # Ensure the specified Y-axis column exists in the DataFrame
    if y_axis not in df.columns:
        print(f"Column '{y_axis}' does not exist in the DataFrame.")
        return
    
    # Convert time intervals to just the start time in hours
    df['Time'] = pd.to_datetime(df['hourly_stats_aggregated_by_audience_time_zone'].str.split(' - ').str[0], format='%H:%M:%S').dt.hour
    
    # Sort DataFrame by Time
    df = df.sort_values(by=['Time'])
    
    # Days of the week and corresponding colors for differentiation
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'grey', 'pink']
    
    # Create the figure
    fig = go.Figure()
    
    # Loop through each day and add a bar trace
    for day, color in zip(days_of_week, colors):
        # Filter data for the specific day
        day_data = df[df['day_of_week'] == day]
        
        # Add trace if data for the day exists
        if not day_data.empty:
            fig.add_trace(go.Bar(
                x=day_data['Time'], 
                y=day_data[y_axis], 
                name=day,
                marker_color=color,
                hovertemplate=(
                    f"Hour: %{{x}}<br>"
                    f"{y_axis}: %{{y}}<br>"
                    f"Spend: $%{{customdata[0]:.2f}}<br>"
                    f"Impressions: %{{customdata[1]}}<br>"
                    f"Clicks: %{{customdata[2]}}<br>"
                    f"Leads: %{{customdata[3]}}<br>"
                    f"Link Clicks: %{{customdata[4]}}<br>"
                    f"Post Engagement: %{{customdata[5]}}<br>"
                    f"Page Engagement: %{{customdata[6]}}<br>"
                    f"Post Reaction: %{{customdata[7]}}"
                ),
                customdata=day_data[['spend', 'impressions', 'clicks', 'lead', 'link_click', 'post_engagement', 'page_engagement', 'post_reaction']].values
            ))
    
    # Update layout with titles and axis labels
    fig.update_layout(
        title=f'{y_axis} Over Hours for Each Day of the Week',
        xaxis_title='',  # Empty x-axis title
        yaxis_title=y_axis,
         xaxis=dict(
            tickmode='linear',
            tickvals=list(range(24)),  # Assuming hours are from 0 to 23
            ticktext=[str(hour) for hour in range(24)]  # Labels for each hour
        ),
        barmode='stack',  # Set the bars to be stacked
        template='plotly_white'
    )
    
    # Show the plot
    return fig
def plot_insights(df, y_axis):
    """
    Plots a heatmap for each day of the week using the specified Y-axis column from the DataFrame.
    Includes all details in the hover information.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing data.
    - y_axis (str): The column name to be used for the heatmap's color intensity.

    Returns:
    - fig (go.Figure): The Plotly figure object.
    """
    # Ensure the specified Y-axis column exists in the DataFrame
    if y_axis not in df.columns:
        print(f"Column '{y_axis}' does not exist in the DataFrame.")
        return
    
    # Convert time intervals to just the start time in hours
    df['Time'] = pd.to_datetime(df['hourly_stats_aggregated_by_audience_time_zone'].str.split(' - ').str[0], format='%H:%M:%S').dt.hour
    
    # Sort DataFrame by Time
    df = df.sort_values(by=['Time'])
    
    # Days of the week in order
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create a pivot table with Time as columns, days of the week as rows, and y_axis values
    heatmap_data = df.pivot_table(index='day_of_week', columns='Time', values=y_axis, aggfunc='sum').reindex(days_of_week)
    
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',  # Choose a colorscale (e.g., Viridis, Plasma, etc.)
        hovertemplate=(
            f"Day: %{{y}}<br>"
            f"Hour: %{{x}}<br>"
            f"{y_axis}: %{{z}}<br>"
        )
    ))
    
    # Update layout with titles and axis labels
    fig.update_layout(
        title=f'{y_axis} Heatmap Over Hours and Days of the Week',
        xaxis_title='Hour of the Day',
        yaxis_title='Day of the Week',
        template='plotly_white'
    )
    
    # Show the plot
    return fig
def create_heatmap(df, metric):

    # Pivot table to aggregate data by day_of_week and hour_of_day
    heatmap_data = df.pivot_table(
        index="hourly_stats_aggregated_by_audience_time_zone",
        columns="day_of_week",
        values=metric,
        aggfunc="sum",
    ).fillna(0)

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    x_labels = []
    for day in days:
        if day in list(heatmap_data.columns):
            x_labels.append(day)
    fig = px.imshow(
        heatmap_data,
        labels={
            "x": "Day of Week",
            "y": "Hour of Day",
            "color": metric,
            "hover_data": ["lead", "impressions", "clicks", "spends"],
        },
        # x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        x=x_labels,
        y=sorted(df["hourly_stats_aggregated_by_audience_time_zone"].unique()),
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        title=f"Heatmap of {metric} by Day of Week and Hour of Day",
        xaxis_nticks=36,
    )
    fig.update_layout(width=600, height=1000)
    return fig

def plot_cumulative_leads(df):
    # Ensure the date columns are in datetime format
    df['date_start'] = pd.to_datetime(df['date_start'])
    df = df.sort_values(by='date_start')
    
    # Calculate the cumulative sum of leads
    df['cumulative_leads'] = df['lead'].cumsum()
    
    # Create the Plotly figure
    fig = go.Figure()
    
    # Add a trace for the cumulative leads
    fig.add_trace(go.Scatter(
        x=df['date_start'],
        y=df['cumulative_leads'],
        mode='lines',  # Changed from 'lines+markers' to 'lines'
        name='Cumulative Leads',
        line=dict(color='red')
    ))
    
    # Update the layout of the figure
    fig.update_layout(
        title='Cumulative Increase of Leads Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative Leads',
        template='plotly_white'
    )
    
    return fig
def plot_cumulative_link_clicks(df):
    # Ensure the date columns are in datetime format
    df['date_start'] = pd.to_datetime(df['date_start'])
    df = df.sort_values(by='date_start')
    
    # Calculate the cumulative sum of link clicks
    df['cumulative_link_clicks'] = df['link_click'].cumsum()
    
    # Create the Plotly figure
    fig = go.Figure()
    
    # Add a trace for the cumulative link clicks
    fig.add_trace(go.Scatter(
        x=df['date_start'],
        y=df['cumulative_link_clicks'],
        mode='lines',
        name='Cumulative Link Clicks',
        line=dict(color='blue'),
        hovertext=df[['lead', 'cpl']].apply(lambda row: f"Leads: {row['lead']}<br>CPL: {row['cpl']}", axis=1),
        hoverinfo='text+x+y'  # Shows the custom hover text and the x and y values
    ))
    
    # Update the layout of the figure
    fig.update_layout(
        title='Cumulative Increase of Link Clicks Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative Link Clicks',
        template='plotly_white'
    )
    
    return fig