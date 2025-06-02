# ai-blog-generator-interview-AyushMehta

## Local Installation & Running Guide

Follow these steps to set up and run the app on your local machine:

### Clone the Repository

```sh
git clone <repository-url>
cd ai-blog-generator-interview-AyushMehta


### Create and Activate a Virtual Environment (Recommended)
python -m venv Ai-blog-generator
Ai-blog-generator\Scripts\activate


###  Install Dependencies
pip install -r [requirements.txt]

### Set Up Environment Variables
ai-blog-generator=YOUR_OPENAI_API_KEY
groq-api-key=YOUR_GROQ_API_KEY


### Run the Application
python app.py


### Use the App
Visit http://127.0.0.1:5000/ to check if the server is running.
Generate a blog post by visiting:
http://127.0.0.1:5000/generate?keyword=YOUR_KEYWORD



### Output
The generated blog post will be saved as a .md file in the project directory.
The response will also include the generated blog post in JSON format.