import re, random

resolveRegex = re.compile(r"@\[(.+?)\]")
matchRegex = re.compile(r"$\[([0-9]+?)\]")

def resolveMessage(message, aidata, match=None):
	def resolveFunc(match):
		id = match.group(1)
		entry = aidata[id]
		
		type = entry["type"]
		if type == "fixed":
			return entry["fvalue"]
		elif type == "random":
			return random.choice(entry["values"])
		else:
			raise Exception("Resolve type is invalid!")
			
	resolved = resolveRegex.sub(resolveFunc, message)
	
	if match != None:
		resolved = matchRegex.sub(lambda m: match.group(int(m)), resolved)
		
	if resolved == message:
		return resolved
	else:
		return resolveMessage(resolved, aidata, match)