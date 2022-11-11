import pandas as pd
import streamlit as st 
import requests

st.write('Welcome to the Zillow API Searcher')
pd.set_option('display.max_columns', None)
#Input parameters
rapid_api_key = st.text_input('Enter your API Key')
status_type = st.selectbox('Status:',('ForSale','ForRent','RecentlySold'))
home_type  = st.selectbox('HomeType:',('LotsLand','Multi-family','Apartments','Houses','Manufactured','Condos','Townhomes'))
city = st.text_input('Enter the desired city', 'santa cruz')
state = st.text_input('Enter the desired state', 'ca')
minPrice = st.number_input('Enter Minimum Price')
maxPrice = st.number_input('Enter Maximum Price')
sqftMin= st.number_input('Enter Minimum SQFT')
lotSizeMin = st.selectbox('Minimum Lot Size:', ('1,000 sqft','2,000 sqft','3,000 sqft','4,000 sqft','5,000 sqft','7,500 sqft','1/4 acre/10,890 sqft','1/2 acre/21,780 sqft','1 acre/43,560 sqft'))
lotSizeMin = st.selectbox('Minimum Lot Size:', ('1,000 sqft','2,000 sqft','3,000 sqft','4,000 sqft','5,000 sqft','7,500 sqft','1/4 acre/10,890 sqft','1/2 acre/21,780 sqft','1 acre/43,560 sqft','2 acres/87,120 sqft','5 acres/217,800 sqft','10 acres/435,600 sqft','\
20 acres/871,200 sqft','50 acres/2,178,000 sqft','100 acres/4,356,000 sqft'))
search_str = city + ', ' + state
print('Search string:', search_str)
#unique key
url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
# api query
querystring = {"location":search_str,
               "status_type":status_type,
               "home_type":home_type,
               "minPrice": minPrice,
               "maxPrice": maxPrice,
               "sqftMin": sqftMin}
# for api 
headers = {
    'x-rapidapi-host': "zillow-com1.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key
    }

z_for_sale_resp = requests.request("GET", url, headers=headers, params=querystring)

# transform to json
z_for_sale_resp_json = z_for_sale_resp.json()
z_for_sale_resp_json['props']
## to DF
df_z_for_sale = pd.json_normalize(data=z_for_sale_resp_json['props'])
# get zpids to a list
zpid_list = df_z_for_sale['zpid'].tolist()
# create empty list
prop_detail_list = []

# iterate through list of properties
for zpid in zpid_list:

  # end point
  url = "https://zillow-com1.p.rapidapi.com/property"

  querystring = {"zpid":zpid}

  # header
  headers = {
      'x-rapidapi-host': "zillow-com1.p.rapidapi.com",
      'x-rapidapi-key': rapid_api_key
      }

  # get property detail
  z_prop_detail_resp = requests.request("GET", url, headers=headers, params=querystring)
  z_prop_detail_resp_json = z_prop_detail_resp.json()

  # wait 1 sec based on limit
  time.sleep(.75)

  prop_detail_list.append(z_prop_detail_resp_json)
df_z_prop_detail = pd.json_normalize(prop_detail_list)
# columns of interest
detail_cols = ['streetAddress', 
 'city',
 'county',
 'zipcode',
 'state',
 'price',
 'homeType',
 'timeOnZillow', 
 'zestimate',
 'rentZestimate',
 'livingArea',
 'bedrooms',
 'bathrooms',
 'yearBuilt',
 'description',
 'priceHistory',
 'taxHistory',
 'zpid'
 ]

# retain limited columns for output
df_z_prop_detail_output = df_z_prop_detail[detail_cols]
st.dataframe(df_z_prop_detail_output)
