from collections import OrderedDict

class Record:
	def __init__(self):
		self.__dict__['_inner'] = OrderedDict()
		
	def __setattr__(self,k,v):			
		self.__dict__['_inner'][k] = v
		
	def __getattr__(self,k):
		return self.__dict__['_inner'][k]
		
	def __setitem__(self,k,v):			
		self.__dict__['_inner'][k] = v
	
	def __getitem__(self,k):			
		return self.__dict__['_inner'][k]	
		
	def items(self):		
		return self._inner.items()
	
	def as_dict(self):
		return self.__dict__['_inner']
	
		
	def as_list(self):
		return self.__dict__['_inner']
		
		ls = []
		for k,v in self.items():
			ls.append((k,v))
		return ls

	@classmethod
	def from_dict(Cls, kvs):
		r = Cls()
		r.__dict__['_inner'] = kvs
		return r


	@classmethod
	def from_list(Cls, kvs):
		r = Cls()
		for k,v in kvs.items():
			r[k] = v
		return r

