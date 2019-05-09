import boto3
import matplotlib.pyplot as plt
import datetime

dynamo_client = boto3.client('dynamodb')
dynamo_table = 'TrendSeekers'


def handler(inputf, context):

    for msg in inputf['Records']:
        # only consider insert events (ignore remove and modify)
        if msg['eventName'] != 'INSERT':
            return 0

        print('Received new vote!')

        # parse the table to get the data
        parsed_stream_event = read_stream_item(msg)
        print(parsed_stream_event)

        # get data from table - 7 days window - and plot it
        # todo: delete older data points?
        data = query_table()

    return 0


def read_stream_item(item):
    """ Parses dynamo stream records into less of a nightmare """

    parsed_msg = {'event': item['eventName']}

    for k in item['dynamodb']['NewImage']:
        parsed_msg[k] = item['dynamodb']['NewImage'][k]['S']

    return parsed_msg


def query_table():
    # ToDO: if the table gets big this will be paginated, and need to be read within a loop

    cutoff_date = (datetime.date.today() - datetime.timedelta(8)).strftime("%Y-%m-%d")

    resp= dynamo_client.scan(
            TableName=dynamo_table,
            IndexName='voteID',
            Select='ALL_ATTRIBUTES',
            ScanFilter='#tmp > :t',
            ExpressionAttributeValues={":t": {"S": cutoff_date}},
            ExpressionAttributeNames = {"#tmp": 'timestamp'})

    # parse items
    data_points = []
    for item in resp['Items']:
        data_points += {
                           item['voteID']['S']:
                               {
                                    'timestamp': item['timestamp']['S'],
                                    'choice': item['choice']['S']
                                }
                       },

    print('Found %i total data points for this time period' % len(data_points))

    # sample output:
    # [
        # {'f7b8add78c8618dbad11f6d30476c247': {'timestamp': '2018-10-05 18:53:48',
                                               # 'choice': 'Stumptown'}},
        # {'0048e0fcc2f193b9f019735c946af662': {'timestamp': '2018-10-05 18:54:29',
                                               # 'choice': 'BlueBottle'}}
    # ]

    return data_points

