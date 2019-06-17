f = open("work.txt", "a")

if f.read(1):
	print('empty')   
else:
	# file is empty
	print("weird")
			