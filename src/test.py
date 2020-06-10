from main.models import *

u = Profile.objects.get(username='sam')
u.get_followers()
u.get_following()
u.get_posts_feed()