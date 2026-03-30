from cms.api import add_plugin, create_page, create_title
from cms.models import PageContent
from cms.utils.placeholder import rescan_placeholders_for_obj
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client
from django.test.testcases import TestCase
from djangocms_versioning.models import Version

from postgres_searchindex.contrib.djangocms.compat import LT_CMS_40
from postgres_searchindex.models import IndexEntry
from postgres_searchindex.tests.test_app.cms_plugins import TestPlugin


class CMSIndexingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_basic_placeholder_indexing(self):
        the_content = "en field1"
        user = User.objects.create_superuser("admin", "", "admin")

        page = create_page("page_en", "base.html", "en", created_by=user)
        create_title("de", "page_de", page, created_by=user)
        if LT_CMS_40:
            placeholder_en = page.get_placeholders(slot="content")
        else:
            page_content_en = PageContent.admin_manager.filter(
                page=page, language="en"
            ).first()
            rescan_placeholders_for_obj(page_content_en)
            placeholder_en = page_content_en.placeholders.get(slot="content")
        add_plugin(placeholder_en, TestPlugin, "en", field1=the_content)

        call_command("postgres_searchindex_update")
        qs = IndexEntry.objects.all()
        self.assertEqual(qs.count(), 0)
        # English page should have the text plugin
        if LT_CMS_40:
            page.publish("en")
        else:
            Version.objects.get_for_content(page_content_en).publish(user)
        content_en = self.client.get(page.get_absolute_url())
        self.assertRegex(str(content_en.content), the_content)

        # index
        call_command("postgres_searchindex_update")
        qs = IndexEntry.objects.all()
        self.assertEqual(qs.filter(content__contains=the_content).count(), 1)
