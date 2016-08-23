import utils, re, random

class ChatbotSession(object):
	def __init__(self, aidata):
		self._aidata = aidata
		self._resolveFixedData()
		self.stack = []
		
	def processMessage(self, message):
		for id, value in self._aidata.items():
			type = value["type"]
			if type == "message":
				if value["trigger"] == "regex":
					for regex in value["triggers"]:
						match = re.match(regex, message, re.IGNORECASE)
						if match != None:
							return self.respond(id)
							
		return self.respond("fail")
		
	def respond(self, id, match=None):
		tag = self._aidata[id]
		
		if "condition" in tag.keys():
			condition = False
			for x in self.stack[-tag["conditionlevel"]:]:
				if tag["condition"] == x:
					condition = True
			if not condition:
				print("DEBUG: Condition %s failed. Level=%d, Stack=%s" % (tag["condition"], tag["conditionlevel"], str(self.stack)))
				return None
				
			print("DEBUG: Condition %s succeeded. Level=%d, Stack=%s" % (tag["condition"], tag["conditionlevel"], str(self.stack)))
				
		if "push" in tag.keys():
			self.stack.append(tag["push"])
			print("DEBUG: Pushed %s to stack! Stack is now %s." % (tag["push"], str(self.stack)))
		if "pop" in tag.keys():
			for pop in tag["pop"]:
				if self.stack[-1] == pop:
					self.stack.pop()
					print("DEBUG: Popped %s from stack! Stack is now %s." % (pop, str(self.stack)))
					break
		
		if "responses" in tag and len(tag["responses"]) > 0:
			message = random.choice(tag["responses"])
			return utils.resolveMessage(message, self._aidata, match)
		
	def _resolveFixedData(self):
		for id, value in self._aidata.items():
			if value["type"] == "fixed":
				value["fvalue"] = utils.resolveMessage(value["value"], self._aidata)