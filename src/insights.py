import streamlit as st
def platforminsights(data):
    # Calculate CPL (Cost Per Lead) and CPLC (Cost Per Link Click)
    data['cpl'] = data['spend'] / data['lead']
    data['cplc'] = data['spend'] / data['link_click']
    
    # Normalize metrics for scoring leads
    data['Leads_Normalized'] = data['lead'] / data['lead'].max()
    data['CPL_Normalized'] = 1 - (data['cpl'] / data['cpl'].max())  # Reverse normalization for CPL
    data['Leads_Score'] = data['Leads_Normalized'] + data['CPL_Normalized']
    
    # Normalize metrics for scoring link clicks
    data['Link_Clicks_Normalized'] = data['link_click'] / data['link_click'].max()
    data['CPLC_Normalized'] = 1 - (data['cplc'] / data['cplc'].max())  # Reverse normalization for CPLC
    data['Link_Clicks_Score'] = data['Link_Clicks_Normalized'] + data['CPLC_Normalized']
    
    # Separate data for Facebook and Instagram
    fb_data = data[data['publisher_platform'] == 'facebook']
    insta_data = data[data['publisher_platform'] == 'instagram']
    

    # Calculate total leads, CPL, link clicks, and CPLC for Facebook and Instagram
    fb_leads = fb_data['lead'].sum()
    insta_leads = insta_data['lead'].sum()
    
    fb_cpl = fb_data['cpl'].mean()
    insta_cpl = insta_data['cpl'].mean()
    
    fb_link_clicks = fb_data['link_click'].sum()
    insta_link_clicks = insta_data['link_click'].sum()
    
    fb_cplc = fb_data['cplc'].mean()
    insta_cplc = insta_data['cplc'].mean()
    
    # Determine the platform with more leads and link clicks
    platform_with_more_leads = 'facebook' if fb_leads > insta_leads else 'instagram'
    platform_with_more_link_clicks = 'facebook' if fb_link_clicks > insta_link_clicks else 'instagram'
    
    # Get top 3 positions for Facebook and Instagram based on leads score
    fb_top_positions_leads = fb_data.sort_values(by='Leads_Score', ascending=False).head(3)
    insta_top_positions_leads = insta_data.sort_values(by='Leads_Score', ascending=False).head(3)
    
    # Get top 3 positions for Facebook and Instagram based on link clicks score
    fb_top_positions_link_clicks = fb_data.sort_values(by='Link_Clicks_Score', ascending=False).head(3)
    insta_top_positions_link_clicks = insta_data.sort_values(by='Link_Clicks_Score', ascending=False).head(3)
    
    # Output results for leads
    st.markdown(f"**Facebook Leads:** {fb_leads}")
    st.markdown(f"**Instagram Leads:** {insta_leads}")
    
    # Output results for link clicks
    st.markdown(f"**Facebook Link Clicks:** {fb_link_clicks}")
    st.markdown(f"**Instagram Link Clicks:** {insta_link_clicks}")

    
def age_gender_insights(data):
    # Calculate CPL (Cost Per Lead) and CPLC (Cost Per Link Click)
    data['cpl'] = data['spend'] / data['lead']
    data['cplc'] = data['spend'] / data['link_click']
    
    # Normalize metrics for scoring leads
    data['Leads_Normalized'] = data['lead'] / data['lead'].max()
    data['CPL_Normalized'] = 1 - (data['cpl'] / data['cpl'].max())  # Reverse normalization for CPL
    data['Leads_Score'] = data['Leads_Normalized'] + data['CPL_Normalized']
    
    # Normalize metrics for scoring link clicks
    data['Link_Clicks_Normalized'] = data['link_click'] / data['link_click'].max()
    data['CPLC_Normalized'] = 1 - (data['cplc'] / data['cplc'].max())  # Reverse normalization for CPLC
    data['Link_Clicks_Score'] = data['Link_Clicks_Normalized'] + data['CPLC_Normalized']
    
    # Group by age and gender
    age_gender_group = data.groupby(['age', 'gender']).agg({
        'lead': 'sum',
        'cpl': 'mean',
        'link_click': 'sum',
        'cplc': 'mean',
        'Leads_Score': 'mean',
        'Link_Clicks_Score': 'mean'
    }).reset_index()
    
    # Calculate total leads, CPL, link clicks, and CPLC for each group
    age_gender_leads = age_gender_group['lead'].sum()
    age_gender_cpl = age_gender_group['cpl'].mean()
    age_gender_link_clicks = age_gender_group['link_click'].sum()
    age_gender_cplc = age_gender_group['cplc'].mean()
    
    # Get top 3 age-gender groups based on leads score
    top_age_gender_leads = age_gender_group.sort_values(by='Leads_Score', ascending=False).head(3)
    
    # Get top 3 age-gender groups based on link clicks score
    top_age_gender_link_clicks = age_gender_group.sort_values(by='Link_Clicks_Score', ascending=False).head(3)
    
    
    for index, row in top_age_gender_leads.iterrows():
        st.write(f"Age Range: {row['age']}, Gender: {row['gender']}: Leads = {row['lead']}, CPL = {row['cpl']:.2f}")
        break
    
    # Output results for link clicks
    st.markdown(f"**Total Link Clicks:** {age_gender_link_clicks}")
    for index, row in top_age_gender_link_clicks.iterrows():
        st.write(f"Age Range: {row['age']}, Gender: {row['gender']}: Link Clicks = {row['link_click']}, CPLC = {row['cplc']:.2f}")
        break
    
