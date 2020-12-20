from django.urls import path
from .views import index_view, personal_view, task_status_view, \
    ToolListView, ContactFormView, ToolDetailView, about_view, \
    order_list_view, OrderDetailView, OrderCreateView, OrderUpdateView, \
    UserCreateView, LoginUserView, LogoutUserView, OrderDeleteView, \
    reports_view, ToolTypeListView, OrderDownloadView

app_name = 'recognition'

urlpatterns = [
    path('', index_view, name='index'),
    path('task_status/', task_status_view, name='task_status'),
    # path('personal/<int:pk>/', personal_view, name='personal'),
    path('personal/', personal_view, name='personal'),
    path('reports/', reports_view, name='reports'),
    path('tool_list/<int:pk>/', ToolDetailView.as_view(), name='tool_info'),
    path('tool_list/', ToolListView.as_view(), name='tool_list'),
    path('tooltype_list/', ToolTypeListView.as_view(), name='tooltype_list'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('about/', about_view, name='about'),
    path('order_list/<int:pk>/order_update/', OrderUpdateView.as_view(),
         name='order_update'),
    path('order_list/<int:pk>/order_delete/', OrderDeleteView.as_view(),
         name='order_delete'),
    path('order_list/<int:pk>/order_download/', OrderDownloadView.as_view(),
         name='order_download'),
    path('order_list/<int:pk>/', OrderDetailView.as_view(),
         name='order_detail'),
    path('order_list/', order_list_view, name='order_list'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('registry/', UserCreateView.as_view(), name='registry'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
