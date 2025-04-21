import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

import scipy.stats as stats
from scipy.stats import chi2
from scipy.stats import kstest
from sklearn.metrics import root_mean_squared_error, mean_absolute_percentage_error

def show_module02():
    st.title("02 Probability Distribution Analysis")
    st.subheader("Purpose")
    st.write('''
            Probability Distribution Analysis is a fundamental statistical method in hydrology used to model extreme events such as flood discharge by estimating likelihood and predicting return period
            (e.g. a "100-year return period"). This approach quantifies uncertainty by assessing the probability of various hydrological outcomes. There are several theoretical distributions, including
            Normal, Log Normal, Pearson III, Log Pearson III, and Gumbel, to determine the best predictive model.
            ''')

    df = st.session_state.get("df",None)
    if df is not None:
        options = [2,5,10,25,50,100,200,500,1000]
        return_periods = st.pills("Return Periods:", options, selection_mode="multi")

        return_periods = np.array(return_periods, dtype=float)
        probability = 1 - (1/return_periods)
        with st.expander("Table and Generation Graph "):
            st.subheader('Visualization and Table of Distribution')
            def probability_distribution_analysis(df):
                # Normal Distribution
                avg_rain, std_rain = np.mean(df['Annual Max']), np.std(df['Annual Max'])
                norm_values = stats.norm.ppf(probability, loc=avg_rain, scale=std_rain)
                # Log Normal Distribution
                log_df = np.log(df['Annual Max'])
                log_avg_rain, log_std_rain = np.mean(log_df), np.std(log_df)
                log_norm_values = np.exp(stats.norm.ppf(probability, loc=log_avg_rain, scale=log_std_rain))
                # Pearson III Distribution
                skewness = stats.skew(df['Annual Max'])
                pearson3_values = stats.pearson3.ppf(probability, skew=skewness, loc=avg_rain, scale=std_rain)
                # Log Pearson III Distribution
                skewness_log = stats.skew(log_df)
                log_pearson3_values = np.exp(stats.pearson3.ppf(probability, skew=skewness, loc=log_avg_rain, scale=log_std_rain))
                # Gumbel Distribution
                gumbel_values1 = stats.gumbel_r.ppf(probability, loc=avg_rain, scale=std_rain) # Gumbel in General Statistics
                gumbel_values2 = avg_rain + (std_rain * 0.7797) * ((-np.log(-np.log(1 - 1 / return_periods)) - 0.5772)) # Gumbel calculated based on the Gumbel formula for hydrology
            
                # DataFrame
                result = pd.DataFrame({
                    'Return Period (y)': return_periods,
                    'Normal': norm_values,
                    'Log-Normal': log_norm_values,
                    'Pearson III': pearson3_values,
                    'Log-Pearson III': log_pearson3_values,
                    'Gumbel 1': gumbel_values1,
                    'Gumbel 2': gumbel_values2
                })
                result = result.round(1)
                st.session_state.result = result
                
                st.line_chart(st.session_state.result, x = "Return Period (y)",
                        y=["Normal","Log-Normal","Pearson III","Log-Pearson III","Gumbel 1","Gumbel 2"],
                        y_label="Return Period Rainfall (mm)")
            probability_distribution_analysis(st.session_state.df)
            st.dataframe(st.session_state.result)
            
        with st.expander("Based Calculation & Probability Plot"):
            st.subheader("Based Distribution Data Frame & Graph:")
            st.write("Data Frame")
            def based_distribution (df):
                df_temp = df.copy()
                df_temp = df_temp.drop(columns=['Year'])
                df_temp = df_temp.sort_values(by='Annual Max',ascending=False).reset_index(drop=True)
                df_temp['rank'] = range(1,len(df_temp)+1)
                df_temp['p'] = round(1-df_temp['rank']/(len(df_temp)+1),4)
                df_temp['T'] = ((len(df_temp) + 1) / df_temp['rank']).round(2)

                avg_rain, std_rain, log_avg, log_std_rain, skewness, skewness_log= (
                    np.mean(df_temp['Annual Max']), np.std(df_temp['Annual Max']),
                    np.mean(np.log(df_temp['Annual Max'])), np.std(np.log(df_temp['Annual Max'])),
                    stats.skew(df_temp['Annual Max']), stats.skew(np.log(df_temp['Annual Max']))
                )

                df_temp['Normal'] = stats.norm.ppf(df_temp['p'], loc=avg_rain, scale=std_rain).round(1)
                df_temp['Log Normal'] = np.exp(stats.norm.ppf(df_temp['p'], loc=log_avg, scale=log_std_rain)).round(1)
                df_temp['Pearson 3'] = stats.pearson3.ppf(df_temp['p'], skew=skewness, loc=avg_rain, scale=std_rain).round(1)
                df_temp['Log Pearson 3'] = np.exp(stats.pearson3.ppf(df_temp['p'], skew=skewness_log, loc = log_avg, scale = log_std_rain)).round(1)
                df_temp['Gumbel 1'] = stats.gumbel_r.ppf(df_temp['p'], loc=avg_rain, scale=std_rain).round(1)
                df_temp['Gumbel 2'] = (avg_rain + (std_rain * 0.7797) * ((-np.log(-np.log(1 - 1/df_temp['T'])) - 0.5772))).round(1)
                
                st.session_state.df_temp = df_temp
                st.dataframe(st.session_state.df_temp)

                # Histogram of Distribution
                print('Graph of Distribution\n')
                bins_number = 10
                st.session_state.distributions = ['Annual Max', 'Normal', 'Log Normal', 'Pearson 3', 'Log Pearson 3', 'Gumbel 1', 'Gumbel 2']
                st.session_state.markers = ['o','s','^','v','D','p','*']
                st.session_state.linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (1, 1))]
                
                st.write('Histogram')

                # X Scale
                x_min = min([df_temp[dist].min() for dist in st.session_state.distributions])
                x_max = max([df_temp[dist].max() for dist in st.session_state.distributions])

                # Y Scale
                max_counts = []
                for dist in st.session_state.distributions:
                    counts, _ = np.histogram(df_temp[dist], bins=bins_number)
                    max_counts.append(counts.max())
                y_max = max(max_counts)

                cols = 3
                rows = (len(st.session_state.distributions) + 2) // cols

                fig, axes = plt.subplots(rows, cols, figsize=(8, 3 * rows))

                axes = axes.flatten() if len(st.session_state.distributions) > 1 else [axes]

                for i, dist in enumerate(st.session_state.distributions):
                    sns.histplot(df_temp[dist], bins=bins_number, kde=True, color='skyblue', edgecolor='black', ax=axes[i])
                    axes[i].set_title(f'Distribution: {dist}')
                    axes[i].set_xlabel('Value')
                    axes[i].set_ylabel('Frequency')
                    axes[i].set_xlim(x_min, x_max)
                    axes[i].set_ylim(0, y_max)

                for j in range(i+1, len(axes)):
                    fig.delaxes(axes[j])

                fig.tight_layout()
                st.pyplot(fig)
            based_distribution(st.session_state.df)    
            
            st.write("Distribution Plot")
            fig, ax = plt.subplots(figsize=(10, 6))
            for dist, marker, ls in zip(st.session_state.distributions, st.session_state.markers, st.session_state.linestyles):
                ax.plot(st.session_state.df_temp[dist], st.session_state.df_temp['p'], label=dist,
                        marker=marker, linestyle=ls, linewidth=1.5, markersize=6)
            ax.set_xlabel('Rainfall (mm)')
            ax.set_ylabel('Exceedance Probability (1 - P)')
            ax.set_title('Rainfall Frequency Analysis: Probability Plot')
            ax.set_xlim(0, np.max(st.session_state.df_temp[st.session_state.distributions].max())+20)
            ax.set_ylim(0, 1)
            ax.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)
            ax.legend()
            st.pyplot(fig)
    else:
        st.warning("Please input the annual maximum rainfall data in the sidebar to proceed with the Probability Distribution Analysis.")
    
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
    show_module02()