"""
Assignment 2 Programming 3
Data Sciences for Life Sciences
Author: Daan Steur
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
from tabulate import tabulate

class exploration:

    def data_exploration_csv(self):
        # Set console printing options 
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 20)
        pd.set_option('display.width', 1000)

        # Upload the data
        df = pd.read_csv(self, sep=",", decimal=".", keep_default_na=False, na_values='', index_col=0)

        # Column indices of selected continuous variables
        cols_continuous = [1,2,3,4,5,6,7,8,9,10,11]
        # Data frame of the continuous variables
        df_num = df.iloc[:,cols_continuous]
        # Column indices of selected discrete variables
        cols_discrete = [0,12]
        # Data frame of the discrete variables
        df_cat = df.iloc[:,cols_discrete]
        # Continuous variables, descriptive statistics
        df_num.sort_index(axis=1, inplace=True, key=lambda x: x.str.lower())
        df_num_stats = df_num.describe()
        df_num_stats = df_num_stats.transpose()
        df_num_stats.drop(columns=['25%', '75%'], inplace=True)
        df_num_stats.rename(columns={"count": "N Valid", "mean": "Mean", "50%": "Median", 
                                    "std": "SD", "min": "Min", "max": "Max"}, inplace=True)
        df_num_stats["N Obs"] = df_num.shape[0]
        df_num_stats["N Missing"] = df_num.isna().sum()
        df_num_stats["% Complete"] = (df_num_stats["N Valid"] / df_num_stats["N Obs"])*100
        df_num_stats["N Unique"] = df_num.nunique(dropna=True)
        df_num_stats["MAD"] = df_num.apply(lambda x: stats.median_abs_deviation(x, scale="normal", nan_policy='omit'))
        df_num_stats["Skewness"] = df_num.skew(axis=0)
        df_num_stats["Kurtosis"] = df_num.kurtosis(axis=0)
        df_num_stats.loc[df_num_stats["Min"]>0,"CV"] = df_num_stats["SD"] / df_num_stats["Mean"]
        df_num_stats = df_num_stats.round(2)
        df_num_stats.loc[df_num_stats["Min"]<=0,"CV"] = ""

        ## Reorder columns to be similar to the output of the R app 
        df_num_stats = df_num_stats.reindex(columns=["N Obs", "N Missing", "N Valid", 
                                                    "% Complete", "N Unique", "Mean", 
                                                    "SD", "Median", "MAD", "Min", "Max", 
                                                    "Skewness", "Kurtosis", "CV"]) 

        ## Restrict size of characters of index 
        cnames = np.array(df_num_stats.index).astype('str')
        csize = min(np.max(np.char.str_len(cnames)),25)
        df_num_stats.index = list(map(lambda x: x[:csize], cnames))

        ## Output
        print(tabulate(df_num_stats, headers='keys', tablefmt="simple"))
        
    def Categorical_Variables_csv(self):
        #Pre_processing
        # Set console printing options 
        pd.set_option('display.max_rows', 5000)
        pd.set_option('display.max_columns', 200)
        pd.set_option('display.width', 10000)

        # Upload the data
        df = pd.read_csv(self, sep=",", decimal=".", keep_default_na=False, na_values='', index_col=0)


        # Column indices of selected continuous variables
        cols_continuous = [1,2,3,4,5,6,7,8,9,10,11]
        # Data frame of the continuous variables
        df_num = df.iloc[:,cols_continuous]
        # Column indices of selected discrete variables
        cols_discrete = [0,12]
        # Data frame of the discrete variables
        df_cat = df.iloc[:,cols_discrete]

        ## Table Totals 
        nobs = np.ones(df_cat.shape[1])*df_cat.shape[0]
        nobs = nobs.astype(int)
        df_cat.sort_index(axis=1, inplace=True, key=lambda x: x.str.lower())
        df_cat = df_cat.astype("string")
        df_cat_stats = pd.DataFrame(nobs, columns=['N Obs'], index=df_cat.columns)
        df_cat_stats["N Missing"] = df_cat.isna().sum()
        df_cat_stats["N Valid"] = df_cat.count()
        df_cat_stats["% Complete"] = (df_cat_stats["N Valid"] / df_cat_stats["N Obs"])*100
        df_cat_stats["N Unique"] = df_cat.nunique(dropna=False)
        df_cat_stats = df_cat_stats.round(2)

        ### Restrict size of characters of index 
        cnames = np.array(df_cat_stats.index).astype('str')
        csize = min(np.max(np.char.str_len(cnames)),25)
        df_cat_stats.index = list(map(lambda x: x[:csize], cnames))

        ### Output
        print(tabulate(df_cat_stats, headers='keys', tablefmt="simple"))