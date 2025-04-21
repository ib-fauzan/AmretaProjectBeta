import streamlit as st
import streamlit.components.v1 as components

def show_feedback():
    st.title("📋 Amreta Project – User Feedback Form")
    st.markdown("We value your feedback to improve the Amreta Project. Please fill out the form below:")

    # Replace the URL below with your actual Google Form link (embed version)
    google_form_url = "https://forms.gle/7hjje6C6zw7Z95C17"

    components.iframe(google_form_url, height=700, scrolling=True)
    linkedin_badge = """
    <style>
    .linkedin-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    max-width: 300px;
    margin: 10px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    background: white;
    }

    .linkedin-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 119, 181, 0.2);
    border-color: #0077B5;
    }

    .linkedin-link {
    text-decoration: none;
    color: inherit;
    display: flex;
    align-items: center;
    gap: 10px;
    }

    .linkedin-link:hover {
    text-decoration: none;
    }

    .linkedin-name {
    font-weight: 600; 
    color: #0077B5;
    transition: color 0.3s ease;
    }

    .linkedin-card:hover .linkedin-name {
    color: #005582;
    }

    .linkedin-title {
    font-size: 0.8em;
    color: #666;
    }
    </style>

    <div class="linkedin-card">
    <a href="https://www.linkedin.com/in/iqbalfauzanh/" target="_blank" class="linkedin-link">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="40" style="border-radius: 4px;">
        <div>
        <div class="linkedin-name">Iqbal F. Herlambang | © 2025 </div>
        <div class="linkedin-title">Water Resources Eng. Data Scientist</div>
        </div>
    </a>
    </div>
    """
    st.markdown(linkedin_badge, unsafe_allow_html=True)
if __name__ == "__main__":
    show_feedback()