# audio notification
from pydub import AudioSegment
from pydub.playback import play

volume_discount = 5
correct_sound = AudioSegment.from_mp3('sounds/correct.mp3') - volume_discount
incorrect_sound = AudioSegment.from_mp3('sounds/incorrect.mp3') - volume_discount


def play_correct():
	play(correct_sound)

def play_incorrect():
	play(incorrect_sound)

