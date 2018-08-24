import numpy as np
import pandas as pd
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import os
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder

os.chdir("..")
# open a file connection here to save results
f = open("analysis/plots/results.txt", 'w')
sys.stdout = f
headers = None
# load the data retrieved from MYSQL
with open('headers.json') as f:
    headers = json.load(f)
test_features_df = pd.read_csv(sys.argv[1], names=headers['test_features'])
train_features_df = pd.read_csv(sys.argv[2], names=headers['train_features'])
train_sal_df = pd.read_csv(sys.argv[3], names=headers['train_salaries'])

# trained encoders dict
trained_encoders = {}
neg_mse = 0

# make a list of numeric and categorical features by manual inspection
numeric = ['yearsExperience', 'milesFromMetropolis']
categorical = ['companyId', 'jobType', 'degree', 'major', 'industry']
id_col = ["jobId"]
# merge the data frames on JOBID
train_df = pd.merge(train_features_df, train_sal_df, on='jobId')
del train_features_df
del train_sal_df

# Are there any outliers?
print('Outlier Analysis')
stat = train_df.salary.describe()
print(stat)
IQR = stat['75%'] - stat['25%']
upper = stat['75%'] + 1.5 * IQR
lower = stat['25%'] - 1.5 * IQR
print('The upper and lower bounds for suspected outliers are {} and {}.'.format(upper, lower))


# plotting function

def plot_feature(df, col):
    '''
    Dependency of salary on features
    '''
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    if df[col].dtype == 'int64':
        df[col].value_counts().sort_index().plot()
    else:
        # change the categorical variable to category type and order their level by the mean salary
        # in each category
        mean = df.groupby(col)['salary'].mean()
        df[col] = df[col].astype('category')
        levels = mean.sort_values().index.tolist()
        df[col].cat.reorder_categories(levels, inplace=True)
        df[col].value_counts().plot()
    plt.xticks(rotation=45)
    plt.xlabel(col)
    plt.ylabel('Counts')
    plt.subplot(1, 2, 2)
    plt.title(col.upper() + " Graph")

    if df[col].dtype == 'int64' or col == 'companyId':
        # plot the mean salary for each category and fill between the (mean - std, mean + std)
        mean = df.groupby(col)['salary'].mean()
        std = df.groupby(col)['salary'].std()
        mean.plot()
        plt.fill_between(range(len(std.index)), mean.values - std.values, mean.values + std.values,
                         alpha=0.1)
    else:
        sns.boxplot(x=col, y='salary', data=df)

    plt.xticks(rotation=45)
    plt.ylabel('Salaries')
    plt.savefig("analysis/plots/" + col.upper() + ".png")


def clean_data(df):
    """
    Function to retain rows with salary >0 and to remove duplicate jobID's
    :param df:
    :return: df
    """
    df = df[df.salary > 0]
    df = df.drop_duplicates(subset="jobId")
    return df


def encode_labels(df):
    """
    Encode categorical labels and return the data frame
    :param df:
    :return df:
    """
    for col in categorical:
        le = LabelEncoder()
        le.fit(df[col])
        df[col] = le.transform(df[col])
        trained_encoders[col] = le
    return df


def decode_labels(df):
    """
    Decode labels and return the data frame
    :param df:
    :return df:
    """
    for col in categorical:
        df[col] = trained_encoders[col].inverse_transform(df[col])
    return df


def cross_validate(model, x, Y):
    """
    Cross validate with the parameter model
    :param model:
    :return:
    """
    mse = cross_val_score(model, x, Y, cv=3, n_jobs=1, scoring='neg_mean_squared_error')
    neg_mse = -1 * np.mean(mse)  # negative mse float value
    return neg_mse


def predict_salaries(model, test_features, X, y):
    """
    Predict the salaries for test data
    :param model:
    :param test_features:
    :param X:
    :param y:
    :return:
    """
    model.fit(X, y)
    return model.predict(test_features)


# created all helper functions above

train_df = clean_data(train_df)

# visualize salary range

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.boxplot(train_df.salary)
plt.subplot(1, 2, 2)
sns.distplot(train_df.salary, bins=20)
plt.savefig("analysis/plots/salary_distribution.png")

# visualize other features
plot_feature(train_df, 'companyId')
plot_feature(train_df, 'jobType')
plot_feature(train_df, 'degree')
plot_feature(train_df, 'major')
plot_feature(train_df, 'industry')
plot_feature(train_df, 'yearsExperience')
plot_feature(train_df, 'milesFromMetropolis')

# random shuffle rows

# test train split
Y = train_df.salary
train_df.drop(["salary", "jobId"], inplace=True, axis=1)
x = train_df

# encode labels
x = encode_labels(x)
test_jobs = test_features_df.jobId
test_features_df.drop(["jobId"], axis=1, inplace=True)
test_features_df = encode_labels(test_features_df)

# model  - Hand tuned hyper parameters
model = RandomForestRegressor(n_estimators=60, n_jobs=1, max_depth=15, min_samples_split=80,
                              max_features=1.0, verbose=0)

# cross validate
neg_mse = cross_validate(model, x, Y)

# predict
predictions = predict_salaries(model, test_features_df, x, Y)
test_features_df = decode_labels(test_features_df)
predictions = pd.DataFrame(predictions, columns=["salary predictions"])
predictions = pd.concat([test_jobs, test_features_df, predictions], ignore_index=True
                        , axis=1)
test_headers = headers['test_features'] + ["salary"]
predictions.columns = test_headers
predictions.to_csv("analysis/plots/predictions.csv", index=False)
print("A hand tuned Random forest regressor is used to predict the salary and the MSE is " + str(neg_mse))
print("Check out the feature plots for more insights")
f.close()
