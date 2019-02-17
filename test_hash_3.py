import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon

def main(): #matplotlib coloured hash version

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	# draw hatch
	ax1.bar(range(1, 5), range(1, 5), color='none', edgecolor='red', hatch="/", lw=1., zorder = 0)
	# draw edge
	ax1.bar(range(1, 5), range(1, 5), color='none', edgecolor='k', zorder=1, lw=2.)

	ax1.set_xticks([1.5, 2.5, 3.5, 4.5])
	plt.savefig("hatch_line.png")
	#plt.show()
	print("saved image as hatch_line.png")
	

if __name__ == "__main__":
	main()

