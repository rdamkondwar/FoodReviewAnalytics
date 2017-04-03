### Table A is created using the file "yelp_data.csv" found in this directory.
### Table B is created using the file "zomato_data.csv" found in this directory.

### Attributes of Table A and Table B :
- ID : The unique Id of the restaurant.
- name : Full name of the restaurant.
- address : Address (including street name) of the restaurant.
- city : Name of the city restaurant is located in.
- zipcode : Zipcode of the area restaurant is located in.
- latitude : Latitude cordinate of the restaurant.
- longitude : Longitude cordinate of the restaurant. 
- review_count : The count of reviews received by the restaurant.
- rating : Aggregate rating received by an restaurant.
- zomato_id : The unique business id of the restaurant corresponding to the zomato dataset.
- yelp_id : The unique business id of the restaurant corresponding to the yelp dataset.

### Number of tuples in Table A : 144072
### Number of tuples in Table B : 3600

### D.csv contains all tuples that survive the blocking step. Number of tuples in Table D : 2472
### Number of tuples sampled from Table D to create labeled Table G (G.csv) : 600
### Number of tuples in the training set Table I (I.csv) taken from Table G : 300
### Number of tuples in the test set Table J (J.csv) taken from Table G : 300
