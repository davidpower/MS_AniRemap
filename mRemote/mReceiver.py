# -*- coding:utf-8 -*-

from pymel.core import *
import socket


def Singleton(cls):
	instances = {}
	
	def Instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return Instance

@Singleton
class MReceiver(object):
	"""docstring for MReceiver"""
	def __init__(self):
		self.host = ''
		self.port = ''
		self.maps = {}

	def portOpen(self, mode, langue, port= None):
		self._setMode(mode)
		self._setPort(port)
		ipaddr = self._getAddr()
		commandPort(n= ipaddr, stp= langue)
		self.maps[self.port] = {'ipaddr' : ipaddr,
								'langue' : langue,
								'status' : True}
		return ipaddr

	def portClose(self, port):
		if port == 0:
			for p in self.maps:
				if self.maps[p]['status']:
					self.portClose(p)
			return None
		ipaddr = self.maps[str(port)]['ipaddr']
		commandPort(n= ipaddr, cl= 1)
		if not commandPort(ipaddr, q= 1):
			self.maps[str(port)]['status'] = False

	def portCheck(self):
		def _printPort(portDict, s):
			for p in portDict:
				l = portDict[p]['langue']
				m = portDict[p]['ipaddr'].rjust(22, ' ')
				p = p.rjust(6, ' ')
				print '%s %s %s @ %s' % (p, s, m, l)
		port_on, port_off = self._portStatus()
		print '\n' + '> '*25
		print 'commandPort ON\n' + '- '*25
		_printPort(port_on, '|')
		print '. '*25
		print 'commandPort OFF\n' + '- '*25
		_printPort(port_off, 'X')
		print '< '*25

	def _portStatus(self):
		port_on = {}
		port_off= {}
		for p in self.maps:
			if self.maps[p]['status']:
				port_on[p] = self.maps[p]
			else:
				port_off[p]= self.maps[p]
		return port_on, port_off

	def _setMode(self, mode):
		if mode == 'LAN':
			self.host = socket.gethostbyname(socket.gethostname())
		if mode == 'local':
			self.host = 'localhost'

	def _setPort(self, port):
		""" get free port """
		if port:
			self.port = port
			return None
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('',0))
		s.listen(1)
		self.port = str(s.getsockname()[1])
		s.close()

	def _getAddr(self):
		return '%s:%s' % (self.host, self.port)