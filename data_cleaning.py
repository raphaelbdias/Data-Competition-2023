import pandas as pd
from shapely.wkt import loads
import json
import regex as re

def read_json_file(file_path):
    """
    Read JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The parsed JSON data.

    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def convert_date_columns(df, date_columns):
    # Convert 'Date' column to correct format
    df['Date'] = [str(i).replace('_', '') for i in df['Date']]
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert other date columns to correct format
    date_columns = date_columns
    for column in date_columns:
        df[column] = pd.to_datetime(df[column])

    return df


def detect_outliers_iqr(data, outliers):
    data = sorted(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    # print(q1, q3)
    IQR = q3-q1
    lwr_bound = q1-(1.5*IQR)
    upr_bound = q3+(1.5*IQR)
    # print(lwr_bound, upr_bound)
    for i in data: 
        if (i<lwr_bound or i>upr_bound):
            outliers.append(i)
    return outliers# Driver code




def load_wkt_coordinates(df, column_name):
    """
    Load WKT (Well-Known Text) coordinates from a dataframe column using the Shapely library.

    Args:
        df (pandas.DataFrame): The dataframe containing the WKT coordinates.
        column_name (str): The name of the column containing the WKT coordinates.

    Returns:
        pandas.DataFrame: The dataframe with loaded Shapely geometries.

    """
    df[column_name] = df[column_name].apply(lambda x: loads(x))
    return df


# create a new function to clean the tweets 
def remove_hashtags_usernames(tweet):
    # Use regex to match hashtags (starting with #) and usernames (starting with @)
    tweet = re.sub(r'#\w+', '', tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r"http\S+", "", tweet)
    return tweet

# Search for tweets containing a specific string
def keyword_query(df, column, word):
    search_string = word # Replace with your desired search string

    # Use str.contains() to filter tweets
    filtered_df = df[df[column].str.contains(search_string, case=True)]
    return(filtered_df)