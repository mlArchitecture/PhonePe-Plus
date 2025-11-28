import os
import csv
import matplotlib.pyplot as plt
import base64
import io
import numpy as np

with open('aggregated_transaction.csv','r') as f:
    data = csv.reader(f)
    data = list(data)

def get_aggregated_year_quarter(year: int, quarter: str):
    total_transactions_amount = 0
    total_transactions = 0
    for row in data[1:]:
        if int(row[2]) == year and row[3] == quarter:
            total_transactions_amount += float(row[6])
            total_transactions += int(row[5])
    return total_transactions_amount, total_transactions, total_transactions_amount / total_transactions if total_transactions > 0 else 0

def get_categories_data(year: int, quarter: str):
    amount_dict = {'Recharge & bill payments': 0, 'Peer-to-peer payments': 0, 'Merchant payments': 0, 'Financial Services': 0, 'Others': 0}
    for row in data[1:]:
        if int(row[2]) == year and row[3] == quarter:
            category = row[4]
            amount = float(row[6])
            amount_dict[category] += amount
    return amount_dict

def get_states_data_top(year: int, quarter: str, top_n: int = 5):
    state_data = {}
    for row in data[1:]:
        if int(row[2]) == year and row[3] == quarter:
            state = row[1]
            amount = float(row[6])
            state_data[state] = state_data.get(state, 0) + amount
    sorted_states = sorted(state_data, key=lambda x: state_data[x], reverse=True)
    return sorted_states[:top_n]

