import uuid # Required for unique book instances
from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Genre(models.Model):
    """
    책 장르를 나타내는 모델 (예 : 공상 과학, 논픽션).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def display_genre(self):
        """
        장르 문자열을 만듭니다. 관리자에 장르를 표시하는 데 필요합니다.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """
        Model 객체를 나타내는 문자열 (관리자 사이트 등)
        """
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # 책은 한 명의 작성자 만 가질 수 있지만 작성자는 여러 개의 책을 가질 수 있으므로 사용되는 외래 키
    # 파일에서 아직 선언되지 않았으므로 객체가 아닌 문자열로 작성하십시오.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    # 장르는 많은 책을 포함 할 수 있기 때문에 ManyToManyField가 사용되었습니다. 책은 여러 장르를 포괄 할 수 있습니다.
    # 장르 클래스가 이미 정의되어 있으므로 위의 개체를 지정할 수 있습니다.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])




class BookInstance(models.Model):
    list_filter = ('status', 'due_back')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)



class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}, {1}'.format(self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']
