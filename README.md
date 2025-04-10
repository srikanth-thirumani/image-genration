# AI Image Generator

A Streamlit application that generates images using the Stability AI API (DreamStudio).

![AI Image Generator](https://via.placeholder.com/650x400)

## Features

- Generate AI images using text prompts
- Simple and intuitive user interface
- Real-time image generation
- Safety filters for appropriate content

## Installation

### Prerequisites

- Python 3.7+
- Stability AI API key (from [DreamStudio](https://dreamstudio.ai/))

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/srikanth-thirumani/image-generation.git
   cd ai-image-generator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```
   DREAMSTUDIO_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser at `http://localhost:8501`

3. Enter a text prompt in the input field

4. Click the "Generate Image" button

5. Wait for the image to be generated and displayed

## Advanced Features

### Customizing Image Generation Parameters

You can enhance the application by adding controls for advanced parameters:

```python
# Add these to your Streamlit app
st.sidebar.header("Advanced Settings")

# Image dimensions
img_size = st.sidebar.selectbox(
    "Image Size", 
    options=["512x512", "768x768", "1024x1024"], 
    index=0
)

# Number of steps (higher = better quality but slower)
steps = st.sidebar.slider("Generation Steps", min_value=10, max_value=150, value=30)

# CFG Scale (how closely the image follows the prompt)
cfg_scale = st.sidebar.slider("CFG Scale", min_value=1, max_value=20, value=7)

# Model selection
engine = st.sidebar.selectbox(
    "Engine",
    options=["stable-diffusion-xl-1024-v1-0", "stable-diffusion-v1-5"],
    index=0
)
```

Update the `generate_image` function to use these parameters:

```python
def generate_image(text, engine_id, steps, cfg_scale, width, height):
    # Parse dimensions
    width_val, height_val = map(int, img_size.split('x'))
    
    # Initialize the Stability API client
    stability_api = client.StabilityInference(
        key=DREAMSTUDIO_API,
        verbose=True,
        engine=engine_id,  # Engine ID from dropdown
    )
    
    # Generate image based on the prompt text
    answers = stability_api.generate(
        prompt=text,
        seed=95456,
        steps=steps,  # Number of diffusion steps
        cfg_scale=cfg_scale,  # How strictly the diffusion process adheres to the prompt
        width=width_val,
        height=height_val,
    )
    # ...rest of function remains the same
```

### Adding Image Download Feature

```python
if generated_img:
    st.image(generated_img, caption="Generated Image", use_column_width=True)
    
    # Add download button
    img_buffer = io.BytesIO()
    generated_img.save(img_buffer, format="PNG")
    
    st.download_button(
        label="Download Image",
        data=img_buffer.getvalue(),
        file_name=f"ai_generated_{prompt_text[:20]}.png",
        mime="image/png"
    )
```

### Multiple Generation Mode

Allow users to generate multiple variations of the same prompt:

```python
# Add this to your sidebar
num_images = st.sidebar.slider("Number of Images", min_value=1, max_value=4, value=1)

# Modify the generation part
if st.button("Generate Image(s)"):
    if prompt_text:
        with st.spinner(f"Generating {num_images} image(s)..."):
            # Create columns for images
            if num_images > 1:
                cols = st.columns(min(num_images, 2))
                
                for i in range(num_images):
                    col_idx = i % 2
                    with cols[col_idx]:
                        seed = 95456 + i  # Different seed for each image
                        generated_img = generate_image(prompt_text, engine, steps, cfg_scale, width_val, height_val, seed)
                        if generated_img:
                            st.image(generated_img, caption=f"Image {i+1}", use_column_width=True)
                            # Add download button for each image
                            img_buffer = io.BytesIO()
                            generated_img.save(img_buffer, format="PNG")
                            st.download_button(
                                label=f"Download Image {i+1}",
                                data=img_buffer.getvalue(),
                                file_name=f"ai_generated_{i+1}.png",
                                mime="image/png"
                            )
            else:
                # Original single image generation code
                generated_img = generate_image(prompt_text, engine, steps, cfg_scale, width_val, height_val)
                if generated_img:
                    st.image(generated_img, caption="Generated Image", use_column_width=True)
                    # Download button code
```

## Security Considerations

- **Never commit your API key** directly in the code
- Always use environment variables or a secure secrets manager
- Implement prompt filtering to prevent inappropriate content
- Add user authentication for public deployments

## Troubleshooting

- **Error: Connection failed**: Check your internet connection and API key
- **Error: Safety filters triggered**: Modify your prompt to be more appropriate
- **Slow generation**: Reduce image size or number of steps

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Stability AI](https://stability.ai/) for their image generation API
- [Streamlit](https://streamlit.io/) for the wonderful web app framework
