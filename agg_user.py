import os
import csv
with open('aggregated_user.csv','r') as f:
    data = csv.reader(f)
    data = list(data)
    print(data[1])

def get_aggregated_year_quarter_user(year: int, quarter: str):
    total_users =0
   
    for row in data[1:]:
        if int(row[2])==year and row[3]==quarter:
            total_users += int(row[5])
            
    return total_users



