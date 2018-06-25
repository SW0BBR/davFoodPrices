import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import math
import numpy  as np
def calcMean(dataFrame, query=None):
	if(query):
		dataFrame = dataFrame.query(query)
	return dataFrame.price.mean()


def calcStandardDev(dataFrame, query=None):
	if(query):
		dataFrame = dataFrame.query(query) 
	return dataFrame.price.std()

def findOutliers(dataFrame, threshold):
	mean = dataFrame.price.mean()
	stdev = dataFrame.price.std()
	abs_threshold = threshold * stdev
	mask = (dataFrame['price'] < mean - abs_threshold) | (dataFrame['price'] > mean + abs_threshold)
	return dataFrame[mask]
	

def fullEDA(dataFrame, query): 
	df = dataFrame.query(query)
	print("Statistics for " + query + ":")
	print("Number of rows: {}".format(df.shape[0]))
	print("Mean price: {}".format(df.price.mean()))
	print("Standard Deviation: {}".format(df.price.std()))

	t = 1
	outliers = findOutliers(df, t)
	prevN_inliers = 0
	while outliers.shape[0] > 0:
		N_outliers = outliers.shape[0]
		N_inliers = df.shape[0] - N_outliers
		P_inliers_cumul = round(float(N_inliers * 100) / df.shape[0], 1)
		P_inliers = round(float((N_inliers-prevN_inliers) * 100) / df.shape[0], 1)
		print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows ({} %)".format(t-1, t, N_inliers-prevN_inliers, P_inliers, N_inliers, P_inliers_cumul))
		t = t + 1
		prevN_inliers = N_inliers
		outliers = findOutliers(df, t)
	print("Rows between {} and {} standard deviations: {} ({}%), cumulative: {} rows (100 %)".format(t-1, t, df.shape[0]-prevN_inliers, round(float((df.shape[0]-prevN_inliers)*100)/df.shape[0], 1), df.shape[0]))

def boxPlot(dataFrame, query):
	dataFrame = dataFrame.query(query)
	dataFrame.boxplot("price")
	plt.show()



# Chart price history based on a query.
# For every unique currency included in the query, a different plot is generated.
# If such a plot includes multiple products, it takes the mean price of each product (from all countries)
# If such a plot includes only one product, it takes the mean price of the product per country (from all districts)
def chartPriceHistory(dataFrame, query, ax=None):
	dataFrame = dataFrame.query(query)
	unique_currencies = dataFrame.currency.unique()
	N_currencies = len(unique_currencies)
	print(N_currencies)
	rows = math.floor(math.sqrt(N_currencies))
	cols = math.ceil(N_currencies / rows)
	x = 1
	for currency in unique_currencies:
		print(currency, x)
		plt.subplot(rows, cols, x)
		x = x + 1
		this_currency = dataFrame.query("currency == \"" + currency + "\"")
		unique_products = this_currency._product.unique()

		if len(unique_products) > 1:
			for product in unique_products:
				print(product)
				this_product = this_currency.query("_product==\"" + product + "\"")
				this_product = this_product.sort_values(by=['year', 'month'])
				month_means = []
				year_months = [] 
				for year in this_product.year.unique():
					this_year = this_product.query("year==" + str(year))
					print(year)
					for month in this_year.month.unique():
						this_month = this_year.query("month==" + str(month))
						print(month)
						month_means.append(this_month.price.mean())
						year_months.append(dt.datetime(year=year, month=month, day=1))
				if(ax):
					plt.plot(year_months, month_means, label=product, ax=ax)
				else:
					plt.plot(year_months, month_means, label=product)
			plt.legend()
			# plt.show()

		else:
			for product in this_currency._product.unique():
				print(product)
				this_product = this_currency.query("_product==\"" + product + "\"")
				for country in this_product.country.unique():
					print(country)
					this_country = this_product.query("country==\"" + country + "\"")
					this_country = this_country.sort_values(by=['year', 'month'])
					month_means = []
					year_months = []
					for year in this_country.year.unique():
						this_year = this_country.query("year==" + str(year))
						for month in this_year.month.unique():
							this_month = this_year.query("month==" + str(month))
							month_means.append(this_month.price.mean())
							year_months.append(dt.datetime(year=year, month=month, day=1))
				if(ax):
					ax.plot(year_months, month_means, label=str(country)+", " + str(product))
				else:
					ax.plot(year_months, month_means, label=str(country)+", " + str(product))
			plt.legend()
	# plt.legend()
	# plt.show()

# # Chart price history based on a query.
# # For every unique currency included in the query, a different plot is generated.
# # If such a plot includes multiple products, it takes the mean price of each product (from all countries)
# # If such a plot includes only one product, it takes the mean price of the product per country (from all districts)
# def chartPriceHistory(dataFrame, query):
# 	dataFrame = dataFrame.query(query)


# 	if len(unique_crops) > 1:
# 		for crop in unique_crops:
# 			print(crop)
# 			this_crop = dataFrame.query("Item==\"" + crop + "\"")
# 			this_crp = this_crop.sort_values(by=['year'])
# 			year_months = [] 
# 			for year in this_product.year.unique():
# 				this_year = this_product.query("year==" + str(year))
# 				print(year)

# 			plt.plot(year_months, month_means, label=product)
# 		plt.legend()
# 		# plt.show()

