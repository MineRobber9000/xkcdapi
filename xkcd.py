import requests

class InvalidComic(Exception):
	pass

class Comic(object):
	def __init__(self,num=None,donterror=False):
		if num:
			r = requests.get("https://xkcd.com/{!s}/info.0.json".format(num))
			if r.status_code!=200:
				if donterror:
					self.num = num
					self.fakeit = True
				else:
					raise InvalidComic("Invalid XKCD comic \""+str(num)+"\"")
			else:
				self.__dict__.update(r.json())
				self.fakeit = False
		else:
			r = requests.get("https://xkcd.com/info.0.json")
			if r.status_code!=200:
				if donterror:
					self.num = 0
					self.fakeit = True
				else:
					raise InvalidComic("Cannot locate latest comic.")
			else:
				self.__dict__.update(r.json())
				self.fakeit = False

	def __getattr__(self,k):
		if k=="fakeit" or k=="num":
			return object.__getattr__(self,k)
		if self.fakeit:
			return ""
		else:
			return object.__getattr__(self,k)
