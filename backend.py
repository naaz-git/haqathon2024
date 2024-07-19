from Retriever import *
from ModelManager import ModelManager

def get_response(mod, msg):
    #mod = ModelManager()
    return mod.prompt_model(msg)

def create_retriever(team_id):
    retriever_obj = Retriever()
    retriever_obj.retrieve_data(team_id)

# Not sure what send_message does? 
def send_message():
    msg = input()
    return msg
    
def get_teams():
    #hardcoded for now but in the future should be imported from somewhere
    return ["hardware", "software", "devops"]
