from models import *
import random
from exo import Scanner
from datetime import datetime

class Control():

    def spectrum(self):
        spector = [(33000,150000,'O'),(10000,30000,'B'),(7500,10000,'A'),(6000, 7500, 'F'), (5200, 6000, 'G'), (3700, 5200, 'K'), (1000, 3700, 'M'), (200, 1000, 'L')]
        return spector
    def picture(self, code, member):
        spector = Control().spectrum()
        letters = 'OBAFGKML'
        if code == 1:
            if member.temperature :
                for i in spector:
                    if i[0] <= int(member.temperature) < i[1] :
                        this_spec = i[2]+'_star'
                        return this_spec
#                return 'G_star'  # if temperature not in range setting G type
            else:
                if member.spectraltype:
                    for i in member.spectraltype:
                        if i.isupper():
                            if i in letters:
                                return i + '_star'
                            else:
                                return 'G_star'
                else:
                    return 'G_star'
        elif code == 2:
            solar = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
            earth_rad = 0.091130
            earth_mas = 0.003145
            uranus_rad = 0.36277
            uranus_mas = 0.0457
            jupiter_mas = 1
            jupiter_rad = 1
            mercury_mas = 0.000173
            mercury_rad = 0.03490
            if member.name in solar:
                return member.name

            if member.mass :
                if member.mass >=  jupiter_mas:
                    pic = 'Gas_Giant_'+str(random.randint(1,3))
                elif uranus_mas <= member.mass <  jupiter_mas:
                    pic = 'Icy_Giant_'+str(random.randint(1,2))
                elif earth_mas * 15 < member.mass < uranus_mas:
                    pic = 'Minnie_Neptune_1'
                elif earth_mas < member.mass <= earth_mas * 15:
                    pic = 'Super_Earth_'+str(random.randint(1,3))
                elif mercury_mas < member.mass <= earth_mas:
                    pic = 'Earth_like_'+str(random.randint(1,3))
                elif member.mass <= mercury_mas:
                    pic = 'Moon_like_1'
                return pic
            elif member.radius :
                if member.radius >=  jupiter_rad:
                    pic = 'Gas_Giant_'+str(random.randint(1,3))
                elif uranus_rad <= member.radius <  jupiter_rad:
                    pic = 'Icy_Giant_'+str(random.randint(1,2))
                elif earth_rad * 4 < member.radius < uranus_rad:
                    pic = 'Minnie_Neptune_1'
                elif earth_rad < member.radius <= earth_rad * 4:
                    pic = 'Super_Earth_'+str(random.randint(1,3))
                elif mercury_rad < member.radius <= earth_rad:
                    pic = 'Earth_like_'+str(random.randint(1,3))
                elif member.radius <= mercury_rad:
                    pic = 'Moon_like_1'
                return pic
            else:
                return 'Gas_Giant_'+str(random.randint(1,3)) # if no mass or radius found Gas giant pucture returned
        else:
            return False

    def jsonviz(self, member):
        group = member.__class__.__name__

        if group == 'System':
            pathway = member.name
            node = "{id: %s,  group : '%s', odds: '%s'}" % (1,  group , member.id)
            edge = False

        elif group == 'Binary':
            node = "{id: %s,  group : '%s', odds: '%s', value: 100}" % (member.local_id, group , member.id)
            edge = "{from: %s, to: %s}" % (member.parent_id, member.local_id)

        else:
            if group == 'Star':
                pic = Control().picture(1, member)

                print pic
                if member.radius is None:
                    val = 100
                else:
                    val = member.radius * 100


            if group == 'Planet':
                 pic = Control().picture(2, member)
                 if member.radius is None:
                     val = 10
                 else:
                    val = member.radius * 10


            node = "{id: %s, label: '%s', group : '%s', odds: '%s', value: '%s', image: '/static/images/icons/%s.png' }" % (member.local_id, member.name, group , member.id, val, pic)
            edge = "{from: %s, to: %s}" % (member.parent_id, member.local_id)
        return node, edge


    def family(self, data):
        if data.__class__.__name__ == 'System':
            system = data
        else:
            system = data.homesystem
        planets = Planet.select().where(Planet.homesystem == system)
        binnies = Binary.select().where(Binary.homesystem == system)
        stars = Star.select().where(Star.homesystem == system)
        the_happy_family = [system]
        the_happy_family.extend(binnies)
        the_happy_family.extend(stars)
        the_happy_family.extend(planets)
        return the_happy_family



    def update(self):
        try:
            x = Scanner().get_fields()
            db_last_update = Planet.select().order_by(Planet.lastupdate.desc()).limit(1)
            db_last = (db_last_update[0].name, db_last_update[0].lastupdate)
        except:
            return False
        new_stuff = []
        for data_dict in x[2]:
            if 'lastupdate' in data_dict:

                if data_dict['lastupdate'] is None:
                    continue
                else:
    #                    lupdate = datetime.strptime(v,'%y/%m/%d').strftime('%Y-%m-%d')
    #
    #                    if lupdate > uptime:
    #                        uptime = lupdate
