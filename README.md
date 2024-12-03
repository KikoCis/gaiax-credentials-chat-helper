# Gaia-X Credential Serice Assistant

This project was created for the Gaia-X Hackathon December 2024, responding to the challenges proposed by Aire Networks and CTIC.

 **DISCLAIMER**: This is NOT an official Gaia-X tool or implementation. This project was created as part of a hackathon challenge and should be considered a proof of concept only. It is not endorsed by or affiliated with Gaia-X AISBL or any official Gaia-X initiative.

This project was created for the Gaia-X Hackathon December 2024, responding to the challenges proposed by Aire Networks and CTIC.


## Hackathon Challenge Context

This solution addresses the Professional Challenge: Automatic Generation of Gaia-X Self-Descriptions, focusing on:
- Automatic generation of Self-Descriptions
- Integration with Let's Encrypt as Trust Anchor
- Implementation of the Gaia-X Trust Framework
- Support for Verifiable Credentials (VC) 2.0

The assistant is designed to help developers and technical teams working with Gaia-X implementations by providing expert guidance and automated analysis of technical issues.

## Technical Solution

This is a specialized chat assistant powered by Ollama and the qwen2.5:1.5b model, providing expert guidance on:
- Gaia-X Trust Framework
- Verifiable Credentials
- Technical implementations
- Self-Description generation
- Certificate management

## Prerequisites

- Python 3.8+
- Ollama installed and running
- qwen2.5:1.5b model pulled in Ollama

## Setup Instructions

1. **Install Ollama**: Follow the instructions at [Ollama's official website](https://ollama.ai/download).

2. **Pull the qwen2.5:1.5b model**:
   ```bash
   ollama pull qwen2.5:1.5b
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Assistant

### API Mode

To run the assistant in API mode, execute the following command:

```bash
python main.py --mode api
```

The API will be available at `http://localhost:8000`. You can use the `/analyze-output` endpoint to analyze error messages.

### Console Mode

To interact with the assistant via the console, use:

```bash
python main.py --mode console
```

Type your questions directly into the console. Type 'exit' to end the session.

### Web Mode

To run the assistant with a web interface, use:

```bash
python main.py --mode web
```

Access the web interface at `http://localhost:8000`.

## Important Notes

- Ensure Ollama is running before starting the assistant.
- The prompt has been specifically prepared for the qwen2.5:1.5b model to provide accurate and context-aware responses.
- The assistant uses a memory system to maintain context across interactions, enhancing the quality of responses.

## Challenge Objectives Addressed

1. **Automatic Self-Description Generation**
   - Integration with OpenAPI/AsyncAPI specifications
   - Automatic metadata extraction
   - JSON-LD format compliance

2. **Let's Encrypt Integration**
   - Support for automated certificate management
   - Integration with v1-staging branch of GXDCH
   - Clear handling of EV-SSL vs non-EV-SSL certificates

3. **Technical Documentation**
   - Comprehensive error analysis
   - Clear guidance on technical implementations
   - Integration support for Verifiable Credentials

## Evaluation Criteria Met

- Automatic processing of OpenAPI/AsyncAPI specifications
- Generation of compliant Self-Descriptions
- Integration with Let's Encrypt certificates
- Clear error handling and user guidance
- Comprehensive technical documentation

## Troubleshooting

- If you encounter issues with the model, ensure it is correctly pulled and running in Ollama.
- Check that all Python dependencies are installed correctly.

## References

- Gaia-X Digital Clearing House: https://gaia-x.eu/gxdch/
- VC Data Model 2.0: W3C
- Gaia-X Trust Framework
- Let's Encrypt Documentation

## Hackathon Information

This project was developed as part of the Gaia-X Hackathon (December 2024), addressing the Professional Challenge proposed by Aire Networks and CTIC for the automatic generation of Gaia-X Self-Descriptions.

## Authors

- [Jacinto Arias](https://github.com/jacintoArias)
- [Kiko Cisneros](https://github.com/kikoCis)
- [Pedro Gómez](https://github.com/pegomez)
- [Álvaro Manuel Recio Pérez](https://github.com/amrecio)
- [Javier D. Serrano](https://github.com/JavierDSer)

