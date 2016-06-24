# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^mobile/', views.mobile, name='mobile'),
	url(r'^bugrecord/', views.bugrecord, name='bugrecord'),
	url(r'^getallbug/', views.getAllBug, name='getallbug'),
	url(r'^newbug/(?P<bugtype>\S+)/(?P<bugid>[0-9]+)/$', views.newbug, name='newbug'),
	url(r'^getnewbugelements/', views.getNewBugElements, name='getnewbugelements'),
	url(r'^bugdetail/(?P<bugid>\d+)/$', views.bugdetail, name='bugdetail'),
	url(r'^getonebug/(?P<bugid>[0-9]+)/$', views.getOneBugElement, name='getonebug'),
	url(r'^updatebug/(?P<bugid>[0-9]+)/$', views.updateBugContent, name='updatebug'),
	url(r'^newproject/', views.newproject, name='newproject'),
	url(r'^getbugaccordingtocondition/$', views.getBugAccordingToCondition, name='getBugAccordingToCondition'),
	url(r'^idcardquery/', views.idcardquery, name='idcardquery'),
]
