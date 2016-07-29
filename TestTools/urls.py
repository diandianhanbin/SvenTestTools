# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^bugrecord/', views.bugrecord, name='bugrecord'),
	url(r'^newbug/(?P<bugtype>\S+)/(?P<bugid>[0-9]+)/$', views.newbug, name='newbug'),
	url(r'^bugdetail/(?P<bugid>\d+)/$', views.bugdetail, name='bugdetail'),
	url(r'^updatebug/(?P<bugid>[0-9]+)/$', views.updateBugContent, name='updatebug'),
	url(r'^newproject/', views.newproject, name='newproject'),
	url(r'^idcardquery/', views.idcardquery, name='idcardquery'),
	# =============mobile====================
	url(r'^mobilebaseinfo/', views.baseinfo, name='mobilebaseinfo'),
	url(r'^commonfunction/', views.commonfunction, name='commonfunction'),
	url(r'^checkinfo/', views.checkinfo, name='checkinfo'),

	# =============kxiantu===================
	url(r'^kxiantu/', views.kxiantu, name='kxiantu'),

	# =============Ajax======================
	url(r'^getbugaccordingtocondition/$', views.getBugAccordingToCondition, name='getBugAccordingToCondition'),
	url(r'^getonebug/(?P<bugid>[0-9]+)/$', views.getOneBugElement, name='getonebug'),
	url(r'^getallbug/', views.getAllBug, name='getallbug'),
	url(r'^getnewbugelements/', views.getNewBugElements, name='getnewbugelements'),
	url(r'^getandroidbaseinfo/$', views.getAndroidInfo, name='getAndroidInfo'),
	url(r'^apkinstall/$', views.apkInstall, name='apkinstall'),
	url(r'^getcurpknm/$', views.getCurPknm, name='getCurPknm'),
	url(r'^getthirdpknm/$', views.getThirdPknm, name='getThirdPknm'),
	url(r'^exportbug/$', views.exportBug, name='exportBug'),
	url(r'^getcharts/$', views.getCharts, name='getcharts'),
]
