class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("author must be of type Author")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be of type Magazine")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not (5 <= len(title) <= 50):
            raise ValueError("title must be between 5 and 50 characters inclusive")

        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        raise AttributeError("Title is immutable")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        if not isinstance(author, Author):
            raise TypeError("Author must be an instance of Author class")
        self._author = author

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, magazine):
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be an instance of Magazine class")
        self._magazine = magazine


class Author:
    all = []

    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = name
        Author.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        raise AttributeError("Name is immutable")

    @property
    def articles(self):
        return [article for article in Article.all if article.author is self]

    @property
    def magazines(self):
        return list({article.magazine for article in self.articles})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        categories = {article.magazine.category for article in self.articles}
        return list(categories)


class Magazine:
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")

        self._name = name
        self._category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name is immutable")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        raise AttributeError("Category is immutable")

    @property
    def articles(self):
        return [article for article in Article.all if article.magazine is self]

    @property
    def contributors(self):
        return list({article.author for article in self.articles})

    @property
    def article_titles(self):
        return [article.title for article in self.articles]

    def add_article(self, author, title):
        return Article(author, self, title)

    def contributing_authors(self):
        author_counts = {}
        for article in self.articles:
            if article.author in author_counts:
                author_counts[article.author] += 1
            else:
                author_counts[article.author] = 1
        return [author for author, count in author_counts.items() if count > 2]

    @classmethod
    def top_publisher(cls):
        if not cls.all:
            return None
        return max(cls.all, key=lambda magazine: len(magazine.articles))

    def __setattr__(self, key, value):
        if key in ["_name", "_category"] and hasattr(self, key):
            raise AttributeError(f"{key[1:]} is immutable")
        super().__setattr__(key, value)
