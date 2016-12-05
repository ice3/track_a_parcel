[![Build Status](https://travis-ci.org/ice3/track_a_parcel.svg?branch=reboot)](https://travis-ci.org/ice3/track_a_parcel)

# track_a_parcel
Application to track parcels.

Use the (myparcels.ru) API to get the informations.


# Installation

    git clone https://github.com/ice3/track_a_parcel.git
    ## create a virtualenv if you want
    ## I use `pew new -p python3.4 parcel` and `pew workon parcel`
    pip3 install -r requirements.txt
  
## Database management

Before the first launch, you need to create the database according the models. This is done with the command :
 
    ./db_create.py

------------------------------------

When you change the models, use `db_migrate.py` to update the database schema.  

/!\ there will be errors, because the migration scripts don't pickle the datetime.datetime.now function correctly, you need to change this manually in the migration scripts...


# Run 

If you want to run the app to test it :

    ./run.py
    
# Tests

We use pytest as a test runner :

    pytest  # launch the tests...
    pytest --cov=app --cov-report html  # to get an HTML coverage report
