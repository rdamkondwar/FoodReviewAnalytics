import json
import os

with open("output.csv","r") as infile:
	
	# City map to keep track of the city names in the merged table.
	cityMap = {}
	counter = 0
	for line in infile:
		if (counter == 0):
			counter += 1
			continue
		output = ""
		listTokens = line.split(",")

		#Check if the id is equal in left and right tables.
		if (listTokens[0] == listTokens[1]):
			output += listTokens[0] + ","

		#Select the name with maximum length from left and right tables.
		if (len(listTokens[4]) >= len(listTokens[14])):
			output += listTokens[4] + ","
		else:
			output += listTokens[14] + ","

		#Select the address with maximum length from left and right tables.
		if (len(listTokens[11]) >= len(listTokens[21])):
			output += listTokens[11] + ","
		else:
			output += listTokens[21] + ","

		''' Check which city name is better.
			
			Check if any of the previous tuples had a similar city name.
			If yes then include that city name in the merged table
			If city name exists in the corresponding address,
			it might not be an area name
		'''
		if (listTokens[5] != listTokens[15]):
			#print "Different city found in ",listTokens[5]," and ",listTokens[15],"Addresses : ",listTokens[11]," and ",listTokens[21]
			if listTokens[5] in cityMap:
				if listTokens[15] in cityMap:
					if cityMap[listTokens[5]] >= cityMap[listTokens[15]] :
						output += listTokens[5] + ","
					else:
						output += listTokens[15] + ","
				else:
					output += listTokens[5] + ","
			else:
				if listTokens[15] in cityMap:
					output += listTokens[15] + ","
				else:
					if (listTokens[5] in listTokens[11]):
						output += listTokens[5] + ","
					elif (listTokens[5] in listTokens[21]):
						output += listTokens[5] + ","
					elif (listTokens[15] in listTokens[11]):
						output += listTokens[15] + ","
					elif (listTokens[15] in listTokens[21]):
						output += listTokens[15] + ","
		else:
			if listTokens[5] not in cityMap:
				cityMap.setdefault(listTokens[5],1)
			else:
				cityMap[listTokens[5]] += 1
			output += listTokens[5] + ","

		#Zipcode should be equal as it is the blocked attribute. Hence extract it from any table
		output += listTokens[6] + ","

		#Take the average values of the latitude and longitude from both the tables
		if ((float(listTokens[8]) != listTokens[18] or listTokens[9] != listTokens[19])):
			output += str((float(listTokens[8]) + float(listTokens[18])) / 2) + ","
			output += str((float(listTokens[9]) + float(listTokens[19])) / 2) + ","

		# Add the review counts in both the tables and copy the value to final table
		total = int(listTokens[7]) + int(listTokens[17])
		output += str(total) + ","

		# Calculate the aggregate rating using weighted sum of ratings from both sources.
		combined_rating = 0
		if (total != 0):
			combined_rating = (float(listTokens[7])*float(listTokens[10]) + float(listTokens[17])*float(listTokens[20]))/total
		else:
			combined_rating = int(listTokens[10])
		output += str(combined_rating) + ","

		#Copy zomato_id and yelp_id as it is.
		if(int(listTokens[12]) == 0):
			output += str(listTokens[22]) + ","
		else:
			output += str(listTokens[12]) + ","

		if(listTokens[13] == 0):
			output += str(listTokens[23]) + ","
		else:
			output += str(listTokens[13])

		print output
		counter += 1

	#print cityMap
