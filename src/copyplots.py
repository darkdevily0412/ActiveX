
import streamlit as st
import plotly.graph_objects as go
from nltk import bigrams
from collections import Counter
from wordcloud import STOPWORDS, WordCloud
def truncate_text(text):
    words = text.split()
    truncated_words = words[:10]
    truncated_text = " ".join(truncated_words)
    return truncated_text
def create_wordcloud(df, num, den, truncate=False):
    # Calculate the link clicks to impressions ratio
    df["metric"] = df[num] / df[den]

    # Drop rows with NaN values in 'link_clicks_impressions_ratio' and 'asset_text'
    df = df.dropna(subset=["metric", "asset_text"])

    if truncate is True:
        df["asset_text"] = df["asset_text"].apply(truncate_text)

    # Initialize an empty dictionary to hold word frequencies
    word_freq = {}

    # Define additional stopwords
    additional_stopwords = {
        "and",
        "to",
        "with",
        "at",
        "the",
        "in",
        "for",
        "on",
        "of",
        "a",
        "an",
        "&",
        "-",
    }
    stopwords = STOPWORDS.union(additional_stopwords)

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Tokenize the asset text
        words = row["asset_text"].split()
        ratio = row["metric"]
        # Update word frequencies with the performance ratio
        for word in words:
            # Convert to lowercase to treat words as case-insensitive
            _word = word.lower()
            if _word not in stopwords:
                if _word in word_freq:
                    word_freq[_word] += ratio
                else:
                    word_freq[_word] = ratio

    # Generate the word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
    ).generate_from_frequencies(word_freq)

    # Convert the word cloud to an image
    image = wordcloud.to_image()

    # Display the word cloud in Streamlit
    st.image(image, use_column_width=True)
def create_bigram_wordcloud(df, col,num, den, truncate=False):
    # Calculate the metric (e.g., link clicks to impressions ratio)
    df["metric"] = df[num] / df[den]

    # Drop rows with NaN values in 'metric' and 'asset_text'
    df = df.dropna(subset=["metric", col])

    # Optionally truncate the asset text to the first 10 words
    if truncate:
        df[col] = df[col].apply(truncate_text)

    # Initialize an empty Counter to hold bigram frequencies
    bigram_freq = Counter()

    # Define additional stopwords
    additional_stopwords = {
        "and",
        "to",
        "with",
        "at",
        "the",
        "in",
        "for",
        "on",
        "of",
        "a",
        "an",
        "&",
        "-",
    }
    stopwords = STOPWORDS.union(additional_stopwords)

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Tokenize the asset text into words
        words = [
            word.lower()
            for word in row[col].split()
            if word.lower() not in stopwords
        ]
        ratio = row["metric"]

        # Create bigrams from the list of words
        bigram_list = list(bigrams(words))

        # Update bigram frequencies with the performance ratio
        for bigram in bigram_list:
            bigram_str = " ".join(bigram)  # Convert the tuple to a string
            bigram_freq[bigram_str] += ratio

    # Generate the word cloud from the bigram frequencies
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
    ).generate_from_frequencies(bigram_freq)

    # Convert the word cloud to an image
    image = wordcloud.to_image()

    # Display the word cloud in Streamlit
    st.image(image, use_column_width=True)