# 		else:
# 			# for product in this_currency._product.unique():
# 			# 	print(product)
# 			# 	this_product = this_currency.query("_product==\"" + product + "\"")
# 			for country in this_product.country.unique():
# 				print(country)
# 				this_country = this_product.query("country==\"" + country + "\"")
# 				this_country = this_country.sort_values(by=['year', 'month'])
# 				month_means = []
# 				year_months = []
# 				for year in this_country.year.unique():
# 					this_year = this_country.query("year==" + str(year))
# 					for month in this_year.month.unique():
# 						this_month = this_year.query("month==" + str(month))
# 						month_means.append(this_month.price.mean())
# 						year_months.append(dt.datetime(year=year, month=month, day=1))

# 				plt.plot(year_months, month_means, label=str(country)+", " + str(product))
# 			plt.legend()
# 	# plt.legend()
# 	plt.show()

def getLinkedProducts(product):
	linked_products = pd.read_csv('Linked_products.csv', encoding='UTF-8', delimiter=";")
	prod = linked_products.query('price_df_product == \"' + product + '\"')
	return prod.production_df_product.unique()

def getYearMean(df, year): 
	df = df.query("year ==" + str(year))
	return df.price.mean()

def chartPriceProductionHistory(price_df, prod_df, links_df, product, country):
	price_df = price_df.query("_product== \"" + product + "\" & country==\"" + country + "\"")
	price_df = price_df.sort_values(by=['year', 'month'])
	month_means = []
	year_months = []
	for year in price_df.year.unique():
		this_year = price_df.query("year==" + str(year))
		for month in this_year.month.unique():
			this_month = this_year.query("month==" + str(month))
			month_means.append(this_month.price.mean())
			year_months.append(dt.datetime(year=year, month=month, day=1))
	# plt.plot(year_months, month_means, label=str(country)+", " + str(product))
	# plt.legend()
	# plt.show()

	linked_products = getLinkedProducts(product)
	print(linked_products)
	for linked_prod in linked_products:
		prod_df = prod_df.query("Item == \"" + linked_prod + "\" & Area == \"" + country + "\"")
		year_prods = []
		years = []
		for year in prod_df.Year.unique():
			this_year = prod_df.query("Year==" + str(year))
			year_prods.append((this_year.iloc[0]["Value"]))
			years.append(dt.datetime(year=year, month=6, day= 30))
	# 		year_prods.append(this_year.
	# 		years.append(dt.datetime(year=year, month=6, day=1))
	# plt.plot(years, year_prods, label=str(country)+", " + str(product))
	# plt.legend()
	# plt.show()


	fig, ax1 = plt.subplots()
	ax1.plot(year_months, month_means, label=str(country)+", " + str(product))
	ax1.set_ylabel('Price', color='b')
	ax1.tick_params('y', colors='b')

	ax2 = ax1.twinx()
	ax2.set_ylabel('Production (Tonnes)')
	ax2.plot(years, year_prods, label=str(country)+", " + str(product))

	fig.tight_layout()
	plt.show()



# def chartPriceProductionHistory(df, query):
# 	df = df.query(query)

# 	unique_products = df._product.unique()
# 	N_products = len(unique_products)
# 	rows = math.floor(math.sqrt(N_products))
# 	cols = math.ceil(N_products / rows)
# 	x = 1
# 	for product in unique_products:
# 		plt.subplot(rows,cols, x)
# 		x = x + 1
# 		this_product = df.query("_product == \"" + product + "\"")
# 		linked_prods = getLinkedProducts(product)
# 		for linked_prod in linked_prods:	
# 			for country in this_product.country.unique():
# 				print(country)
# 				this_country = this_product.query("country==\"" + country + "\"")
# 				this_country = this_country.sort_values(by=['year', 'month'])
# 				years = []
# 				year_means = []
# 				for year in this_country.year.unique():
# 					this_year = this_country.query("year==" + str(year))
# 					year_means.append(this_year.price.mean())
# 					for month in this_year.month.unique():
# 						this_month = this_year.query("month==" + str(month))
# 						month_means.append(this_month.price.mean())
# 						years.append(dt.datetime(year=year, month=6, day=30))

# 					plt.plot(year_months, month_means, label=str(country)+", " + str(product))



if __name__ == '__main__':
	price_df = pd.read_csv('WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

	price_df.rename(columns={'adm0_id': 'country_ID', 'adm0_name': 'country', 'adm1_id' : 'district_ID', \
	                   'adm1_name' : 'district', 'mkt_id' : 'market_ID', 'mkt_name' : 'market' , \
	                   'cm_id' : 'product_ID','cm_name' : '_product', 'cur_id' : 'currency_ID', \
	                   'cur_name' : 'currency', 'pt_id' : 'sale_ID', 'pt_name' : 'sale', 'um_id' : 'unit_ID', \
	                   'um_name' : 'unit', 'mp_month' : 'month', 'mp_year' : 'year', 'mp_price' : 'price', \
	                   'mp_commoditysource' : 'source'}, inplace=True)

	prod_df = pd.read_csv('cleaned_reduced_production.csv')

	links_df = pd.read_csv('Linked_products.csv', delimiter=";")

	query = '_product == "Rice" | _product == "Rice (low quality)"' 
	# fullEDA(df, query)
	# boxPlot(df, query)
	chartPriceHistory(price_df, query)
	# chartPriceProductionHistory(price_df, prod_df, links_df, "Wheat", "India")