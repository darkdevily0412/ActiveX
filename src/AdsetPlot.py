
import plotly.graph_objects as go

import pandas as pd
def seg1df1(df1):
    grouped_df = df1.groupby('publisher_platform').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean')
    ).reset_index()
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']

    hover_text = grouped_df.apply(
        lambda row: f"Platform: {row['publisher_platform']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}",
        axis=1
    )
    bar_chart = go.Bar(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_leads'],
        name='Sum of Leads',
        hoverinfo='text',
        
        
        )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create the layout with dual y-axes
    layout = go.Layout(
        title='Leads and Spends by Publisher Platform',
        xaxis=dict(title='Publisher Platform'),
        yaxis=dict(title='Sum of Leads'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
def seg1df2(df1):
    df1['publisher_platform_position'] = df1['publisher_platform'] + '_' + df1['platform_position']

    # Group by the new concatenated column and calculate metrics
    grouped_df = df1.groupby('publisher_platform_position').agg(
        leads=('lead', 'sum'),
        spends=('spend', 'sum')
    ).reset_index()
    # Calculate CPL (Cost Per Lead)
    grouped_df['cpl'] = grouped_df['spends'] / grouped_df['leads']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['cpl'],
        mode='markers+text',
        text=grouped_df['publisher_platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles,
            color=grouped_df['leads'], 
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Leads: %{x}<br>' +
            'CPL: %{y:.2f}<br>' +
            'Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads with Labels',
        xaxis_title='Leads',
        yaxis_title='CPL (Cost Per Lead)',
        # showlegend=False,
    )

# Show the plot
    # fig.show()
    return fig
def seg1df3(df1):
    df_filtered = df1[df1['publisher_platform'] == 'facebook']
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    # Calculate CPL (Cost Per Lead)
    grouped_df['avg_cpls'] = grouped_df['sum_spends'] / grouped_df['sum_leads']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['avg_cpls'],
        
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads for Facebook',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()

    return fig
def seg1df4(df1):
    df_filtered = df1[df1['publisher_platform'] == 'instagram']
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    # Calculate CPL (Cost Per Lead)
    grouped_df['avg_cpls'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['avg_cpls'],
        
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads for Instagram',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg2df1(df1):
    df1['cpc']=df1['cpc'].astype(float)
    df1['clicks']=df1['clicks'].astype(float)
    grouped_df = df1.groupby('publisher_platform').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpc=('cpc', 'mean')
    ).reset_index()
    grouped_df['act_cpc'] = grouped_df['sum_spends'].astype('float') / grouped_df['sum_clicks'].astype('float')
    hover_text = grouped_df.apply(
        lambda row: f"Platform: {row['publisher_platform']}<br>"
                    f"Sum of Clicks: {row['sum_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPC: {row['avg_cpc']:.2f}<br>"
                    f"Actual CPC: {row['act_cpc']:.2f}",
        axis=1
    )
    bar_chart = go.Bar(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_clicks'],
        name='Sum of Clicks',
        hoverinfo='text',
        hovertext=hover_text,
    )
    line_chart = go.Scatter(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
        
    )
    layout = go.Layout(
        title='Clicks and Spends by Publisher Platform',
        xaxis=dict(title='Publisher Platform'),
        yaxis=dict(title='Sum of Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)
    # fig.show()
    return fig
def seg2df2(df1):
    df1['cpc']=df1['cpc'].astype(float)
    df1['clicks']=df1['clicks'].astype(float)
    df1['publisher_platform_position'] = df1['publisher_platform'] + '_' + df1['platform_position']

    # Group by the new concatenated column and calculate metrics
    grouped_df = df1.groupby('publisher_platform_position').agg(
        clicks=('clicks', 'sum'),
        spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPC (Cost Per Click)
    grouped_df['cpc'] = grouped_df['spends'] / grouped_df['clicks']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['publisher_platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles,
            color=grouped_df['clicks'],  # Color based on clicks
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks with Labels',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
    )

    # Show the plot
    # fig.show()
    return fig
def seg2df3(df1):
    df1['cpc']=df1['cpc'].astype(float)
    df1['clicks']=df1['clicks'].astype(float)
    df_filtered = df1[df1['publisher_platform'] == 'facebook']
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    grouped_df['avg_cpc'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_clicks'],
        y=grouped_df['avg_cpc'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks for Facebook',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )
    # fig.show()
    return fig
def seg2df4(df1):
    df1['cpc']=df1['cpc'].astype(float)
    df1['clicks']=df1['clicks'].astype(float)
    df1['publisher_platform_position'] = df1['publisher_platform'] + '_' + df1['platform_position']
    df_filtered = df1[df1['publisher_platform'] == 'instagram']
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPC (Cost Per Click)
    grouped_df['avg_cpc'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()
    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_clicks'],
        y=grouped_df['avg_cpc'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks for Instagram',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg3df1(df3):
    df3['cpl']=df3['spend']/df3['lead']
    grouped_df = df3.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean')
    ).reset_index()

    # Calculate the actual CPL
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']

    # Create a bar chart for sum_leads
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}",
        axis=1
    )

    bar_chart = go.Bar(
        x=grouped_df['age'],
        y=grouped_df['sum_leads'],
        name='Sum of Leads',
        hoverinfo='text',
    )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['age'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create the layout with dual y-axes
    layout = go.Layout(
        title='Leads and Spends by Age Group',
        xaxis=dict(title='Age'),
        yaxis=dict(title='Sum of Leads'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    # Show the plot
    # fig.show()
    return fig
def seg3df2(df3):
    # Group by gender and calculate metrics
    grouped_df2 = df3.groupby('gender').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate the average CPL and the actual CPL
    grouped_df2['avg_cpls'] = grouped_df2['sum_spends'] / grouped_df2['sum_leads']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df2['sum_leads'],
        y=grouped_df2['avg_cpls'],
        mode='markers+text',
        text=grouped_df2['gender'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df2['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df2['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df2['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Gender: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads by Gender',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg3df3(df3):
    # Group by age and calculate metrics
    grouped_df3 = df3.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate average CPL (Cost Per Lead)
    grouped_df3['avg_cpls'] = grouped_df3['sum_spends'] / grouped_df3['sum_leads']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df3['sum_leads'],
        y=grouped_df3['avg_cpls'],
        mode='markers+text',
        text=grouped_df3['age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df3['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df3['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df3['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads by Age',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()    
    return fig
def seg3df4(df3):
    df3['gender_age'] = df3['gender'] + '_' + df3['age']

    # Group by the new concatenated column and calculate metrics
    grouped_df4 = df3.groupby('gender_age').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate average CPL (Cost Per Lead)
    grouped_df4['avg_cpls'] = grouped_df4['sum_spends'] / grouped_df4['sum_leads']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df4['sum_leads'],
        y=grouped_df4['avg_cpls'],
        mode='markers+text',
        text=grouped_df4['gender_age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df4['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df4['sum_spends'] / 100) if not grouped_df4['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df4['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Gender_Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads by Gender and Age',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg3df5(df3):
    df_filtered = df3[df3['gender'] == 'male']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPL (Cost Per Lead)
    grouped_df['avg_cpls'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    # Create the bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['avg_cpls'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads for Males by Age',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg3df6(df3):
    df_filtered = df3[df3['gender'] == 'female']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPL (Cost Per Lead)
    grouped_df['avg_cpls'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    # Create the bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['avg_cpls'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Average CPL: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Leads for Females by Age',
        xaxis_title='Sum of Leads',
        yaxis_title='Average CPL (Cost Per Lead)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg4df1(df3):
    df3['cpc'] = df3['spend'] / df3['clicks']
    grouped_df = df3.groupby('age').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpcs=('cpc', 'mean')
    ).reset_index()
    grouped_df['act_cpc'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Clicks: {row['sum_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPC: {row['avg_cpcs']:.2f}<br>"
                    f"Actual CPC: {row['act_cpc']:.2f}",
        axis=1
    )
    bar_chart = go.Bar(
        x=grouped_df['age'],
        y=grouped_df['sum_clicks'],
        name='Sum of Clicks',
        hoverinfo='text',
    )
    line_chart = go.Scatter(
        x=grouped_df['age'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
        hovertext=hover_text,
    )
    layout = go.Layout(
        title='Clicks and Spends by Age Group',
        xaxis=dict(title='Age'),
        yaxis=dict(title='Sum of Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)
    # fig.show()
    return fig
def seg4df2(df3):
    # Group by gender and calculate metrics
    grouped_df2 = df3.groupby('gender').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate the average CPC and the actual CPC
    grouped_df2['avg_cpcs'] = grouped_df2['sum_spends'] / grouped_df2['sum_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df2['sum_clicks'],
        y=grouped_df2['avg_cpcs'],
        mode='markers+text',
        text=grouped_df2['gender'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df2['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df2['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df2['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks'),
        ),
        hovertemplate=(
            'Gender: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Gender',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg4df3(df3):
    grouped_df3 = df3.groupby('age').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate average CPC (Cost Per Click)
    grouped_df3['avg_cpcs'] = grouped_df3['sum_spends'] / grouped_df3['sum_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df3['sum_clicks'],
        y=grouped_df3['avg_cpcs'],
        mode='markers+text',
        text=grouped_df3['age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df3['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df3['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df3['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks'),
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Age',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg4df4(df3):
    # Concatenate gender and age to create a new column
    df3['gender_age'] = df3['gender'] + '_' + df3['age']

    # Group by the new concatenated column and calculate metrics
    grouped_df4 = df3.groupby('gender_age').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate average CPC (Cost Per Click)
    grouped_df4['avg_cpcs'] = grouped_df4['sum_spends'] / grouped_df4['sum_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df4['sum_clicks'],
        y=grouped_df4['avg_cpcs'],
        mode='markers+text',
        text=grouped_df4['gender_age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df4['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df4['sum_spends'] / 100) if not grouped_df4['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df4['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks'),
        ),
        hovertemplate=(
            'Gender_Age: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Gender and Age',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg4df5(df3):
    # Filter the dataset for males
    df_filtered = df3[df3['gender'] == 'male']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPC (Cost Per Click)
    grouped_df['avg_cpcs'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']

    # Create the bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_clicks'],
        y=grouped_df['avg_cpcs'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks for Males by Age',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg4df6(df3):
    # Filter the dataset for females
    df_filtered = df3[df3['gender'] == 'female']


    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPC (Cost Per Click)
    grouped_df['avg_cpcs'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']

    # Create the bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_clicks'],
        y=grouped_df['avg_cpcs'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_clicks'],  # Color based on clicks
            colorbar=dict(title='Sum of Clicks')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Clicks: %{x}<br>' +
            'Average CPC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks for Females by Age',
        xaxis_title='Sum of Clicks',
        yaxis_title='Average CPC (Cost Per Click)',
        showlegend=False,
    )
    return fig
def seg5df1(df1):
    # Group by publisher_platform and calculate the required metrics

    grouped_df = df1.groupby('publisher_platform').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cplc=('cplc', 'mean')
    ).reset_index()

    # Calculate the actual CPLC
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Generate hover text for each bar and line
    hover_text = grouped_df.apply(
        lambda row: f"Platform: {row['publisher_platform']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPLC: {row['avg_cplc']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create the bar chart for sum_link_clicks with a custom color
    bar_chart = go.Bar(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_link_clicks'],
        name='Sum of Link Clicks',
        hoverinfo='text',
        hovertext=hover_text,
        marker=dict(color='rgb(34, 163, 192)')  # Custom color for the bar chart
    )

    # Create the line chart for sum_spends on a secondary y-axis with a custom color
    line_chart = go.Scatter(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
        hovertext=hover_text,
        line=dict(color='rgb(255, 127, 14)'),  # Custom color for the line chart
        marker=dict(color='rgb(255, 127, 14)')  # Same color for markers
    )

    # Create the layout with dual y-axes
    layout = go.Layout(
        title='Link Clicks and Spends by Publisher Platform',
        xaxis=dict(title='Publisher Platform'),
        yaxis=dict(title='Sum of Link Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
def seg5df2(df1):
    # Create a new column by concatenating 'publisher_platform' and 'platform_position'
    df1['publisher_platform_position'] = df1['publisher_platform'] + '_' + df1['platform_position']

    # Group by the new concatenated column and calculate metrics
    grouped_df = df1.groupby('publisher_platform_position').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPLC (Cost Per Link Click)
    grouped_df['cplc'] = grouped_df['spends'] / grouped_df['link_clicks']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['publisher_platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles,
            color=grouped_df['link_clicks'],  # Color based on the number of link clicks
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks with Labels',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        # showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg5df3(df1):
    df_filtered = df1[df1['publisher_platform'] == 'facebook']
    
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    
    # Calculate CPLC (Cost Per Link Click)
    grouped_df['avg_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['avg_cplc'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks for Facebook',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()

    return fig
def seg5df4(df1):
    df_filtered = df1[df1['publisher_platform'] == 'instagram']
    
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    
    # Calculate CPLC (Cost Per Link Click)
    grouped_df['avg_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['avg_cplc'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks for Instagram',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg6df1(df3):
    df3['cplc'] = df3['spend'] / df3['link_click']
    grouped_df = df3.groupby('age').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate the actual CPLC
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Create hover text for the chart
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bar chart for sum_link_clicks
    bar_chart = go.Bar(
        x=grouped_df['age'],
        y=grouped_df['sum_link_clicks'],
        name='Sum of Link Clicks',
        hoverinfo='text',
    )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['age'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create the layout with dual y-axes
    layout = go.Layout(
        title='Link Clicks and Spends by Age Group',
        xaxis=dict(title='Age'),
        yaxis=dict(title='Sum of Link Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    # Show the plot
    # fig.show()
    return fig
def seg6df2(df3):
    # Group by gender and calculate metrics
    grouped_df2 = df3.groupby('gender').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate the average CPLC and the actual CPLC
    grouped_df2['avg_cplcs'] = grouped_df2['sum_spends'] / grouped_df2['sum_link_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df2['sum_link_clicks'],
        y=grouped_df2['avg_cplcs'],
        mode='markers+text',
        text=grouped_df2['gender'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df2['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df2['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df2['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Gender: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Gender',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg6df3(df3):
    # Group by age and calculate metrics
    grouped_df3 = df3.groupby('age').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate average CPLC (Cost Per Link Click)
    grouped_df3['avg_cplcs'] = grouped_df3['sum_spends'] / grouped_df3['sum_link_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df3['sum_link_clicks'],
        y=grouped_df3['avg_cplcs'],
        mode='markers+text',
        text=grouped_df3['age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df3['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df3['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df3['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()    
    return fig
def seg6df4(df3):
    df3['gender_age'] = df3['gender'] + '_' + df3['age']

    # Group by the new concatenated column and calculate metrics
    grouped_df4 = df3.groupby('gender_age').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate average CPLC (Cost Per Link Click)
    grouped_df4['avg_cplcs'] = grouped_df4['sum_spends'] / grouped_df4['sum_link_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df4['sum_link_clicks'],
        y=grouped_df4['avg_cplcs'],
        mode='markers+text',
        text=grouped_df4['gender_age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df4['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref = 2. * (max(grouped_df4['sum_spends'] / 100) if not grouped_df4['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df4['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Gender_Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Gender and Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg6df5(df3):
    df_filtered = df3[df3['gender'] == 'male']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPLC (Cost Per Link Click)
    grouped_df['avg_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    
    # Create the bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['avg_cplc'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks for Males by Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg6df6(df3):
    df_filtered = df3[df3['gender'] == 'female']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPLC (Cost Per Link Click)
    grouped_df['avg_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    
    # Create the bubble chart
    fig = go.Figure()
    if grouped_df.empty:
        return fig
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['avg_cplc'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Average CPLC: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks for Females by Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Average CPLC (Cost Per Link Click)',
        showlegend=False,
    )

    # Show the plot
    # fig.show()
    return fig
def seg7df1(df1):
    grouped_df = df1.groupby('publisher_platform').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    
    # Calculate average CPL and CPL (Cost Per Link Click)
    grouped_df['avg_cpls'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks'].replace(0, 1)  # Avoid division by zero

    hover_text = grouped_df.apply(
        lambda row: f"Platform: {row['publisher_platform']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"CPLC: {row['cplc']:.2f}",
        axis=1
    )
    
    # Create a bar chart for sum_leads
    bar_chart = go.Bar(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_leads'],
        name='Sum of Leads',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for sum_link_clicks on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['publisher_platform'],
        y=grouped_df['sum_link_clicks'],
        mode='lines+markers',
        name='Sum of Link Clicks',
        yaxis='y2',
        hoverinfo='text',
    )
    
    # Create another line chart for CPL (Cost Per Link Click) on a third y-axis
    cplc_chart = go.Scatter(
        x=grouped_df['publisher_platform'],
        y=grouped_df['cplc'],
        mode='lines+markers',
        name='CPLC',
        yaxis='y3',
        hoverinfo='text',
    )

    # Create the layout with dual y-axes and an additional y-axis for CPLC
    layout = go.Layout(
        title='Leads, Link Clicks, and CPLC by Publisher Platform',
        xaxis=dict(title='Publisher Platform'),
        yaxis=dict(title='Sum of Leads'),
        yaxis2=dict(title='Sum of Link Clicks', overlaying='y', side='right'),
        yaxis3=dict(title='CPLC', overlaying='y', side='right', anchor='x'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart, cplc_chart], layout=layout)

    return fig

    
    fig = go.Figure()
    platforms = df1['publisher_platform'].unique()
    for platform in platforms:
        df_platform = df1[df1['publisher_platform'] == platform]
        fig.add_trace(go.Scatter(
            x=df_platform['sum_leads'],
            y=df_platform['sum_link_clicks'],
            mode='markers',
            marker=dict(
                size=df_platform['sum_spends'] / 100,
                sizemode='area',
                sizeref=2. * max(df_platform['sum_spends'] / 100) / (100**2),
                color=df_platform['publisher_platform'],  # Color by platform
                colorbar=dict(title='Publisher Platform')
            ),
            text=df_platform['publisher_platform'],
            textposition='middle center',
            name=platform,
            hovertemplate=(
                'Publisher Platform: %{text}<br>' +
                'Sum of Leads: %{x}<br>' +
                'Sum of Link Clicks: %{y}<br>' +
                'Sum of Spends: %{marker.size}<br>'
            ),
        ))
    fig.update_layout(
        title='Leads vs. Link Clicks by Publisher Platform',
        xaxis_title='Sum of Leads',
        yaxis_title='Sum of Link Clicks',
        showlegend=True,
    )
    return fig
def seg7df2(df1):
    df1['publisher_platform_position'] = df1['publisher_platform'] + '_' + df1['platform_position']

    # Group by the new concatenated column and calculate metrics
    grouped_df = df1.groupby('publisher_platform_position').agg(
        leads=('lead', 'sum'),
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPL (Cost Per Lead) - although not used in this chart
    grouped_df['cpl'] = grouped_df['spends'] / grouped_df['leads']

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['link_clicks'],
        mode='markers+text',
        text=grouped_df['publisher_platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color based on leads
            colorbar=dict(title='Leads')
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Leads: %{x}<br>' +
            'Link Clicks: %{y}<br>' +
            'Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Link Clicks',
        xaxis_title='Leads',
        yaxis_title='Link Clicks',
        showlegend=False
    )

    # Show the plot
    # fig.show()
    return fig
def seg7df3(df1):
    # Filter for Facebook platform
    df_filtered = df1[df1['publisher_platform'] == 'facebook']
    
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['sum_link_clicks'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Sum of Link Clicks: %{y}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Link Clicks for Facebook',
        xaxis_title='Sum of Leads',
        yaxis_title='Sum of Link Clicks',
        showlegend=False,
    )

    return fig
def seg7df4(df1):
    # Filter for Instagram platform
    df_filtered = df1[df1['publisher_platform'] == 'instagram']
    
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['sum_link_clicks'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Sum of Link Clicks: %{y}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Link Clicks for Instagram',
        xaxis_title='Sum of Leads',
        yaxis_title='Sum of Link Clicks',
        showlegend=False,
    )

    return fig
def seg8df1(df3):
    # Calculate CPL and CPLC
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']
    
    # Group by age and calculate metrics
    grouped_df = df3.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()
    
    # Calculate the actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bar chart for sum_leads
    bar_chart = go.Bar(
        x=grouped_df['age'],
        y=grouped_df['sum_leads'],
        name='Sum of Leads',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for sum_link_clicks on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['age'],
        y=grouped_df['sum_link_clicks'],
        mode='lines+markers',
        name='Sum of Link Clicks',
        yaxis='y2',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create the layout with dual y-axes
    layout = go.Layout(
        title='Leads and Link Clicks by Age Group',
        xaxis=dict(title='Age'),
        yaxis=dict(title='Sum of Leads'),
        yaxis2=dict(title='Sum of Link Clicks', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
def seg8df2(df3):
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Group by age and calculate metrics
    grouped_df = df3.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Create a bubble chart with annotations
    fig = go.Figure()

    # Add scatter trace for leads vs. link clicks
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['sum_leads'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{y}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Link Clicks by Age Group',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Sum of Leads',
        showlegend=False,
    )

    return fig
def seg8df3(df3):
    # Calculate CPL and CPLC
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Group by gender and calculate metrics
    grouped_df2 = df3.groupby('gender').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate the actual CPL and CPLC
    grouped_df2['act_cpl'] = grouped_df2['sum_spends'] / grouped_df2['sum_leads']
    grouped_df2['act_cplc'] = grouped_df2['sum_spends'] / grouped_df2['sum_link_clicks']

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df2['sum_link_clicks'],
        y=grouped_df2['sum_leads'],
        mode='markers+text',
        text=grouped_df2['gender'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df2['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df2['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df2['sum_link_clicks'],  # Color based on link clicks
            colorbar=dict(title='Sum of Link Clicks'),
        ),
        hovertemplate=(
            'Gender: %{text}<br>' +
            'Sum of Leads: %{y}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df2[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Link Clicks by Gender',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Sum of Leads',
        showlegend=False,
    )

    return fig
def seg8df4(df3):
    # Create concatenated column for gender and age
    df3['gender_age'] = df3['gender'] + '_' + df3['age']
    
    # Calculate CPL and CPLC
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']
    
    # Group by the new concatenated column and calculate metrics
    grouped_df4 = df3.groupby('gender_age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()
    
    # Calculate actual CPL and CPLC
    grouped_df4['act_cpl'] = grouped_df4['sum_spends'] / grouped_df4['sum_leads']
    grouped_df4['act_cplc'] = grouped_df4['sum_spends'] / grouped_df4['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df4.apply(
        lambda row: f"Gender_Age: {row['gender_age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df4['sum_link_clicks'],
        y=grouped_df4['sum_leads'],
        mode='markers+text',
        text=grouped_df4['gender_age'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df4['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * (max(grouped_df4['sum_spends'] / 100) if not grouped_df4['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df4['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Gender_Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Sum of Leads: %{y}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df4[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']].values,
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Link Clicks by Gender and Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Sum of Leads',
        showlegend=False,
    )

    return fig
def seg8df5(df3):
    df_filtered = df3[df3['gender'] == 'male']

    # Calculate CPL and CPLC
    df_filtered['cpl'] = df_filtered['spend'] / df_filtered['lead']
    df_filtered['cplc'] = df_filtered['spend'] / df_filtered['link_click']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['sum_leads'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads'),
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Sum of Leads: %{y}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']].values,
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Link Clicks for Males by Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Sum of Leads',
        showlegend=False,
    )

    return fig
def seg8df6(df3):
    df_filtered = df3[df3['gender'] == 'female']

    # Calculate CPL and CPLC
    df_filtered['cpl'] = df_filtered['spend'] / df_filtered['lead']
    df_filtered['cplc'] = df_filtered['spend'] / df_filtered['link_click']

    # Group by age and calculate metrics
    grouped_df = df_filtered.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_link_clicks'],
        y=grouped_df['sum_leads'],
        mode='markers+text',
        text=grouped_df['age'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * (max(grouped_df['sum_spends'] / 100) if not grouped_df['sum_spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Sum of Leads: %{y}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']].values,
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPL vs Link Clicks for Females by Age',
        xaxis_title='Sum of Link Clicks',
        yaxis_title='Sum of Leads',
        showlegend=False,
    )

    return fig
def seg9df1(df1):
    # Group by publisher_platform and calculate metrics
    grouped_df = df1.groupby('publisher_platform').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()
    
    # Calculate CPL and CPL (Cost Per Link Click)
    grouped_df['cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks'].replace(0, 1)  # Avoid division by zero

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Publisher Platform: {row['publisher_platform']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['cpl']:.2f}<br>"
                    f"CPLC: {row['cplc']:.2f}",
        axis=1
    )

    # Create the bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['publisher_platform'],  # Labels for the bubbles
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Publisher Platform: %{text}<br>' +
            'Sum of Link Clicks: %{x}<br>' +
            'Sum of Leads per Link Click (CPLC): %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'CPLC: %{customdata[1]:.2f}<br>'
        ),
        customdata=grouped_df[['cpl', 'cplc']].values,
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs. Link Clicks by Publisher Platform',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click (CPLC)',
        showlegend=True,
    )

    return fig
def seg9df2(df1):
    df1['publisher_platform_position'] = df1['publisher_platform'] + '_' + df1['platform_position']

    # Group by the new concatenated column and calculate metrics
    grouped_df = df1.groupby('publisher_platform_position').agg(
        leads=('lead', 'sum'),
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPLC (Cost Per Link Click)
    grouped_df['cplc'] = grouped_df['spends'] / grouped_df['link_clicks'].replace(0, 1)  # Avoid division by zero

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['publisher_platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color based on leads
            colorbar=dict(title='Leads')
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Leads per Link Click (CPLC): %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Leads per Link Click by Platform Position',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click (CPLC)',
        showlegend=False
    )

    return fig
def seg9df3(df1):
    # Filter for Facebook platform
    df_filtered = df1[df1['publisher_platform'] == 'facebook']
    
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPLC (Cost Per Link Click)
    grouped_df['cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks'].replace(0, 1)  # Avoid division by zero

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Leads per Link Click (CPLC): %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Leads per Link Click for Facebook',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click (CPLC)',
        showlegend=False,
    )

    return fig
def seg9df4(df1):
    # Filter for Instagram platform
    df_filtered = df1[df1['publisher_platform'] == 'instagram']
    
    # Group by platform_position and calculate metrics
    grouped_df = df_filtered.groupby('platform_position').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')
    ).reset_index()

    # Calculate CPLC (Cost Per Link Click)
    grouped_df['cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks'].replace(0, 1)  # Avoid division by zero

    # Create a bubble chart with labels on bubbles
    fig = go.Figure()
    if grouped_df.empty:
        return fig
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['platform_position'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Platform Position: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Leads per Link Click (CPLC): %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Leads per Link Click for Instagram',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click (CPLC)',
        showlegend=False,
    )

    return fig
def seg10df1(df3):
    # Calculate CPL and CPLC
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']
    
    # Group by age and calculate metrics
    grouped_df = df3.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()
    
    # Calculate the actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    grouped_df['lead_per_link_click'] = grouped_df['sum_leads'] / grouped_df['sum_link_clicks']
    
    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()
    if grouped_df.empty:
        return fig
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['lead_per_link_click'],
        mode='markers+text',
        text=grouped_df['age'],
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Lead per Link Click: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Lead per Link Click by Age Group',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False,
    )

    return fig
def seg10df2(df3):
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Group by age and calculate metrics
    grouped_df = df3.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    grouped_df['lead_per_link_click'] = grouped_df['sum_leads'] / grouped_df['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['lead_per_link_click'],
        mode='markers+text',
        text=grouped_df['age'],
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Lead per Link Click: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Lead per Link Click by Age Group',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False,
    )

    return fig
def seg10df3(df3):
    # Calculate CPL and CPLC
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Group by gender and calculate metrics
    grouped_df2 = df3.groupby('gender').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df2['act_cpl'] = grouped_df2['sum_spends'] / grouped_df2['sum_leads']
    grouped_df2['act_cplc'] = grouped_df2['sum_spends'] / grouped_df2['sum_link_clicks']
    grouped_df2['lead_per_link_click'] = grouped_df2['sum_leads'] / grouped_df2['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df2.apply(
        lambda row: f"Gender: {row['gender']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df2['sum_leads'],
        y=grouped_df2['lead_per_link_click'],
        mode='markers+text',
        text=grouped_df2['gender'],
        textposition='middle center',
        marker=dict(
            size=grouped_df2['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df2['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df2['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Gender: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Lead per Link Click: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df2[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Lead per Link Click by Gender',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False,
    )

    return fig
def seg10df4(df3):
    # Calculate CPL and CPLC
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Group by gender and age and calculate metrics
    grouped_df2 = df3.groupby(['gender', 'age']).agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df2['act_cpl'] = grouped_df2['sum_spends'] / grouped_df2['sum_leads']
    grouped_df2['act_cplc'] = grouped_df2['sum_spends'] / grouped_df2['sum_link_clicks']
    grouped_df2['lead_per_link_click'] = grouped_df2['sum_leads'] / grouped_df2['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df2.apply(
        lambda row: f"Gender: {row['gender']}<br>"
                    f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df2['sum_leads'],
        y=grouped_df2['lead_per_link_click'],
        mode='markers+text',
        text=grouped_df2['age'],
        textposition='middle center',
        marker=dict(
            size=grouped_df2['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df2['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df2['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Gender: %{text}<br>' +
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Lead per Link Click: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df2[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Lead per Link Click by Gender and Age',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False,
    )

    return fig
def seg10df5(df3):
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Filter by gender
    filtered_df = df3[df3['gender'] == 'male']

    # Group by age and calculate metrics
    grouped_df = filtered_df.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    grouped_df['lead_per_link_click'] = grouped_df['sum_leads'] / grouped_df['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['lead_per_link_click'],
        mode='markers+text',
        text=grouped_df['age'],
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Lead per Link Click: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Lead per Link Click by Age (Male)',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False,
    )

    return fig
def seg10df6(df3):
    df3['cpl'] = df3['spend'] / df3['lead']
    df3['cplc'] = df3['spend'] / df3['link_click']

    # Filter by gender
    filtered_df = df3[df3['gender'] == 'female']

    # Group by age and calculate metrics
    grouped_df = filtered_df.groupby('age').agg(
        sum_leads=('lead', 'sum'),
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpls=('cpl', 'mean'),
        avg_cplcs=('cplc', 'mean')
    ).reset_index()

    # Calculate actual CPL and CPLC
    grouped_df['act_cpl'] = grouped_df['sum_spends'] / grouped_df['sum_leads']
    grouped_df['act_cplc'] = grouped_df['sum_spends'] / grouped_df['sum_link_clicks']
    grouped_df['lead_per_link_click'] = grouped_df['sum_leads'] / grouped_df['sum_link_clicks']

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Age: {row['age']}<br>"
                    f"Sum of Leads: {row['sum_leads']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']}<br>"
                    f"Average CPL: {row['avg_cpls']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplcs']:.2f}<br>"
                    f"Actual CPL: {row['act_cpl']:.2f}<br>"
                    f"Actual CPLC: {row['act_cplc']:.2f}",
        axis=1
    )

    # Create a bubble chart
    fig = go.Figure()
    if grouped_df.empty:
        return fig
    fig.add_trace(go.Scatter(
        x=grouped_df['sum_leads'],
        y=grouped_df['lead_per_link_click'],
        mode='markers+text',
        text=grouped_df['age'],
        textposition='middle center',
        marker=dict(
            size=grouped_df['sum_spends'] / 100,  # Adjust size for visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['sum_spends'] / 100) / (100**2),
            sizemin=4,  # Minimum bubble size
            color=grouped_df['sum_leads'],  # Color based on leads
            colorbar=dict(title='Sum of Leads')
        ),
        hovertemplate=(
            'Age: %{text}<br>' +
            'Sum of Leads: %{x}<br>' +
            'Lead per Link Click: %{y:.2f}<br>' +
            'Sum of Spends: %{marker.size}<br>' +
            'Average CPL: %{customdata[0]:.2f}<br>' +
            'Average CPLC: %{customdata[1]:.2f}<br>' +
            'Actual CPL: %{customdata[2]:.2f}<br>' +
            'Actual CPLC: %{customdata[3]:.2f}<br>'
        ),
        customdata=grouped_df[['avg_cpls', 'avg_cplcs', 'act_cpl', 'act_cplc']]
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Lead per Link Click by Age (Female)',
        xaxis_title='Sum of Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False,
    )

    return fig
