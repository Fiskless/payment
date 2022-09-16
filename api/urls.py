from django.urls import path, include

from .views import ItemDetail, \
    create_session_for_item, \
    create_session_for_order,\
    CancelledView, \
    SuccessView, \
    OrderDetail

urlpatterns = [
    path('buy_item/<int:id>/', create_session_for_item,
         name='create_session_for_item'),
    path('buy_item/<int:id>/success/', SuccessView.as_view(),
         name='successed_payment_item'),
    path('buy_item/<int:id>/cancelled/', CancelledView.as_view(),
         name='cancelled_payment_item'),
    path('buy_order/<int:id>/', create_session_for_order,
         name='create_session_for_order'),
    path('buy_order/<int:id>/success/', SuccessView.as_view(),
         name='successed_payment_order'),
    path('buy_order/<int:id>/cancelled/', CancelledView.as_view(),
         name='cancelled_payment_order'),
    path('item/<int:id>/', ItemDetail.as_view(), name='get_item_info'),
    path('order/<int:id>/', OrderDetail.as_view(), name='get_order_info'),
]