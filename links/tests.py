from django.test import TestCase
from links.models import Category

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should result True for categories where views
        are zero or positive
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation to make sure that when we add a category an
        appropriate slug line is created
        """
        cat = cat('Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
