"""
LCSH Assistant - A Streamlit app for suggesting Library of Congress Subject Headings
"""
import os
import streamlit as st
from dotenv import load_dotenv

from app.gemini_client import GeminiClient
from app.file_utils import process_uploaded_file, process_multiple_files, combine_file_contents

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="LCSH Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
def load_css():
    """Load custom CSS"""
    st.markdown("""
    <style>
    /* Base styles */
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    /* Info box */
    .info-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 1.25rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        color: #1E3A8A;
        font-size: 1.05rem;
        line-height: 1.6;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* File info */
    .file-info {
        background-color: #F9FAFB;
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        border: 1px solid #E5E7EB;
        display: flex;
        align-items: center;
        font-size: 0.95rem;
    }
    
    .file-info:before {
        content: "📄";
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        border-radius: 0.375rem 0.375rem 0 0;
        padding: 0 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #1E40AF !important;
        border-bottom: 2px solid #3B82F6 !important;
    }
    
    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        .main-header, .sub-header {
            color: #93C5FD;
            border-bottom-color: #374151;
        }
        
        .info-box {
            background-color: #1E293B;
            border-left: 5px solid #3B82F6;
            color: #E5E7EB;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .file-info {
            background-color: #1F2937;
            border: 1px solid #4B5563;
            color: #E5E7EB;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #1E293B !important;
            color: #93C5FD !important;
            border-bottom: 2px solid #3B82F6 !important;
        }
        
        .stButton > button {
            background-color: #3B82F6;
        }
        
        .stButton > button:hover {
            background-color: #2563EB;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    load_css()
    
    # Header
    st.markdown('<h1 class="main-header">LCSH Assistant</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">A tool for suggesting Library of Congress Subject Headings '
        'for East Asian language materials.</div>',
        unsafe_allow_html=True
    )
    
    # Sidebar for API key
    with st.sidebar:
        st.markdown("## Settings")
        api_key = st.text_input(
            "Enter your Google Gemini API Key",
            type="password",
            help="Your API key will not be stored and will be cleared when the session ends.",
            value=os.getenv("GEMINI_API_KEY", "")
        )
        
        st.markdown("---")
        st.markdown("## About")
        st.markdown(
            "LCSH Assistant helps librarians assign Library of Congress Subject Headings "
            "to East Asian language materials. It analyzes bibliographic information and "
            "suggests appropriate subject headings validated through the LCSH API."
        )
        st.markdown("---")
        st.markdown("### Privacy Notice")
        st.markdown(
            "This application does not store any user data or API keys. "
            "All data is processed in-memory and cleared when the session ends."
        )
    
    # Check if API key is provided
    if not api_key:
        st.warning("Please enter your Google Gemini API Key in the sidebar to use the application.")
        return
    
    # Initialize tabs
    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])
    
    # Text input tab
    with tab1:
        st.markdown('<h2 class="sub-header">Enter Bibliographic Information</h2>', unsafe_allow_html=True)
        text_input = st.text_area(
            "Enter bibliographic information about the material",
            height=200,
            placeholder="Enter title, author, publication information, table of contents, abstract, or any other bibliographic information..."
        )
        
        if st.button("Generate LCSH Recommendations", key="text_button"):
            if not text_input:
                st.error("Please enter some bibliographic information.")
            else:
                with st.spinner("Generating LCSH recommendations..."):
                    try:
                        # Initialize Gemini client
                        gemini_client = GeminiClient(api_key)
                        
                        # Generate recommendations
                        result = gemini_client.generate_lcsh_recommendations(text_input=text_input)
                        
                        # Display results
                        st.markdown('<h2 class="sub-header">LCSH Recommendations</h2>', unsafe_allow_html=True)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Error generating recommendations: {str(e)}")
    
    # File upload tab
    with tab2:
        st.markdown('<h2 class="sub-header">Upload Files</h2>', unsafe_allow_html=True)
        st.markdown(
            "Upload one or more files containing bibliographic information. "
            "Supported formats: TXT, DOCX, PDF, and images (JPG, PNG, etc.)."
        )
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=["txt", "docx", "pdf", "jpg", "jpeg", "png"],
            accept_multiple_files=True
        )
        
        # Display information about uploaded files
        if uploaded_files:
            st.markdown('<h3 class="sub-header">Uploaded Files</h3>', unsafe_allow_html=True)
            
            for file in uploaded_files:
                file_size_kb = round(file.size / 1024, 2)
                st.markdown(
                    f'<div class="file-info">{file.name} ({file_size_kb} KB)</div>',
                    unsafe_allow_html=True
                )
        
        if st.button("Generate LCSH Recommendations", key="file_button"):
            if not uploaded_files:
                st.error("Please upload at least one file.")
            else:
                with st.spinner("Processing files and generating LCSH recommendations..."):
                    try:
                        # Process the uploaded files
                        processed_files = process_multiple_files(uploaded_files)
                        
                        # Combine file contents
                        combined_text, first_image = combine_file_contents(processed_files)
                        
                        # Initialize Gemini client
                        gemini_client = GeminiClient(api_key)
                        
                        # Generate recommendations
                        result = gemini_client.generate_lcsh_recommendations(
                            text_input=combined_text,
                            image_input=first_image
                        )
                        
                        # Display results
                        st.markdown('<h2 class="sub-header">LCSH Recommendations</h2>', unsafe_allow_html=True)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Error processing files or generating recommendations: {str(e)}")

if __name__ == "__main__":
    main() 