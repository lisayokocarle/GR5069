###importing necessary packages
import requests
import pandas as pd


###creating function that organizes all of the data returned from API Get request
def organizer(row):
    embedded_df = pd.DataFrame(row['events'])
    return embedded_df


###API get function
def apiget2(city, key):

    url = 'https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&apikey={api}'
    param1 = ({'city':city})
    
    r= requests.get(url.format(api=key), params=param1)
        
    if r.status_code == 200:
        
        test_json=r.json()
        objectids= test_json['_embedded']
            
        final_df = pd.DataFrame(objectids)
       
    else: 
        return r.status_code

def onethousand_apiget(city, key):
    
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&apikey={api}'
    param1 = ({'city':city})
    
    r= requests.get(url.format(api=key), params=param1)
        
    if r.status_code == 200:
        
        test_json=r.json()
        objectids= test_json['_embedded']
        page_number = test_json['page']
        
        full_result = []
        final_df = pd.DataFrame(objectids)
        
        for page in range(2,int(1000/page_number['size'])):
            s = requests.get(url.format(api=key)+'&page={p}'.format(p=page))
            if s.status_code == 200:
                s_json = s.json()
                full_result.append(s_json['_embedded'])
        
                for rows in full_result:
                    test = organizer(rows)
                    final_df = pd.concat([final_df, test])
                    return final_df
                
            else:
                return s.status_code
            
    
    
  
                