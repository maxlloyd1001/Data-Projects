import numpy as np
import streamlit as st
import pandas as pd
import requests



st.title('Welcome to my data cleaner!!!')
st.write('Welcome, this is my data cleaner. This is a automated system that is controlled by you the user'
         ' and its function is to prepare your data for model and analysis.')

st.subheader('Upload your data')
st.write('Here you must decide how to upload your data, chose either the API or File option.'
         ' Make sure to use an API that is open and public but make sure you can trust the source,'
         ' this is the same with any file uploads, make sure you trust the source.')

file = st.checkbox('File submission')
api = st.checkbox('API submission')
if file:
    my_csv = st.file_uploader('Select a CSV!',
                              type = 'CSV',
                              accept_multiple_files=False)
    my_df = pd.read_csv(my_csv)
    st.write('Below is your data in a pandas dataframe, look through the data to make sure this is what you expected to'
             ' see. Make sure that your data is not corrupted or there are any extra columns that should not be there.')
    st.write(my_df)
    st.write('Here you can see the shape of your dataframe')
    st.write(my_df.shape)

    st.subheader('Heads or Tails and Data Types')
    st.write('Here you can select if you would like to view the head or tail of your dataset'
             ' and the number of rows you would like to view.')
    num=st.number_input('How many row would you like to view',5,20)
    head=st.radio('View from top (head) or bottom (tail)',('Head','Tail'))
    if head=='Head':
        st.dataframe(my_df.head(num))
    else:
        st.dataframe(my_df.tail(num))

    st.write('Here you can view your datatypes in the columns of your dataset')
    foo = my_df.dtypes.astype(str)
    st.write(foo)

    columns = [col for col in my_df]
    options1 = st.multiselect('Select the columns you would like to change to a string', columns)
    options2 = st.multiselect('Select the columns you would like to change to a int', columns)
    options3 = st.multiselect('Select the columns you would like to change to a float', columns)
    options4 = st.multiselect('Select the columns you would like to change to a date', columns)
    options5 = st.multiselect('Select the columns you would like to change to a bool', columns)
    options6 = st.multiselect('Select the columns you would like to change to a category', columns)
    def typefixer(data,op1,op2,op3,op4,op5,op6):
        for col in op1:
            data[col] = data[col].astype(str)
        for col in op2:
            data[col] = data[col].astype(int)
        for col in op3:
            data[col] = data[col].astype(float)
        for col in op4:
            data[col] = pd.to_datetime(data[col])
        for col in op5:
            data[col] = data[col].astype(bool)
        for col in op6:
            data[col] = data[col].astype('category')
        return data
    if st.checkbox('Fix my data types'):
        my_df = typefixer(my_df, options1, options2, options3, options4, options5, options6)
        st.write('Lets take a look at your new data types')
        foo = my_df.dtypes.astype(str)
        st.write(foo)

    st.subheader('Column formatting')
    st.write('Below you will be able to make a changes to how the columns within your dataset look, '
        ' this can be making all of the columns names the same format for example')
    st.write('The button below will make all the column names lowercase and will remove any whitespaces and replace the underscores'
        ' to keep your columns tidy and consistent.')

    def columnfixer(data):
        data.columns = data.columns.str.lower().str.replace('[^0-9a-zA-Z]+','_',regex=True)
        return data
    if st.checkbox('Tidy your columns'):
        my_df = columnfixer(my_df)
        st.write(my_df)
    columns = [col for col in my_df]
    st.subheader('Sorting the nulls')
    st.write("In this section we can sort out any missing values through a variety of methods, but first we will look at the"
             " percentage of missing values in each column.")
    dfnull = my_df.isnull().sum()/len(my_df)*100
    st.write(dfnull)
    st.write('Using the checkbox below will remove any columns that contain more than 40% nulls')

    def nullifier(data):
        data.dropna(thresh=data.shape[0]*0.6,how='all',axis=1, inplace=True)
        return data
    if st.checkbox('Drop your bad columns'):
        my_df = nullifier(my_df)
        dfnull = my_df.isnull().sum()/len(my_df)*100
        st.write(dfnull)

    st.write('Here you can select any numeric column and a function will be apllied to turn all the missing values into either'
             ' the mean or the median.')
    option1 = st.multiselect('Select columns to fill the nulls with the mean', columns)
    option2 = st.multiselect('Select columns to fill the nulls with the median', columns)
    def nullmean(data,option):
        for col in option:
            data[col].fillna(data[col].mean())
        return data
    if st.checkbox('Fill with mean'):
        my_df = nullmean(my_df, option1)
    def nullmedian(data,option):
        for col in option:
            data[col].fillna(data[col].median())
        return data
    if st.checkbox('Fill with median'):
        my_df = nullmedian(my_df, option2)
    st.write('Here you can manually drop a column that either has no use in your data or for any other reason')
    option3 = st.multiselect('Select columns to manually drop', columns)
    def nullmanual(data, option):
        for col in option:
            data.drop([col], axis = 1, inplace=True)
            return data
    if st.checkbox('Drop selected columns'):
        nullmanual(my_df, option3)
    st.write('Finally drop the remaining rows that contain a null value')
    def nullrow(data):
       data=data.dropna()
       return data
    st.write('Press the checkbox below to run all these functions and remove the last of your nulls')
    if st.checkbox('Fix all nulls'):
        my_df = nullrow(my_df)
        st.write('Final check for null values')
        dfnull = my_df.isnull().sum()/len(my_df)*100
        st.write(dfnull)
    st.write('Now lets take another look at your null free data')
    head=st.radio('View from top or bottom',('Head','Tail'))
    if head=='Head':
        st.dataframe(my_df.head(10))
    else:
        st.dataframe(my_df.tail(10))

    st.subheader('Lets make some graphs')
    st.write('In this  section you can use your clean data to produce some basic graphical analysis to check that your '
             ' data has been successfully cleaned')
    st.write('Your y axis will be the mean of that column ')
    x = st.selectbox('Select your x axis', columns)
    y = st.selectbox('Select your y axis', columns)
    st.line_chart(my_df[x],my_df[y].mean())

    st.subheader('Get your data back')
    st.write('Select the box below to receive your clean data')
    def convert_df(df):
       return df.to_csv().encode('utf-8')

    csv = convert_df(my_df)

    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='my_df.csv',
    mime='text/csv',
    )



if api:
    st.subheader('API')
    url = st.text_input('Enter the url', value="")
    response = requests.get(url)
    st.write('Most APIs especially public ones are already clean as they are usually up to date data so '
             ' instead of cleaning, this system will allow your to receive your API in a dataframe from a JSON'
             ' format which can be downloaded as a CSV file.')
    st.write(response)
    jason = response.json()
    st.write(type(jason))
    st.write('Below are the keys of the data.')
    st.write(jason.keys())
    st.write('Type in the key from the list above that you would like to take a closer look at.')
    key = st.text_input('Enter the key', value="")
    my_df = pd.DataFrame.from_dict(jason[key], orient="index")
    st.write(my_df)
    st.write('Here you can view the datatypes already assigned.')
    foo = my_df.dtypes.astype(str)
    st.write(foo)
    st.write('Most APIs do not contain nulls but here you can check, the table shows the percentage of nulls in each '
             ' column.')
    dfnull = my_df.isnull().sum()/len(my_df)*100
    st.write(dfnull)


    st.write('Now you can retrieve your API as a dataframe.')
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(my_df)

    st.download_button(
        label="Download your data as CSV",
        data=csv,
        file_name='my_api_df.csv',
        mime='text/csv',
    )








