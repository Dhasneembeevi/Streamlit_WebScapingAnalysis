# # gemini_interaction.py (This file is not strictly needed for the Streamlit app,
# # but it shows how to interact with Gemini directly)

# import google.generativeai as genai

# # Replace with your actual Gemini API key
# GEMINI_API_KEY = "AIzaSyCM87KDRP2Kdv6cDlXlkm-c8HJGh8VSlWo"
# genai.configure(api_key=GEMINI_API_KEY)

# def query_gemini(prompt):
#     """Sends a prompt to the Gemini Pro model and returns the response."""
#     try:
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error querying Gemini API: {e}"

# if __name__ == "__main__":
#     user_query = input("Enter your query for Gemini AI: ")
#     gemini_response = query_gemini(user_query)
#     print("\nGemini AI's Response:")
#     print(gemini_response)
    
# streamlit_app.py

import streamlit as st
import google.generativeai as genai

# Replace with your actual Gemini API key
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key="AIzaSyCM87KDRP2Kdv6cDlXlkm-c8HJGh8VSlWo")

def query_gemini(prompt):
    """Sends a prompt to the Gemini Pro model and returns the response."""
    try:
        modelTest = genai.list_models()
        print(modelTest)

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error querying Gemini API: {e}"

st.title("Interact with Gemini AI")

user_prompt = st.text_area("Enter your prompt for Gemini AI:", height=150)

if st.button("Get Response"):
    if user_prompt:
        with st.spinner("Fetching response from Gemini AI..."):
            gemini_response = query_gemini(user_prompt)
        st.subheader("Gemini AI's Response:")
        st.markdown(gemini_response)
    else:
        st.warning("Please enter a prompt.")    