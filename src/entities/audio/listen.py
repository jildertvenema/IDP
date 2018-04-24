from entities.audio.audio import Audio
import sounddevice as sd


class Listen(Audio):
    SAMPLE_RATE = 44100
    DURATION = 5  # secondes
    CHANNELS = 2  # stereo

    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    sd.play(recording)
    sd.wait()


def main():
    SAMPLE_RATE = 44100
    DURATION = 5  # secondes
    CHANNELS = 2  # stereo

    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    sd.play(recording)
    sd.wait()


main()
