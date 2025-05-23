import pandas as pd 
import os
import kagglehub
from sklearn.preprocessing import StandardScaler

def churn_etl_pipeline():
    # Download latest version
    path = kagglehub.dataset_download("shubhammeshram579/bank-customer-churn-prediction")

    file_path = os.path.join(path, "Churn_Modelling.csv")

    df=pd.read_csv(file_path)

    df.drop(['RowNumber','CustomerId','Surname'],axis=1,inplace=True)

    df = pd.get_dummies(df, columns=['Geography'])
    df['Gender']=df['Gender'].replace({"Male":1,"Female":2})

    # Outliers removal
    def remove_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    numerical_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
    # Applying the removal for each numerical feature
    for column in numerical_features:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    # List of numerical features to scale
    numerical_features = ['CreditScore', 'Age', 'Balance', 'EstimatedSalary']

    # Initialize the scaler
    scaler = StandardScaler()

    # Fit and transform the numerical features
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    #Converting to csv
    df.to_csv('s3://churnairflowbucket/final_dataframe.csv', index=False)