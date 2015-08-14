#!/usr/bin/python
from src import *
from campcontrol import *
import shelve
import datetime
import json
import logging
import glob
import os
import smtplib
from email.mime.text import MIMEText



def check_for_stage_1(data, campaigns, spent=100):
    for camp in session.query(Campaigns).filter(Campaigns.id.in_(campaigns)).all():
        total = camp.total_cost()
        #print data
        if total > spent and data[unicode(camp.id)]['stage']==0: ## TODO
            data[unicode(camp.id)]['stage'] = 1
            camp.status = check_status(True)
            data[unicode(camp.id)]['date'] = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
            logging.info('Campaign {} reached stage 1 - will stop now'.format(camp.id))


def check_for_stage_2(data, campaigns):
    now = datetime.datetime.now()
    for camp in campaigns:
        curr_data = data[unicode(camp)]
        if curr_data['stage'] == 1 and seconds_from(curr_data['date'])>7200:
            logging.info('Campaign {} reached stage 2 - will optimize and start now'.format(camp))
            data[unicode(camp)]['stage'] = 2
            run_optimalization(camp)
            session.query(Campaigns).get(int(camp)).status = check_status(False)
            log_stats(camp)

def log_stats(camp):
    camp = session.query(Campaigns).get(int(camp))
    logging.info("Campaign {} has {} conversions, {} impressions".format(
        camp.id, camp.total_conv(), camp.total_imps()
        ))

def check_status(active):
    return [ u'paused', u'active'][active]


def run_optimalization(camp):
    for o in session.query(Campaigns).get(camp).orders:
        print o
        os.system('cd /home/model/m3/DCO_v1/; Rscript kiepske_banery_i_hosty.R {}'.format(o.hash))
        disable_banners()
    #Rscript kiepske_banery_i_hosty.R IzJyqinyiNHcx8moREiL


def disable_banners():
    out = []
    for each in glob.glob('/home/model/m3/DCO_v1/*.creative.bad'):
        out.extend( [unicode(hash.strip()) for hash in open(each)])
        os.remove(each)
    for crea in session.query(Creatives).filter(Creatives.hash.in_(out)).all():
        logging.info("Banner {} that was {} will now be paused #[{}]".format(
            crea.id, crea.status, crea.hash
            ))


def check_for_stage_3(data, campaigns, spent=100):
    for camp in session.query(Campaigns).filter(Campaigns.id.in_(campaigns)).all():
        total = camp.total_cost()
        if total > spent and data[unicode(camp.id)]['stage']==2: ## TODO
            data[unicode(camp.id)]['stage'] = 3
            camp.status = check_status(True)
            data[unicode(camp.id)]['date'] = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
            logging.info('Campaign {} reached stage 3 - will stop now'.format(camp.id))


def seconds_from(word):
    now = datetime.datetime.now()
    then = datetime.datetime.strptime(word, "%Y%m%d %H%M%S")
    return (now - then).total_seconds()

def check_for_new(in_dict, camps):
    for camp in camps:
        #print in_dict
        if not in_dict.has_key(unicode(camp)):
            logging.info('New campaign {}'.format(camp))
            data[unicode(camp)] = {
                    'date':None,
                    'stage':0,             
                    }
    return in_dict


def get_json(filename):
    return json.loads(open(filename).read())

def dump_json(filename, data):
    with open(filename, 'w') as fw:
        fw.write(json.dumps(data))

def email_to():
    log = 'work.log'
    if os.path.exists(log):
        content = open(log).read()
        if content == '': return
        msg = MIMEText(content)
        msg['Subject'] = 'Automat - {}'.format(datetime.datetime.now())
        e_from = 'Automaton@works.pl'
        adresy = [x.strip() for x in open('emails.txt')]
        s = smtplib.SMTP('localhost')
        s.sendmail(e_from, adresy, msg.as_string())
        s.quit()
        fw = open('big.log', 'a')
        fw.write(content)
        fw.close()
        os.remove(log)

        



def main():
    global data
    spent_1 = 200
    spent_2 = 330

    current_dir = os.path.dirname(os.path.realpath(__file__))
    conf_file = os.path.join(current_dir, 'config')
    config = ConfigParser.ConfigParser()
    config.read(conf_file)
    campaign_file = config.get('main', 'campaign_file')
    campaign_file = os.path.join(current_dir, campaign_file)
    campaigns = [int(x) for x in open(campaign_file)]
    data = get_json('our.json')
    data = check_for_new(data, campaigns)
    check_for_stage_1(data, campaigns, spent_1 )
    check_for_stage_2(data, campaigns,)
    check_for_stage_3(data, campaigns, spent_2 )
    #check_for_stage_4(data, campaigns,)
#    data.close()
    #session.commit() 
    dump_json('our.json', data)
    email_to()


if __name__=="__main__":
    main()
