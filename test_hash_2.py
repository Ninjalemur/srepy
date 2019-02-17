import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import numpy as np

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
		#plt.show()
		plt.savefig("matplotlib.png")
		print("chart saved as matplotlib.png")
		break

if __name__ == "__main__":
	main()

