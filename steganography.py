import wave

# The function to get the sequence of bits which can be changed
# to substitute for the bits in the audio
def sequence_generator(byte_array_length, key, message_length):
    bits = []
    n = byte_array_length
    key = int(key)

    for i in range(message_length):
        position = (15485863 * key + 2038074743 * i) % n
        while position in range(0, 33):
            position = (15485863 * key + 2038074743 * i) % n

        bits.append(position)

    return bits

def encode(byte_array, key, message):
    # Convert the text data to a bit array
    message_bits = [int(i) for i in ''.join([bin(ord(c)).lstrip('0b').rjust(8, '0') for c in message])]
    message_len = len(message_bits)
    message_len_bin = bin(message_len)[2:].zfill(32)
    
    for i in range(32):
        byte_array[i] = (byte_array[i] & 254) | int(message_len_bin[i])

    positions = sequence_generator(len(byte_array), key, message_len)
    
    # Iterate over the text bits and hide them in the LSB of the audio data
    for i in range(len(positions)):
        byte_array[positions[i]] = (byte_array[positions[i]] & 254) | message_bits[i]

    return byte_array

def run_encode(audio_path, key, message, audio_output_path):
    # Open the audio file in read mode
    with wave.open(audio_path, "rb") as audio_file:
        # Read the frames of the audio file
        frames = audio_file.readframes(-1)
        # Convert the frames to a byte array
        byte_array = bytearray(frames)
        byte_array = encode(byte_array, key, message)
    
    # Write the modified audio data to a new file
    with wave.open(audio_output_path, "wb") as hidden_audio:
        hidden_audio.setparams(audio_file.getparams())
        hidden_audio.writeframes(byte_array)
    
    return "The data has been hidden successfully"

def run_decode(audio_output_path, key):
    with wave.open(audio_output_path, "rb") as audio_file:
        # Read the frames of the audio file
        frames = audio_file.readframes(-1)
        # Convert the frames to a byte array
        byte_array = bytearray(frames)

    message_len_bin = ""
    for i in range(32):
        bit = bin(byte_array[i])[2:].zfill(8)
        message_len_bin += str(bit[-1])

    message_len = int(message_len_bin, 2)
    positions = sequence_generator(len(byte_array), key, message_len)
    
    message_bits = []
    for i in range(len(positions)):
        message_bits.append(byte_array[positions[i]] & 1)
    
    message = ''.join([chr(int(''.join(map(str, message_bits[i:i+8])), 2)) for i in range(0, len(message_bits), 8)])
    
    return message

sample_audio_path = "C:/Users/laksh/OneDrive/Desktop/steganography/GOT Theme.wav"
suggested_output_path = "C:/Users/laksh/OneDrive/Desktop/steganography/GOT Theme_hidden.wav"

# User inputs
print(f"Suggested sample audio path: {sample_audio_path}")
audio_path = input(f"Enter audio path (or press Enter to use the suggested path): ")
if not audio_path:
    audio_path = sample_audio_path

key = int(input("enter key : "))
message = input("Enter the message : ")

print(f"Suggested output path for encoded audio: {suggested_output_path}")
audio_output_path = input(f"Enter output path for audio (or press Enter to use the suggested path): ")
if not audio_output_path:
    audio_output_path = suggested_output_path

print(run_encode(audio_path, key, message, audio_output_path))
print("The decoded text from the audio is:", run_decode(audio_output_path, key))

