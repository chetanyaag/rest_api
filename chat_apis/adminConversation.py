def admin_conversation(number, message, chat_user):

    #here only conversation
    if chat_user==False:
        return "Not in Database"

    chat_state = chat_user.get('chat_state')
    if chat_state == "0":
        # todo set chat_state=1
        return "Hi Admin\n Please Enter the Employee Code." 

    if chat_state == "1":
        #check message
        if True:
            # set state = 2
            return "Please Enter the month and year in mm/yy format."
        else:
            return "Sorry, This Employee does not exits in my database"

        
    if chat_state == "2":
        #check message in db
        if True:
            return "data"
        else:
            return "Hi Admin, \nYou can initiate the chat."
    # if chat_state == "0":
    #     pass