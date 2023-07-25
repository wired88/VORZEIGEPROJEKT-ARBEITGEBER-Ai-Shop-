


class Basket():
    """
        class to check if the user has already a session if not,
        djnago will give the visior a new session to store the data

    """

    def __init__(self, request):
        self.session = request.session
        # first we check if the visiter has a session
        basket = self.session.get('skey')
        # if not, we give the visitor new session data
        if 'skey' not in request.session:
            basket = self.session['skey'] = {
            }
        self.basket = basket

    def add(self, product):
        """
            updating and adding users basket session data
            1. get the product id (from the image the user chose) from the val of button.
            2. if the product is not in the basket(...) the product will be added to the session-data
            3. self.session.modified = True - tells django that the session-data has chenged and save them correctly
            in the session
        """
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {'price': float(product.price)}
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        print(self.basket)
        if product_id in self.basket:
            print('bgt', product_id)
            del self.basket[product_id]
        self.session.modified = True
