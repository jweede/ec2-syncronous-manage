ec2-syncronous-manage
=====================

An example of how to synchronously manage your ec2 instances with python and boto

## Prereqs
 - boto

`sudo pip install boto`

## Setup
Needs a configuration file at `~/.boto`:

    [Credentials]
    aws_access_key_id = AXXXXXXXXXXXX
    aws_secret_access_key = qXXXXXXXXXXXX+XXXXXXXXXX

These are your amazon management keys, which are easy to generate a la: [AWS access keys](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/using-credentials.html#using-credentials-access-key)

If you'd rather not add another config file, just change line 8 to:

    self.conn = boto.EC2Connection('<aws access key>', '<aws secret key>')