import struct

import numpy as np
def read_and_separate_by_psna(file_path):
    with open(file_path, 'rb') as file:
        # Read the entire content of the file
        data = file.read()

        # Find the indices of occurrences of 'PSNA' in the data
        psna_indices = [i for i in range(len(data)) if data[i:i+4] == b'PSNA']

        # If 'PSNA' is found, separate the data accordingly
        if psna_indices:
            # Initialize a list to store separated data
            separated_data = []

            # Initialize the starting index for slicing
            start_index = 0

            # Iterate through the start indices and separate the data
            for psna_index in psna_indices:
                # Extract data from the last 'PSNA' occurrence to the current 'PSNA' occurrence
                separated_chunk = data[start_index:psna_index]

                # Convert the separated chunk to a byte array
                byte_array = bytearray(separated_chunk)

                # Append the byte array to the list
                separated_data.append(byte_array)

                # Update the starting index for the next iteration
                start_index = psna_index + 4

            # Add the remaining data after the last 'PSNA'
            if start_index < len(data):
                remaining_chunk = data[start_index:]
                separated_data.append(bytearray(remaining_chunk))

            return separated_data
        else:
            # 'PSNA' not found in the data
            print("'PSNA' not found in the binary file.")
            return None


# testing for myself to make sure entry is byte array
def is_byte_array(entry):
    return isinstance(entry, (bytes, bytearray))


def segment_array(byte_array):

    body_len = byte_array[0:4] # int
    i_body_len = int.from_bytes(body_len,"big")
    status = byte_array[4:8] # byte array
    adc_bitmap = byte_array[8:12] # convert to binary with space btwn each 8 chunk of
    seq_hi = byte_array[12:16] # int
    i_seq_hi = int.from_bytes(seq_hi,"big")
    seq_low = byte_array[16:20] # int
    i_seq_low = int.from_bytes(seq_low,"big")
    sec = byte_array[20:24] # int
    i_sec = int.from_bytes(sec, "big")
    nano = byte_array[24:28] # int
    i_nano = int.from_bytes(nano, "big")
    adc = byte_array[28:]

    print("body len = " + str(i_body_len))
    print("status = " + str(status))
    print("adcb = " + str(adc_bitmap))
    print("seq hi = " + str(i_seq_hi))
    print("seq low = " + str(i_seq_low))
    print("sec = " + str(i_sec))
    print("nano = " + str(i_nano))
    print("adc = " + str(adc))

    a = [i_body_len, status, adc_bitmap, i_seq_hi, i_seq_low, i_sec, i_nano, adc]
    arr = np.asarray(a, dtype=object)

    return arr



#### useless, was for testing purposes
# def segment_byte_arrays(byte_arrays):
#     segmented_data = []
#
#     for byte_array in byte_arrays:
#         # Check if the length of the byte array is divisible by 4
#         if len(byte_array) % 4 != 0:
#             print(f"Warning: Byte array length not divisible by 4. Padding with zeros.")
#
#         # Iterate through the byte array in 4-byte chunks
#         for i in range(0, len(byte_array), 4):
#             chunk = byte_array[i:i+4]
#             # If the chunk is less than 4 bytes, pad with zeros
#             chunk += bytes(4 - len(chunk))
#             segmented_data.append(chunk)

#    return segmented_data
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    file_path = ('ndata.dat')
    print('working on it...')
    result = read_and_separate_by_psna(file_path)
    print('done')
    # test = result[1][3] # should print 184 aka B8 in hex, index 3 of first byte array entry
    result_1 = segment_array(result[1])
    print(result_1[0])
    # print(asdf[1]) # prints (b'e\x13\x04\x10') cuz it segments each 4 bytes into a separate array entry


