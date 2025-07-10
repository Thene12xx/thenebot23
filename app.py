@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip().lower()
    print("User input:", user_input)

    # Custom predefined responses
    custom_responses = {
        'hi': "Hello there thenemate!",
        'who are you': "I am thenebot powered by TinyLLaMA.",
        'bye': "Goodbye! Come back soon to thene.",
    }    

    if user_input in custom_responses:
        return jsonify({'response': custom_responses[user_input]})

    # Else: fall back to TinyLLaMA
    try:
        result = subprocess.run(
            ['ollama', 'run', 'tinyllama', user_input],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        response = result.stdout.decode().strip()
        error_output = result.stderr.decode().strip()

        if error_output:
            print("Ollama Error:", error_output)

        print("TinyLLaMA Response:", response)
        return jsonify({'response': response})

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({'error': str(e)})
