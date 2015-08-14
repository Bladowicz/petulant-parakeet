#!/usr/bin/python
from src import *
import datetime
import campcontrol as con
import logging
import ConfigParser
import os
import sys

def check_status(active_hour):
    return [ u'paused', u'active'][active_hour]



def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    conf_file = os.path.join(current_dir, 'config')
    config = ConfigParser.ConfigParser()
    config.read(conf_file)
    campaign_file = config.get('main', 'campaign_file')
    start = int(config.get('timer', 'start'))
    end = int(config.get('timer', 'end'))
    campaign_file = os.path.join(current_dir, campaign_file)
    campaigns = [int(x) for x in open(campaign_file)]
    if len(campaigns)==0: sys.exit()
    hhh = datetime.datetime.now().hour
    emituj = not hhh <= start and not hhh >= end
    print hhh<=start, hhh, '<=', start
    print hhh>=end, hhh, '>=',  end
    new_status = check_status(emituj)
    print campaigns, emituj, new_status
    for camp in con.session.query(con.Campaigns).filter(con.Campaigns.id.in_(campaigns)).all():
        for order in camp.orders:
            if order.status != new_status:
                order.status = new_status
                logging.info('Order {} for campaign {} is now {}'.format(order.id, camp.id, new_status))
    con.session.commit()


if __name__=="__main__":
    main()
