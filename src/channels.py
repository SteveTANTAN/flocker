import data
import random
from error import InputError
import auth
from other import clear

def channels_list(token):
    #initialise the channels list
    data.init_channels()
    
    # initialise the users list
    data.init_users()
    
    #get the u_id of the authorised user
    for i in data.users:
        if i['token'] == token:
            user_id = i['u_id']
            break   
    #make a loop to check each channels       
    i = 0
    channel_list = []
    for i in range(len(data.channels)):
        j = 0
        #check if the user in this channel
        for j in range(len(data.channels[i]['all_members'])):
            if data.channels[i]['all_members'][j]['u_id'] == user_id:        
                channel_list.append(data.channels[i])
        
    return channel_list
def channels_listall(token):

    #just return all channels? sure about that?
    return data.channels
    
def create_channel_id(channels):
    
    # create a random 32 bit unsigned integer
    channel_id = random.randint(0, 0xFFFFFFFF)

    # a recursive function to check whether the channel_id is unique
    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel_id = create_channel_id(channels)
            break
    
    return channel_id

def channels_create(token, name, is_public):    
    #initialise the channels list
    data.init_channels()
    # initialise the users list
    data.init_users()
    
    if len(name) > 20:
        raise InputError
        return
    
    for i in data.users:
        if i['token'] == token:
            owner_id = i['u_id']
            owner_FN = i['name_first']
            owner_LN = i['name_last']
            break    
    
    channel_id = create_channel_id(data.channels)
    channel_new = {
        'name': name,
        'channel_id':channel_id,
        'owner': [
            {
                'u_id': owner_id,
                'name_first': owner_FN,
                'name_last': owner_LN,
            }
        ],
        'all_members': [
            {
                'u_id': owner_id,
                'name_first': owner_FN,
                'name_last': owner_LN,
            }
        ],   
        'is_public': is_public,
    }
    
    data.append_channels(channel_new)
    

    return channel_id
'''
clear()
#initialise the channels list
data.init_channels()
# initialise the users list
data.init_users()
#create two user and take their id and token
user1 = auth.auth_register('1234@test.com', 'password', 'FirstN', 'LastN')
user1 = auth.auth_login('1234@test.com', 'password')
u1_id = user1['u_id']
u1_token = user1['token']

user2 = auth.auth_register('2345@test.com', 'password', 'FirstN2', 'LastN2')
user2 = auth.auth_login('2345@test.com', 'password')
u2_id = user2['u_id']
u2_token = user2['token']

#create a channel by user1 in channels and return its channel id
channel_1_id = channels_create(u1_token,'team',True)

#create a channel by user2 in channels and return its channel id
channel_2_id = channels_create(u2_token,'team2',True)

print(data.channels)

channel_listall = [
        {
            'name':'team',
            'channel_id':channel_1_id,
            'owner':[
                {
                    'u_id': u1_id,
                    'name_first': 'FirstN',
                    'name_last': 'LastN'
                }
            ],
            'all_members':[
                {
                    'u_id': u1_id,
                    'name_first': 'FirstN',
                    'name_last': 'LastN'
                }
            ],
            'is_public':True
        } , {
            'name':'team2',
            'channel_id':channel_2_id,
            'owner':[
                {
                    'u_id': u2_id,
                    'name_first': 'FirstN2',
                    'name_last': 'LastN2'
                }
            ],
            'all_members':[
                {
                    'u_id': u2_id,
                    'name_first': 'FirstN2',
                    'name_last': 'LastN2'
                }
            ],            
            'is_public':True
        }
    ]
print(channel_listall)
print(channels_listall(u1_token))
if channel_listall == channels_listall(u1_token):
    print("yes")
'''
