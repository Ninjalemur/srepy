import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import numpy as np

class srepy_printer:
	""" 
	main routine that takes in inputs and generates output
	calls all the other classes and routines
	
	arguments (construction):
	cds_file: path to a cds file. requires fields x,y,z
	pds_file: path to a project/pds file
	"""

	def __init__(self,cds_data,pd_sdata,geo=None):
		self.raw_cds = cds_data
		self.raw_pds = pd_sdata

		if geo == None:
			pass
		else:
			#filter cds and pds by geo
			pass

	def print_plans(self,date_interval=3):
		""" 
		master routine that loops and prints all the plans
		"""
		if date_interval not in [3,6,12]:
			print("invalid date_interval {}. only 3,6,12 are accepted".format(date_interval))
			exit()
		self.date_interval = date_interval
		if self.sanity_checks() == True:
			pass
		else:
			print("Pre-run check failed. Please clean data before continuing")
			exit()
		
		self.get_date_backbone()
		
		#filter  cds data to date_backbone
		self.cds = self.raw_cds[self.raw_cds["Date"].isin(self.date_backbone)]

		de_ids = self.cds.Group.unique()
		#open pdf file
		for de_id in de_ids:
			curr_supply = self.cds.loc[cds['Group'] == de_id]

			#parse data frame. sum to building status. filter to demand_id

			# call each chart and write each chart to temp folder

			# assemble charts on page. create next page

		#save and close pdf file

	def get_date_backbone(self):
		"""
		gets the date backbone based on interval desired. checks latest A for feed_date
		"""
		max_actual_date = self.cds.loc[self.cds['Forecast_version'] == "A"]["Date"].max()
		date_backbone = self.quarters_range("2018-12-31")
		self.date_backbone = date_backbone

	def quarters_range(self,date_from, years_ahead=10):
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
		for curr_year in range(start_year,start_year+years_ahead+1):
			for curr_mm_dd in mm_dd_suffixes:
				curr_date = str(curr_year)+curr_mm_dd
				if curr_date >= date_from:
					result.append(curr_date)

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
	outouts:
	"""
	def __init__(self):
		pass
	def generate_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""
		pass

class cap_req_chart:
	""" 
	generates the capacity required chart and writes it to temp_dir
	args:
	outouts:
	"""
	def __init__(self):
		pass
	def generate_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""
		pass

class suit_status_chart:
	""" 
	generates the suit status chart and writes it to temp_dir
	args:
	outouts:
	"""
	def __init__(self):
		pass
	def generate_chart(self):
		""" 
		main routine that does the data parsing and generates chart, and saves chart
		"""
		pass

class pds_chart:
	""" 
	generates the suit status chart and writes it to temp_dir
	args:
	outouts:
	"""
	def __init__(self):
		pass
	def generate_chart(self):
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
	
	printer = srepy_printer(cds,pds)
	printer.print_plans()



if __name__ == "__main__":
	main()

