### Declarations packages and libraries
import boto3
import datetime
import pandas as pd

### Create boto3 client for Cost Explorer
client = boto3.client('ce')


### Function to get the cost analysis

def cost_analysis(start_date=None, end_date=None, granularity='DAILY', tag_key='None',frequency='WEEKLY'):
    
    today = datetime.date.today()
    if start_date is None and end_date is None:
        end_date = today - datetime.timedelta(days=1)

        if frequency == 'WEEKLY':
            print('weekly analysis')
            start_date = str(today - datetime.timedelta(days=7))
            response = get_analysis(start_date=start_date, end_date=end_date, granularity=granularity, tag_key=tag_key)
            print(response)

        elif frequency == 'MONTHLY':
            print('monthly analysis')
            start_date = str(today - datetime.timedelta(days=30))
            response = get_analysis(start_date=start_date, end_date=end_date, granularity=granularity, tag_key=tag_key)
            print(response)

        elif frequency == 'YEARLY':
            print('yearly analysis')
            start_date = str(today - datetime.timedelta(days=365))
            response = get_analysis(start_date=start_date, end_date=end_date, granularity=granularity, tag_key=tag_key)
            print(response)

    elif frequency == 'CUSTOM':
        print('custom analysis')
        response = get_analysis(start_date=start_date, end_date=end_date, granularity=granularity, tag_key=tag_key)
        print(response)

    else:
        print('Invalid input parameters')
        response = 'Invalid input parameters'
    
    if response!= 'Invalid frequency':
        save_to_excel(response)
    return response


def get_analysis(start_date, end_date, granularity,tag_key='dev'):
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': str(start_date),
            'End': str(end_date)
        },
        Granularity= granularity,
        Metrics=[ 'NetAmortizedCost'],
        Filter={
            'Not': {
                'Dimensions': {
                    'Key': 'RECORD_TYPE',
                    'Values': [
                        'Tax', 'Credit', 'UpfrontAmortizedCost',
                    ]
                }
            }
        },
    )
    return response



### save the cost analysis to a Excel file

def save_to_excel(response=None):
    if response is None:
        print('No data to save')
    else:
        df = pd.DataFrame(response['ResultsByTime'])
        df['start_Date'] = df['TimePeriod'].apply(lambda x: x['Start'])
        df['end_Date'] = df['TimePeriod'].apply(lambda x: x['End'])
        df['Amount'] = df['Total'].apply(lambda x: x['NetAmortizedCost']['Amount'])
        df['Unit'] = df['Total'].apply(lambda x: x['NetAmortizedCost']['Unit'])
        df = df[['start_Date', 'end_Date', 'Amount', 'Unit']]
        df.to_excel('cost_analysis.xlsx', index=False)
        print('Data saved to Excel file')

if __name__ == "__main__":
    # cost_analysis(start_date='2023-10-01', end_date='2023-10-31', granularity='DAILY', tag_key='None',frequency='CUSTOM')
    cost_analysis()
