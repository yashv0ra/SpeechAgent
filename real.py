import threading
import time
import voice_in
import text_io
import voice_out

def task1():
        voice_in.main()

def task2():
        text_io.main()
def task3():
        voice_out.main()
# Create thread objects
thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)
thread3 = threading.Thread(target=task3)

# Start the threads
thread1.start()
thread2.start()
thread3.start()

# Join the threads to the main thread to keep them running
thread1.join()
thread2.join()
thread3.join()
# run these two commands in terminal before use: 
# export GROQ_API_KEY=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
# export DEEPGRAM_API_KEY=5112f394cfb185257a9ffddf6ffb982358ec1934

