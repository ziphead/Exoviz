from lxml import etree
import urllib, gzip, io
from models import *

class Scanner():
    def __init__(self):
        url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
        self.dbxml = etree.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.urlopen(url).read())))
        self.tree = self.dbxml.xpath('/systems')
        self.sysid = 1
        self.binid = 1
        self.starid = 1
        self.local_id = 0
        self.sysinfo = []   
        self.starinfo = []
        self.bodyinfo = []
        self.bininfo = []
        
    def attr_check(self,attr, text): # this method appends object attributes  in a list
        self.attr = attr
        xlist = []
        for key, val in attr.iteritems():
            val = str(val)
            text = str(text)
            x = text + ' : ' + key + ' = ' + val + ' / '
            xlist.append(x)
        return xlist
        
    def separation_check(self, attr, tag): # this method appends object attributes  in a list
        self.attr = attr
        self.tag = tag
        xlist = []
        right_tag = 'separation'
        for key, val in attr.iteritems():
            if val == 'AU':
                right_tag = 'separation_au'
                continue
            elif val == 'arcsec':
                right_tag = 'separation_arcsec'
                continue
            val = str(val)
            tag = str(tag)
            x = tag + ' : ' + key + ' = ' + val + ' / '
            xlist.append(x)
        return right_tag, xlist

#Star wrapper
    def star_finder(self, data, dataid, parent):
        self.starid += 1
        my_id = self.starid
        sn = {}   
        self.local_id += 1  
        me_local = self.local_id 
        sn['id'] = my_id
        sn['local_id'] = me_local  
        sn['parent_id'] = parent
        sn['homesystem'] = self.sysid
        
        for star in data:
            tag = star.tag.lower()
            if star.tag == 'planet':
                self.planet_finder(star, my_id, me_local)
                continue
            if star.tag == 'binary' :
                self.bin_finder(star, my_id, me_local)
                continue 
            if star.tag == 'name':
                if 'name'  in sn:
                    sn['names'] = sn.get('names', '') + ' ' + star.text
                    continue
                else:
                    sn['name'] = star.text
                    continue
            
            if star.attrib != '':
                sn[tag] = star.text
                attrib = self.attr_check(star.attrib, star.tag) 
                band = ' '.join(attrib)  
                sn['attributes'] = sn.get('attributes', '') + band  
            else :
                sn[tag] = star.text
                
        self.starinfo.append(sn)
        
#Planet wrapper        
    def planet_finder(self, data, dataid, parent):
        bd = {}   
        self.local_id += 1  
        me_local = self.local_id 
        bd['local_id'] = me_local  
        bd['parent_id'] = parent
        bd['homesystem'] = self.sysid
        for planet in data:
            tag = planet.tag.lower()
            # for planets orbiting other planets : code modifications should be made here (and extra table rows needed)
            if planet.tag == 'name':
                if 'name'  in bd:
                    bd['names'] = bd.get('names', '') + ' ' + planet.text
                    continue
                else:
                    bd['name'] = planet.text
                    continue
            if planet.tag == 'separation':
                find_unit = self.separation_check(planet.attrib, planet.tag)
                bd[find_unit[0]] = planet.text                 
                band = ' '.join(find_unit[1])  
                bd['attributes'] = bd.get('attributes', '') + band
                continue
            if planet.tag == 'list':
                bd['planet_list'] = planet.text
            if planet.attrib != '':
                bd[tag] = planet.text
                attrib = self.attr_check(planet.attrib, planet.tag) 
                band = ' '.join(attrib)  
                bd['attributes'] = bd.get('attributes', '') + band  
            else :
                bd[tag] = planet.text
        self.bodyinfo.append(bd)

