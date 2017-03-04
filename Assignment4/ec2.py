
# coding: utf-8

# In[1]:

import pytemperature
from fabric.api import *

env.host_string='ec2-52-43-135-7.us-west-2.compute.amazonaws.com'
env.user = "ubuntu"
env.key_filename = ['/Users/linzeyang/Desktop/BIA-660/Stevens-key.pem']


# In[2]:

# run a command on the server to make sure you're connected
run('uname -a')


# In[3]:

# stop the service for your project so you can edit the code
sudo('service myproject stop')


# In[4]:

# stop nginx so you can use port 41593 for testing
sudo('service nginx stop')


# In[5]:

# download the current code for your project
get('myproject.py')


# In[5]:

pwd


# In[6]:

# cd into the directory created when you downloaded the project.py file
import os
os.chdir('ec2-52-43-135-7.us-west-2.compute.amazonaws.com')


# In[7]:

ls


# In[ ]:

# edit the code in a separate window, feel free to use my code
put('myproject.py')


# In[ ]:

# if you are using my code with TextBlob make sure to install TextBlob to the chatbot env
with prefix('source activate chatbot'):
   run('pip install textblob


# In[ ]:

# we need to use our chatbot virtual environment to run the server code
with prefix('source activate chatbot'):
    run('python myproject.py')
    
#if you need to stop the server script, just select this cell and click the stop button at the top


# In[19]:

# after you've stopped the server, make sure it's not still running remotely
sudo('killall python')


# In[119]:

sudo('service myproject start')
sudo('service nginx start')

