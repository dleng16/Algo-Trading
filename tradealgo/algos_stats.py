from matplotlib import pyplot as plt
import matplotlib.ticker
import pandas






class algo_analysis:

	def __init__(self, file = None):
		self.file = file
		f = open(file, 'r')
		line_text = None
		data = []
		self.variables = None

		line = f.readline()
		self.variables = line.split()

		line = f.readline()
		for i in line.split():
			temp = []
			temp.append(float(i))
			data.append(temp)
		while line:
			line = f.readline()
			line = line.split()
			for i in range(len(line)):
				data[i].append(float(line[i]))

		data[0] = [60*int(i) for i in data[0]]
		data[0] = [data[0][i] + int(data[1][i]) for i in range(len(data[0]))] # convert hours and minutes to total minutes of day (combine data)

		#data[0] = 60*data[0] + data[1]
		#data = float(data)
		j = 0
		for i in data:
			plt.figure(j)
			plt.plot(data[0], i)
			plt.xlabel(self.variables[j])
			#axes = plt.axes()
			#axes.get_xaxis().get_major_formatter().set_useOffset(False)
			plt.locator_params(axis='y', nbins=20)
			print(self.variables[j])
			j = j + 1


		plt.show()


		#print(data)

