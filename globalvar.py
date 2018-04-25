#!/usr/bin/python
# -*- coding: utf-8 -*-
class GlobalVar: 
	db_handle = 0 
	mq_client = 0 
def set_db_handle(db): 
	GlobalVar.db_handle = db 
def get_db_handle(): 
	return GlobalVar.db_handle 
def set_mq_client(mq_cli): 
	GlobalVar.mq_client = mq_cli 
def get_mq_client(): 
	return GlobalVar.mq_client 