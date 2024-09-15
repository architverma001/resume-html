# PDF to HTML Conversion App

This project converts PDF files into HTML format using OpenAI. It involves extracting text from a PDF and then generating HTML from that text with the help of OpenAI's API.

## Overview

Initially, the focus was on processing the PDF input to extract the text, which was achieved using Python libraries. Instead of directly developing the app, I opted to test and iterate in Google Colab due to its user-friendly interface and continuous testing capability.

To evaluate OpenAI’s performance in generating HTML from the extracted text, I used the GPT-3.5 model, which worked well. Once satisfied, I crafted a suitable prompt for the task.

Next, I moved to building the application, choosing FastAPI since I had recently been learning about it. API keys were managed using `.env` files with dynamic key updates. The frontend was developed with basic HTML and Bootstrap for the index page.

Finally, the app was deployed on Render.

Deployed App Link: [PDF to HTML Converter](https://resume-html-79dx.onrender.com/)
