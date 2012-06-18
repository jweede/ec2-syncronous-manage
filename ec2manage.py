#!/usr/bin/env python

import boto, sys, time

class ec2_session():

    def __init__(self):
        self.conn = boto.connect_ec2()
        self.instance_names = self._init_name_id_dict()
        #Constants
        self._poll_secs = 5

    def _init_name_id_dict(self):
        reservations = self.conn.get_all_instances()
        instances = {}
        return dict([ (i.tags['Name'], i) 
                     for r in reservations 
                     for i in r.instances 
                     if 'Name' in i.tags ])

    def start_instance_names(self, instances):
        print ("Starting: %s" % instances)
        self.conn.start_instances( [self.instance_names[k].id for k in instances] )
        self._wait_for_state(instances, u'running')

    def stop_instance_names(self, instances):
        print ("Stopping: %s" % instances)
        self.conn.stop_instances( [self.instance_names[k].id for k in instances] )
        self._wait_for_state(instances, u'stopped')

    def _wait_for_state(self, instances, desired_state):
        instance_objs = [self.instance_names[k] for k in instances ]

        finished = False
        while not finished:
            time.sleep(self._poll_secs)
            for i in instance_objs:
                i.update()
            instance_state = [i.state for i in instance_objs]
            print instance_state
            finished = reduce( lambda accum, i: accum and (i==desired_state), 
                               instance_state,
                               True )
    

if __name__ == '__main__':
    e = ec2_session()
    e.start_instance_names(['gateway', 'proxy'])
    e.stop_instance_names (['gateway', 'proxy'])



    