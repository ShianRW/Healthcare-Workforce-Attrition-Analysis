# ==========================================
# OWNER: SHIAN RAVENEAU-WRIGHT
# ==========================================

# ==========================================
# SCRIPT SETUP & FILE IMPORT
# ==========================================

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import seaborn as sns

file_path = "C:\\Users\\shian\\Documents\\Data Analytics\\Data In Motion\\Milestone Projects\\Milestone #4\\watson_healthcare_modified2.csv"
df = pd.read_csv(file_path)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# ==========================================
# FILE COLUMNS LIST:
# ==========================================

atr = 'Attrition'                   # String - 'Yes / No'
dep = 'Department'                  # String
age = 'Age'                         # Int
gen = 'Gender'                      # String - 'Female / Male'
edu = 'Education'                   # Int - Ranking
rol = 'JobRole'                     # String
sat = 'JobSatisfaction'             # Int - Ranking
dis = 'DistanceFromHome'            # Int
bal = 'WorkLifeBalance'             # Int - Ranking
per = 'PerformanceRating'           # Int - Ranking
inc = 'MonthlyIncome'               # Int
yrs_com = 'YearsAtCompany'          # Int
yrs_pro = 'YearsSinceLastPromotion' # Int
yrs_rol = 'YearsInCurrentRole'      # Int
yrs_wrk = 'TotalWorkingYears'       # Int
tra = 'TrainingTimesLastYear'       # Int
ove = 'OverTime'                    # String - 'Yes / No'
num_com = 'NumCompaniesWorked'      # Int


# ==========================================
# HELPER FUNCTIONS
# ==========================================

# FORMAT AND PRINT % DATA FOR CATEGORICAL VARIABLES
def display_rates(series, title):
    print(title)
    print(series.map(lambda x: f"{x:.1f}%"))
    print('-' * 24)


# PRINT DESCRIPTIVE STATISTICS FOR NUMERICAL VARIABLES
def display_stats(dataframe, title):
    print(title)
    print(dataframe)
    print('-' * 24)


# CREATE AND FORMAT BAR CHART
def plot_bar_chart(
    data,
    title,
    xlabel,
    ylabel="Attrition Rate (%)",
    colors=["#0E8388"],
    max_color="#E2664B",
):
  plt.figure(figsize=(10, 8))

  bars = plt.bar(data.index.astype(str), data.values, color=colors)

  plt.title(title, fontweight="bold")

  plt.tick_params(left=False, bottom=False, labelleft=False)

  plt.ylim(0, max(data.values) + 5)

  for bar in bars:
    height = bar.get_height()
    if height == max(data.values):
      bar.set_color(max_color)

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.1f}%",
        ha="center",
        va="bottom",
    )
  plt.tight_layout()


# CREATE AND FORMAT BOX PLOT
def plot_box_plot(x_data, y_data, title, ylabel, df_source=None):
    plt.figure(figsize=(10, 6))
    
    sns.boxplot(
        x=x_data, y=y_data, data=df_source, 
        palette=['#0E8388','#E2664B'], width=0.4, showmeans=True, 
        meanprops={
            "marker": "D", "markerfacecolor": "orange",
            "markeredgecolor": "black", "markersize": 8
        }
    )
    
    plt.title(title,fontweight='bold')
    plt.ylabel(ylabel,fontweight='bold')
    plt.xticks(ticks=[0, 1], labels=['Retained', 'Attrited'])
    
    plt.tick_params(bottom=False)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    mean_marker = mlines.Line2D(
        [], [], color='none', marker='D', markerfacecolor='orange', 
        markeredgecolor='black', markersize=8, label='Mean'
    )
    plt.legend(handles=[mean_marker], loc='upper right')
    plt.tight_layout()


# CREATE AND FORMAT LINE GRAPH
def plot_line_graph(data, title, xlabel, ylabel='Attrition Rate (%)', color='#E2664B'):
    plt.figure(figsize=(10, 4))
    x = data.index.values
    y = data.values

    plt.plot(x, y, marker='o', linestyle='-', color=color, linewidth=2.5, markersize=6)

    for xi, yi in zip(x, y):
        plt.text(
            xi, yi + 1.2, f"{yi:.1f}%", ha='center', va='bottom', fontsize=8, color='black',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='lightgray', alpha=0.8)
        )

    plt.title(title, fontweight='bold')
    plt.xlabel(xlabel)

    plt.tick_params(left=False, bottom=False, labelleft=False)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.ylim(0, max(y) + 10)
    plt.tight_layout()


