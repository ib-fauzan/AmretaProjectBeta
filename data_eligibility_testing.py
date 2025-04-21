import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.stats import t
from scipy.stats import f
import scipy.stats as stats

def show_module01():
    st.title("01 Data Eligibility Testing")
    st.subheader("Purpose")
    st.write('''
             To ensure hydrological data (rainfall, streamflow, etc.) 
             meets quality standards for analysis and modeling.
             ''')
    
    ### RAPS TEST ####
    
    with st.expander('A. RAPS (Rescaled Adjusted Partial Sums)'):
        st.subheader("RAPS (Rescaled Adjusted Partial Sums)")
        st.caption("is a statistical method for identifying changes in trend or stationarity in time series data.")
        if st.button("Calculate!",key="calculate_raps"):
            with st.spinner("Calculating...⏳"):
                time.sleep(1)
                st.success("Calculation completed! ✅")
                st.write("The result:")
                def RAPS (df):
                    df_raps = df.copy()
                    n = len(df_raps)
                    sum_data = np.sum(df_raps['Annual Max'])
                    mean_data = np.mean(df_raps['Annual Max'])
                    std_data = np.std(df_raps['Annual Max'])

                    df_raps['sk*'] = df_raps['Annual Max'] - mean_data
                    df_raps['sk**'] = df_raps['sk*']/std_data
                    df_raps['|sk**|'] = np.abs(df_raps['sk**'])

                    sk_min = np.min(df_raps['sk**'])
                    sk_max = np.max(df_raps['sk**'])
                    R = sk_max - sk_min
                    Q = np.max(df_raps['|sk**|'])

                    Q_per_n = round(Q/(n**0.5),3)
                    R_per_n = round(R/(n**0.5),3)

                    N_values = np.array([10, 20, 30, 40, 50, 100, np.inf])
                    Q95_values = np.array([1.14, 1.22, 1.24, 1.26, 1.27, 1.29, 1.36])  # example for 95% control
                    R95_values = np.array([1.28, 1.43, 1.5, 1.53, 1.55, 1.62, 1.75])

                    Q95_bnd = np.interp(n, N_values, Q95_values)
                    R95_bnd = np.interp(n, N_values, R95_values)

                    if Q_per_n < Q95_bnd:
                        st.write(f'Q/n = {Q_per_n} < Q95 Max = {Q95_bnd} (95%) ACCEPTED ✅')
                    else:
                        st.write(f'Q/n = {Q_per_n} > Q95 Max = {Q95_bnd} (95%) NOT ACCEPTED ❌')

                    if R_per_n < R95_bnd:
                        st.write(f'R/n = {R_per_n} < R95 Max = {R95_bnd} (95%) ACCEPTED ✅')
                    else:
                        st.write(f'R/n = {R_per_n} > R95 Max = {R95_bnd} (95%) NOT ACCEPTED ❌')
                    
                    # Step 1: Average & Standard Deviation
                    sigma = np.std(df_raps['Annual Max'], ddof=1)

                    # Step 2: Calculate S_k (Adjusted Partial Sum)
                    S_k = np.cumsum(df_raps['sk*'])

                    # Step 3: Calculate RAPS
                    R_k = S_k / sigma
                    
                    plot_data_raps = pd.DataFrame({
                        'Year/Time': df_raps.index,
                        'RAPS': R_k,
                        'zero line':0
                    }).set_index('Year/Time')
                    
                    st.line_chart(plot_data_raps[['RAPS','zero line']],x_label="Year/Time",y_label='RAPS',color=["#0000FF","#FF0000"])
                    
                    tableraps = st.dataframe(
                        df_raps
                    )
                RAPS(st.session_state.df)
    ### TRENDLESSNESS TEST ####
    with st.expander('B. Trendlessness Test'):
        st.subheader("Trendlessness Test")
        st.caption("is a statistical method to test whether a time series has a trend or not.")
        st.caption('Test decision:')
        st.caption('If t-statistic < t-critical → Trendlessness ACCEPTED (no significant trend)')
        st.caption('If t-statistic > t-critical → Trend NOT ACCEPTED (trend detected)')

        if st.button("Calculate!",key ="calculate_trendless"):
            with st.spinner("Calculating..."):
                time.sleep(1)
                st.success("Calculation completed! ✅")
                st.write("The result:")
                def Trendlessness (df):
                    df_trendless = df.copy()
                    n = len(df)
                    df_trendless['rank'] = range(1, len(df_trendless) + 1)
                    df_trendless['rainfall_ranking'] = sorted(df_trendless['Annual Max'],reverse=True)
                    df_trendless['Rt'] = df_trendless['rainfall_ranking'].map(df_trendless.set_index('Annual Max')['rank'])
                    df_trendless['dt2'] = (df_trendless['rank'] - df_trendless['Rt'])**2
                    count = df_trendless['dt2'].sum()
                    kp = 1-((6*count)/((n**3)-n))
                    t_stat = round(kp*(np.sqrt((n-2)/(1-(kp**2)))),3)

                    ddof = n - 2 # Degrees of Freedom
                    alpha = 0.05 # level of significance

                    t_critical = round(t.ppf(1-(alpha/2),ddof),3)

                    if t_stat < t_critical:
                        st.write(f't = {t_stat} < tc = {t_critical} (5%) Trendlessness = ACCEPTED ✅')
                    else:
                        st.write(f't = {t_stat} > tc = {t_critical} (5%) Trend = NOT ACCEPTED ❌')
                    
                    df_trendlessness = st.dataframe(df_trendless)
                    return None
                Trendlessness(st.session_state.df)
                
    ## HOMOGENITY TEST ####
    with st.expander('C. Homogenity Test (F-Test & t-test)'):
        st.caption('To compare variances between two datasets and determine if they are statistically similar')
        if st.button("Calculate!",key="calculate_homogenity"):
            with st.spinner("Calculating...⏳"):
                time.sleep(1)
                st.success("Calculation completed! ✅")
                def Homogen_test (df):
                    df_homogen = df.copy()
                    n = len(df_homogen)
                    n_half = int(n/2)
                    N1 = df_homogen['Annual Max'][:n_half]
                    N2 = df_homogen['Annual Max'][n_half:]
                    n_N1 = len(N1)
                    n_N2 = len(N2)
                    avg_N1 = np.mean(N1)
                    avg_N2 = np.mean(N2)
                    std_N1 = np.std(N1)
                    std_N2 = np.std(N2)
                    ddof_1 = n_N1 - 1
                    ddof_2 = n_N2 - 1

                    alpha = 0.05 # level of significance

                    # F-Test
                    F_stat = round((np.var(N1)/np.var(N2)),3)
                    F_critical = round(f.ppf(1-(alpha/2),n_N1,n_N2),3)
                    if F_stat < F_critical:
                        st.write(f'F stat = {F_stat} < F critical = {F_critical} (5%) ACCEPTED ✅')
                        st.write('The dataset are homogeneous')
                    else:
                        st.write(f'F stat = {F_stat} > F critical = {F_critical} (5%) NOT ACCEPTED ❌')
                        st.write('The dataset are not homogeneous')

                    # t-test
                    sigma = np.sqrt(((n_N1*std_N1**2)+(n_N2*std_N2**2))/(n_N1+n_N2-2))
                    t_stat = round((avg_N1-avg_N2)/((sigma*np.sqrt(1/n_N1+1/n_N2))),3)
                    ddof_df = n_N1 + n_N2 - 2
                    t_critical = round(t.ppf(1-(alpha/2),ddof_df),3)
                    if t_stat < t_critical:
                        st.write(f't stat = {t_stat} < t critical = {t_critical} (5%) ACCEPTED ✅')
                        st.write('The dataset are homogeneous')
                    else:
                        st.write(f't stat = {t_stat} > t critical = {t_critical} (5%) NOT ACCEPTED ❌')
                        st.write('he dataset are not homogeneous')
                Homogen_test(st.session_state.df)
    
    ### INLIER-OUTLIER TEST ####
    with st.expander('D. Inlier-Outlier Test'):
        st.caption("Identify data points that deviate abnormally from the dataset's pattern.")
        st.write("""
                 Note: The test highlights potential anomalies but 
                 requires domain knowledge to determine if exclusion is justified.
                 """)
        
        if st.button("Calculate!",key="calculate_outlier"):
            with st.spinner("Calculating...⏳"):
                time.sleep(1)
                st.success("Calculation completed! ✅")
                def Outlier_test (df):
                    df_outlier = df.copy()
                    n = len(df_outlier)
                    df_outlier['ln x'] = round(np.log(df_outlier['Annual Max']),2)
                    avg_ln = np.mean(df_outlier['ln x'])
                    skew_ln = df_outlier['ln x'].skew()
                    std_ln = np.std(df_outlier['ln x'])
                    # Given
                    n_data = [
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                        24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50,
                        60, 70, 80, 90, 100, 120, 140
                    ]
                    # Given
                    kn_values = [
                        2.036, 2.080, 2.134, 2.178, 2.213, 2.247, 2.279, 2.309, 2.338, 2.365,
                        2.390, 2.415, 2.438, 2.467, 2.468, 2.502, 2.532, 2.560, 2.586, 2.610,
                        2.661, 2.682, 2.701, 2.719, 2.736, 2.750, 2.804,
                        2.837, 2.867, 2.893, 2.918, 2.940, 3.078, 3.129
                    ]

                    Kn = np.interp(n, n_data, kn_values)
                    Xh = round(np.exp(avg_ln+Kn*std_ln),1)
                    Xl = round(np.exp(avg_ln-Kn*std_ln),1)
                    
                    # Save to session_state
                    
                    st.session_state.Xh = Xh
                    st.session_state.Xl = Xl
                    st.session_state.df_outlier = df_outlier
                    st.session_state.above_upper_bound = df_outlier[df_outlier['Annual Max'] > Xh]
                    st.session_state.below_lower_bound = df_outlier[df_outlier['Annual Max'] < Xl]
                    

                    st.write("\nData above the upper limit (Xh):", st.session_state.above_upper_bound)
                    st.write("\nData below the lower limit (Xl):", st.session_state.below_lower_bound)
                    st.dataframe(st.session_state.df_outlier)
                Outlier_test(st.session_state.df)
    
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
    show_module01()