def attributeinsights(data):
    # Calculate CPL (Cost Per Lead) and CPLC (Cost Per Link Click)
    data['attributes']=data['attributes'].fillna('None')
    data['cpl'] = data['spend'] / data['lead']
    data['cplc'] = data['spend'] / data['link_click']
    
    # Normalize metrics for scoring leads
    data['Leads_Normalized'] = data['lead'] / data['lead'].max()
    data['CPL_Normalized'] = 1 - (data['cpl'] / data['cpl'].max())  # Reverse normalization for CPL
    data['Leads_Score'] = data['Leads_Normalized'] + data['CPL_Normalized']
    
    # Normalize metrics for scoring link clicks
    data['Link_Clicks_Normalized'] = data['link_click'] / data['link_click'].max()
    data['CPLC_Normalized'] = 1 - (data['cplc'] / data['cplc'].max())  # Reverse normalization for CPLC
    data['Link_Clicks_Score'] = data['Link_Clicks_Normalized'] + data['CPLC_Normalized']
    
    # Group by 'attributes'
    attribute_group = data.groupby('attributes').agg({
        'lead': 'sum',
        'cpl': 'mean',
        'link_click': 'sum',
        'cplc': 'mean',
        'Leads_Score': 'mean',
        'Link_Clicks_Score': 'mean'
    }).reset_index()
    
    # Calculate total leads, CPL, link clicks, and CPLC for each attribute
    total_leads = attribute_group['lead'].sum()
    avg_cpl = attribute_group['cpl'].mean()
    total_link_clicks = attribute_group['link_click'].sum()
    avg_cplc = attribute_group['cplc'].mean()
    
    # Get top 3 attributes based on leads score
    top_attributes_leads = attribute_group.sort_values(by='Leads_Score', ascending=False).head(3)
    
    # Get top 3 attributes based on link clicks score
    top_attributes_link_clicks = attribute_group.sort_values(by='Link_Clicks_Score', ascending=False).head(3)
    
    # Output results for leads
    st.markdown(f"**Total Leads:** {total_leads}")
    st.markdown(f"**Average CPL:** {avg_cpl:.2f}")
    
    for index, row in top_attributes_leads.iterrows():
        st.markdown(f"- **Attribute:** {row['attributes']} - **Leads:** {row['lead']}, **CPL:** {row['cpl']:.2f}")
    
    # Output results for link clicks
    st.markdown(f"**Total Link Clicks:** {total_link_clicks}")
    st.markdown(f"**Average CPLC:** {avg_cplc:.2f}")
    
    for index, row in top_attributes_link_clicks.iterrows():
        st.markdown(f"- **Attribute:** {row['attributes']} - **Link Clicks:** {row['link_click']}, **CPLC:** {row['cplc']:.2f}")
    
    # Top-performing attributes in terms of leads-CPL score
   
def groupplatforminsights(data):
    # Calculate CPL (Cost Per Lead) and CPLC (Cost Per Link Click)
    data['cpl'] = data['spend'] / data['lead']
    data['cplc'] = data['spend'] / data['link_click']

    # Normalize metrics for scoring leads
    data['Leads_Normalized'] = data['lead'] / data['lead'].max()
    data['CPL_Normalized'] = 1 - (data['cpl'] / data['cpl'].max())  # Reverse normalization for CPL
    data['Leads_Score'] = data['Leads_Normalized'] + data['CPL_Normalized']

    # Normalize metrics for scoring link clicks
    data['Link_Clicks_Normalized'] = data['link_click'] / data['link_click'].max()
    data['CPLC_Normalized'] = 1 - (data['cplc'] / data['cplc'].max())  # Reverse normalization for CPLC
    data['Link_Clicks_Score'] = data['Link_Clicks_Normalized'] + data['CPLC_Normalized']

    return data

