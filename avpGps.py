'''
Created on Apr 13, 2012

@author: Yongxu
'''
import math
import time
EARTHRADIUS=6371000.0

class GPS:
    @staticmethod
    def validNMEA(data):
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
    def stringToValue(latitude,longitude):
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

        return (math.radians(lat),math.radians(lon))

    @staticmethod
    def distance(lat1,lon1,lat2,lon2,earthRadius=EARTHRADIUS):
        dLat=lat2-lat1
        dLon=lon2-lon1
        a=math.sin(dLat/2)**2+math.sin(dLon/2)**2*math.cos(lat1)*math.cos(lat2)
        c=2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        d=earthRadius*c
        return d

    @staticmethod
    def bearing(lat1,lon1,lat2,lon2,earthRadius=EARTHRADIUS):
    #        dLat=GPS.toRad(lat2-lat1)
        dLon=lon2-lon1

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
