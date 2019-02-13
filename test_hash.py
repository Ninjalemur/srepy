import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import numpy as np

def misc(): #original seaboard version
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



def main(): #matplotlib version
	input_folder =  "./input/"
	cds_file = "calc_data_source.csv"
	project_file = "proj.csv"


	cds = pd.read_csv(input_folder+cds_file)
	proj = pd.read_csv(input_folder+project_file)
	
	de_ids = cds.Group.unique()
	
	#drop geo,region just for test
	cds = cds.drop(['Geo'],axis=1) 
	cds = cds.drop(['Region'],axis=1) 
	cds = cds.drop(['Consumption'],axis=1) 
	cds = cds.drop(['Suit'],axis=1) 
	cds = cds[pd.notnull(cds['Capacity'])]

	for de_id in de_ids:
		curr_supply = cds.loc[cds['Group'] == de_id]
		curr_supply = curr_supply.drop(['Group'],axis=1) #drop de_id column
		print(curr_supply)
		curr_supply_pivot = curr_supply.pivot_table(
				#index=["Date","Suit"],
				index=["Date"],
				columns="Status",
				values="Capacity"
				)
		#print(curr_supply_pivot)

		patterns = ( '\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/','\\','/')
		
		supply_chart = curr_supply_pivot[["Existing","Target"]].plot.bar(stacked=True)
		for i,bar in enumerate(supply_chart.patches):
			bar.set_hatch(patterns[i])
		plt.show()
		break

if __name__ == "__main__":
	main()

