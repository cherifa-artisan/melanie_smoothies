# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



cnx = st.connection('snowflake')
session = cnx.session()

ingredients_string = ''


# Write directly to the app
st.title("Customize your Smoothie")


name_on_order = st.text_input('Write your name:')

st.write('The name on your smoothie will be: ', name_on_order)



my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients = st.multiselect('Choose up to 5 ingredients: ', my_dataframe, max_selections=5)

if ingredients:
    st.write(ingredients)
    for ingredient in ingredients:
        ingredients_string += ingredient + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        st.subheader(ingredient + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        # st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

time_to_insert = st.button('Submit')

    
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

if time_to_insert and ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
    st.stop()

    