def plot_state_transactions_bar():
    state_data = {}
    for row in data[1:]:
        state = row[1]
        amount = float(row[6])
        transaction = int(row[5])
        
        if state not in state_data:
            state_data[state] = [amount, transaction]  # ✅ FIX: Actually assign to dictionary
        else:
            state_data[state][0] += amount
            state_data[state][1] += transaction
    
    states = list(state_data.keys())
    amounts = [state_data[state][0] for state in states]
    transactions = [state_data[state][1] for state in states]
    
    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    ax1.bar(states, [val / 1e6 for val in amounts], color='#4CAF50')
    ax1.set_title('Total Transaction Amount by State', fontsize=14, fontweight='bold')
    ax1.set_xlabel('States', fontsize=12)    
    ax1.set_ylabel('Amount (in Millions)', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    
    ax2.bar(states, [transaction / 1e4 for transaction in transactions], color='#FF6B6B')
    ax2.set_title('Total Number of Transactions by State', fontsize=14, fontweight='bold')
    ax2.set_xlabel('States', fontsize=12)    
    ax2.set_ylabel('Transactions (in 10,000s)', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64_bar = base64.b64encode(buffer.read()).decode()
    plt.close()
    return image_base64_bar

def plot_category_pie():
    state_data = {}
    for row in data[1:]:
        state = row[1]
        amount = float(row[6])
        transaction = int(row[5])
        
        if state not in state_data:
            state_data[state] = [amount, transaction] 
        else:
            state_data[state][0] += amount
            state_data[state][1] += transaction
    
    states = list(state_data.keys())
    amounts = [state_data[state][0] for state in states]
    transactions = [state_data[state][1] for state in states]
    
    fig, ax = plt.subplots(1, 2, figsize=(20, 20))
    
    colors = plt.get_cmap('tab20').colors
    
    ax[0].pie(amounts, labels=states, autopct='%1.1f%%', colors=colors)
    ax[0].set_title('Transaction Amount Distribution by State', fontsize=18, fontweight='bold')
    
    ax[1].pie(transactions, labels=states, autopct='%1.1f%%', colors=colors)
    ax[1].set_title('Number of Transactions Distribution by State', fontsize=18, fontweight='bold')
    
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64_pie = base64.b64encode(buffer.read()).decode()
    plt.close()
    return image_base64_pie

def calculate_variance_top_states_amount(top_n: int = 5):
    state_data={}
    for row in data[1:]:
        state=row[1]
        amount=float(row[6])
        if state not in state_data:
            temp=[amount]
            state_data[state]=temp
        else:
            state_data[state].append(amount)
    variance_dict={}
    for state in state_data:
        amounts=state_data[state]
        if len(amounts)>1:
            variance=np.std(amounts)
            variance_dict[state]=variance
    sorted_variance=sorted(variance_dict,key=lambda x:variance_dict[x],reverse=True)
    return sorted_variance[:top_n]
def calculate_variance_top_states_transaction(top_n: int = 5):
    state_data={}
    for row in data[1:]:
        state=row[1]
        transaction=float(row[5])
        if state not in state_data:
            temp=[transaction]
            state_data[state]=temp
        else:
            state_data[state].append(transaction)
    variance_dict={}
    for state in state_data:
        amounts=state_data[state]
        if len(amounts)>1:
            variance=np.std(amounts)
            variance_dict[state]=variance
    sorted_variance=sorted(variance_dict,key=lambda x:variance_dict[x],reverse=True)
    return sorted_variance[:top_n]

with open('map_transaction.csv','r') as f:
        data_dist=csv.reader(f)
        data_dist=list(data_dist)
print(type(data_dist[0][2]))

def distAnalysis(distName: str):
    amount = []
    transactions = []

    for row in data_dist[1:]:
        if row[4] == distName:
            amount.append(float(row[6]))
            transactions.append(float(row[5]))
    
    

    if not amount or not transactions:
        return None, 0, 0, 0, 0, 0, 0
    
    var_amount = np.std(amount)
    var_transactions = np.std(transactions)  
    max_amount = max(amount)
    max_trans = max(transactions)
    min_amount = min(amount)
    min_transaction = min(transactions)
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    ax[0].plot(amount, label='Amount')
    ax[1].plot(transactions, label='Transactions')
    ax[0].set_title("Amount Analysis")  # Fixed: set_title, not settitle
    ax[0].set_xlabel('Index')           # Fixed: set_xlabel, not xlabel
    ax[0].set_ylabel('Amount')          # Fixed: set_ylabel, not ylabel
    ax[1].set_title("Transactions Analysis")  # Fixed: set_title
    ax[1].set_xlabel('Index')           # Fixed: set_xlabel
    ax[1].set_ylabel('Transactions')    # Fixed: set_ylabel


    ax[0].legend()
    ax[1].legend()

    ax[0].grid(True, alpha=0.3)
    ax[1].grid(True, alpha=0.3)
    
    plt.tight_layout()

    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64_dist = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return image_base64_dist, round(var_amount,2), round(var_transactions,2), round(max_amount,2), round(max_trans,2), round(min_amount,2), round(min_transaction,2)


def distAnalysisPie():
    dict_dist_amount={}
    for row in data_dist[1:]:
        dict_dist_amount[row[4]]=row[6]
    

    dict_dist_trans={}
    for row in data_dist[1:]:
        dict_dist_trans[row[4]]=row[5]
    fig,axes=plt.subplots(1,2)
    
    axes[0].pie([float(dict_dist_amount[i]) for i in sorted(dict_dist_amount,key=lambda x:dict_dist_amount[x])[:5]],labels=sorted(dict_dist_amount,key=lambda x:dict_dist_amount[x])[:5],explode=[0.05]*5)
    axes[0].set_title('Amount Pie Chart')

    axes[1].pie([float(dict_dist_trans[i]) for i in sorted(dict_dist_trans,key=lambda x:dict_dist_trans[x])[:5]],labels=sorted(dict_dist_trans,key=lambda x:dict_dist_trans[x])[:5],explode=[0.05]*5)
    axes[1].set_title('Transactions Pie Chart')

    buffer=io.BytesIO()
    
    plt.savefig(buffer,format='png',dpi=100, bbox_inches='tight')
    buffer.seek(0)

    image_pie=base64.b64encode(buffer.read()).decode()

    return image_pie
    

def barPlot(dist_name: str):
    dict_new = {}
    for row in data_dist[1:]:
        if row[4] == dist_name:
            if row[2] not in dict_new:
                temp = [float(row[6]), int(row[5])]
                dict_new[row[2]] = temp
            else:
                dict_new[row[2]][0] += float(row[6])
                dict_new[row[2]][1] += int(row[5])
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    
    ax[0].bar([item for item in dict_new.keys()], 
              [round(item[0], 2) for item in dict_new.values()])
    ax[0].set_xlabel('Year') 
    ax[0].set_ylabel('Amount')
    ax[0].set_title('Amount v/s Year')
    ax[0].tick_params(axis='x', rotation=45) 
    
    
    ax[1].bar([item for item in dict_new.keys()], 
              [item[1] for item in dict_new.values()])
    ax[1].set_xlabel('Year') 
    ax[1].set_ylabel('Transactions') 
    ax[1].set_title('Transactions v/s Year')
    ax[1].tick_params(axis='x', rotation=45)  
    
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, dpi=100, format='png', bbox_inches='tight') 
    buffer.seek(0)
    image_bar = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return image_bar



                


    
    
    
    

