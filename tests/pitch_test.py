import unittest
from app.models import Comment, Pitch

class PitchModelTest(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(id = 1, title = 'What Makes a Place So Boring', pitch_content = 'Where is the boring place located? And whom should you ask—a composer/a cognitive psychologist?', category = 'Pickup Lines', upvote = 28, downvote = 6, author = 'Trir All'
)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)