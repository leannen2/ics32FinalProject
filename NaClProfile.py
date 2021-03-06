# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin

HOST = '168.235.86.101'
PORT = 3021

# TODO: Install the pynacl library so that the following modules are available
# to your program.
import json, os
from pathlib import Path
import pathlib

# TODO: Import the Profile and Post classes
from Profile import Profile, DsuFileError, DsuProfileError
from ds_messenger import DirectMessage,DirectMessenger
from Contact import Contact
import time
class MessengerProfile(Profile):
    def __init__(self):
        super().__init__(username='markLeanneYash', password='thisisapwd')
        self.sent_msg = {}
        self.retrieved_msg = {}
        # self.add_all_msg()

    def add_sent_msg(self, dir_msg: DirectMessage):
        """
        Appends sent messages as DirectMessage object into sent_msg attribute
        """
        if dir_msg.recipient not in self.retrieved_msg:
            self.retrieved_msg[dir_msg.recipient] = [dir_msg]
        self.retrieved_msg[dir_msg.recipient].append(dir_msg)

    def add_all_msg(self):
        """
        Adds all messages as DirectMessage objects into set_msg attribute
        """
        dsm = DirectMessenger(HOST, self.username, self.password)
        new_msg = dsm.retrieve_all()
        for msg in new_msg:
            if msg.sender not in self.retrieved_msg:
                self.retrieved_msg[msg.sender] = [msg]
            else:
                self.retrieved_msg[msg.sender].append(msg)

    def add_retrieved_msg(self):
        """
        Appends new retrieved messages as DirectMessage object into sent_msg attribute
        """
        dsm = DirectMessenger(HOST, self.username, self.password)
        new_msg = dsm.retrieve_new()
        if new_msg:
            for msg in new_msg:
                if msg.sender not in self.retrieved_msg:
                    self.retrieved_msg[msg.sender] = [msg]
                else:
                    self.retrieved_msg[msg.sender].append(msg)
            return True
        else:
            return False
        # self.save_profile('/Users/leannenguyen/Desktop/ics32FinalProject/messages.dsu')
    
    def add_contact_profile(self, contact_name):
        """
        Adds new contact into retrieved_msg
        """
        self.retrieved_msg[contact_name] = []

    def get_contact_objs(self):
        """
        Creates list of Contact objects from the retrieved messages and returns the list
        """
        contacts = []
        for contact in self.retrieved_msg:
            new_contact = Contact(contact, self.gen_msg_thread(contact))
            contacts.append(new_contact)
        return contacts

    def get_msg_from_contact(self, contact: str):
        """
        Returns list of retrieved messages as DirectMessage objects with given contact
        """

        if contact in self.retrieved_msg:
            return self.retrieved_msg[contact]
        else:
            print('contact not in retrived msg')
            return []

    def get_msg_log_for_all_contacts(self):
        """
        Returns dictionary of all contacts and their message logs
        """
        msg_dict = {}
        for contact in self.retrieved_msg:
            msg_dict[contact] = self.gen_msg_thread(contact)
        return msg_dict
    
    def gen_msg_thread(self, contact: str):
        """
        Generates and returns a string with all messages exchanged with a contact
        """
        retrieved = self.get_msg_from_contact(contact)
        msg_thread = ''
        for msg in retrieved:
            if msg.recipient == 'me':
                msg_thread += f'{msg.sender}: {msg.message}\n\n'
            else:
                msg_thread += f'me: {msg.message}\n\n'
        return msg_thread

    def get_msg(self):
        """
        Returns retrieved_msg
        """
        return self.retrieved_msg

    def load_profile(self, path: str) -> None:
        """
        Loads existing DSU File into profile object
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                # for msg_obj in obj['sent_msg']:
                #     msg = DirectMessage(msg_obj['recipient'], msg_obj['message'], msg_obj['timestamp'])
                #     self.sent_msg.append(msg)
                messages = obj['retrieved_msg']
                for contact, msg_list in messages.items():
                    self.retrieved_msg[contact] = []
                    for msg in msg_list:
                        msg_obj = DirectMessage(msg['recipient'], msg['message'], msg['timestamp'], msg['sender'])
                        self.retrieved_msg[contact].append(msg_obj)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
        

if __name__ == '__main__':
    profile = MessengerProfile()
    # profile.load_profile('/Users/leannenguyen/Desktop/ics32FinalProject/messages.dsu')
    p = pathlib.Path().resolve() / 'messages.dsu'
    profile.save_profile(p)
    messages = profile.retrieved_msg
    print(messages)
    blah = profile.add_retrieved_msg()
    print('blah', blah)
    # print(messages)
    # for message in messages:
    #     print(message, messages[message])
    # msg_thread = profile.gen_msg_thread('leanyash')

    # print(msg_thread)



    # msgs = profile.get_msg_log_for_all_contacts()
    # for contact, msg in msgs.items():
    #     print(contact)
    #     print(msg)
    # dsm = DirectMessenger(dsuserver=HOST, username='markLeanneYash', password='thisisapwd')
    # dsm.send(message='hi', recipient='mark')
    # dir_msg = DirectMessage('leanyash', 'hi', time.time())
    # profile.add_sent_msg(dir_msg)
    # contacts = profile.get_contact_objs()
    # for contact in contacts:
    #     print(contact.name, contact.msg_log)
    profile.add_retrieved_msg()

