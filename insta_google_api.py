import requests
import json
import sys
import webbrowser
import ctypes
 
#Usage:

#   python insta_google_api.py lakeplacid 5
#   check the last 5 pages of images that has taken in lake placid and open them in the web browser


key ='2228213740.1fb234f.a87267e857be4f4f8e4ea0cee36cabaf' 

#Create a dictionary for use with requests - note name is payload - but this could any name
payload = {"access_token":key}
#Turn off SSL warning - maybe you shouldn't do this in real life?
requests.packages.urllib3.disable_warnings()
#create a blank location ID list
location_ID=[]
i=0
#if TRUE it means there is another page in Instagram API
continue_loop =True

j=1;

message = """<!DOCTYPE html>
<html>
<head>
<style>
img { 
    width:10%; 
}
</style>
</head>
<body>
"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Google API%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


#Sample: https://maps.googleapis.com/maps/api/geocode/json?address=lake%20placid

Image_URL=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+sys.argv[1])
data = json.loads(Image_URL.text)
#status shows if the location address is correct or not. it returns two values: OK and ZERO_RESULTS
status=data['status']
#print status,data
#check if the location entered is valid 
if("OK" in status):
	#Extracting the name of the place from Google API
	google_name= data['results'][0]['address_components'][0]['long_name']
	#input("***************************Mahe 5***************************")
	#Lat and Lng of the place
	lat=data['results'][0]['geometry']['location']['lat']
	lng=data['results'][0]['geometry']['location']['lng']
		
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Google API%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Instagram API%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	
	
	#Request to find location ID by using lat and lng from Google API
	#Sample:https://api.instagram.com/v1/locations/search?lat=44.2794911&lng=-73.9798713
	Location_info_Req = requests.get('https://api.instagram.com/v1/locations/search?lat='+str(lat)+'&lng='+str(lng),params=payload,verify=False)#make the request
	Location_info_data = json.loads(Location_info_Req.text)
	#print lat,lng
	'''
	For each location ID(most of the time, we have multiple results for specific Latitude and longitude),
	check whether the name presented in Google Map API is similar to what Instagram API founds. If so add it to the list.
	'''
	for location in Location_info_data['data']:
		if google_name in location['name']:
				location_ID.append(location['id'])
			
	

	if(location_ID):
		for ID in location_ID:
			while i < int(sys.argv[2]):
					#https://api.instagram.com/v1/locations/941768875/media/recent
					#https://api.instagram.com/v1/locations/941768875/media/recent?access_token=2228213740.1fb234f.a87267e857be4f4f8e4ea0cee36cabaf&max_id=1047891689146467251
					#by default continue_loop is True but if there is not other page in Instagram API to continue it will be changed to False.
					if(continue_loop):
					
						Images_request = requests.get('https://api.instagram.com/v1/locations/'+ID+'/media/recent',params=payload,verify=False)#make the request
						Images_data = json.loads(Images_request.text)
						#print Images_data['pagination'],Images_data, ID						
						#print bool(Images_data['pagination']),Images_data['pagination']
						#check if there is more page to show
						if(Images_data['pagination']):
							payload = {"access_token":key,"max_id":Images_data['pagination'][u'next_max_id']}
							#print "not null"
						else:
							#since there is no more page the continue_loop is changed to false
							continue_loop= False
						
						f = open(google_name+'Photoes'+'.html','w')
						#check if there is any image data
						if (Images_data['data']):			
							for image in Images_data['data']:
								#print image['images']['low_resolution']['url']						
								
								#web browser settings
								new = 1 # open in a new tab, if possible
								# open a public URL
								url = image['images']['low_resolution']['url']
								#<img src="http://www.w3schools.com/images/w3schools_green.jpg" alt="W3Schools.com">

								message+="<img src="+url+" "+"alt=W3Schools.com>"
								message+="<br />"
								f.write(message)
								
								
								#webbrowser.open(url,new=new)
						else:
							ctypes.windll.user32.MessageBoxA(0, "Currently there is not image available for the location you entered", "No Image Available", 1)

				        
					i+=1
	else:
		ctypes.windll.user32.MessageBoxA(0, "Currently there is no image available for the location you entered", "No Image Available", 1)
else:
	ctypes.windll.user32.MessageBoxA(0, "Please correct the location and try again.", "Location is not available", 1)  
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Instagram API%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
f = open(google_name+'Photoes'+'.html','w')
message+= '''</body>
</html>
'''
f.write(message)
f.close()
webbrowser.open_new_tab(google_name+'Photoes'+'.html')