#CREATE AND FORMAT PIE CHART
def plot_pie_chart(df_source, target_col, atr_col, title, colors):

    leavers_only = df_source[df_source[atr_col] == 1]
    data = leavers_only[target_col].value_counts().sort_index()
    
    plt.figure(figsize=(10, 10))
    plt.pie(
        data.values, labels=data.index, autopct='%1.1f%%', 
        startangle=90, colors=colors, textprops={'fontweight': 'bold'}
    )
    plt.title(title, fontweight='bold')
    plt.axis('equal') 
    plt.tight_layout()

# ==========================================
# ATTRITION ANALYSIS
# ==========================================

#------------------------------------------------------
# TOTAL NUMBER OF EMPLOYEES & OVERALL ATTRITION RATES
#------------------------------------------------------

df[atr] = (df[atr] == 'Yes').astype(int)

total_employees = len(df)
leavers = df[atr].sum()
stayers = total_employees - leavers
atr_rate = df[atr].mean() * 100 

print('-' * 24)
print(f'Total number of employees: {total_employees}')
print('-' * 24)
print(f'Overall attrition rate: {atr_rate:.1f}%')
print('-' * 24)
print(f'Total number of employees who left: {leavers}')
print(f'Total number of employees who stayed: {stayers}')
print('-' * 24)

#----------------------------------------
# CATEGORICAL ATTRITION RATES (mean())
#----------------------------------------

# DEPARTMENT
atr_dep = df.groupby(dep)[atr].mean() * 100
display_rates(atr_dep, 'Attrition rate by department:')

# GENDER
atr_gen = df.groupby(gen)[atr].mean() * 100
display_rates(atr_gen, 'Attrition rate by gender:')

# EDUCATION LEVEL
atr_edu = df.groupby(edu)[atr].mean() * 100
display_rates(atr_edu, 'Attrition rate by education level:')

# JOB ROLE
custom_order = ['Admin', 'Administrative', 'Nurse', 'Therapist', 'Other']
atr_rol = df.groupby(rol)[atr].mean().reindex(custom_order) * 100 
display_rates(atr_rol, 'Attrition rate by job role:')

# JOB SATISFACTION SCORE
atr_sat = df.groupby(sat)[atr].mean() * 100
display_rates(atr_sat, 'Attrition rate by job satisfaction score:')

# WORK LIFE BALANCE
atr_bal = df.groupby(bal)[atr].mean() * 100
display_rates(atr_bal, 'Attrition rate by work life balance score:')

# PERFORMANCE RATING
atr_per = df.groupby(per)[atr].mean() * 100
display_rates(atr_per, 'Attrition rate by performance rating:')

# TRAINING TIMES LAST YEAR
atr_tra = df.groupby(tra)[atr].mean() * 100
display_rates(atr_tra, 'Attrition rate by training times last year (hrs):')

# OVERTIME
atr_ove = df.groupby(ove)[atr].mean() * 100
display_rates(atr_ove, 'Attrition rate by overtime:')

# NUMBER OF COMPANIES WORKED AT
atr_num_com = df.groupby(num_com)[atr].mean() * 100
display_rates(atr_num_com, 'Attrition rate by number of companies worked at:')

#----------------------------------------
# NUMERICAL ATTRITION STATS (describe())
#----------------------------------------

rename_dict = {0: 'Stayed', 1: 'Left'}

# DISTANCE FROM HOME
atr_dis = df.groupby(atr)[dis].describe().rename(index=rename_dict)
display_stats(atr_dis, 'Attrition rate by distance from home:')

# AGE
atr_age = df.groupby(atr)[age].describe().rename(index=rename_dict)
display_stats(atr_age, 'Attrition by age:')

# MONTHLY INCOME
atr_inc = df.groupby(atr)[inc].describe().rename(index=rename_dict)
display_stats(atr_inc, 'Attrition by monthly income ($):')

# YEARS AT COMPANY
atr_yrs_com = df.groupby(atr)[yrs_com].describe().rename(index=rename_dict)
display_stats(atr_yrs_com, 'Attrition by years at company:')

# YEARS SINCE LAST PROMOTION
atr_yrs_pro = df.groupby(atr)[yrs_pro].describe().rename(index=rename_dict)
display_stats(atr_yrs_pro, 'Attrition by years since last promotion:')

# YEARS IN CURRENT ROLE
atr_yrs_rol = df.groupby(atr)[yrs_rol].describe().rename(index=rename_dict)
display_stats(atr_yrs_rol, 'Attrition by years in current role:')

# TOTAL WORKING YEARS
atr_yrs_wrk = df.groupby(atr)[yrs_wrk].describe().rename(index=rename_dict)
display_stats(atr_yrs_wrk, 'Attrition by total working years:')


# ==========================================
# CHART GENERATION
# ==========================================

# FONT FORMATTING
plt.rcParams.update({
    'font.size': 14,  # General text & data labels
    'axes.titlesize': 18,  # Chart titles
    'axes.labelsize': 14,  # Axis labels (x and y)
    'xtick.labelsize': 13,  # X-axis tick labels
    'ytick.labelsize': 13,  # Y-axis tick labels
})


