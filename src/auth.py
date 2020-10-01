import data
from error import InputError
import re
import random
import string

# Joseph Jeong is the only one that touched this sofar
# 29 SEP 2020

# checks that the email is validly formatted email
def regex_email_check(email):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email) == None:  
        raise InputError
    return

# check for a particular data type in users list
def check_in_users(data_type, users, item):
    focus_user = None
    for user in users:
        if user[data_type] == item:
            focus_user = user
            break
    return focus_user

# create a 20 character long ascii string for token    
def create_token(u_id, users):
    # create list of random characters and length of token
    valid_characters = string.ascii_letters + string.digits + string.punctuation
    token_length = 20

    # create a random token
    token = "".join(random.choices(valid_characters, k = token_length))

    # check that token is unique
    for user in users:
        if user['token'] == token:
            token = create_token(u_id, users)
            break

    return token

# create a random 32 bit unsigned integer to use as a u_id
def create_u_id(users):
    # create a random 32 bit unsigned integer
    u_id = random.randint(0, 0xFFFFFFFF)

    # simple recursive function to check whether u_id is unique
    for user in users:
        if user['u_id'] == u_id:
            u_id = create_u_id(u_id, users)
            break
    
    return u_id

# creates variable numbers at the end of the string
# flawed because it isn't optimal randomisation
# BUT it does the job -> every handle will ALWAYS be unique
# Even 10,000 of the same name...
def handle_variabliser(handle, variabliser_num, variabliser, users):

    # check if the handle is unique
    check = check_in_users('handle_str', users, handle)
    # if not modify it further

    if check != None:
        # check if there are any variabliser characters to iterate through
        # if not, variabilise more characters
        if not variabliser:
            variabliser = string.ascii_letters + string.digits
            # need to modify it further
            variabliser_num += 1
            
        # if true, try other variable characters
        else:
            # variabilise the string accordingly
            handle = handle[0:(-1 * variabliser_num)]
            
            for x in range(variabliser_num):
                character = random.choice(variabliser)
                variabliser = variabliser.replace(character, '')
                handle = handle + character
        
        handle = handle_variabliser(handle, variabliser_num, variabliser, users)
    return handle

# generates a unique handle
def handle_generator(name_first, name_last, users):

    # create base concatenation
    raw_concatenation = name_first + name_last
    if len(raw_concatenation) > 20:
        raw_concatenation = raw_concatenation[:20]
    
    # create a unique handle
    handle = handle_variabliser(raw_concatenation, 0, '', users)
    return handle

#handles error checking for auth_register
def auth_register_error_check(email, password, name_first, name_last):
    # initialise user data
    data.init_users()

    # check for valid input
    regex_email_check(email)
    
    # check if email is already used
    if check_in_users('email', data.users, email) != None:
        raise InputError

    # check len(password) >= 6
    if len(password) < 6:
        raise InputError

    #check first name matches requirements
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError

    #check Last Name matches requirements
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    return

# function to register a new user to the program
def auth_register(email, password, name_first, name_last):
    
    # checks for InputError
    auth_register_error_check(email, password, name_first, name_last)

    # create a unique u_id
    u_id = create_u_id(data.users)

    # creates a random and unique token
    token = create_token(u_id, data.users)

    # generate handle
    handle = handle_generator(name_first, name_last, data.users)

    # create and store a user object
    user = {
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'token': token,
        'password': password
    }
    data.append_users(user)

    # creates an object with u_id and token
    token_object = {
        'u_id': u_id,
        'token': token
    }

    return token_object

# used to log user into program
def auth_login(email, password):
    # initialise user data
    data.init_users()

    # check if email is valid
    regex_email_check(email)
    
    # check if email is used by user
    # will raise InputError if user is not stored
    focus_user = check_in_users('email', data.users, email)
    if focus_user == None:
        raise InputError

    # check password
    if focus_user['password'] != password:
        raise InputError

    # if everything checks out, create token
    u_id = focus_user['u_id']
    token = create_token(u_id, data.users)

    # creates an object with u_id and token
    token_object = {
        'u_id': u_id,
        'token': token
    }

    # add token to program
    data.add_token(token_object)

    return token_object

# used to log user out of program
def auth_logout(token):

    # search for token in token dict
    user = data.remove_token(token)

    # Returns accordingly if token is found
    if user == None:
        return {'is_success': False}
    else:
        return {'is_success': True}