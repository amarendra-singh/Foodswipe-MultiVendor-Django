from django.test import TestCase

# Create your tests here.
from datetime import time
for h in range(0,24):
    for m in range(0,30):
        print(time(h,m))