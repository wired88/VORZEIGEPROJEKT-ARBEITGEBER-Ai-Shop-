

class Home:
    """
        class to store user input in session-data (for search)
    """

    def __init__(self, request):
        self.session = request.session
        search_data = self.session.get('search_data')
        if 'search_data' not in request.session:
            search_data = self.session['search_data'] = {
            }
        self.search_data = search_data

    def get_data(self):
        pass