def paymentLinkclick(df):
    df1=df
    # Check if required columns are present
    #(df1.columns)
    required_columns = ['clicks', 'cpc', 'spend', 'Payment plan']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'Payment plan' columns.")

    # Group by payment plan and calculate metrics
    grouped_df = df1.groupby('Payment plan').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each payment plan
        spend=('spend', 'sum')
    ).reset_index()
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['Payment plan'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100 if not grouped_df['spend'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles,
            color=grouped_df['clicks'],  # Color by number of clicks
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Payment Plan: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks with Payment Plan',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def paymentclick(df1):
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click']
    # Group by the 'payment_plan' column and calculate metrics
    grouped_df = df1.groupby('Payment plan').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['Payment plan'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100  if not grouped_df['spends'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks or use another metric
            colorbar=dict(title='Link Clicks')  # Color bar to indicate the scale
        ),
        hovertemplate=(
            'Payment Plan: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def paymentlplc(df1):
    # Calculate Lead Per Link Click (LPLC)
    df1['lplc'] = df1['lead'] / df1['link_click'].replace(0, 1)  # Avoid division by zero
    
    # Group by the 'Payment plan' column and calculate metrics
    grouped_df = df1.groupby('Payment plan').agg(
        leads=('lead', 'sum'),
        spends=('spend', 'sum'),
        lplc=('lplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['lplc'],
        mode='markers+text',
        text=grouped_df['Payment plan'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color by leads
            colorbar=dict(title='Leads')  # Color bar to indicate the scale
        ),
        hovertemplate=(
            'Payment Plan: %{text}<br>' +
            'Leads: %{x}<br>' +
            'LPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of LPLC vs Leads by Payment Plan',
        xaxis_title='Leads',
        yaxis_title='LPLC (Lead Per Link Click)',
        showlegend=False
    )

    return fig
def emojisLinkclick(df):
    # Check if required columns are present
    required_columns = ['clicks', 'cpc', 'spend', 'Emojis Present']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'emojis_present' columns.")
    df['Emojis Present'] = df['Emojis Present'].fillna('No')
    # Group by emojis presence and calculate metrics
    grouped_df = df.groupby('Emojis Present').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each group
        spend=('spend', 'sum')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['Emojis Present'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100 if not grouped_df['spend'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by number of clicks
            # Choose a color scale
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Emojis Present: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks with Emojis Present',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def emojisclick(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'Emojis Present']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'Emojis Present' columns.")
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'emojis_present' column and calculate metrics
    grouped_df = df1.groupby('Emojis Present').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['Emojis Present'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            'Emojis Present: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks with Emojis Present',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def emojislplc(df1):
    # Check if required columns are present
    required_columns = ['lead', 'link_click', 'spend', 'Emojis Present']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'lead', 'link_click', 'spend', and 'Emojis Present' columns.")
    
    df1['Emojis Present'] = df1['Emojis Present'].fillna('No')

    # Calculate Lead Per Link Click (LPLC)
    df1['lplc'] = df1['lead'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'Emojis Present' column and calculate metrics
    grouped_df = df1.groupby('Emojis Present').agg(
        leads=('lead', 'sum'),
        spends=('spend', 'sum'),
        lplc=('lplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['lplc'],
        mode='markers+text',
        text=grouped_df['Emojis Present'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100, default=1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color by leads
            colorbar=dict(title='Leads')  # Add a color bar for leads
        ),
        hovertemplate=(
            'Emojis Present: %{text}<br>' +
            'Leads: %{x}<br>' +
            'LPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of LPLC vs Leads with Emojis Present',
        xaxis_title='Leads',
        yaxis_title='LPLC (Lead Per Link Click)',
        showlegend=False
    )

    return fig
def exclamationLinkclick(df):
    # Check if required columns are present
    required_columns = ['clicks', 'cpc', 'spend', 'Exclamation in 20 words']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'Exclamation in 20 words' columns.")
    
    df['Exclamation in 20 words'] = df['Exclamation in 20 words'].fillna('No')
    
    # Group by exclamation presence and calculate metrics
    grouped_df = df.groupby('Exclamation in 20 words').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each group
        spend=('spend', 'sum')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['Exclamation in 20 words'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100 if not grouped_df['spend'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by number of clicks
            # Choose a color scale
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Exclamation in 20 words: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks with Exclamation in 20 words',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def exclamationClick(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'Exclamation in 20 words']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'Exclamation in 20 words' columns.")
    
    df1['Exclamation in 20 words'] = df1['Exclamation in 20 words'].fillna('No')
    
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'Exclamation in 20 words' column and calculate metrics
    grouped_df = df1.groupby('Exclamation in 20 words').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['Exclamation in 20 words'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            'Exclamation in 20 words: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks with Exclamation in 20 words',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def exclamationlplc(df1):
    # Check if required columns are present
    required_columns = ['lead', 'link_click', 'spend', 'Exclamation in 20 words']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'lead', 'link_click', 'spend', and 'Exclamation in 20 words' columns.")
    
    df1['Exclamation in 20 words'] = df1['Exclamation in 20 words'].fillna('No')
    
    # Calculate Leads per Link Click
    df1['leads_per_click'] = df1['lead'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'Exclamation in 20 words' column and calculate metrics
    grouped_df = df1.groupby('Exclamation in 20 words').agg(
        leads=('lead', 'sum'),
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        leads_per_click=('leads_per_click', 'mean')  # Average leads per link click
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['leads_per_click'],
        mode='markers+text',
        text=grouped_df['Exclamation in 20 words'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color by leads
            colorbar=dict(title='Leads')  # Add a color bar for leads
        ),
        hovertemplate=(
            'Exclamation in 20 words: %{text}<br>' +
            'Leads: %{x}<br>' +
            'Leads per Link Click: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads per Link Click vs Leads with Exclamation in 20 Words',
        xaxis_title='Leads',
        yaxis_title='Leads per Link Click',
        showlegend=False
    )

    return fig
def nameLinkclick(df):
    # Check if required columns are present
    required_columns = ['clicks', 'cpc', 'spend', 'name']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'name' columns.")
    
    
    # Group by name and calculate metrics
    grouped_df = df.groupby('name').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each group
        spend=('spend', 'sum')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['name'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100 if not grouped_df['spend'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by number of clicks
            # Choose a color scale
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Name: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Name',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def nameClick(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'name']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'name' columns.")
    
    
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'name' column and calculate metrics
    grouped_df = df1.groupby('name').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['name'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1 ) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            'Name: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Name',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def addressLinkclick(df):
    # Check if required columns are present
    required_columns = ['clicks', 'cpc', 'spend', 'address']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'address' columns.")
    
    # Group by address and calculate metrics
    grouped_df = df.groupby('address').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each group
        spend=('spend', 'sum')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['address'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100 if not grouped_df['spend'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by number of clicks
            # Choose a color scale
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Address: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Address',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def addressClick(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'address']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'address' columns.")
    
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'address' column and calculate metrics
    grouped_df = df1.groupby('address').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['address'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            'Address: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Address',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def priceLinkclick(df):
    # Check if required columns are present
    required_columns = ['clicks', 'cpc', 'spend', 'price']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'price' columns.")
    
    # Group by price and calculate metrics
    grouped_df = df.groupby('price').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each group
        spend=('spend', 'sum')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['price'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100 if not grouped_df['spend'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by number of clicks
            # Choose a color scale
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Price: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Price',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def priceClick(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'price']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'price' columns.")
    
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'price' column and calculate metrics
    grouped_df = df1.groupby('price').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['price'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            # Choose a color scale
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            'Price: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Price',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def emojiLinkclick(df):
    # Check if required columns are present
    required_columns = ['clicks', 'cpc', 'spend', 'emoji']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'cpc', 'spend', and 'emoji' columns.")
    
    # Group by emoji and calculate metrics
    grouped_df = df.groupby('emoji').agg(
        clicks=('clicks', 'sum'),
        cpc=('cpc', 'mean'),  # Use mean CPC for each group
        spend=('spend', 'sum')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=grouped_df['emoji'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spend'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spend'] / 100, default=1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by number of clicks
            # Choose a color scale
            colorbar=dict(title='Number of Clicks')  # Add a color bar for clicks
        ),
        hovertemplate=(
            'Emoji: %{text}<br>' +
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks by Emoji',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False,
    )

    return fig
def emojiClick(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'emoji']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'emoji' columns.")
    
    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'emoji' column and calculate metrics
    grouped_df = df1.groupby('emoji').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=grouped_df['emoji'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100, default=1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            # Choose a color scale
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            'Emoji: %{text}<br>' +
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks by Emoji',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def emojilplc(df1):
    # Check if required columns are present
    required_columns = ['lead', 'link_click', 'spend', 'emoji']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'lead', 'link_click', 'spend', and 'emoji' columns.")
    
    # Calculate Lead Per Link Click (LPLC)
    df1['lplc'] = df1['lead'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'emoji' column and calculate metrics
    grouped_df = df1.groupby('emoji').agg(
        leads=('lead', 'sum'),
        spends=('spend', 'sum'),
        lplc=('lplc', 'mean')
    ).reset_index()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['lplc'],
        mode='markers+text',
        text=grouped_df['emoji'],  # Labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100, default=1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color by leads
            colorbar=dict(title='Leads')  # Add a color bar for leads
        ),
        hovertemplate=(
            'Emoji: %{text}<br>' +
            'Leads: %{x}<br>' +
            'LPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>'
        ),
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of LPLC vs Leads by Emoji',
        xaxis_title='Leads',
        yaxis_title='LPLC (Lead Per Link Click)',
        showlegend=False
    )

    return fig
def attributesLinkclicks(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'attributes']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', and 'attributes' columns.")
    
    df1['attributes'] = df1['attributes'].fillna('No')

    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'attributes' column and calculate metrics
    grouped_df = df1.groupby('attributes').agg(
        link_clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        cplc=('cplc', 'mean')
    ).reset_index()
    
    # Extract the first letter of each attribute for the labels
    first_letters = grouped_df['attributes'].apply(
        lambda x: "".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])
    ).tolist()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['link_clicks'],
        y=grouped_df['cplc'],
        mode='markers+text',
        text=first_letters,  # Use first letters as labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['link_clicks'],  # Color by link clicks
            colorscale='Viridis',  # Choose a color scale
            colorbar=dict(title='Link Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            "Attributes: %{customdata}<br>" +  # Display the full attributes
            'Link Clicks: %{x}<br>' +
            'CPLC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>' +
            '<extra></extra>'  # Remove the trace name from hover info
        ),
        customdata=grouped_df['attributes']  # Pass full attributes for hover text
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPLC vs Link Clicks with Attributes',
        xaxis_title='Link Clicks',
        yaxis_title='CPLC (Cost Per Link Click)',
        showlegend=False
    )

    return fig
def attributesClick(df1):
    # Check if required columns are present
    required_columns = ['clicks', 'spend', 'attributes']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'clicks', 'spend', and 'attributes' columns.")
    
    df1['attributes'] = df1['attributes'].fillna('No')

    # Calculate Cost Per Link Click (CPLC)
    df1['cpc'] = df1['spend'] / df1['clicks'].replace(0, 1)  # Avoid division by zero

    # Group by the 'attributes' column and calculate metrics
    grouped_df = df1.groupby('attributes').agg(
        clicks=('clicks', 'sum'),
        spends=('spend', 'sum'),
        cpc=('cpc', 'mean')
    ).reset_index()
    
    # Extract the first letter of each attribute for the labels
    first_letters = grouped_df['attributes'].apply(
        lambda x: "".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])
    ).tolist()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['clicks'],
        y=grouped_df['cpc'],
        mode='markers+text',
        text=first_letters,  # Use first letters as labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['clicks'],  # Color by link clicks
            colorscale='Viridis',  # Choose a color scale
            colorbar=dict(title='Clicks')  # Add a color bar for link clicks
        ),
        hovertemplate=(
            "Attributes: %{customdata}<br>" +  # Display the full attributes
            'Clicks: %{x}<br>' +
            'CPC: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>' +
            '<extra></extra>'  # Remove the trace name from hover info
        ),
        customdata=grouped_df['attributes']  # Pass full attributes for hover text
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of CPC vs Clicks with Attributes',
        xaxis_title='Clicks',
        yaxis_title='CPC (Cost Per Click)',
        showlegend=False
    )

    return fig
def attributeslplc(df1):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'attributes', 'lead']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', 'attributes', and 'lead' columns.")
    
    df1['attributes'] = df1['attributes'].fillna('No')

    # Calculate Cost Per Link Click (CPLC)
    df1['cplc'] = df1['spend'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Calculate Leads per Link Click
    df1['leads_per_link_click'] = df1['lead'] / df1['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'attributes' column and calculate metrics
    grouped_df = df1.groupby('attributes').agg(
        leads=('lead', 'sum'),
        clicks=('link_click', 'sum'),
        spends=('spend', 'sum'),
        leads_per_link_click=('leads_per_link_click', 'mean')  # Average leads per click
    ).reset_index()

    # Extract the first letter of each attribute for the labels
    first_letters = grouped_df['attributes'].apply(
        lambda x: "".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])
    ).tolist()
    
    # Create a bubble chart with labels on bubbles
    fig = go.Figure()

    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=grouped_df['leads'],
        y=grouped_df['leads_per_link_click'],
        mode='markers+text',
        text=first_letters,  # Use first letters as labels
        textposition='middle center',
        marker=dict(
            size=grouped_df['spends'] / 100,  # Adjust size for better visibility
            sizemode='area',
            sizeref=2. * max(grouped_df['spends'] / 100 if not grouped_df['spends'].empty else 1) / (100**2),
            sizemin=4,  # Minimum size of the bubbles
            color=grouped_df['leads'],  # Color by leads
            colorscale='Viridis',  # Choose a color scale
            colorbar=dict(title='Leads')  # Add a color bar for leads
        ),
        hovertemplate=(
            "Attributes: %{customdata}<br>" +  # Display the full attributes
            'Leads: %{x}<br>' +
            'Leads per Link Click: %{y:.2f}<br>' +
            'Spends: %{marker.size:.2f}<br>' +
            '<extra></extra>'  # Remove the trace name from hover info
        ),
        customdata=grouped_df['attributes']  # Pass full attributes for hover text
    ))

    # Update layout
    fig.update_layout(
        title='Bubble Chart of Leads vs Leads per Click with Attributes',
        xaxis_title='Leads',
        yaxis_title='Leads per link Click',
        showlegend=False
    )

    return fig
def linkclickattributes(df):
    # Group by 'attributes' and aggregate
    grouped_df = df.groupby('attributes').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum')  # Use sum_spends instead of avg_cpl
    ).reset_index()
    grouped_df['act_spend'] = grouped_df['sum_spends']  # Directly use sum_spends as act_spend
    
    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Attribute: {row['attributes']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']:.2f}<br>"
                    f"Actual Spend: {row['act_spend']:.2f}",
        axis=1
    )
    
    # Extract the first letter of each attribute for x-axis labels
    first_letters = grouped_df['attributes'].apply(lambda x: " ".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])).tolist()

    # Create a bar chart for sum_link_clicks
    bar_chart = go.Bar(
        x=grouped_df['attributes'],
        y=grouped_df['sum_link_clicks'],
        name='Sum of Link Clicks',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['attributes'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
    )

    # Create the layout with dual y-axes and improved x-axis labels
    layout = go.Layout(
        title='Link Clicks and Spend by Attribute',
        xaxis=dict(
            title='Attribute',
            tickangle=-45,  # Rotate x-axis labels for better readability
            tickmode='array',  # Use a custom tick array
            tickvals=grouped_df['attributes'],  # Set the tick values to the unique attributes
            ticktext=first_letters,  # Set the tick texts to the first letter of each attribute
        ),
        yaxis=dict(title='Sum of Link Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
    # Calculate Cost Per Link Click (CPLC)
def cplcattributes(df):
    df['cplc'] = df['spend'] / df['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by 'attributes' and aggregate
    grouped_df = df.groupby('attributes').agg(
        sum_link_clicks=('link_click', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cplc=('cplc', 'mean')  # Calculate average CPLC
    ).reset_index()
    
    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Attribute: {row['attributes']}<br>"
                    f"Sum of Link Clicks: {row['sum_link_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']:.2f}<br>"
                    f"Average CPLC: {row['avg_cplc']:.2f}",
        axis=1
    )
    
    # Extract the first letter of each attribute for x-axis labels
    first_letters = grouped_df['attributes'].apply(lambda x: " ".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])).tolist()

    # Create a bar chart for sum_spends
    bar_chart = go.Bar(
        x=grouped_df['attributes'],
        y=grouped_df['sum_spends'],
        name='Sum of Spends',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for avg_cplc on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['attributes'],
        y=grouped_df['avg_cplc'],
        mode='lines+markers',
        name='Average CPLC',
        yaxis='y2',
        hoverinfo='text',
    )

    # Create the layout with dual y-axes and improved x-axis labels
    layout = go.Layout(
        title='Sum of Spends and Average CPLC by Attribute',
        xaxis=dict(
            title='Attribute',
            tickangle=-45,  # Rotate x-axis labels for better readability
            tickmode='array',  # Use a custom tick array
            tickvals=grouped_df['attributes'],  # Set the tick values to the unique attributes
            ticktext=first_letters,  # Set the tick texts to the first letter of each attribute
        ),
        yaxis=dict(title='Sum of Spends'),
        yaxis2=dict(title='Average CPLC', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
def clickattributes(df):
    # Group by 'attributes' and aggregate
    grouped_df = df.groupby('attributes').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum'),  # Updated to sum_spends
        avg_cpc=('cpc', 'mean')  # Changed from avg_cpls to avg_cpc
    ).reset_index()
    grouped_df['act_cpc'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']
    
    # Extract the first letter of each item in comma-separated attributes for x-axis labels
    first_letters = grouped_df['attributes'].apply(
        lambda x: "".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])
    ).tolist()

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Attribute: {row['attributes']}<br>"
                    f"Sum of Clicks: {row['sum_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']:.2f}<br>"  # Updated to sum_spends
                    f"Average CPC: {row['avg_cpc']:.2f}<br>"
                    f"Actual CPC: {row['act_cpc']:.2f}",
        axis=1
    )
    
    # Create a bar chart for sum_clicks
    bar_chart = go.Bar(
        x=grouped_df['attributes'],
        y=grouped_df['sum_clicks'],
        name='Sum of Clicks',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['attributes'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
    )

    # Create the layout with dual y-axes and improved x-axis labels
    layout = go.Layout(
        title='Clicks and Spends by Attribute',
        xaxis=dict(
            title='Attribute',
            tickangle=-45,  # Rotate x-axis labels for better readability
            tickmode='array',  # Use a custom tick array
            tickvals=grouped_df['attributes'],  # Set the tick values to the unique attributes
            ticktext=first_letters,  # Set the tick texts to the first letters of each attribute
        ),
        yaxis=dict(title='Sum of Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
def cpcattributes(df):
    # Group by 'attributes' and aggregate
    grouped_df = df.groupby('attributes').agg(
        sum_clicks=('clicks', 'sum'),
        sum_spends=('spend', 'sum'),  # Updated to sum_spends
        avg_cpc=('cpc', 'mean')  # Changed from avg_cpls to avg_cpc
    ).reset_index()
    grouped_df['act_cpc'] = grouped_df['sum_spends'] / grouped_df['sum_clicks']
    
    # Extract the first letter of each item in comma-separated attributes for x-axis labels
    first_letters = grouped_df['attributes'].apply(
        lambda x: "".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])
    ).tolist()

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Attribute: {row['attributes']}<br>"
                    f"Sum of Clicks: {row['sum_clicks']}<br>"
                    f"Sum of Spends: {row['sum_spends']:.2f}<br>"  # Updated to sum_spends
                    f"Average CPC: {row['avg_cpc']:.2f}<br>"
                    f"Actual CPC: {row['act_cpc']:.2f}",
        axis=1
    )
    
    # Create a bar chart for sum_clicks
    bar_chart = go.Bar(
        x=grouped_df['attributes'],
        y=grouped_df['sum_spends'],
        name='Sum of Spends',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['attributes'],
        y=grouped_df['act_cpc'],
        mode='lines+markers',
        name='Avg of CPC',
        yaxis='y2',
        hoverinfo='text',
    )

    # Create the layout with dual y-axes and improved x-axis labels
    layout = go.Layout(
        title='Clicks and Spends by Attribute',
        xaxis=dict(
            title='Attribute',
            tickangle=-45,  # Rotate x-axis labels for better readability
            tickmode='array',  # Use a custom tick array
            tickvals=grouped_df['attributes'],  # Set the tick values to the unique attributes
            ticktext=first_letters,  # Set the tick texts to the first letters of each attribute
        ),
        yaxis=dict(title='Sum of Clicks'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
def lplcattributes(df):
    # Check if required columns are present
    required_columns = ['link_click', 'spend', 'attributes', 'lead']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain 'link_click', 'spend', 'attributes', and 'lead' columns.")
    
    df['attributes'] = df['attributes'].fillna('No')
    
    # Calculate Leads per Link Click
    df['leads_per_click'] = df['lead'] / df['link_click'].replace(0, 1)  # Avoid division by zero

    # Group by the 'attributes' column and calculate metrics
    grouped_df = df.groupby('attributes').agg(
        sum_link_click=('link_click', 'sum'),
        sum_leads=('lead', 'sum'),
        sum_spends=('spend', 'sum'),
        avg_cpc=('cpc', 'mean'),  # Optional, if needed for additional insights
        leads_per_click=('leads_per_click', 'mean')  # Average leads per link click
    ).reset_index()
    
    # Extract the first letter of each item in comma-separated attributes for x-axis labels
    first_letters = grouped_df['attributes'].apply(
        lambda x: "".join([i.lstrip()[0].upper() if i.lstrip() else 'None' for i in x.split(',')])
    ).tolist()

    # Create hover text
    hover_text = grouped_df.apply(
        lambda row: f"Attribute: {row['attributes']}<br>"
                    f"Leads per Link Click: {row['leads_per_click']:.2f}<br>"  # Updated to leads_per_click
                    f"Sum of Spends: {row['sum_spends']:.2f}<br>"  # Updated to sum_spends
                    f"Average CPC: {row['avg_cpc']:.2f}",  # Optional
        axis=1
    )
    
    # Create a bar chart for leads_per_click
    bar_chart = go.Bar(
        x=grouped_df['attributes'],
        y=grouped_df['leads_per_click'],
        name='Leads per Link Click',
        hoverinfo='text',
        hovertext=hover_text,
    )

    # Create a line chart for sum_spends on a secondary y-axis
    line_chart = go.Scatter(
        x=grouped_df['attributes'],
        y=grouped_df['sum_spends'],
        mode='lines+markers',
        name='Sum of Spends',
        yaxis='y2',
        hoverinfo='text',
    )

    # Create the layout with dual y-axes and improved x-axis labels
    layout = go.Layout(
        title='Leads per Link Click and Spends by Attribute',
        xaxis=dict(
            title='Attribute',
            tickangle=-45,  # Rotate x-axis labels for better readability
            tickmode='array',  # Use a custom tick array
            tickvals=grouped_df['attributes'],  # Set the tick values to the unique attributes
            ticktext=first_letters,  # Set the tick texts to the first letters of each attribute
        ),
        yaxis=dict(title='Leads per Link Click'),
        yaxis2=dict(title='Sum of Spends', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1),
        hovermode='x',
    )

    # Combine the charts
    fig = go.Figure(data=[bar_chart, line_chart], layout=layout)

    return fig
