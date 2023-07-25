from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from home.models import UserAddPicture, GraphicUpload
from .basket import Basket


# Create your views here.

class BasketHomeView(ListView):
    template_name = 'basket/basket.html'
    model = UserAddPicture

    def get_context_data(self, **kwargs):
        user_add_pictures = []
        graphic_uploads = []
        total_price = 0
        context = super().get_context_data(**kwargs)
        for prod_id in self.request.session.get('skey', []):
            if UserAddPicture.objects.filter(id=prod_id).exists():
                user_add_pictures.append(UserAddPicture.objects.get(id=prod_id))
            else:
                graphic_uploads.append(GraphicUpload.objects.get(id=prod_id))
        user_add_pictures += graphic_uploads
        context['session_data'] = user_add_pictures

        """
            calc total price
        """
        for object in context['session_data']:
            total_price += object.price
        context['total_price'] = total_price
        return context






def basket_add(request):
    '''
        a easy function to add a product to the basket.

        1. try to get the session from the user ( if he doesn't has one djnago will create it for him )
        2. check if the action from request is post
        3. get the value of the variable (in the script basket/script.js) productid (value= object.product_id)
        4. check if the id is from UserAddPicture- Model or GraphicUpload model and get the object with the id
        5. add the chosed product to the user-session
        6. get a response
    '''

    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        if UserAddPicture.objects.filter(id=product_id).exists():
            product = get_object_or_404(UserAddPicture, id=product_id)
            print('yes')
        else:
            product = get_object_or_404(GraphicUpload, id=product_id)
            print('noo')
        basket.add(product=product)
        response = JsonResponse({'test': 'data'})
        return response


def basket_delete(request):
    """
        function to delete single session-data.
        1. get the Basket-model to iterate over
        2. get the id from the button the user has clicked on (keep in mind to use in ajax the class selector to save
        the object.id as value in the button otherwise(with the id) you will gt all-times the id from the first object
        you get with your for loop.
        3. check wich model the user has clicked on
        4. run the remove-method from basket.py and return the response

    """

    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('delete_object_id'))
        try:
            product = get_object_or_404(UserAddPicture, id=product_id)
        except:
            product = get_object_or_404(GraphicUpload, id=product_id)
        basket.remove(product=product)
        response = JsonResponse({'test': 'data'})
        return response
    return render(request, 'basket/basket.html')
