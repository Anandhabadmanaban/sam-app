import json
import boto3
import datetime
import os

# AWS Clients
ec2 = boto3.client('ec2',region_name=os.environ.get('AWS_REGION', 'us-east-1'))
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'VPCRecords')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod')
        if method == 'POST':
            return create_vpc(event)
        elif method == 'GET':
            return get_vpc(event)
        else:
            return respond(400, {"message": "Invalid HTTP method"})
    except Exception as e:
        return respond(500, {"error": str(e)})

def create_vpc(event):
    data = json.loads(event.get('body', '{}'))
    cidr_block = data.get('cidr_block', '10.0.0.0/16')
    subnet_cidrs = data.get('subnet_cidrs', ['10.0.1.0/24', '10.0.2.0/24'])
    
    # Create VPC
    vpc_resp = ec2.create_vpc(CidrBlock=cidr_block)
    vpc_id = vpc_resp['Vpc']['VpcId']
    
    # Enable DNS Hostnames
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    
    # Create subnets
    subnet_ids = []
    for subnet_cidr in subnet_cidrs:
        subnet_resp = ec2.create_subnet(VpcId=vpc_id, CidrBlock=subnet_cidr)
        subnet_ids.append(subnet_resp['Subnet']['SubnetId'])
    
    # Store in DynamoDB
    table.put_item(Item={
        'vpc_id': vpc_id,
        'subnet_ids': subnet_ids,
        'region': ec2.meta.region_name,
        'created_at': datetime.datetime.utcnow().isoformat()
    })
    
    return respond(200, {'vpc_id': vpc_id, 'subnet_ids': subnet_ids})

def get_vpc(event):
    params = event.get('queryStringParameters') or {}
    vpc_id = params.get('vpc_id')
    if not vpc_id:
        return respond(400, {"message": "Missing vpc_id parameter"})
    
    try:
        resp = table.get_item(Key={'vpc_id': vpc_id})
    except Exception as e:
        return respond(500, {"error": str(e)})
    
    if 'Item' not in resp:
        return respond(404, {"message": "VPC not found"})
    
    return respond(200, resp['Item'])

def respond(status, body):
    return {
        'statusCode': status,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }


#Once deployed, note the API Gateway endpoint:

#POST /create-vpc

#GET /get-vpc?vpc_id=<vpc_id>'''

# curl -X POST https://dyc35ookp0.execute-api.us-east-1.amazonaws.com/Prod/create-vpc -H "Content-Type: application/json" -d '{"cidr_block": "10.1.0.0/16", "subnet_cidrs": ["10.1.1.0/24","10.1.2.0/24"]}'

 # curl -X POST https://dyc35ookp0.execute-api.us-east-1.amazonaws.com/Prod/create-vpc \
#-H "Content-Type: application/json" \
#-d '{"cidr_block": "10.1.0.0/16", "subnet_cidrs": ["10.1.1.0/24","10.1.2.0/24"]}'



