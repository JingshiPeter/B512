import requests
import scipy
import csv
import itertools

#API_key = "AIzaSyDTsSeQGLBSVcavJmuPzArVLuGt7MGXaSw"
API_key="AIzaSyASJIoQthVWFmCoUcULOPe6tAPTRo5PGng"
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

def getTime(add1, add2):
    #Get travel time from two addresses
    add1 = getAddress(add1)
    directions = "https://maps.googleapis.com/maps/api/directions/json?"
    r = requests.get(directions + "origin=" + add1 + "&destination=" + add2 + "&key=" + API_key)
    try:
        result = r.json()["routes"][0]["legs"][0]["duration"]["value"]
        return result
    except: return 0

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

def test_addresses():
    add_list = ["407 Radam Ln","5701 West Slaughter Lane","1120 South Lamar Blvd.","2700 West Anderson Lane",
                "6507 Burnet Road","3003 S. Lamar Blvd Ste F100","96 Rainey Street","321 W. Ben White Blvd",
                "9070 Research Blvd, STE 101","10817 FM 2222","317 E. 6th","1900 South First","11680A Research Road",
                "909 W Mary St","201 Brazos","4477 S. Lamar","609 Davis St","5204 FM 2222","3116 S Congress","8300 N FM 620","1109 South Lamar Blvd",
                "1400 South Congress Avenue, STE.190A","2438 West Anderson Lane","69 Rainey Street",
                "401 West 2nd Street","5425 Burnet Rd","520 w. 6th","6301 Parmer Ln","2421 Webberville Rd","13301 N. US Hwy. 183 Bldg A","507 Calles Street","1509 S. Lamar Blvd, Ste 600",
                "3601 South Congress Avenue","2900 Duval St.","3508 South Lamar Blvd","12221 Riata Trace Pkwy, Suite 100",
                "704 W St. Johns Ave","9012 Research Blvd","9012 Research Blvd STE C4","4960 West Hwy. 290",
                "801 Red River Street","12164 N Mo PAC Expy","11601 Domain Dr. Ste 200","4024 S Lamar",
                "1000 East 41st Street","7211 Burnet Rd","900 N. Austin Ave. 410"]
    return add_list

add_list = ["407 Radam Ln","5701 West Slaughter Lane","1120 South Lamar Blvd.","2700 West Anderson Lane",
"6507 Burnet Road","3003 S. Lamar Blvd Ste F100","96 Rainey Street","321 W. Ben White Blvd",
"9070 Research Blvd, STE 101","10817 FM 2222","317 E. 6th","1900 South First","11680A Research Road",
"909 W Mary St","201 Brazos","4477 S. Lamar","609 Davis St","5204 FM 2222","3116 S Congress","8300 N FM 620","1109 South Lamar Blvd",
"1400 South Congress Avenue, STE.190A","2438 West Anderson Lane","69 Rainey Street",
"401 West 2nd Street","5425 Burnet Rd","520 w. 6th","6301 Parmer Ln","2421 Webberville Rd","13301 N. US Hwy. 183 Bldg A","507 Calles Street","1509 S. Lamar Blvd, Ste 600",
"3601 South Congress Avenue","2900 Duval St.","3508 South Lamar Blvd","12221 Riata Trace Pkwy, Suite 100",
"704 W St. Johns Ave","9012 Research Blvd","9012 Research Blvd STE C4","4960 West Hwy. 290",
"801 Red River Street","12164 N Mo PAC Expy","11601 Domain Dr. Ste 200","4024 S Lamar",
"1000 East 41st Street","7211 Burnet Rd","900 N. Austin Ave. 410"]

queryEdges(add_list)
print len(add_list)