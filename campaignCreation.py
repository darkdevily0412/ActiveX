import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
import uuid
import facebook
from PIL import Image
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.adobjects.adimage import AdImage
from facebook_business.api import FacebookAdsApi

load_dotenv()

# Initialize Google Generative AI
api_key = "AIzaSyCF4LEk9GiPZQbwtRJZCSD_5rCCKJutgEI"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Streamlit app title
st.title("AI-Powered Ad Content Generator & Facebook Ad Uploader")

# Initialize session state variables if not already set
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'image_description' not in st.session_state:
    st.session_state.image_description = None
    
def upload_image_and_get_hash(image_file, ad_account_id, access_token):
    # Define the directory and create it if it doesn't exist
    save_directory = 'F:\Projects\hackathon'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Create a unique filename for the uploaded image
    unique_filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(save_directory, unique_filename)
    print(file_path)

    # Save the uploaded image to the specified path
    with open(file_path, 'wb') as f:
        f.write(image_file.read())

    try:
        # Initialize Facebook Ads API
        FacebookAdsApi.init(access_token=access_token)

        # Upload the image
        image = AdImage(parent_id=ad_account_id)
        image[AdImage.Field.filename] = file_path  # Path to your image file
        image.remote_create()

        image_hash = image[AdImage.Field.hash]
        return image_hash
    except Exception as e:
        raise Exception(f"Error uploading image: {str(e)}")

tab1, tab2 = st.tabs(["Ad Generation", "Facebook Ad Upload"])

with tab1:
    st.header("Generate AI-Powered Ad Content")

    # Input fields for ad content
    prompt = st.text_input("Enter your ad prompt:", placeholder="E.g., A summer sale for fashion products")
    uploaded_image = st.file_uploader("Optional: Upload an image for the ad", type=["jpg", "png", "jpeg"])
    print(uploaded_image)
    user_content = st.text_area("Optional: Provide specific content", placeholder="Leave empty to generate content")
    target_audience = st.text_input("Define your target audience:", placeholder="E.g., young adults, fashion enthusiasts")
    website_link = st.text_input("Enter the website link for your products:", placeholder="https://example.com")

    # Function to generate ad content using AI
    def generate_ad_content(prompt, target_audience, website_link, image_description=None):
        if image_description:
            ai_prompt = f"""Create an engaging and detailed ad with 10-13 lines of content using the following description: '{image_description}'.
                            The target audience is '{target_audience}'. 
                            Include emojis to make the content more attractive and exciting. 
                            Make sure to incorporate a clickable link to purchase: '{website_link}'. 
                            Avoid using any brackets and ensure the ad title is exactly 3 words."""
        else:
            ai_prompt = f"""Create an engaging and detailed ad with 10-13 lines of content for the following prompt: '{prompt}'.
                            The target audience is '{target_audience}'. 
                            Include emojis to make the content more attractive and exciting. 
                            Make sure to incorporate a clickable link to purchase: '{website_link}'. 
                            Avoid using any brackets and ensure the ad title is exactly 3 words."""

        try:
            response = model.generate_content([ai_prompt])
            return response.text.strip() if response else "Error: No response from AI"
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            return "Failed to generate content."

    # Function to generate image description from uploaded image
    def describe_image(image):
        image_bytes = image.read()
        image = Image.open(io.BytesIO(image_bytes))

        try:
            response = model.generate_content(["What is in this photo?", image])
            return response.text.strip() if response else "A high-quality image relevant to the prompt"
        except Exception as e:
            st.error(f"Error describing image: {str(e)}")
            return "Error describing image."

    # Generate content button
    if st.button("Generate Ad Content", key="generate_ad_button"):
        if not user_content and uploaded_image:
            st.session_state.image_description = describe_image(uploaded_image)
            st.write("Generating content based on the uploaded image using AI...")
            st.session_state.generated_content = generate_ad_content(prompt, target_audience, website_link, image_description=st.session_state.image_description)
        elif not user_content:
            st.write("Generating content using AI...")
            st.session_state.generated_content = generate_ad_content(prompt, target_audience, website_link)
        else:
            st.session_state.generated_content = user_content

    # Display the generated content and optional image
    st.subheader("Generated Ad Content")
    if st.session_state.generated_content:
        st.write(st.session_state.generated_content)
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

