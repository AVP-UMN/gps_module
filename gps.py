'''
Created on Apr 13, 2012

@author: Yongxu
'''
import math
import time
EARTHRADIUS=6371000.0

class GPS:
    def __init__(self):
        self.time=0
        self.latitude=0
        self.longitude=0
        self.speed=0
        self.direction=0
        self.isValid=False
        self.lastValidTime=0;
        pass

    
    def update(self,data):
        if not self.dataValid(data):
            self.isValid=False
            return False
        fields= data.split(',')
        if fields[0]=='$GPRMC':
            newtime=int(fields[1][0:2])*3600+int(fields[1][2:4])*60+float(fields[1][4:])
            if newtime>self.time:
                if fields[2]=='A':
                    self.isValid=True
                    self.time=newtime
                    self.lastValidTime=self.time
                    self.latitude=int(fields[3][:2])+float(fields[3][2:])/60
                    if fields[4]=='S':
                        self.latitude=-self.latitude
                    self.longitude=int(fields[5][0:3])+float(fields[5][3:])/60
                    if fields[6]=='W':
                        self.longitude=-self.longitude
                    self.speed=float(fields[7])*0.5144444 #knot to m/s
                    self.direction=float(fields[8]) 
                    return True                   
                else:
                    self.time=newtime
                    self.isValid=False
                    return False            
            else:
                self.isValid=False
                return False     
    @staticmethod  
    def dataValid(data):
        if(data[0]!='$' or '*' not in data):
            return False
        else:
            x=0
            starPos=data.rfind('*')
            for a in data[1:starPos]:
                x^=ord(a)
            if(x==int(data[starPos+1:],16)):
                return True
        return False
    
    @staticmethod
    def distance(lat1,lon1,lat2,lon2,earthRadius=EARTHRADIUS):
        dLat=GPS.toRad(lat2-lat1)
        dLon=GPS.toRad(lon2-lon1)
        lat1=GPS.toRad(lat1)
        lat2=GPS.toRad(lat2)
        a=math.sin(dLat/2)**2+math.sin(dLon/2)**2*math.cos(lat1)*math.cos(lat2)
        c=2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        d=earthRadius*c
        return d 
    
    @staticmethod
    def bearing(lat1,lon1,lat2,lon2,earthRadius=EARTHRADIUS):
#        dLat=GPS.toRad(lat2-lat1)
        dLon=GPS.toRad(lon2-lon1)
        lat1=GPS.toRad(lat1)
        lat2=GPS.toRad(lat2)
        
        y=math.sin(dLon)*math.cos(lat2)
        x=math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
        
        return math.atan2(y, x)
    
    @staticmethod
    def direction(lat1,lon1,lat2,lon2,earthRadius=EARTHRADIUS):
        '''
        return (x,y):
            x------>East
            y------>North
        '''
        dist=GPS.distance(lat1, lon1, lat2, lon2, earthRadius)
        bearing=GPS.bearing(lat1, lon1, lat2, lon2, earthRadius)
        
        return (dist*math.sin(bearing),dist*math.cos(bearing))
    
    @staticmethod
    def distance_(GPSPoint,GPSOrigin):
        return GPS.distance(GPSOrigin[0],GPSOrigin[1],GPSPoint[0],GPSPoint[1])
    @staticmethod
    def bearing_(GPSPoint,GPSOrigin):
        return GPS.bearing(GPSOrigin[0],GPSOrigin[1],GPSPoint[0],GPSPoint[1])
    @staticmethod
    def direction_(GPSPoint,GPSOrigin):
        return GPS.direction(GPSOrigin[0],GPSOrigin[1],GPSPoint[0],GPSPoint[1])
    @staticmethod
    def toMeterCoordinate(GPSPoint,GPSOrigin):
        return GPS.direction(GPSOrigin[0],GPSOrigin[1],GPSPoint[0],GPSPoint[1])
        
    @staticmethod
    def toRad(degree):
        return (degree/180.0*math.pi)%(2*math.pi)
    
    @staticmethod
    def toDeg(radians):
        deg=radians*180.0/math.pi%360
        if deg>180:
            deg=deg-360
        elif deg<-180:
            deg=deg+360
        return deg
    
    def getTime(self):
        return self.time


    def getLatitude(self):
        return self.latitude


    def getLongitude(self):
        return self.longitude


    def getSpeed(self):
        return self.speed


    def getDirection(self):
        return self.direction


    def getIsValid(self):
        return self.isValid


    def getLastValidTime(self):
        return self.lastValidTime
    
    @staticmethod
    def degToDec(d,m,s):
        return (d+m/60+s/3600)
    @staticmethod
    def toDec(latitude,longitude):
        if latitude[-1]=='S' or latitude[-1]=='s':
            lat=-1
        else:
            lat=1
        
        if longitude[-1]=='W' or longitude[-1]=='w':
            lon=-1
        else:
            lon=1
            
        fields=latitude[:-1].split(' ')
        lat=lat*(float(fields[0])+float(fields[1])/60+float(fields[2])/3600)
        
        fields=longitude[:-1].split(' ')
        lon=lon*(float(fields[0])+float(fields[1])/60+float(fields[2])/3600)
        
        return (lat,lon)
    
    @staticmethod    
    def toRadDec(latitude,longitude):
        lat,lon=GPS.toDec(latitude,longitude)
        return (GPS.toRad(lat),GPS.toRad(lon))
        

if __name__=='__main__':    
#    g=GPS()   
#    g.update("$GPRMC,085359.000,A,3401.2971,N,11829.2133,W,0.01,190.04,130412,,,A*7D")
#    
#    print g.time, g.latitude, g.longitude, g.speed, g.direction, g.isValid
    t=time.clock()
#    print GPS.distance(GPS.degToDec(34.0, 0.0, 55.52), - GPS.degToDec(118.0, 28.0, 13.77), GPS.degToDec(34.0, 0.0, 57.52), - GPS.degToDec(118.0, 28.0, 11.80))
#    print 180.0/math.pi*GPS.bearing(GPS.degToDec(34.0, 0.0, 55.52), - GPS.degToDec(118.0, 28.0, 13.77), GPS.degToDec(34.0, 0.0, 57.52), - GPS.degToDec(118.0, 28.0, 11.80))
#    print GPS.distance(GPS.degToDec(40.0, 44.0, 55.0), - GPS.degToDec(73.0, 59.0, 11.0), 40.7486, -73.9864)
#    print 180.0/math.pi*GPS.Bearing(GPS.degToDec(40.0, 44.0, 55.0), - GPS.degToDec(73.0, 59.0, 11.0), 40.7486, -73.9864)
#    print 180.0/math.pi*GPS.Bearing(12.3, 45.6, 78.9, -10.11)
#    for i in range(100000):
#        GPS.distance(GPS.degToDec(50.0, 21.0, 50.0), -GPS.degToDec(4.0, 9.0, 25.0), 40.7486, -73.9864)
#    print time.clock()-t
#    print GPS.distance(34,-118,35,-117)
#    print GPS.bearing(34,-118,35,-117)
#    
#    print GPS.direction(34,-118,33,-119)

    print GPS.toRadDec('34 00 50.08N', '118 28 24.11W')