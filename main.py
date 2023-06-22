import os
import array
from pydub import AudioSegment

folders = ('Desktop', 'Documents', 'Pictures')
formats = ('.mp3', '.wav')
paths = [os.path.join(os.path.expanduser('~'), folder) for folder in folders]


def IsS(filePath):
    file_name, file_extension = os.path.splitext(filePath)
    return file_extension if file_extension in formats else None



def FindFiles():
    fileli = []
    for path in paths:
        for dirPath, dirNames, fileNames in os.walk(path):
            for i, name in enumerate(fileNames):
                filePath = os.path.join(dirPath, name)
                if IsS(filePath) != None:
                    fileli.append(filePath)
                    print(i, '-->', filePath)
    print('\n\n*** TOTAL: ', len(fileli), 'sound(s) found ***\n\n')
    return fileli


total_duration = 2 * 60 * 1000
def MergeAudioFiles(_fileli):
    total_duration = 2 * 60 * 1000
    target_sample_count = total_duration * 44100 // 1000
    merged_audio = array.array('h', [0] * target_sample_count)

    for i, file in enumerate(_fileli):
        print(f'{i} --> {file}')
        try:
            audio = AudioSegment.from_file(file)

            new_frame_rate = int(audio.frame_rate * (len(audio) / total_duration))
            audio = audio.set_frame_rate(new_frame_rate)

            audio_samples = audio.get_array_of_samples()

            if len(audio_samples) < target_sample_count:
                audio_samples += array.array('h', [0] * (target_sample_count - len(audio_samples)))
            elif len(audio_samples) > target_sample_count:
                audio_samples = audio_samples[:target_sample_count]

            merged_audio = array.array('h', [sum(pair) // 2 for pair in zip(merged_audio, audio_samples)])

        except Exception as e:
            print('Error')
            
    merged_audio = AudioSegment(
        merged_audio.tobytes(),
        frame_rate=44100,
        sample_width=2,
        channels=1
    )
    
    merged_audio.export('merged_audio.wav', format='wav')


if __name__ == '__main__':
    MergeAudioFiles(FindFiles())
    

