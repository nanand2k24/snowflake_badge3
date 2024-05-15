# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize your Smoothie!! :balloon:")
st.write(
"""
This is test!!!
""")

cnx=st.connection('snowflake')
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie: ')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list = st.multiselect(
    'Choose upto 5 ingradients: ', my_dataframe
    , max_selections=5
    )

if ingredient_list:
    ingredient_string = ''

    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_chosen+ '""')
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredient_string + """', '""" + name_on_order + """')"""
 
    time_to_submit = st.button('Submit Order', type="primary")

    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' +name_on_order, icon="✅")


