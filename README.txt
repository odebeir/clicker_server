============================
Click server
============================

Simple http server used in conjunction with Notebook for Ipython

The projects is base on

1 - a simple http server that run on the presenter pc

2 - a toolbox that the presenter must import from it's notebook session

3 - a webclient for each participant

--------------
DEPENDENCIES
--------------
all dependencies should be included in EPD or similar distributions...

(to be checked...)

--------------
INSTALL
--------------

(to be done...)

python setup.py install

--------------
USAGE
--------------

starting the server:

    > python custom_handler.py

starting a notebook session

    > ipython notebook --pylab=inline

inside notebook:

    In[1]: from notebook_tools import ask

the following command:

    In[2]: ask('a,b,c',sec=10)

will start a session during which each client can answer with a webclient

e.g.

    http://10.0.1.6:8000/A

    where 10.0.1.6 is the ip address of the presenter pc.
