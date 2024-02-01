import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Kết nối đến SQL Server
server = 'NGUYENTHITHUYNH' 
database = 'TutorialDB'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

def run_query(search_query):
    query = "SELECT * FROM Products WHERE title LIKE ?"
    cursor = conn.cursor()
    cursor.execute(query, ['%' + search_query + '%'])
    results = cursor.fetchall()
    cursor.close()
    formatted_results = [tuple(row) for row in results]
    
    return formatted_results

st.title('Product Search in SQL Server')

search_query = st.text_input('Enter a keyword to search in product titles')

if st.button('Search'):
    if search_query:
        results = run_query(search_query)
        if results:
            try:
                df = pd.DataFrame(results, columns=['product_id', 'title', 'price', 'link', 'discount', 'saled'])
                df['price'] = df['price'].apply(float)

                # Using Streamlit's columns to create a two-column layout
                col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed

                with col1:
                    st.write('Search Results:')
                    st.dataframe(df, width = 600)  # Adjust the height as needed

                with col2:
                    # Create a histogram for "price"
                    st.write('Histogram for Price:')
                    plt.hist(df['price'], bins=20, edgecolor='k')
                    plt.xlabel('Price')
                    plt.ylabel('Frequency')
                    st.pyplot()

                    # Create a histogram for "discount"
                    st.write('Histogram for Discount:')
                    plt.hist(df['discount'], bins=20, edgecolor='k')
                    plt.xlabel('Discount')
                    plt.ylabel('Frequency')
                    st.pyplot()

            except Exception as e:
                st.write("Error while creating DataFrame:", e)
        else:
            st.write('No results found.')
        
    else:
        st.write('Please enter a search query.')
