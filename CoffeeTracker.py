import boto3
import datetime
import hashlib
import sys

dynamo_client = boto3.client('dynamodb')
dynamo_table = 'TrendSeekers'


def handler(inputf, context):

    # TODO: support double clicktype

    # sample trigger message
    # {'serialNumber': 'G030MD040444SC96', 'batteryVoltage': '1603mV', 'clickType': 'SINGLE'}

    if inputf['serialNumber'] == 'G030MD040444SC96':
        button = 'Stumptown'
    elif inputf['serialNumber'] == 'G030MD045236P11V':
        button = 'BlueBottle'
    else:
        print('ERROR invalid serial number')
        sys.exit(1)

    # build the item
    voteID = generatevoteId(button, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    item = {
        'voteID': voteID,
        'choice': button,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # add to the dynamo table
    put_item_in_dynamo(item, dynamo_table)

    print('Sent item to dynamo for choice %s with voteID %s' %(button, voteID))

    return

def put_item_in_dynamo(item, dynamo_table):

    for i in item:
        # dyDB requires data type to be declared (here, string)
        # this fn assumes all values are strings
        item[i] = {'S': str(item[i])}

    response = dynamo_client.put_item(
            TableName=dynamo_table,
            Item=item
    )
    print(response)
    return


def generatevoteId(*args):
    if len(args) == 0:
        raise ValueError('generatevoteId requires at least one argument.')
    else:
        s = ''.join(['%s' % arg for arg in args]).encode('utf-8')
    return hashlib.md5(s).hexdigest()