def groupage_gender_insights(data):
    # Calculate CPL (Cost Per Lead) and CPLC (Cost Per Link Click)
    data['cpl'] = data['spend'] / data['lead']
    data['cplc'] = data['spend'] / data['link_click']

    # Normalize metrics for scoring leads
    data['Leads_Normalized'] = data['lead'] / data['lead'].max()
    data['CPL_Normalized'] = 1 - (data['cpl'] / data['cpl'].max())  # Reverse normalization for CPL
    data['Leads_Score'] = data['Leads_Normalized'] + data['CPL_Normalized']

    # Normalize metrics for scoring link clicks
    data['Link_Clicks_Normalized'] = data['link_click'] / data['link_click'].max()
    data['CPLC_Normalized'] = 1 - (data['cplc'] / data['cplc'].max())  # Reverse normalization for CPLC
    data['Link_Clicks_Score'] = data['Link_Clicks_Normalized'] + data['CPLC_Normalized']

    # Group by age and gender
    age_gender_group = data.groupby(['age', 'gender']).agg({
        'lead': 'sum',
        'cpl': 'mean',
        'link_click': 'sum',
        'cplc': 'mean',
        'Leads_Score': 'mean',
        'Link_Clicks_Score': 'mean'
    }).reset_index()

    return age_gender_group

def groupattributeinsights(data):
    # Fill missing attributes with 'None'
    data['attributes'] = data['attributes'].fillna('None')
    data['cpl'] = data['spend'] / data['lead']
    data['cplc'] = data['spend'] / data['link_click']

    # Normalize metrics for scoring leads
    data['Leads_Normalized'] = data['lead'] / data['lead'].max()
    data['CPL_Normalized'] = 1 - (data['cpl'] / data['cpl'].max())  # Reverse normalization for CPL
    data['Leads_Score'] = data['Leads_Normalized'] + data['CPL_Normalized']

    # Normalize metrics for scoring link clicks
    data['Link_Clicks_Normalized'] = data['link_click'] / data['link_click'].max()
    data['CPLC_Normalized'] = 1 - (data['cplc'] / data['cplc'].max())  # Reverse normalization for CPLC
    data['Link_Clicks_Score'] = data['Link_Clicks_Normalized'] + data['CPLC_Normalized']

    # Group by attributes
    attribute_group = data.groupby('attributes').agg({
        'lead': 'sum',
        'cpl': 'mean',
        'link_click': 'sum',
        'cplc': 'mean',
        'Leads_Score': 'mean',
        'Link_Clicks_Score': 'mean'
    }).reset_index()

    return attribute_group

def generate_adset_json(platform_data, age_gender_data, attribute_data):

    platform_data=groupplatforminsights(platform_data)
    age_gender_data=groupage_gender_insights(age_gender_data)
    attribute_data=groupattributeinsights(attribute_data)
    """
    Generates a JSON configuration for updating an ad set dynamically based on provided data insights.

    Args:
        platform_data (DataFrame): Insights from platforminsights function.
        age_gender_data (DataFrame): Insights from age_gender_insights function.
        attribute_data (DataFrame): Insights from attributeinsights function.

    Returns:
        dict: JSON configuration for updating an ad set.
    """

    # Determine the top-performing platform
    top_platform = 'facebook' if platform_data[platform_data['publisher_platform'] == 'facebook']['Leads_Score'].mean() > platform_data[platform_data['publisher_platform'] == 'instagram']['Leads_Score'].mean() else 'instagram'

    # Determine the top-performing age-gender group
    top_age_gender_group = age_gender_data.sort_values(by='Leads_Score', ascending=False).iloc[0]

    # Determine the top attribute based on leads score
    top_attribute = attribute_data.sort_values(by='Leads_Score', ascending=False).iloc[0]['attributes']

    # Construct JSON configuration for updating the ad set
    adset_json = {
        "name": f"Updated Ad Set - {top_platform.capitalize()}",
        "daily_budget": 10000,  
        "bid_amount": 200,      
        "status": "PAUSED",     
        "targeting": {
            "geo_locations": {
                "countries": ["US"]  
            },
            "age_min": int(top_age_gender_group['age'].split('-')[0]),  
            "age_max": int(top_age_gender_group['age'].split('-')[-1]), 
            "genders": [1 if top_age_gender_group['gender'] == 'female' else 0], 
            "custom_audiences": [{"id": top_attribute}],  
        },
        "optimization_goal": "LEAD_GENERATION",  
        "billing_event": "IMPRESSIONS",         
    }

    return adset_json