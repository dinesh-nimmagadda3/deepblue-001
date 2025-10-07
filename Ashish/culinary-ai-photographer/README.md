#  Culinary AI Photographer

Transform your simple food photos into delicious, professional-grade masterpieces with the power of AI. This web application provides an easy-to-use interface to upload a food image, and our AI assistant will transform it into a stunning, professional-quality photograph with a perfect 1:1 aspect ratio, ready for your food blog or social media.

![Culinary AI Photographer Screenshot](https://storage.googleapis.com/aistudio-hosting/project-assets/b2a1e3b4-f3d8-4a1e-8e6f-7d1c2d3b4e5f/app_screenshot.png)

## ✨ Features

-   **AI-Powered Image Transformation**: Utilizes Google's Gemini API (`gemini-2.5-flash-image`) to intelligently edit and enhance food photos.
-   **Two Transformation Modes: Reimagine & Polish**:
    -   **Reimagine**: Creates a completely new, professional scene. The AI rethinks the plating, utensils, and setting to be authentic and contextual to the dish.
    -   **Polish**: Re-plates your dish in a clean, minimalist style. The AI places the food on a pristine white ceramic plate within a bright studio setting, improving the composition and lighting for a sharp, appetizing, photorealistic look.
-   **Enlarge Image View**: Click on the generated AI photo to view it in a full-screen modal, perfect for appreciating the details.
-   **Download Generated Image**: Easily save the high-quality, AI-generated photo to your device with a single click.
-   **Simple File Upload**: Upload your food images (JPEG, PNG, WebP) from your device with a simple, clickable interface.
-   **Contextual Prompts**: Add a text label (e.g., "Spaghetti Bolognese") to give the AI more context for better, more accurate results.
-   **Side-by-Side Comparison**: Instantly compare your original photo with the professionally generated image.
-   **Responsive Design**: A clean, modern, and fully responsive UI built with Tailwind CSS that works beautifully on all devices.
-   **Loading & Error States**: Clear feedback for users during image processing and for any potential errors.

## 🚀 How It Works

This application is a single-page web app built with modern frontend technologies.

1.  **Image Upload**: The user selects a food photo from their computer. The app reads the file and displays it as a preview.
2.  **Choose a Mode**: The user selects one of two modes:
    -   **Reimagine**: For creating a brand-new professional composition.
    -   **Polish**: For re-plating the dish in a clean, minimalist studio style.
3.  **AI Prompting**: The user can optionally provide a text label for the food. When the "Make it Professional" button is clicked, the app sends the image data and a carefully crafted text prompt (specific to the chosen mode) to the Gemini API.
4.  **Gemini API Call**: The `gemini-2.5-flash-image` model processes the input image and text. Based on the selected mode, the AI will either completely reimagine the scene or re-plate the dish in a minimalist studio style for a clean, professional look.
5.  **Display & Interact**: The API returns the newly generated image, which is then displayed alongside the original. The user can click to enlarge the new image or download it directly.

## 🛠️ Tech Stack

-   **Frontend**: [React](https://reactjs.org/) & [TypeScript](https://www.typescriptlang.org/)
-   **AI Model**: [Google Gemini API (`gemini-2.5-flash-image`)](https://ai.google.dev/) via `@google/genai` SDK
-   **Styling**: [Tailwind CSS](https://tailwindcss.com/)
-   **Bundling/Environment**: The app is designed to run in an environment where `esbuild` or a similar tool handles module resolution, as seen in `index.html`.

## ⚙️ Setup and Running

To run this project, you need to have an environment that can serve the static files and provide the necessary API key.

1.  **Clone the repository** (or have the project files).
2.  **Set up your API Key**: The application requires a Google Gemini API key. This key must be available as an environment variable named `API_KEY`.

    ```
    # In your environment setup (e.g., .env file or server configuration)
    API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

3.  **Serve the files**: Use a simple local server to host the `index.html` and its associated JavaScript/TypeScript files.

##  usage

1.  Open the application in your web browser.
2.  Click the **"Upload Food Photo"** button or the placeholder card and select an image file from your device.
3.  Your uploaded image will appear in the "Original Food Photo" card.
4.  (Optional but recommended) In the text box, type the name of the food (e.g., "Avocado Toast", "Chocolate Lava Cake").
5.  Select your desired mode: **Reimagine** or **Polish**.
6.  Click the **"Make it Professional"** button.
7.  Wait a few moments while the AI works its magic. A loading spinner will indicate that the image is being processed.
8.  The new, professionally styled image will appear in the "Professional AI Photo" card.
9.  Click on the new image to view it in a larger pop-up.
10. Click the **"Download Photo"** button to save the image to your computer.