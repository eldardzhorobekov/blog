from main.models import *

u = Profile.objects.get(username='sam')
u.get_followers()
u.get_following()
u.get_posts_feed()



from main.models import *
u = Profile.objects.get(username='sam')
p = Post.objects.all().first()
p.read_by_user(u)
