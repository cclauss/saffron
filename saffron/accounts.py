import subprocess
import argparse
import random
import pprint
import json
import os
from web3 import Web3
from web3.personal import Personal
from web3.eth import Eth
from saffron.utils import create_account
from saffron.genesis import Chain
from saffron.database import account_exists

def from_db(name=None, address=None):
	'''initialize an account

	    Args:
	        name (str): name of token.
	        address (str): chain address.

	    Returns:
	        str: return value of init_account
	'''
	assert name != None or address != None, 'Supply either a name or an address to query the DB with'
	print('{}, {}'.format(address, name))
	a = database.init_account(name=name, address=address)
	return a

def new_account_to_db(name=None, password=None):
	'''initialize an account on the chain

	    Args:
	        name (str): name of token.
	        password (str): account password for chain.

	'''
	assert name and password, 'Name and password required to create a new account'
	assert account_exists(name=name) == None, 'Choose a unique name for your account'
	address = create_account(password)
	Chain().database.insert_account(name, address)

class Account:
	'''An interface to an account

	    Attributes:
	        _address (str): chain address.
	        _name (str): name of token/chain.

		Ethereum methods :
			self.p.importRawKey
			self.p.newAccount
			self.p.listAccounts
			self.p.getListAccounts
			self.p.sendTransaction
			self.p.signAndSendTransaction
			self.p.lockAccount
			self.p.unlockAccount
			self.p.sign
			self.p.ecRecover
	    '''
	def __init__(self, name=None, address=None, password=None, chain=None):
		'''initialize the class
			TODO : document chain ()
			TODO : salt passwords with bcrypt or better

			Args:
		        _address (str): chain address.
	        	_name (str): name of token/chain.
		        password (str): password to account

		'''
		_name, _address = account_exists(name=name)
		if not _address:
			self.address = create_account(password)
			self.name = name
			Chain().database.insert_account(name, self.address)
			self._new_account = True
		else:
			self.name = _name
			self.address = _address
			self._new_account = False
		node_info = json.loads(open(os.environ['NODE_INFO_JSON']).read())
		self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:{port}".format(port=node_info.get('rpcport'))))
		self.p = Personal(self.web3)

	@classmethod
	def _from_db(self, name=None, address=None):
		return

	def balance(self):
		return Eth.get_balance(self.address)


