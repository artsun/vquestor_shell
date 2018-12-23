class Vertex:
    """"
    USER:  {user_id: {'first_name': 'name', 'last_name': 'lastname', 'bdate': 'xx.xx.xx'}}
    LINKS:  {user_id: {'first_name': 'name', 'last_name': 'lastname', 'bdate': 'xx.xx.xx'},
            user_id: {'first_name': 'name', 'last_name': 'lastname', 'bdate': 'xx.xx.xx'}}
    """
    __slots__ = ['user', 'links', 'nodes']

    def __init__(self, user='', links='', nodes=None):
        self.links = links
        self.user = user
        if nodes is None:
            self.nodes = list()
