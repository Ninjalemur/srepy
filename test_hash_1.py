import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import numpy as np

def main(): #original seaboard version
	sns.set_style('whitegrid')
	data1 = pd.DataFrame(np.random.rand(17, 3), columns=['A', 'B', 'C']).assign(Location=1)
	data2 = pd.DataFrame(np.random.rand(17, 3) + 0.2, columns=['A', 'B', 'C']).assign(Location=2)
	data3 = pd.DataFrame(np.random.rand(17, 3) + 0.4, columns=['A', 'B', 'C']).assign(Location=3)
	cdf = pd.concat([data1, data2, data3])
	mdf = pd.melt(cdf, id_vars=['Location'], var_name=['Letter'])
	ax = sns.barplot(x="Location", y="value", hue="Letter", data=mdf, errwidth=0)

	num_locations = len(mdf.Location.unique())
	hatches = itertools.cycle(['/', '//', '+', '-', 'x', '\\', '*', 'o', 'O', '.'])
	for i, bar in enumerate(ax.patches):
		if i % num_locations == 0:
			hatch = next(hatches)
		bar.set_hatch(hatch)

	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, fancybox=True, shadow=True)
	fig = ax.get_figure()
	fig.savefig("foo.pdf", bbox_inches='tight')
	fig.savefig("foo.png", bbox_inches='tight')



	c = canvas.Canvas("test.pdf")
	# move the origin up and to the left
	c.translate(inch,inch)
	c.setFillColorRGB(1,0,1)
	c.drawImage("foo.png", 10, 10, 50, 50)
	c.drawImage("foo.png", 60, 60, 50, 50)

	c.showPage() #ends page. everything after is new page

	c.drawImage("foo.png", 10, 10, 50, 50)
	c.drawImage("foo.png", 60, 60, 50, 50)

	c.showPage()
	c.save()
	
	print("print complete. output files: foo.pdf, foo.png, test.pdf")

if __name__ == "__main__":
	main()

