from django.core.management import call_command
from django.test import TestCase

from postgres_searchindex.models import IndexEntry
from postgres_searchindex.tests.test_app.models import TestModel


class IndexingTests(TestCase):
    fixtures = [
        "test_app.json",
    ]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        pass

    def test_rebuild_index(self):
        call_command("postgres_searchindex_rebuild", "--force")
        qs = IndexEntry.objects.all()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs.filter(title__contains="One").count(), 1)

    def test_update_index(self):
        call_command("postgres_searchindex_update")
        qs = IndexEntry.objects.all()
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs.filter(title__contains="One").count(), 1)

    def test_update_index_unpublish(self):
        """
        unpublishing something requires index update
        """
        qs = IndexEntry.objects.all()
        call_command("postgres_searchindex_update")
        one = TestModel.objects.filter(title__contains="One").first()
        one.published = False
        one.save()
        call_command("postgres_searchindex_update")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.filter(title__contains="One").count(), 0)

    def test_update_index_deletion(self):
        """
        generic relations do cascade deletion
        """
        qs = IndexEntry.objects.all()
        call_command("postgres_searchindex_update")
        TestModel.objects.filter(title__contains="One").delete()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.filter(title__contains="One").count(), 0)
