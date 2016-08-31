from flask import Flask, render_template,request, redirect, url_for, flash, jsonify
from models import *
from control import Control
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)


   
@app.route('/')

def Main():
    now = datetime.now().strftime('%y/%m/%d') 
                            
    try:                
        last = Planet.select().join(System).order_by(Planet.lastupdate.desc()).limit(16)
        logging.info('planet grab - ok %s', len(last))
        binnies = Binary.select().join(System).order_by(Binary.local_id.desc()).limit(16)  
        logging.info('bin grab - ok %s', len(binnies))
        pcount = Planet.select().count()
        scount = System.select().count()
        bcount = Binary.select().count()
        starcount = Star.select().count()
        message = ( scount, bcount, starcount, pcount)
        datachunk = []
        binchunk = []
        logging.info('family initiation ')
        for entry in last:
            datachunk.append(entry)
#        for i in datachunk:
#            nams = [c.__class__.__name__ for c in i] 
#            logging.info('list of parents %s', nams)         
        for entry in binnies:
            binchunk.append(entry)
#        for i in binchunk:
#            nams = [c.__class__.__name__ for c in i] 
#            logging.info('list of parents %s', nams)           
        #Control().close()  
        return  render_template('index2.html', message = message,  datachunk = datachunk, binchunk = binchunk )
    except:
        logging.warning('warning! main function failure: No db tables detected. Please install database first')
        print "no db tables detected. Please install database first"
        return redirect(url_for('fail'))
        

@app.route('/search', methods=['POST', 'GET'])
def search_func():
    
    if request.method == 'GET':
        print 'ok get'
    if request.method == 'POST':  
        pathway = request.form['object_name']
        if len(pathway)<=1:
            flash('Sorry, you need to type more than one letter')
            return  render_template('base.html', pathway = pathway)
        try: 

            content =Control().search(pathway)
            number =  "There are %d results matching the query" % (len(content),)
            flash(number)            
            return  render_template('base.html', pathway = pathway, content = content )

        except:
            logging.error('search function has died looking for this : %s', request.form['object_name']) 
            return  render_template('base.html', pathway = 'ERROR Happened' )

    

@app.route('/system/<int:system_id>/viz/')
def viz_sys(system_id):
    logging.info('Check on first base %s', system_id) 
    try:
        target = System.get(System.id == system_id)
        family = Control().family(target)
        mynodes = ["{id: 9999,   hidden: true, value: 0.001 }"]        
        myedges = []
        logging.info('Check on family: %s', family) 
        pathway = target.name
    #        unknown_body_distance = range(1, 10, 1)is not working with the vis.js vizualization
        for member in family: 
            
            data = Control().jsonviz(member)
    #            except:
    #                logging.warning('jsonwiz func failture - on  %s', member.name)
            if data[1]:
                print data[1]
                myedges.append(data[1])
            mynodes.append(data[0])  
            
    # use the code below to order bodies by their distance one day
    #            try:
    #                sem = member.semimajoraxis * 215
    #            except:
    #                sem = (unknown_body_distance.pop(0)/2.0) * 215
    #
    
        logging.info('here are nodes: %s and edges: %s', mynodes, myedges)      
    
        return render_template('vizsys2.html', pathway = pathway,  mynodes = mynodes, myedges = myedges )
    except :
        return redirect(url_for('Main'))

@app.route('/<group>/<int:self_id>/')

def outcome(group, self_id):
    logging.info('here is the group: %s', group) 
    attrs= Control().query(group,self_id)
    dic = attrs._data
    logging.info('dir(): %s', dir(dic))


    return render_template('show.html',  attrs = dic )
#
#
#
@app.route('/fail/')
def fail():
    abort(401)

    
@app.route('/demo/')
def restaurant_menu():
    updates = Control().update()
    if isinstance(updates, str):
        flash(updates)
    else:
        flash('Nothing new yet')
    pcount = Planet.select().order_by(Planet.lastupdate.desc()).limit(5) 
    message =  pcount 
    return render_template('child.html', content = message)
#
#

@app.before_request
def before_request():
    db.connect()
    logging.info('connection opened')


@app.after_request
def after_request(response):
    db.close()
    logging.info('connection closed')
    return response     



    
if __name__ == '__main__' :
    logging.basicConfig(format='%(asctime)s - %(levelname)s- %(message)s', filename='error.log',level=logging.INFO)
    app.secret_key = 'super_secret_key'
    app.debug = True
    scheduler = BackgroundScheduler()
    scheduler.add_job(Control().update, 'interval', hours=24, id='updates')
    try:    
        scheduler.start()
        app.run(host = '0.0.0.0' , port = 8080)
    except (KeyboardInterrupt, SystemExit):
        scheduler.remove_job('updates')
        scheduler.shutdown()
