# PellikenAI

PellikenAI is a Streamlit-based application that integrates various machine learning models for image restoration and upscaling, along with a chatbot powered by OpenAI's GPT-3.5-turbo. The application also features a payment processing system for chat interactions, utilizing AlbyProcessor for handling Lightning Network payments.

## Features

- **Image Restoration**: Restore images using the Tencent ARC GFPGAN model.
- **Image Upscaling**: Upscale images using the Real-ESRGAN model.
- **Chatbot**: Chat with an AI assistant powered by OpenAI's GPT-3.5-turbo.
- **Payment Processing**: Handle payments via the Lightning Network using AlbyProcessor.

## Installation

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Replicate
- Requests
- aiohttp
- qrcode
- PIL (Pillow)
- OpenAI

### Install Dependencies

```bash
pip install streamlit replicate requests aiohttp qrcode pillow openai
```

## Configuration

### Environment Variables

You need to set the following environment variables:

- `REPLICATE_API_TOKEN`: Your Replicate API token.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `ALBY_API_KEY`: Your Alby API key.

You can set these in a `.env` file or directly in your environment.

### Streamlit Secrets

Add your API keys to Streamlit secrets by creating a `secrets.toml` file:

```toml
[secrets]
REPLICATE_API_TOKEN = "your_replicate_api_token"
OPENAI_API_KEY = "your_openai_api_key"
ALBY_API_KEY = "your_alby_api_key"
```

## Usage

### Running the Application

To run the Streamlit application, use the following command:

```bash
streamlit run app.py
```

### Image Restoration

Restore an image using the Tencent ARC GFPGAN model:

```python
restore_image_http(base64_image: str, scale: int)
```

### Image Upscaling

Upscale an image using the Real-ESRGAN model:

```python
upscale_image(base64_image: str, scaling_factor: int)
```

### Chatbot Interaction

Chat with the AI assistant:

```python
handle_chat(prompt_model: PromptModel)
```

## Payment Processing

The application includes functionality to handle payments via the Lightning Network using AlbyProcessor. Payment requests are created and monitored to ensure that the service is paid for before continuing with the chat interaction.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

For support, please join our [Telegram group](https://t.me/+84Fwhhg3VyU3Mjdk).

---

PellikenAI is developed by Walter Maffione. For more information, visit [https://www.pelliken.it/](https://www.pelliken.it/).

