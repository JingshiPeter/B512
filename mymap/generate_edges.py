
import requests
import scipy
import csv
import itertools
class generate_edges(object):
#API_key = "AIzaSyDTsSeQGLBSVcavJmuPzArVLuGt7MGXaSw"
    API_key="AIzaSyASJIoQthVWFmCoUcULOPe6tAPTRo5PGng"

    @staticmethod
    def getAddress(address):
        # example: "7201 Hart Lane" --> "7201+Hart+Lane"
        raw_address = address
        a = ""
        for char in raw_address:
            if(char != " "):
                a += char
            else: a += "+"
        a += "+Austin+TX"
        return a

    @staticmethod
    def getTime(add1, add2):
        #Get travel time from two addresses
        add1 = getAddress(add1)
        directions = "https://maps.googleapis.com/maps/api/directions/json?"
        r = requests.get(directions + "origin=" + add1 + "&destination=" + add2 + "&key=" + API_key)
        try:
            result = r.json()["routes"][0]["legs"][0]["duration"]["value"]
            return result
        except: return 0

    @staticmethod
    def queryEdges(add_list):
        import itertools
        add1_list = []
        add2_list = []
        travel_times = []
        # Get all combinations of add in add_list
        for comb in itertools.permutations(add_list, 2):
            add1 = comb[0]
            add2 = comb[1]
            travel_time = getTime(add1,add2)
            
            add1_list.append(add1)
            add2_list.append(add2)
            travel_times.append(travel_time)
        d = {"node1" : add1_list,"node2" : add2_list,"travel_time_seconds" : travel_times}
        df = pandas.DataFrame(d)
        df.to_csv("edge_data_from_google_p.csv")
        node_df=pandas.DataFrame()
        node_df['nodes']=add_list
        node_df.to_csv("node_data_from_google_p.csv")

    @staticmethod
    def test_addresses():
        add_list = ["407 Radam Ln","5701 W Slaughter Ln","1120 S Lamar Blvd","2700 W Anderson Ln",
                    "6507 Burnet Road","3003 S Lamar Blvd","96 Rainey Street","321 W Ben White Blvd",
                    "9070 Research Blvd 8","10817 Ranch Rd 2222","317 E 6th St 10","1900 S 1st St 11","11680 Research Blvd",
                    "909 W Mary St 13","201 Brazos St 14","4477 S Lamar Blvd 15","609 Davis St 16","5204 Ranch Rd 2222","3116 S Congress","8300 N FM 620","1109 South Lamar Blvd",
                    "1400 South Congress Avenue","2438 W Anderson Ln","69 Rainey Street",
                    "401 W 2nd St","5425 Burnet Rd","520 W 6th St","6301 Parmer Ln","2421 Webberville Rd",
                    "13301 US Highway 183","507 Calles St","1509 S Lamar Blvd",
                    "3601 South Congress Avenue","2900 Duval St","3508 S Lamar Blvd","12221 Riata Trace Pkwy",
                    "704 W St. Johns Ave","9012 Research Blvd","9010 Research Blvd","4960 US Route 290",
                    "801 Red River St","12164 N Mopac Expy","11601 Domain Dr","4024 S Lamar Blvd",
                    "1000 E 41st St","7211 Burnet Rd","900 Austin Highlands Blvd"]
        return add_list

    add_list = ["407 Radam Ln","5701 W Slaughter Ln","1120 S Lamar Blvd","2700 W Anderson Ln",
                    "6507 Burnet Road","3003 S Lamar Blvd","96 Rainey Street","321 W Ben White Blvd",
                    "9070 Research Blvd 8","10817 Ranch Rd 2222","317 E 6th St 10","1900 S 1st St 11","11680 Research Blvd",
                    "909 W Mary St 13","201 Brazos St 14","4477 S Lamar Blvd 15","609 Davis St 16","5204 Ranch Rd 2222","3116 S Congress","8300 N FM 620","1109 South Lamar Blvd",
                    "1400 South Congress Avenue","2438 W Anderson Ln","69 Rainey Street",
                    "401 W 2nd St","5425 Burnet Rd","520 W 6th St","6301 Parmer Ln","2421 Webberville Rd",
                    "13301 US Highway 183","507 Calles St","1509 S Lamar Blvd",
                    "3601 South Congress Avenue","2900 Duval St","3508 S Lamar Blvd","12221 Riata Trace Pkwy",
                    "704 W St. Johns Ave","9012 Research Blvd","9010 Research Blvd","4960 US Route 290",
                    "801 Red River St","12164 N Mopac Expy","11601 Domain Dr","4024 S Lamar Blvd",
                    "1000 E 41st St","7211 Burnet Rd","900 Austin Highlands Blvd"]

    # queryEdges(add_list)
    # print len(add_list)