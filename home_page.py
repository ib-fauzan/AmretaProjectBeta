import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

def show_home():
    st.title("Rainfall Return Period Analyser 0.1 (Beta)")
    st.header("🌧️ Welcome to our hydro-cycle journey!")
    st.write("This tool helps you analyze historical rainfall data to estimate the Return Period of rainfall events—a key concept in hydrology and risk assessment.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌀 What is Return Period?")
        st.image("https://www.open.edu/openlearncreate/pluginfile.php/167901/mod_oucontent/oucontent/12418/64b5afe7/bd6423a5/m2_ss4_fig4.1.jpg", width=400,
                 caption="Hydrology Cycle | Source: Open University")
        st.markdown('''
                    The Return Period (also known as the Recurrence Interval) is the estimated average time interval between rainfall events of a certain intensity or magnitude.
                    For example, a 50-year rainfall event is one that has a 2% chance of being equaled or exceeded in any given year.
                    ''')
        st.write("⚠️ **Common Misconception:**")
        st.markdown("""
                    Many people think a “50-year return period” means the event happens only once every 50 years.
                    That’s not true.

                    Instead, it means:

                    1. The probability of that event occurring in any single year is 2%
                    2. It could happen two years in a row, or even more than once in the same year
                    3. Or it might not occur for 50 years—it's about probability, not prediction

                    It’s similar to rolling a dice: just because a 6 has a 1-in-6 chance doesn’t mean it only appears every 6 rolls.
                    """)
    with col2:
        st.subheader("📊 What Can You Do With This Tool?")
        st.markdown("""
                    With this calculator, you can:
                    1. Input your historical rainfall data
                    2. Analyze statistical properties of the data
                    3. Estimate the Return Periods using various statistical methods:
                        - Normal
                        - Log Normal
                        - Pearson III
                        - Log Pearson III
                        - Gumbel distributions
                    4. Visualize the return period curved for better interpretation
                    5. Perform statistical tests to validate the data quality using:
                        - RAPS (Rescaled Adjusted Partial Sums)
                        - Trendlessness Test
                        - Homogenity Test (F-Test & t-Test)
                        - Inlier-Outlier Test
                        - Chi-Square Test
                        - Smirnov-Kolmogorov Test
                        - RMSE and MAPE Metrics
                    6. Download the results as a CSV file for further analysis
                    """)
        st.subheader("🧰 How to Use It:")
        st.markdown("""
                    1. Use the sidebar to input your rainfall data (annual maximum rainfall).
                    2. Explore the various analysis options available in the sidebar.
                    3. Follow the instructions in each section to perform the analysis.
                    4. Download the results as a CSV file for further analysis.
                    5. Enjoy the process and learn more about hydrology!
                    """)
    
    st.write("""
                ### 🚧 Trial Deployment Notice

                This is a **trial version** of the Rainfall Return Period Calculator, developed as part of an ongoing project to support better **water resources management in Indonesia**.  
                Currently, the app allows users to upload rainfall data and perform **probability distribution analysis**.

                🔧 **Future plans include**:
                - 🌧️ Adding **Losses Curve Number (SCS-CN) method**
                - 🌊 Generating **flow hydrographs**
                - 🚀 A **monetization model** (e.g. subscription access) to help sustain development and drive further innovation

                """)
    
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
    show_home()
