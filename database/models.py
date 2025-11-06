class Book:
    def __init__(self, _id, title, author, year, status):
        self.id = _id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return ("Book(id={}, title={}, author={}, year={}, status={})".
                format(self.id, self.title, self.author, self.year, self.status))

    def __repr__(self):
        return ("Book(id={}, title={}, author={}, year={}, status={})".
                format(self.id, self.title, self.author, self.year, self.status))