import streamlit as st
import pandas as pd
import numpy as np

from home_page import show_home
from data_eligibility_testing import show_module01
from probability_distribution_analysis import show_module02
from feedback import show_feedback

st.set_page_config(page_title="Amreta Project 0.1 (Beta)",
                   page_icon="💧",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                          "Report a bug": "https://forms.gle/QHY5EwsPw43LSQX18",
                          'About': """
                            This tool is born, raised, and developed in Indonesia, to support water resources engineering processes. 
                            For more info, contact herlambang19@gmail.com for any inquiries or project collaboration.
                          """}
                   )
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(140deg, #000000 50%, #00CED1 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", 
                                      "Data Eligibility Testing",
                                      "Probability Distribution Analysis",
                                      "Losses - Curve Number Method",
                                      "Flow Hydrograph",
                                      "Feedback & Bug Report"])
    if page == "Home":
        show_home()
    elif page == "Data Eligibility Testing":
        show_module01()
    elif page == "Probability Distribution Analysis":
        show_module02()
    elif page == "Losses - Curve Number Method":
        st.title("03 Losses - Curve Number Method")
        st.write("Curve Number Method is a hydrological model used to estimate direct runoff or infiltration from rainfall excess. This module is under development and will come in a full version!")
    elif page == "Flow Hydrograph":
        st.title("04 Flow Hydrograph")
        st.write("Flow Hydrograph is a graphical representation of the flow rate of water over time. This module is under development and will come in a full version!")
    elif page == "Feedback & Bug Report":
        show_feedback()
    st.sidebar.markdown("""
    ### 🙌 Support This Project
    If you find Amreta Project useful, feel free to support the development through Trakteer or PayPal:

    <a href="https://trakteer.id/mlasuikiuspi6so0mlvp/tip" target="_blank">
        <button style='padding:10px 20px;background-color:#FF4B4B;border:none;color:white;border-radius:8px;cursor:pointer;font-size:16px;margin-top:10px;'>🚀 Donate via Trakteer</button>
    </a>
    <a href="https://www.paypal.com/paypalme/ibfauzan" target="_blank">
        <button style='padding:10px 20px;background-color:#0070BA;border:none;color:white;border-radius:8px;cursor:pointer;font-size:16px;margin-top:10px;'>💳 Donate via PayPal</button>
    </a>
    """, unsafe_allow_html=True)



with st.sidebar:
    st.sidebar.title("Input")
    with st.expander("Rainfall Data"):
        start_year = st.number_input(
            "Starting Year:",
            min_value = 1900,
            max_value = 2100,
            value = 2010
        )
        end_year = st.number_input(
            "End Year:",
            min_value = 1900,
            max_value = 2100,
            value = 2025
        )

        if end_year <= start_year:
            st.warning("End year should be greater than Starting Year!")
        else:
            num_years = end_year - start_year + 1
            years = list(range(start_year, end_year + 1))
            st.write(f'Please input {num_years} values of annual maximum rainfall in each year')
            default_data = pd.DataFrame({
                'Year': years,
                'Annual Max': [None] * num_years
            })
            annual_input = st.data_editor(
                default_data, 
                num_rows="dynamic", 
                use_container_width=True,
                key="rainfall_input")
            
            if annual_input["Annual Max"].isnull().any():
                st.warning("Please fill in all rainfall values before submitting.")
            else:
                st.session_state.df = annual_input.copy()
                st.session_state.df["Annual Max"] = np.round(pd.to_numeric(st.session_state.df["Annual Max"], errors="coerce"),1)
                st.success("✅ Data has been submitted!")
                st.bar_chart(data=st.session_state.df, x='Year', y='Annual Max', y_label="Annual Max (mm)")
                    

if __name__ == "__main__":
    main()