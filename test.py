

import tempfile

# Create a temporary file
with tempfile.NamedTemporaryFile(suffix=".txt", delete=True) as tmp_file:
    # tmp_file is like a temporary paper on the desk
    print("Temporary file path:", tmp_file.name)

    # Write something to it
    tmp_file.write(b"Hello, I am a temporary file!")
    tmp_file.flush()  # Make sure the content is written

    # Read from it
    tmp_file.seek(0)  # Go back to the start of the file
    content = tmp_file.read()
    print("Content inside the temporary file:", content.decode())

# After the 'with' block, the file disappears automatically
print("Temporary file is gone now!")