#%% [markdown]

# # Scikit-Learn: Complete Walk-Through (for R Users)
#  
# Python is one if not the most used language by data scientists interested in machine learning and deep learning techniques.
# 
# One reason for Python's popularity is without a doubt `scikit-learn`. `scikit-learn` does not need an introduction, but in case you are new to the machine learning space in Python, `scikit-learn` is an all-in-one machine learning library for Python that implements most machine learning techniques you will need in daily use and provides a consistent api and a framework to work with.
#
# As the name of the post implies, this walk-through is partially intended for users coming from R who already have experience with one or both versions of `scikit-learn` in the R world, namely [caret](https://topepo.github.io/caret/) and [mlr3](https://github.com/mlr-org/mlr3).
# 
# So without further ado, let's get started :)
# 
# ## Survial Chances on the Titanic
#
# For this walk-through I will use of the most widely used datasets in machine learning: the titanic dataset.
#
# Firstly, because it's a classic, but more importantely, it is small, readily available and has both numeric, string and missing features. If you want to follow along, you can find the dataset [here](https://www.openml.org/d/40945).

# %%
# Load autoreload module 
# autoreload 1: reload modules imported with %aimport everytime before execution
# autoreload 2: reload all modules
%load_ext autoreload
%autoreload 2
# %%
# Import Libs
import os
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
# %%
# # Import dataset
df_titanic = pd.read_csv("../../data/titanic.csv", sep=",", na_values="?")
df_titanic.head()
# %% [markdown]
# 
# So, now that we have our dataframe let's take a quick look at some summary statistics and plots:

# %%
df_titanic.dtypes
# %%
# Note: by default, only numeric attributes are described and NaN values excluded!
df_titanic.describe()
# %%
df_titanic.describe(include=[object])
# %%
# Check for NaN values per column
df_titanic.isnull().sum()

# %%
px.histogram(df_titanic, x="age", color = "survived",title="Histogram of Age by Survial")
# %%
# Since pandas >0.25 you can aggregate and rename columns in one go:
df_gd = df_titanic.groupby(["sex"], as_index=False). \
                    agg(
                        n_survived=("survived", "sum"),
                        n_sex=("sex", "count")
                       )
# I really like plotly.express, but unfortunately it is not as powerful as ggplot yet
# Converting between discrete and numeric colors for example can only be done by recoding the
# underlying column (https://plotly.com/python/discrete-color/)
df_gd['prop_survived'] = df_gd.n_survived/df_gd.n_sex
px.bar(df_gd, x = "sex", y="prop_survived", title="Survival Probability by Gender")
# %% [markdown]
#
# So, from these initial plots it seems that being male does not really help your survival chances. Now that we have a rough idea how the dataset looks like, let's start preparing the data for modeling.

# %% [markdown]
# ## Data Preparation
#
# Unlike R, Python does not have a dataframe as a native data structure which was later provided by the [pandas](https://github.com/pandas-dev/pandas) library and nowadays also by [datatable](https://github.com/h2oai/datatable). However, when scikit-learn was originally designed in 2007, pandas was not available yet (pandas was first released in 2008). This is probably one of the main reasons why scikit-learn takes some getting used to for R converts who are used to working with dataframes, because scikit-learn expects all inputs in the form of numpy-arrays (though it will automatically convert dataframes as long as they contain only numeric data). 
# 
# Practically, this used to be a bit of a headache, when you had to work with categorial string data as you needed to transform strings into a numeric representation manually. As a result, there are lots and lots of different tutorials online how to best convert strings to work with scikit-learn.
#
# I will show one way based on pandas and one using scikit-learn. But let's get rid of some columns first. Passenger name, ticket number and home.dest might be slightly correlated to survivial, but probably not. I don't know what "boat" and "body" represent and could not find it in the docs, so to make sure we are not accidentally including feature leaks, such as which life boat a person was on, better exclude them. 
# %%
df_titanic.drop(["name", "ticket", "boat", "body", "home.dest"], axis=1, inplace=True)
# %%
# Let's grab only the deck part of the cabin to simplify things:
df_titanic['cabin'] = df_titanic.cabin.astype(str)
df_titanic['cabin'] = df_titanic.cabin.apply(lambda s: s[0])

# cat_vars = df_titanic.columns[df_titanic.dtypes == object].tolist()
cat_vars = ['pclass', 'sex', 'sibsp', 'parch', 'cabin', 'embarked']
num_vars = ['fare', 'age']
# You can also use DataFrame.select_dtypes(...)
# list(df_titanic.select_dtypes(include=['object']).columns)
# %%
# 1) get_dummies() from pandas
# Attention: dummy_na = True includes a dummy column even if there are none!
df_m = pd.get_dummies(df_titanic, columns=cat_vars, drop_first=False, dummy_na=True)
# %% [markdown]
# > Using get_dummies() on a Pandas dataframe can be dangerous when features change between training/test and prediction, because scikit-learn does not know about column names, it only considers column positions!
#
# Let's use scikit-learn for our encoding:
# %% 
oh_enc = OneHotEncoder(sparse=False, categories="auto", drop=None, handle_unknown='error')
X_oh = oh_enc.fit_transform(df_titanic[cat_vars])