# ATTRITION RATE BY DEPARTMENT - BAR CHART
plot_bar_chart(atr_dep, 'Attrition Rate by Department', 'Department')

# ATTRITION RATE BY AGE - BOX PLOT
plot_box_plot(atr, age, 'Attrition by Age', 'Age (yrs)', df_source=df)

# ATTRITION RATE BY GENDER - BAR CHART
plot_bar_chart(atr_gen, 'Attrition Rate by Gender', 'Gender',['#1da38f','#1F3A5F'])

# ATTRITION SPLIT BY GENDER - PIE CHART
plot_pie_chart(df, gen, atr, 'Attrition Split by Gender',['#1da38f','#1F3A5F'])

# ATTRITION RATE BY EDUCATION LEVEL - BAR CHART
plot_bar_chart(atr_edu, 'Attrition Rate by Education Level', 'Education Level')

# ATTRITION RATE BY JOB ROLE - BAR CHART
plot_bar_chart(atr_rol, 'Attrition Rate by Job Role', 'Job Role')

# ATTRITION RATE BY JOB SATISFACTION SCORE - BAR CHART
plot_bar_chart(atr_sat, 'Attrition Rate by Job Satisfaction Score', 'Job Satisfaction Score')

# ATTRITION SPLIT BY JOB SATISFACTION SCORE - PIE CHART
plot_pie_chart(df, sat, atr, 'Attrition Split by Job Satisfaction Score', ['#1F3A5F','#0E8388','#1da38f','#6CA0C0'])

# ATTRITION RATE BY DISTANCE FROM HOME - BOX PLOT
plot_box_plot(atr, dis, 'Attrition Rate by Distance from Home', 'Distance from Home (miles)', df_source=df)

# ATTRITION RATE BY DISTANCE FROM HOME - LINE GRAPH
atr_dis_rate = df.groupby(dis)[atr].mean() * 100
plot_line_graph(atr_dis_rate, ' Avg Attrition Rate by Distance from Home', 'Distance from Home (miles)')

# ATTRITION RATE BY WORK LIFE BALANCE SCORE - BAR CHART
plot_bar_chart(atr_bal, 'Attrition Rate by Work Life Balance Score', 'Work Life Balance Score')

# ATTRITION SPLIT BY WORK LIFE BALANCE SCORE - PIE CHART
plot_pie_chart(df, bal, atr, 'Attrition Split by Work Life Balance Score', ['#1F3A5F','#0E8388','#1da38f','#6CA0C0'])

# ATTRITION RATE BY EMPLOYEE PERFORMANCE RATING - BAR CHART
plot_bar_chart(atr_per, 'Attrition Rate by Employee Performance Rating', 'Employee Performance Rating')

# ATTRITION RATE BY MONTHLY INCOME - BOX PLOT
plot_box_plot(atr, inc, 'Attrition Rate by Monthly Income', 'Income ($)', df_source=df)

# ATTRITION RATE BY YEARS AT COMPANY - BOX PLOT
plot_box_plot(atr, yrs_com, 'Attrition Rate by Years at Company', 'Years at Company', df_source=df)

# ATTRITION RATE BY YEARS SINCE LAST PROMOTION - BOX PLOT
plot_box_plot(atr, yrs_pro, 'Attrition by Years Since Last Promotion', 'Years Since Last Promotion', df_source=df)

# ATTRITION RATE BY YEARS IN CURRENT ROLE - BOX PLOT
plot_box_plot(atr, yrs_rol, 'Attrition by Years in Current Role', 'Years in Current Role', df_source=df)

# ATTRITION RATE BY TOTAL WORKING YEARS - BOX PLOT
plot_box_plot(atr, yrs_wrk, 'Attrition by Total Working Years', 'Total Working Years', df_source=df)

# ATTRITION RATE RATE BY OVERTIME WORKED - BAR CHART
plot_bar_chart(atr_ove, 'Attrition Rate by Overtime Worked (Yes/No)', 'Overtime Worked')

# ATTRITION SPLIT BY OVERTIME WORKED - PIE CHART
plot_pie_chart(df, ove, atr, 'Attrition Split by Overtime Worked', ['#0E8388','#E2664B'])

# ATTRITION RATE BY NUMBER OF OTHER COMPANIES WORKED AT - BAR CHART
plot_bar_chart(atr_num_com, 'Attrition Rate by Number of Other Companies Worked at', 'Number of Companies Worked at')

# ATTRITION RATE BY TRAINING TIMES LAST YEAR - BAR CHART
plot_bar_chart(atr_tra, 'Attrition Rate by Total Training Hours Last Year', 'Total Training Hours Last Year')

# SHOW ALL
plt.show()