#Binary wrapper
    def bin_finder(self, data, dataid, parent):
        self.binid += 1
        my_id = self.binid
        bn = {} 
        self.local_id += 1  
        me_local = self.local_id 
        bn['id'] = my_id  
        bn['local_id'] = me_local  
        bn['parent_id'] = parent
        bn['homesystem'] = self.sysid
        for binstar in data:
            tag = binstar.tag.lower()            
            if binstar.tag == 'star':
                self.star_finder(binstar, my_id , me_local)
                continue
            if binstar.tag == 'planet':
                self.planet_finder(binstar, my_id , me_local)
                continue
            if binstar.tag == 'binary' :
                self.bin_finder(binstar, my_id ,  me_local)
                continue 
            if binstar.tag == 'name':
                if 'name'  in bn:
                    bn['names'] = bn.get('names', '') + ' ' + binstar.text                    
                    continue
                else:
                    bn['name'] = binstar.text
                    continue
            if binstar.tag == 'separation':
                find_unit = self.separation_check(binstar.attrib, binstar.tag)
                bn[find_unit[0]] = binstar.text                 
                band = ' '.join(find_unit[1])  
                bn['attributes'] = bn.get('attributes', '') + band
                continue
            if binstar.attrib != '':                
                bn[tag] = binstar.text
                attrib = self.attr_check(binstar.attrib, binstar.tag) 
                band = ' '.join(attrib)  
                bn['attributes'] = bn.get('attributes', '') + band  
            else :
                bn[tag] = binstar.text
        self.bininfo.append(bn)


    
    def get_fields(self): # This is the main method  it starts xml iteration, gets 4 lists of unique parameter fields for systems, stars, planets, binaries
        for systems in self.dbxml.xpath('/systems/system'):                       
            self.sysid += 1
            self.local_id = 1
            local_id = self.local_id
            stm = {}
            stm['id'] = self.sysid
            stm['local_id'] = local_id 
            for system in systems:
                if system.tag == 'star':
                    self.star_finder(system, self.sysid, local_id)
                    continue
                if system.tag == 'planet':
                    self.planet_finder(system, self.sysid, local_id)
                    continue
                if system.tag == 'binary' :
                    self.bin_finder(system, self.sysid,  local_id)
                    continue 
                if system.tag == 'name':
                    if 'name'  in stm:
                        stm['names'] = stm.get('names', '') + ' ' + system.text
                        continue
                    else:
                        stm['name'] = system.text
                        continue
                if system.attrib != '':
                    stm[system.tag] = system.text
                    attrib = self.attr_check(system.attrib, system.tag) 
                    band = ' '.join(attrib)  
                    stm['attributes'] = stm.get('attributes', '') + band  
                else :
                    stm[system.tag] = system.text

            self.sysinfo.append(stm)

        return self.bininfo, self.starinfo, self.bodyinfo, self.sysinfo

#Creating SQL tables
    def create_tables(self):
        db.create_tables([System, Binary, Star, Planet],  True)    
        print 'Creating tables ==> DONE'

#This function fills the database with dictionary data
    def filler(self, x):
        self.x = x
        binlist = sorted(x[0], key=lambda k: k['id'])
        syslist = sorted(x[3], key=lambda k: k['id'])
        starlist = sorted(x[1], key=lambda k: k['id'])
        #planlist = sorted(x[2], key=lambda k: k['bin'])
        with db.atomic(): # Bulk insert data
            for data_dict in syslist:
                System.create(**data_dict)
                #print data_dict,  '\n system ok'
            for data_dict in binlist:
                Binary.create(**data_dict)
                #print data_dict, '\n binary ok'
            for data_dict in starlist:
                Star.create(**data_dict)
                #print data_dict, '\n star ok'
            for data_dict in x[2]:
                Planet.create(**data_dict)
                #print data_dict, '\n planet ok'

# This fiiler function is for the future nonsql database( in progress )
#    def filler2(self, x):
#        self.x = x
#        binlist = sorted(x[0], key=lambda k: k['bin'])
#        syslist = sorted(x[3], key=lambda k: k['sys'])
#        starlist = sorted(x[1], key=lambda k: k['star'])
#        #planlist = sorted(x[2], key=lambda k: k['bin'])
#        with db.atomic(): # Bulk insert data
#            for data_dict in syslist:
#                System.create(**data_dict)
#                #print data_dict,  '\n system ok'
#            for data_dict in binlist:
#                Binary.create(**data_dict)
#                #print data_dict, '\n binary ok'
#            for data_dict in starlist:
#                Star.create(**data_dict)
#                #print data_dict, '\n star ok'
#            for data_dict in x[2]:
#                Planet.create(**data_dict)
#                #print data_dict, '\n planet ok'


if __name__ == "__main__":
    print 'run control.py'
    #Scanner().create_tables()
    #Scanner().filler()


