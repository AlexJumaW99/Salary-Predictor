import streamlit as st 
import pandas as pd 
import numpy as np
from joblib import dump, load
import streamlit as st
import streamlit_authenticator as stauth

#create usernames and passwords along with names 
names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
passwords = ['123','456']

#hash the passwords (this is a good security measure and is irreversible)
hashed_passwords = stauth.hasher(passwords).generate()

#create an authentication object using the hashed passwords
authenticator = stauth.authenticate(names,usernames,hashed_passwords,
                                   'some_cookie_name','some_signature_key',cookie_expiry_days=30)

st.write('# Jumaiya Salary Predictor')
name, authentication_status = authenticator.login('Login','main')


if authentication_status:
    st.write(
        f'## Welcome, *{name}*'
    )

    df = pd.read_csv('eda.csv')
    df = df.rename(columns={'Employer Provided Sal': 'Employer_Provided_Sal'})

    df_mdl = df[['avg_sal', 'Rating','Size','Type of ownership', 'Industry', 'Sector', 'Revenue','hourly', 'Employer_Provided_Sal', 'State', 'Age', 'job_in_HQ', 'has_python', 'has_spark', 'has_sql','has_excel', 'has_aws', 'has_tableau', 'title_simp', 'seniority', 'desc_len', 'num_competitors']]
    df_dummy = pd.get_dummies(df_mdl)

    X = df_mdl.drop('avg_sal', axis=1)
    y = df_mdl.avg_sal.values

    st.sidebar.header('*Please provide the Job and Company Info:*')


    def user_input_features():
        Rating = st.sidebar.slider('Rating', X.Rating.min(), X.Rating.max(), X.Rating.mean())
        hourly = st.sidebar.slider('Do they pay by the hour?', X.hourly.min(), X.hourly.max())
        Employer_Provided_Sal = st.sidebar.slider('Is the salary provided by the employer?', X.Employer_Provided_Sal.min(), X.Employer_Provided_Sal.max())
        Age = st.sidebar.slider('Age of the company:', X.Age.min(), X.Age.max())
        job_in_HQ = st.sidebar.slider('Is the job in the company HQ?', X.job_in_HQ.min(), X.job_in_HQ.max())
        has_python = st.sidebar.slider('Python', X.has_python.min(), X.has_python.max())
        has_spark = st.sidebar.slider('Spark', X.has_spark.min(), X.has_spark.max())
        has_sql = st.sidebar.slider('Sql', X.has_sql.min(), X.has_sql.max())
        has_excel = st.sidebar.slider('Excel', X.has_excel.min(), X.has_excel.max())
        has_aws = st.sidebar.slider('AWS', X.has_aws.min(), X.has_aws.max())
        has_tableau = st.sidebar.slider('Tableau', X.has_tableau.min(), X.has_tableau.max())
        desc_len = st.sidebar.slider('Please estimate the job description length', X.desc_len.min(), X.desc_len.max(), int(X.desc_len.mean()))
        num_competitors = st.sidebar.slider('No. of Competitors', X.num_competitors.min(), X.num_competitors.max())

    # def pick_size(): #9 in total
        size_ls = [0,0,0,0,0,0,0,0,0]
        size = st.sidebar.selectbox('Company Size:',
                                ('Size_-1', 'Size_1 to 50 employees', 'Size_10000+ employees', 'Size_1001 to 5000 employees', 'Size_201 to 500 employees', 'Size_5001 to 10000 employees', 'Size_501 to 1000 employees', 'Size_51 to 200 employees', 'Size_Unknown'))

        size_list = ['Size_-1', 'Size_1 to 50 employees', 'Size_10000+ employees', 'Size_1001 to 5000 employees', 'Size_201 to 500 employees', 'Size_5001 to 10000 employees', 'Size_501 to 1000 employees', 'Size_51 to 200 employees', 'Size_Unknown']

        for el in size_list:
            if el == size:
                indx = size_list.index(el)
                size_ls[indx] = 1
                break 

            else:
                continue
        
        size_dict = {}

        for key in size_list:
            for value in size_ls:
                size_dict[key] = value
                size_ls.remove(value)
                break 
        
        print(size_dict)

        # if size == '1 to 50 employees':
        #     size_ls[1] = 1 
        
        # elif size == '51 to 200 employees':
        #     size_ls[7] = 1

        # elif size == '201 to 500 employees':
        #     size_ls[4] = 1
        
        # elif size == '501 to 1000 employees':
        #     size_ls[6] = 1

        # elif size == '1001 to 5000 employees':
        #     size_ls[3] = 1
        
        # elif size == '5001 to 10000 employees':
        #     size_ls[5] = 1
        
        # elif size == '10000+ employees':
        #     size_ls[2] = 1
        
        # elif size == 'Unknown':
        #     size_ls[8] = 1
        
        # elif size == 'Missing Data':
        #     size_ls[0] = 1
        
        # return size_ls 

    # def pick_ownership(): #11 in total 
        owner_ls = [0,0,0,0,0,0,0,0,0,0,0]
        owner = st.sidebar.selectbox('Ownership:',
                                    ('Missing Data', 'College/University', 'Private', 'Public', 'Government', 'Hospital', 'NGO', 'Other', 'School/School District', 'Subsidiary/Business Segment', 'Unknown'))
        
        owner_list = ['Missing Data', 'College/University', 'Private', 'Public', 'Government', 'Hospital', 'NGO', 'Other', 'School/School District', 'Subsidiary/Business Segment', 'Unknown']

        for el in owner_list:
            if el == owner:
                indx = owner_list.index(el)
                owner_ls[indx] = 1
                break 

            else:
                continue
        
        # print(owner_ls)

        owner_dict = {}

        for key in owner_list:
            for value in owner_ls:
                owner_dict[key] = value
                owner_ls.remove(value)
                break 
        
        print(owner_dict)

    # def pick_industry(): #60 in total
        ind_ls = [0] * 60
        ind = st.sidebar.selectbox('Industry:',
                                ('Industry_-1', 'Industry_Accounting', 'Industry_Advertising & Marketing', 'Industry_Aerospace & Defense', 'Industry_Architectural & Engineering Services', 'Industry_Auctions & Galleries', 'Industry_Banks & Credit Unions', 'Industry_Beauty & Personal Accessories Stores', 'Industry_Biotech & Pharmaceuticals', 'Industry_Brokerage Services', 'Industry_Colleges & Universities', 'Industry_Computer Hardware & Software', 'Industry_Construction', 'Industry_Consulting', 'Industry_Consumer Product Rental', 'Industry_Consumer Products Manufacturing', 'Industry_Department, Clothing, & Shoe Stores', 'Industry_Education Training Services', 'Industry_Energy', 'Industry_Enterprise Software & Network Solutions', 'Industry_Farm Support Services', 'Industry_Federal Agencies', 'Industry_Financial Analytics & Research', 'Industry_Financial Transaction Processing', 'Industry_Food & Beverage Manufacturing', 'Industry_Gambling', 'Industry_Gas Stations', 'Industry_Health Care Products Manufacturing', 'Industry_Health Care Services & Hospitals', 'Industry_Health, Beauty, & Fitness', 'Industry_IT Services', 'Industry_Industrial Manufacturing', 'Industry_Insurance Agencies & Brokerages', 'Industry_Insurance Carriers', 'Industry_Internet', 'Industry_Investment Banking & Asset Management', 'Industry_K-12 Education', 'Industry_Lending', 'Industry_Logistics & Supply Chain', 'Industry_Metals Brokers', 'Industry_Mining', 'Industry_Motion Picture Production & Distribution', 'Industry_Other Retail Stores', 'Industry_Real Estate', 'Industry_Religious Organizations', 'Industry_Research & Development', 'Industry_Security Services', 'Industry_Social Assistance', 'Industry_Sporting Goods Stores', 'Industry_Staffing & Outsourcing', 'Industry_Stock Exchanges', 'Industry_TV Broadcast & Cable Networks', 'Industry_Telecommunications Manufacturing', 'Industry_Telecommunications Services', 'Industry_Transportation Equipment Manufacturing', 'Industry_Transportation Management', 'Industry_Travel Agencies', 'Industry_Trucking', 'Industry_Video Games', 'Industry_Wholesale'))

        ind_list = ['Industry_-1', 'Industry_Accounting', 'Industry_Advertising & Marketing', 'Industry_Aerospace & Defense', 'Industry_Architectural & Engineering Services', 'Industry_Auctions & Galleries', 'Industry_Banks & Credit Unions', 'Industry_Beauty & Personal Accessories Stores', 'Industry_Biotech & Pharmaceuticals', 'Industry_Brokerage Services', 'Industry_Colleges & Universities', 'Industry_Computer Hardware & Software', 'Industry_Construction', 'Industry_Consulting', 'Industry_Consumer Product Rental', 'Industry_Consumer Products Manufacturing', 'Industry_Department, Clothing, & Shoe Stores', 'Industry_Education Training Services', 'Industry_Energy', 'Industry_Enterprise Software & Network Solutions', 'Industry_Farm Support Services', 'Industry_Federal Agencies', 'Industry_Financial Analytics & Research', 'Industry_Financial Transaction Processing', 'Industry_Food & Beverage Manufacturing', 'Industry_Gambling', 'Industry_Gas Stations', 'Industry_Health Care Products Manufacturing', 'Industry_Health Care Services & Hospitals', 'Industry_Health, Beauty, & Fitness', 'Industry_IT Services', 'Industry_Industrial Manufacturing', 'Industry_Insurance Agencies & Brokerages', 'Industry_Insurance Carriers', 'Industry_Internet', 'Industry_Investment Banking & Asset Management', 'Industry_K-12 Education', 'Industry_Lending', 'Industry_Logistics & Supply Chain', 'Industry_Metals Brokers', 'Industry_Mining', 'Industry_Motion Picture Production & Distribution', 'Industry_Other Retail Stores', 'Industry_Real Estate', 'Industry_Religious Organizations', 'Industry_Research & Development', 'Industry_Security Services', 'Industry_Social Assistance', 'Industry_Sporting Goods Stores', 'Industry_Staffing & Outsourcing', 'Industry_Stock Exchanges', 'Industry_TV Broadcast & Cable Networks', 'Industry_Telecommunications Manufacturing', 'Industry_Telecommunications Services', 'Industry_Transportation Equipment Manufacturing', 'Industry_Transportation Management', 'Industry_Travel Agencies', 'Industry_Trucking', 'Industry_Video Games', 'Industry_Wholesale']

        for el in ind_list:
            if el == ind:
                indx1 = ind_list.index(el)
                ind_ls[indx1] = 1
                break

            else:
                continue
        
        # return ind_ls

        ind_dict = {}

        for key in ind_list:
            for value in ind_ls:
                ind_dict[key] = value
                ind_ls.remove(value)
                break 
        
        print(ind_dict)

        

    # def pick_sector(): #25 in total
        sect_ls = [0] * 25
        sect = st.sidebar.selectbox('Sector:',
                                ('Sector_-1', 'Sector_Accounting & Legal', 'Sector_Aerospace & Defense', 'Sector_Agriculture & Forestry', 'Sector_Arts, Entertainment & Recreation', 'Sector_Biotech & Pharmaceuticals', 'Sector_Business Services', 'Sector_Construction, Repair & Maintenance', 'Sector_Consumer Services', 'Sector_Education', 'Sector_Finance', 'Sector_Government', 'Sector_Health Care', 'Sector_Information Technology', 'Sector_Insurance', 'Sector_Manufacturing', 'Sector_Media', 'Sector_Mining & Metals', 'Sector_Non-Profit', 'Sector_Oil, Gas, Energy & Utilities', 'Sector_Real Estate', 'Sector_Retail', 'Sector_Telecommunications', 'Sector_Transportation & Logistics', 'Sector_Travel & Tourism'))

        sect_list = ['Sector_-1', 'Sector_Accounting & Legal', 'Sector_Aerospace & Defense', 'Sector_Agriculture & Forestry', 'Sector_Arts, Entertainment & Recreation', 'Sector_Biotech & Pharmaceuticals', 'Sector_Business Services', 'Sector_Construction, Repair & Maintenance', 'Sector_Consumer Services', 'Sector_Education', 'Sector_Finance', 'Sector_Government', 'Sector_Health Care', 'Sector_Information Technology', 'Sector_Insurance', 'Sector_Manufacturing', 'Sector_Media', 'Sector_Mining & Metals', 'Sector_Non-Profit', 'Sector_Oil, Gas, Energy & Utilities', 'Sector_Real Estate', 'Sector_Retail', 'Sector_Telecommunications', 'Sector_Transportation & Logistics', 'Sector_Travel & Tourism']

        for el in sect_list:
            if el == sect:
                indx2 = sect_list.index(el)
                sect_ls[indx2] = 1
                break

            else:
                continue
        
        # return sect_ls
        sect_dict = {}

        for key in sect_list:
            for value in sect_ls:
                sect_dict[key] = value
                sect_ls.remove(value)
                break 
        
        print(sect_dict)

    # def pick_revenue(): #14 in total
        rev_ls = [0] * 14
        rev = st.sidebar.selectbox('Company Revenue:',
                                ('Revenue_$1 to $2 billion (USD)', 'Revenue_$1 to $5 million (USD)', 'Revenue_$10 to $25 million (USD)', 'Revenue_$10+ billion (USD)', 'Revenue_$100 to $500 million (USD)', 'Revenue_$2 to $5 billion (USD)', 'Revenue_$25 to $50 million (USD)', 'Revenue_$5 to $10 billion (USD)', 'Revenue_$5 to $10 million (USD)', 'Revenue_$50 to $100 million (USD)', 'Revenue_$500 million to $1 billion (USD)', 'Revenue_-1', 'Revenue_Less than $1 million (USD)', 'Revenue_Unknown / Non-Applicable'))

        rev_list = ['Revenue_$1 to $2 billion (USD)', 'Revenue_$1 to $5 million (USD)', 'Revenue_$10 to $25 million (USD)', 'Revenue_$10+ billion (USD)', 'Revenue_$100 to $500 million (USD)', 'Revenue_$2 to $5 billion (USD)', 'Revenue_$25 to $50 million (USD)', 'Revenue_$5 to $10 billion (USD)', 'Revenue_$5 to $10 million (USD)', 'Revenue_$50 to $100 million (USD)', 'Revenue_$500 million to $1 billion (USD)', 'Revenue_-1', 'Revenue_Less than $1 million (USD)', 'Revenue_Unknown / Non-Applicable']

        for el in rev_list:
            if el == rev:
                indx3 = rev_list.index(el)
                rev_ls[indx3] = 1
                break

            else:
                continue
        
        # return rev_ls

        rev_dict = {}

        for key in rev_list:
            for value in rev_ls:
                rev_dict[key] = value
                rev_ls.remove(value)
                break 
        
        print(rev_dict)

    # def pick_state(): #37 in total
        state_ls = [0] * 37
        state = st.sidebar.selectbox('State:',
                                    ('State_AL', 'State_AZ', 'State_CA', 'State_CO', 'State_CT', 'State_DC', 'State_DE', 'State_FL', 'State_GA', 'State_IA', 'State_ID', 'State_IL', 'State_IN', 'State_KS', 'State_KY', 'State_LA', 'State_MA', 'State_MD', 'State_MI', 'State_MN', 'State_MO', 'State_NC', 'State_NE', 'State_NJ', 'State_NM', 'State_NY', 'State_OH', 'State_OR', 'State_PA', 'State_RI', 'State_SC', 'State_TN', 'State_TX', 'State_UT', 'State_VA', 'State_WA', 'State_WI'))

        state_list = ['State_AL', 'State_AZ', 'State_CA', 'State_CO', 'State_CT', 'State_DC', 'State_DE', 'State_FL', 'State_GA', 'State_IA', 'State_ID', 'State_IL', 'State_IN', 'State_KS', 'State_KY', 'State_LA', 'State_MA', 'State_MD', 'State_MI', 'State_MN', 'State_MO', 'State_NC', 'State_NE', 'State_NJ', 'State_NM', 'State_NY', 'State_OH', 'State_OR', 'State_PA', 'State_RI', 'State_SC', 'State_TN', 'State_TX', 'State_UT', 'State_VA', 'State_WA', 'State_WI']

        for el in state_list:
            if el == state:
                indx4 = state_list.index(el)
                state_ls[indx4] = 1
                break

            else:
                continue
        
        # return state_ls

        state_dict = {}

        for key in state_list:
            for value in state_ls:
                state_dict[key] = value
                state_ls.remove(value)
                break 
        
        print(state_dict)


        title_ls = [0] * 7
        title = st.sidebar.selectbox('Job Title:',
                                    ('title_simp_analyst', 'title_simp_data engineer', 'title_simp_data scientist', 'title_simp_director', 'title_simp_manager', 'title_simp_mle', 'title_simp_na'))

        title_list = ['title_simp_analyst', 'title_simp_data engineer', 'title_simp_data scientist', 'title_simp_director', 'title_simp_manager', 'title_simp_mle', 'title_simp_na']

        for el in title_list:
            if el == title:
                indx5 = title_list.index(el)
                title_ls[indx5] = 1
                break

            else:
                continue
        
        title_dict = {}

        for key in title_list:
            for value in title_ls:
                title_dict[key] = value
                title_ls.remove(value)
                break 
        
        print(title_dict)
        
        # return title_ls

        snr_ls = [0] * 3
        snr = st.sidebar.selectbox('Seniority:',
                                ('seniority_junior', 'seniority_na', 'seniority_senior'))

        snr_list = ['seniority_junior', 'seniority_na', 'seniority_senior']

        for el in snr_list:
            if el == snr:
                indx6 = snr_list.index(el)
                snr_ls[indx6] = 1
                break

            else:
                continue
        
        snr_dict = {}

        for key in snr_list:
            for value in snr_ls:
                snr_dict[key] = value
                snr_ls.remove(value)
                break 
        
        print(snr_dict)
        print(type(snr_dict)) 

        data = {
            'Rating': Rating,
            'hourly': hourly,
            'Employer Provided Salary': Employer_Provided_Sal,
            'Age': Age,
            'has_python': has_python,
            'job_in_HQ': job_in_HQ,
            'has_spark': has_spark,
            'has_sql': has_sql,
            'has_excel': has_excel,
            'has_aws': has_aws,
            'has_tableau': has_tableau,
            'desc_len': desc_len,
            'num_competitors': num_competitors,
        }

        for key, value in title_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        for key, value in state_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        for key, value in rev_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        for key, value in sect_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        for key, value in ind_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        for key, value in owner_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        for key, value in size_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value   

        # for obj in snr_dict:
        for key, value in snr_dict.items():
            print(f'{str(key)}:{value}') #if it doesn't work look here
            data[f'{key}']= value 

        print(data)
    
        #data.set('num_competitors': num_competitors )

        features = pd.DataFrame(data, index=[0])
        return features
        
    df2 = user_input_features()

    st.header('Specified User Input')
    st.write(df2)
    st.write('---')

    sal_mdl = load('salary_model.joblib')

    prediction = sal_mdl.predict(df2)

    st.header('Salary Prediction')
    st.write('Here is your **annual** salary prediction in **thousands of dollars**:')
    st.write(prediction)

    # res = {}

    # for key in snr_list:
    #     for value in snr_ls:
    #         res[key] = value
    #         snr_ls.remove(value)
    #         break 

    # print(res) 


elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')

        

 



