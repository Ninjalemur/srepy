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

	def __init__(self,cds_data,pd_sdata,geo=None,date_interval=3,temp_dir=None,output_file="test.pdf"):
		self.raw_cds = cds_data
		self.raw_pds = pd_sdata
		self.output_file = output_file

		if geo == None:
			pass
		else:
			#filter cds and pds by geo
			pass
		if temp_dir == None:
			self.temp_dir = "{}/".format(
					''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
					)
		else:
			self.temp_dir=temp_dir

		if date_interval not in [3,6,12]:
			print("invalid date_interval {}. only 3,6,12 are accepted".format(date_interval))
			exit()
		self.date_interval = date_interval

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
		print("dirs ok")
		exit()
		
		self.get_date_backbone()
		
		#filter  cds data to date_backbone
		self.cds = self.raw_cds[self.raw_cds["Date"].isin(self.date_backbone)]

		de_ids = self.cds.Group.unique()
		#open pdf file
		c = canvas.Canvas(self.output_file)
		for de_id in de_ids:
			curr_supply = self.cds.loc[self.cds['Group'] == de_id]

			#parse data frame. sum to building status. filter to demand_id

			# call each chart and write each chart to temp folder
			sup = snd_chart(self.cds,self.temp_dir+"snd.png")
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
	
	printer = srepy_printer(cds,pds)
	printer.print_plans()



if __name__ == "__main__":
	main()

