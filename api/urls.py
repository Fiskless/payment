from django.urls import path, include

from .views import ItemDetail, create_session, CancelledView, SuccessView

urlpatterns = [
    path('buy/<int:id>/', create_session, name='create_session'),
    path('item/<int:id>/', ItemDetail.as_view(), name='get_item_info'),
    path('buy/<int:id>/success/', SuccessView.as_view(), name='successed_payment'),
    path('buy/<int:id>/cancelled/', CancelledView.as_view(), name='cancelled_payment'),
]