# OneHotEncoder only includes dummy nan column for columns with nan!
oh_enc.categories_

# Combine numeric and categorical features:
X = np.hstack([df_titanic[num_vars], X_oh])
# %% [markdown]
# Using the OneHotEncoder was a bit more work vs. using `get_dummies()`, but one huge benefit we get is that it integrates neatly into scikit-learns api. Using pipelines, we can do the following:
# %%
num_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')),
                         ('std_scaler', StandardScaler())
                        ])
# Alternatively, a shorter way to construct a pipeline is:
num_pipeline = make_pipeline(SimpleImputer(strategy='median'), StandardScaler())
# Take a look at the pipeline steps:
num_pipeline.steps
# You can access steps by name:
num_pipeline.named_steps["simpleimputer"]

cat_pipeline = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                         ('onehot', OneHotEncoder(sparse=False, handle_unknown="ignore"))
                        ])

preprocessing = ColumnTransformer([('num', num_pipeline, num_vars),
                                   ('cat', cat_pipeline, cat_vars)
                                  ])
# Again, you can use the shortcut: make_column_transformer() similar to make_pipeline()

model_logreg = make_pipeline(preprocessing, LogisticRegression())
# %% [markdown]
# A quick note here: If you use a OneHotEncoder in cross-validation, you need to either specify the categories beforehand or allow it to ignore unknown values. Otherwise you will quite likely induce NaNs in your data, because your train folds might not be big enough to contain all categories found in the corresponding test folds.
#
# If you are interested in running feature selection in a pipeline, check out [this article](https://scikit-learn.org/stable/auto_examples/compose/plot_feature_union.html) from the scikit-learn docs.
# %%
y = df_titanic.survived.values
X = df_titanic.drop(["survived"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
# %%
# Fit the model including the pipeline:
model_logreg.fit(X_train, y_train)
print("Logistic Regression score: {}".format(model_logreg.score(X_test, y_test)))
# %% [markdown]
# Pipelines really shine when they are combined with for example grid search, because we can search for the optimal parameters over the entire pipeline:
# %%
# By default make_pipeline() uses the lowercased class name as name.
# Again, we can use model_logreg.steps to check the names we have to use:
param_grid = {'columntransformer__num__simpleimputer__strategy': ['median', 'mean'],
              'logisticregression__C': [0.01, 0.1, 1, 10, 100]
             }

grid = GridSearchCV(model_logreg, param_grid, cv=10, scoring='roc_auc', verbose=1, error_score="raise")
grid.fit(X_train, y_train)
grid.best_score_
# Display results table
# pd.DataFrame(grid.cv_results_).T
# %% [markdown]
# Let's take a quick look at the results from our grid-search:
# %%
print("Best estimator:\n{}".format(grid.best_estimator_))
# %%
print("Best parameters:\n{}".format(grid.best_params_))
# %%
print("Best cross-validation score (AUC):{}".format(grid.best_score_))
print("Test set AUC: {}".format(roc_auc_score(y_true=y_test, y_score=grid.best_estimator_.predict(X_test))))
print("Test set best score (default=accuracy): {}".format(grid.best_estimator_.score(X_test, y_test)))
# %%
# Run the model on our test data with the best pipeline:
print(grid.best_estimator_.predict(X_test)[0:5])
# Return confidence socres for samples:
# From Sklearn docs:
# The confidence score for a sample is the signed distance of that sample to the hyperplane.
print(grid.best_estimator_.decision_function(X_test)[0:5])

# %% [markdown]
# Last, but not least, I want to quickly show you how you can easily perform nested-cross-validation:

# %%
scores = cross_val_score(
            GridSearchCV(
                model_logreg, 
                param_grid, 
                cv=10, scoring='roc_auc', 
                verbose=1, error_score="raise"), 
            X, y)
# %%
print("Nested cross-validation scores: {}".format(scores))
print("Mean nested-cv-score: {}".format(scores.mean()))

# %% [markdown]
# So, that is about it. I hope this quick walk-through was helpful.
#
# In the beginning I had quite some trouble deciding on a 'canonic' way to do things, because there are quite a number of different ways to get to the same end result. I am quite happy with this workflow at the moment, but if you have anys suggestions to improve the workflow, feel free to open a Github issue :)
#
# ## References
# 
# My post follows many recommendations from the book "Introduction to Machine Learning with Python" and only deviates from it significantely when my book was not up-to-date (e.g. OneHotEncoder could not handle strings when the book was published)


# %% [markdown]
# Get feature names:
# https://stackoverflow.com/questions/54646709/sklearn-pipeline-get-feature-names-after-onehotencode-in-columntransformer

# TODO: Include Feature selection in pipeline?
# TODO: Check if Pipeline always keeps variable order as specified in num_vars, cat_vars or if it is sensitive to underlying ordering
# TODO: difference between gridsearchcv and cross_val_score
# https://stackoverflow.com/questions/24096146/how-is-scikit-learn-gridsearchcv-best-score-calculated
# TODO: get feature names for coeffs


# DONE: Is grid.best_estimator_.predict() == grid.predict()? -> yes, per the docs
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html