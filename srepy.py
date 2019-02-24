import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import random
import string
import numpy as np
import shutil
import os

class srepy_printer:
	""" 
	main routine that takes in inputs and generates output
	calls all the other classes and routines
	
	arguments (construction):
	cds_file: path to a cds file. requires fields x,y,z
	pds_file: path to a project/pds file
	geo (optional): optional string argument for geo to filter to. None means all geos will be printed
	date_interval (optional): 3,6,12. Whether to display quarterly, 6-monthly, or annual intervals
	temp_dir (optional): path to temp directory where chart files are staged before assembling to pdf. If left blank, random one is generated, allowing multiple instances to be run simultaneously
	"""

	def __init__(self,cds_data,pds_data,geo=None,date_interval=12,num_intervals=10,temp_dir=None,output_file="test.pdf"):
		self.raw_cds = cds_data
		self.raw_pds = pds_data
		self.output_file = output_file

		if geo == None:
			pass
		else:
			#filter cds and pds by geo
			self.raw_cds = self.raw_cds.loc[self.raw_cds['Geo'] == geo]
			self.raw_pds = self.raw_pds.loc[self.raw_pds['Geo'] == geo]
		if temp_dir == None:
			self.temp_dir = "_temp_{}/".format(
					''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
					)
		else:
			self.temp_dir=temp_dir

		if date_interval not in [3,6,12]:
			print("invalid date_interval {}. only 3,6,12 are accepted".format(date_interval))
			exit()
		self.date_interval = date_interval

		self.num_intervals = num_intervals

	def print_plans(self):
		""" 
		master routine that loops and prints all the plans
		"""
		if self.sanity_checks() == True:
			pass
		else:
			print("Pre-run check failed. Please clean data before continuing")
			exit()
		
		self.create_fresh_dir(self.temp_dir)
		
		self.cds = self.raw_cds

		#convert Status into Existing, Not Existing
		self.cds['Status'] = np.where(self.cds['Status'] == "Existing", "Existing", "NotExisting")
		
		# get dates that are relevant to current chosen interval
		self.get_date_backbone()
		
		#filter  cds data to date_backbone
		self.cds = self.cds[self.cds["Date"].isin(self.date_backbone)]

		self.supply = self.raw_cds[self.raw_cds["Suit"].notnull()]
		self.demand = self.raw_cds[self.raw_cds["Consumption"].notnull()]
	
		de_ids = self.cds.Group.unique()
		#open pdf file
		c = canvas.Canvas(self.output_file)
		for de_id in de_ids:
			#filter to current demand_id
			curr_supply = self.supply.loc[self.cds['Group'] == de_id]

			#parse data frame. sum to building status. filter to demand_id
			curr_supply = curr_supply[['Date', 'Suit','Status','Capacity']]
			#curr_supply = curr_supply.groupby(['Date', 'Suit','Status'])["Capacity"].apply(lambda x : x.astype(int).sum())

			# call each chart and write each chart to temp folder
			sup = snd_chart(curr_supply,self.temp_dir+"snd.png",x_ticks=self.date_backbone)
			sup.print_chart()

			cap_req = cap_req_chart(self.cds,self.temp_dir+"cap_req.png")
			cap_req.print_chart()

			suit_status = suit_status_chart(self.cds,self.temp_dir+"suit_status.png")
			suit_status.print_chart()

			sup_chart = snd_chart(self.cds,self.temp_dir+"snd.png")
			sup_chart.print_chart()

			pds = pds_chart(self.cds,self.temp_dir+"snd.png")
			pds.print_chart()

			# assemble charts on page. create next page
			c.translate(inch,inch)
			c.setFillColorRGB(1,0,1)
			c.drawImage("foo.png", 10, 10, 50, 50)
			c.drawImage("foo.png", 60, 60, 50, 50)

			c.showPage() #ends page. everything after is new page

			c.drawImage("foo.png", 10, 10, 50, 50)
			c.drawImage("foo.png", 60, 60, 50, 50)

			c.showPage()
		c.save()
		

		#save and close pdf file
		shutil.rmtree(self.temp_dir)
	def create_fresh_dir(self,target_dir):
		if os.path.exists(target_dir):
			shutil.rmtree(target_dir)
		else:
			os.mkdir(target_dir)	

	def get_date_backbone(self):
		"""
		gets the date backbone based on interval desired. checks latest A for feed_date
		"""
		max_actual_date = self.raw_cds.loc[self.raw_cds['Forecast_version'] == "A"]["Date"].max()
		date_backbone = self.quarters_range(max_actual_date)
		self.date_backbone = date_backbone

	def quarters_range(self,date_from):
		"""
		gets the quarters from date_from to date_to
		date_to: string (YYYY-MM-DD) of date to count until
		date_from: string of date to count from
		"""

		result = []
		mm_dd_suffixes = ["-03-31","-06-30","-09-30","-12-31"]

		if self.date_interval == 3:
			pass
		elif self.date_interval == 6:
			mm_dd_suffixes = [mm_dd_suffixes[1],mm_dd_suffixes[3]]
		elif self.date_interval == 12:
			mm_dd_suffixes = [mm_dd_suffixes[3]] ### check this

		try:
			start_year = int(date_from[:4])
		except ValueError:
			print("cannot extract year from start year {}".format(date_from))
			exit()

		i=0
		while len(result) < self.num_intervals:
		#for curr_year in range(start_year,start_year+years_ahead+1):
			for curr_mm_dd in mm_dd_suffixes:
				curr_date = str(start_year+i)+curr_mm_dd
				if curr_date >= date_from:
					result.append(curr_date)
			i+=1
		return(result)
	

	def sanity_checks(self):
		""" 
		checks for certain criteria. fails and stops if criteria not met
		print errors as they arise?
		"""
		return(True)