#                    print data_dict['lastupdate'], 'db last: ', db_last[1]
                    if data_dict['lastupdate'] > db_last[1]:
                        print data_dict['lastupdate'], 'db last: ', db_last[1]
                        new_stuff.extend(data_dict)


        if len(new_stuff) > 0:
            try:
                print 'updating'
                db.drop_tables([Planet, Star, Binary, System ], safe=True)
                print 'drop old'
                Scanner().create_tables()
                Scanner().filler(x)
                return new_staff
            except:
                return False
        else:
            print 'Catalogue is up to date'
            return 'Catalogue is up to date'



    def query(self, it, it_id):

        if it == "Planet":
            query = Planet.get(Planet.id == it_id)
        elif it == "Star":
            query = Star.get(Star.id == it_id)
        elif it == "System":
            query = System.get(System.id == it_id)
        elif it == "Binary":
            query = Binary.get(Binary.id == it_id)

        return query

    def search(self, name):

        p_lookup = Planet.select().join(System).where((Planet.name.contains(name)) |  (Planet.names.contains(name)))
        s_lookup = Star.select().join(System).where((Star.name.contains(name)) |  (Star.names.contains(name)))
        systems =[]
        for each in p_lookup:

            if each.homesystem not in systems:
                systems.append(each.homesystem)
        for each in s_lookup:

            if each.homesystem not in systems:
                systems.append(each.homesystem)

        return systems

if __name__ == "__main__":
    q1 = raw_input('Do you wish to create sql tables or update? \n  To create tables press (1) To update press (2) to get database info press (3): ')
    while q1 != '1' or q1 !='2':
        if q1 == '1':
            Scanner().create_tables()
            x = Scanner().get_fields()
            Scanner().filler(x)
            break

        elif q1 == '2':
            print 'trying to update....'
            Control().update()
            break

        elif q1 == '3':
            q2 = raw_input('Choose (1) to get db status \n Choose (2) to check planet status: '  )
            while q2 != '1' or q2 !='2':
                if q2 == '1':
                    try:
                        pcount = Planet.select().count()
                        scount = System.select().count()
                        bcount = Binary.select().count()
                        starcount = Star.select().count()
                        print "There are:", pcount, "of planets in ",  scount, "systems\n", starcount, "of stars"
                    except:
                        print "no db tables detected. Please install database first"
                    break
                if q2 == '2':
                    Control(). conn()
                    q3 = raw_input('please type the planet name: '  )

#                    lookup = Planet.select().join(System).order_by(Planet.lastupdate.desc()).limit(16)
                    lookup = Planet.select().where((Planet.name.contains(q3)) |  (Planet.names.contains(q3))).limit(8)

                    for entry in lookup:
                        print entry.__class__.__name__
#                        distance = Control().checkonmama(entry)[-1]
                        print entry.name,  'id ==>  ', entry.id

            break

        else:
            print 'wrong input'
            q1 = raw_input('Do you wish to create sql tables or update? \n  To create tables press (1) To update press (2): ')
