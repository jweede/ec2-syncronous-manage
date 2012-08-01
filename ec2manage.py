#!/usr/bin/env python

import boto, sys, time
import itertools

class ec2_session():

    def __init__(self, polling_freq=5):
        # uses ~/.boto
        self.conn = boto.connect_ec2()
        # explicitly state keys
        #self.conn = boto.EC2Connection('<aws access key>', '<aws secret key>')
        self.instance_names = self._init_name_id_dict()
        self._poll_secs = polling_freq

    def _init_name_id_dict(self):
        reservations = self.conn.get_all_instances()
        return { i.tags['Name']: i
                     for r in reservations 
                     for i in r.instances 
                     if 'Name' in i.tags 
                }

    def verify_instance_names(self, instances):
        for name in instances:
            print ("%s: %r" % (name, name in self.instance_names) ) 

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
            finished = reduce( lambda accum, i: accum and (i==desired_state)
                             , instance_state
                             , True )
    

if __name__ == '__main__':
    e = ec2_session()

    def flatten_list( l ):
        return list(itertools.chain.from_iterable(l) )

    names = [ ['gateway', 'proxy']
            , ['masterdb0', 'database1010']
            , ['ql0uno', 'ql0dos1', 'ql0dos2']
            , ['ql0index1']
            , ['ql0service1', 'ql0app1']
            ]
    others = [ ['bh-linux', 'ql0james'] ]

    for n in names:
        e.verify_instance_names( n )
        e.start_instance_names( n )

    #e.stop_instance_names ( flatten_list( names ) ) 



    