class snd_chart:
	""" 
	generates the snd chart and writes it to temp_dir
	args: 
		data: data_frame of input data
		output_file: path where output file should be saved
	outouts: prints output_file to output file path
	"""
	def __init__(self,data,output_file,x_ticks=None,colours=["red","blue","green","yellow","purple","orange"]):
		self.data = data
		self.output_file = output_file
		self.colours = colours
		self.x_ticks = x_ticks
	def print_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""

		#gets dates if not supplied. else use supplied dates
		if self.x_ticks == None:
			dates = self.data[["Date"]].drop_duplicates()
			dates = dates.sort_values(by=['Date'],ascending=[True]).reset_index(drop=True)
			dates = dates["Date"].tolist()
		else:
			dates = self.x_ticks
			dates.sort()
		
		suits = self.data[["Suit"]].drop_duplicates()
		suits = suits.sort_values(by=['Suit'],ascending=[True]).reset_index(drop=True)

		suit_status = self.data[["Suit","Status"]].drop_duplicates()
		suit_status = suit_status.sort_values(by=['Status', 'Suit'],ascending=[True,True]).reset_index(drop=True)

		for index,row in suit_status.iterrows():
			suit = row['Suit']
			status = row['Status']

			#get all date rows for this suit status combi
			single_suit_status = self.data.loc[(self.data['Suit'] == row['Suit']) & (self.data['Status'] == row['Status'])]

			#get index number of suit within suit list
			suit_no = suits[suits['Suit']==suit].index.values.astype(int)[0]

			#get status pattern and colour
			edgecolour = self.colours[suit_no]
			if status == "Existing":
				pattern = None
				colour = self.colours[suit_no]
			else:
				pattern = "//"
				colour = "white"

			#convert single suit status into list of data, depending on capacity at each date
			suit_capacity_over_time = []
			for each_date in dates:
				curr_date_capacity = single_suit_status.loc[(self.data['Date'] == each_date)]
				curr_date_capacity = curr_date_capacity[["Capacity"]].sum()
				curr_date_capacity = curr_date_capacity["Capacity"].tolist()
				suit_capacity_over_time.append(curr_date_capacity)
			suit_capacity_over_time = np.array(suit_capacity_over_time)


			plt.bar(
					range(len(dates)), 
					suit_capacity_over_time, 
					color=colour,
					#linewidth=line_width,
					edgecolor=edgecolour,
					hatch = pattern
					)
			plt.show()
			exit()



class cap_req_chart:
	""" 
	generates the capacity required chart and writes it to temp_dir
	args: 
		data: data_frame of input data
		output_file: path where output file should be saved
	outouts: prints output_file to output file path
	"""
	def __init__(self,data,output_file):
		pass
	def print_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""
		pass

class suit_status_chart:
	""" 
	generates the suit status chart and writes it to temp_dir
	args: 
		data: data_frame of input data
		output_file: path where output file should be saved
	outouts: prints output_file to output file path
	"""
	def __init__(self,data,output_file):
		pass
	def print_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""
		pass

class pds_chart:
	""" 
	generates the pds chart and writes it to temp_dir
	args: 
		data: data_frame of input data
		output_file: path where output file should be saved
	outouts: prints output_file to output file path
	"""
	def __init__(self,data,output_file):
		pass
	def print_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""
		pass

def main():
	input_folder =  "./input/"
	cds_file = "calc_data_source.csv"
	project_file = "proj.csv"

	output_folder = "./output/"

	cds_path = input_folder+cds_file
	pds_path = input_folder+project_file

	cds = pd.read_csv(cds_path)
	pds = pd.read_csv(cds_path)
	
	printer = srepy_printer(cds,pds,geo="CE70")
	printer.print_plans()



if __name__ == "__main__":
	main()

