#===================================================================================================================
# Fields Pulled: Car Name | Car Price | Month of Purchase | Yr of Purchase |  Mileage | CV | Engine Type
# 
# ===================================================================================================================


import requests
from bs4 import BeautifulSoup
import time

#set filename to be written
FNAME = 'ouput.csv'

MAX_PGS=676
PAGE_MAX=30

# function to return url for multipage scrape
def ret_url(num):
#   return "http://www.standvirtual.com/carros/anuncios/?s="+str(num*PAGE_MAX+1) +"&op=search&aktion=find&rub=0&ma=&ez=2008&ezb=2016&front=carros&list=30&sort=4"

#open output
fp = open(FNAME,'wb');

iterat = 0
while iterat<MAX_PGS:
   #Sleep 30sec before making next url request.
   time.sleep(30)
   url = ret_url(iterat)
   iterat+=1

   # Get the request and use soup to parse it
   req = requests.get(url)
   soup = BeautifulSoup(req.content,"lxml", from_encoding="utf-8")
   # Get top level item
   g_data = soup.find_all("div",{"class":"ibox modern"})
   print len(g_data)
   print "START"
   itcnt = 0

   # iterate through the list of top level items
   for itm in g_data:
      itcnt+=1
      #print itcnt
      try:
         carnm = (itm.find_all("div",{"class","iboxm listing_show_mob"})[0].text).encode('utf-8')
      except:
	     pass
      try:
         details = (itm.find_all("div",{"id":"iboxi1"})[0].text).encode('utf-8')
      except:
	     pass
      try:
         price = (itm.find_all("div",{"class":"offer_price"})[0].text).encode('utf-8').strip().replace('.','')
      except:
	     pass
		 
      eng_dies = itm.find_all("img",{"id":"img_diesel"})
      eng_gas = itm.find_all("img",{"id":"img_gas"})
      eng_hyb = itm.find_all("img",{"id":"img_hyb"})
      eng_elec = itm.find_all("img",{"id":"img_ele"})
      eng_check= len(eng_dies)+len(eng_gas)+ len(eng_hyb)+len(eng_elec)
      if eng_check > 1:
         print "Something Wrong! Two Engine types listed"
         break
	  
      if len(eng_dies)>0 : 
         engtype = "Diesel"
      elif len(eng_gas)> 0:
         engtype = "Gasoline"
      elif len(eng_hyb) > 0 :
         engtype = "Hybrid"
      elif  len(eng_elec) > 0 :
         engtype = "Electric"
      else :
         engtype = "NA"
      # Process Details
      print details
      if len(details)>0 and len(details.split('/',1))>1 :
         mon = details.split('/',1)[0]
         yr  = details.split('/',1)[1][0:4]
      else:
         mon="NA"
         yr = "NA"
      if len(details)>0 and len(details.split('/',1))>1 and len(details.split('/',1)[1])>0 and len(details.split('/',1)[1].split("km",1))>0 and len( details.split('/',1)[1].split("km",1)[1])>0 :
         kms= details.split('/',1)[1].split("km",1)[0][4:].replace('.','')
         cv = details.split('/',1)[1].split("km",1)[1][:-2]
      else:
         kms="NA"
         cv="NA"	 
      brand = carnm.strip().split(' ',1)[0]		 
      writestr = str(itcnt)+'|'+ brand+'|'+ carnm+ '|'+price +'|'+ mon +'|'+yr+'|'+kms+'|'+cv +'|'+engtype +'\n'
      fp.write(writestr)
   print "Wrote " + str(itcnt)+" rows"
   
print "Done"
fp.close()