with tab2:
    st.header("Upload Ad to Facebook")

    # Facebook API inputs
    access_token = st.text_input("Facebook Access Token", type="password")
    app_id = st.text_input("Facebook App ID")
    app_secret = st.text_input("Facebook App Secret", type="password")
    ad_account_id = st.text_input("Ad Account ID", placeholder="act_1234567890")
    page_id = st.text_input("Facebook Page ID")

    # Optional fields from the ad generation (image, link, message)
    image_hash = None
    if uploaded_image and access_token and app_id and app_secret and ad_account_id:
        try:
            image_hash = upload_image_and_get_hash(uploaded_image, ad_account_id, access_token)
            st.write(f"Image Hash: {image_hash}")
        except Exception as e:
            st.error(f"Error uploading image: {str(e)}")

    link = st.text_input("Link to your product page", value=website_link)
    message = st.text_area("Generated Ad Message", value=st.session_state.generated_content or "Your ad content will appear here after generation.")
    
    campaign_name = st.text_input("Campaign Name")
    ad_set_name = st.text_input("Ad Set Name")
    ad_creative_name = st.text_input("Ad Creative Name")
    ad_name = st.text_input("Ad name")

    if st.button("Create Facebook Ad Campaign", key="create_facebook_ad"):
        try:
            # Initialize Facebook Ads API
            FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)
            ad_account = AdAccount(ad_account_id)

            # Step 1: Create Campaign
            campaign = ad_account.create_campaign(params={
                Campaign.Field.name: campaign_name,
                Campaign.Field.objective: Campaign.Objective.outcome_traffic,
                Campaign.Field.status: Campaign.Status.paused,
                'special_ad_categories': ['NONE']
            })
            st.success(f"Created Campaign with ID: {campaign['id']}")

            # Step 2: Create Ad Set
            ad_set = ad_account.create_ad_set(params={
                AdSet.Field.name: ad_set_name,
                AdSet.Field.campaign_id: campaign['id'],
                AdSet.Field.daily_budget: 10000,
                AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
                AdSet.Field.optimization_goal: AdSet.OptimizationGoal.link_clicks,
                AdSet.Field.bid_amount: 500,
                AdSet.Field.targeting: {
                    'geo_locations': {'countries': ['US']}
                },
                AdSet.Field.status: AdSet.Status.paused
            })
            st.success(f"Created Ad Set with ID: {ad_set['id']}")

            image_hash = image_hash
            api_version = 'v20.0'  # Use the API version you intend to use, e.g., 'v20.0'

            # Initialize the Facebook Ads API
            FacebookAdsApi.init(access_token=access_token)

            # Define the object story specification for the ad creative
            object_story_spec = {
                "page_id": page_id,
                "link_data": {
                    "image_hash": image_hash,
                    "link": f"https://facebook.com/{page_id}",
                    "message": message
                }
            }

            # Define the degrees of freedom specification
            degrees_of_freedom_spec = {
                "creative_features_spec": {
                    "standard_enhancements": {
                        "enroll_status": "OPT_IN"
                    }
                }
            }

            # Create the ad creative
            ad_creative = AdCreative(parent_id=ad_account_id)
            ad_creative.remote_create(params={
                'name': "My Test Creative Comeback",
                'object_story_spec': object_story_spec,
                'degrees_of_freedom_spec': degrees_of_freedom_spec,
            })

            # Print the created ad creative ID
            st.success(f"Ad Creative ID: {ad_creative.get_id()}")

            # Create the Ad
            ad_params = {
                'name': ad_name,  # This can also be made user-defined if needed
                'adset_id': ad_set['id'],
                'creative': {'creative_id': ad_creative.get_id()},
                'status': 'PAUSED',
            }
            ad = ad_account.create_ad(params=ad_params)
            st.success(f"Created Ad with ID: {ad['id']}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.subheader("show adpreview")

    # Input field for ad set ID to update
    ad_preview = st.text_input("Enter the AD_Creative ID for seeing preview")
    
    def display_iframes(links, items_per_row=3, spacing=20):
        for i in range(0, len(links), items_per_row):
            row_links = links[i : i + items_per_row]
            cols = st.columns(len(row_links))
            for col, link in zip(cols, row_links):
                # Construct the iframe HTML string with desired width and height
                iframe_html = link['body']
                col.markdown(iframe_html, unsafe_allow_html=True)

            # Add spacing after each row, except after the last one
            if i + items_per_row < len(links):
                # You can adjust the spacing by changing the number of empty lines in the Markdown
                st.markdown(
                    f"<div style='margin-bottom: {spacing}px;'></div>",
                    unsafe_allow_html=True,
            )
            
    if st.button("Generate Ad Preview", key="generate_ad_preview"):
        try:
            # Fetch Ad Creative Preview
            FacebookAdsApi.init(access_token=access_token)
            ad_cre = ad_preview
            fields = []
            params = {
                'ad_format': 'DESKTOP_FEED_STANDARD',
            }
            FacebookAdsApi.init(access_token=access_token)
            preview = AdCreative(ad_cre).get_previews(fields=fields, params=params)
            pre = list(preview)
            st.write("Ad Preview:")
            # if isinstance(ad_preview, str):
            #     # Directly display the raw HTML string if it is a string
            #     st.write("Iframe HTML:", ad_preview)

            #     # Display the Ad Preview in Streamlit using the iframe
            #     st.components.v1.html(ad_preview, height=250)
            # else:
            #     st.error(f"Unexpected ad preview format: {type(ad_preview)}")
            display_iframes(pre)
            
        except Exception as e:
            st.error(f"Error fetching ad preview: {str(e)}")

    # Section for updating the ad set
    st.subheader("Update Ad Set")

    # Input field for ad set ID to update
    adset_id_to_update = st.text_input("Enter the Ad Set ID to update")
    
    if st.button("Update Ad Set", key="update_adset_button"):
        try:
            # Initialize Facebook Ads API with your credentials
            FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)
            fields = []
            
            params = {
                'name': 'Updated Ad Set Name',                
                'daily_budget': 10000,                        
                'bid_amount': 200,                            
                'status': 'PAUSED',                           
                'targeting': {                                
                    'geo_locations': {
                        'countries': ['US']
                    },
                    'age_min': 18,
                    'age_max': 45
                },
                # Add more parameters as needed
            }

            # Initialize the AdSet object with the specified Ad Set ID
            adset = AdSet(adset_id_to_update)

            # Update the ad set
            adset.api_update(fields=fields, params=params)
            st.success(f"Ad Set {adset_id_to_update} updated successfully.")
            
        except Exception as e:
            st.error(f"Error updating Ad Set: {str(e)}")