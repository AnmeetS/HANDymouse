# 👋 Welcome to the repository for HANDymouse! 👋



## Inspiration ✨
Virtual Reality has always been a fascinating concept, blurring the lines between the virtual and real world. Recently, I had the opportunity to try on the Meta Quest 3, and as I played around with it, I discovered the intriguing hand tracking features. It sparked my curiosity, making me wonder why such features aren't emphasized more. That curiosity deepened when I learned about the Apple Vision Pro, a headset aiming to allow users to control their experience without any controllers. As a result of this, I was inspired to bring a taste of that interaction to a regular computer using Python.

## The Process 🛠️
Having recently completed courses on machine and deep learning, I initially contemplated doing this by creating a hand tracking model from scratch. However, my research led me to discover Mediapipe, an open-source, cross-platform ML solution for live and streaming media. To my delight, Mediapipe had a hand landmarking model trained with an extensive dataset of approximately 30,000 images. This saved me from the daunting task of capturing that many hand images myself, completly changing my approach.

I used the documentation for the model, along with my prior knowledge of OpenCV, to develop a program that could draw landmarks on the 20 tracked points on my hands and display them in a video capture screen. With this foundation, I devised a game plan to make these landmarks meaningful. After researching how to manipulate the cursor using Python, I embarked on the challenging task of assigning functions to the landmarks.

Through a combination of critical thinking and collaboration (thanks, Dad!), I successfully created a program that could move the mouse on the screen using the location of my index finger. With a little more "critical thinking," I successfully enabled the program to not only click when I brought my index finger and thumb together but also to allow me to drag and drop items on the screen. This is where the project stands today.

## What I Learned 📚
During this journey, I gained valuable insights and skills, including:

- A deeper understanding of OpenCV functions
- Integration of OpenCV with machine learning models like Mediapipe
- Utilization of Autopy, a Python library for managing keyboard and mouse inputs

## What's Next 🔮
I'm not stopping here; my roadmap includes:

- Incorporating additional features like face detection, face landmark detection, and pose detection using Mediapipe.
- Exploring other ML solutions beyond computer vision, such as incorporating voice recognition into the project.
- Integrating the current functionality into my personal website (https://anmeetsekhon.com) to allow users to interact with 3D models.


## Try it out for yourself 👍
1. Install the entire folder.
2. Create a virtual environment in Python 3.8.
3. Use pip to install Mediapipe, TensorFlow, OpenCV, and Autopy.
4. Edit the video capture source value in `Mousemovent.py` to ensure your webcam is used.
5. Run `Mousemovement.py`.
6. Have fun! (Customize settings to improve performance; it's a bit finicky right now.)

Feel free to explore, contribute, and enhance this project any way you see fit. If you have any suggestions or things you would like me to try out, feel free to contact me!