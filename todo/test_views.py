from django.test import TestCase
from .models import item
# Create your tests here.


class TestViews(TestCase):

    def test_get_todo_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_list.html')

    def test_get_add_item_page(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/add_item.html')

    def test_get_edit_item_page(self):
        Item = item.objects.create(name='Test Todo Item')
        response = self.client.get(f'/edit/{Item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_item.html')

    def test_can_add_item(self):
        response = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(response, '/')

    def test_can_delete_item(self):
        Item = item.objects.create(name='Test todo Item')
        response = self.client.get(f'/delete/{Item.id}')
        self.assertRedirects(response, '/')
        expected_item = item.objects.filter(id=Item.id)
        self.assertEqual(len(expected_item), 0)

    def test_can_toggle_item(self):
        Item = item.objects.create(name='Test todo Item', done=True)
        response = self.client.get(f'/toggle/{Item.id}')
        self.assertRedirects(response, '/')
        updated_item = item.objects.get(id=Item.id)
        self.assertFalse(updated_item.done)

    def test_can_edit_item(self):
        Item = item.objects.create(name='Test todo Item')
        response = self.client.post(
            f'/edit/{Item.id}', {'name': 'Updated Name'})
        self.assertRedirects(response, '/')
        updated_item = item.objects.get(id=Item.id)
        self.assertEqual(updated_item.name, 'Updated Name')
