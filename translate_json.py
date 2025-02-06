import openai
import json

from ai_claude import generate_json_translation


def translate_json(input_file, target_language_code, target_language_label):
    """Translate the JSON file and validate the result."""
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data_json = json.dumps(data)
    print(f"Translating...")
    while True:
        try:
            # Call the OpenAI API to translate the JSON
            response = generate_json_translation(data_json, target_language_label)
            print(response)

            # Save the translated JSON to a new file
            output_file = f"../../../../../Audioma2/audioma/src/messages/{target_language_code}.json"
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(response)

            print(f"Translation saved to {output_file}")
            input("Press enter to continue")
            break

        except Exception as e:
            print(f"Error during translation: {e}. Retrying...")
            input("Press enter to continue")


if __name__ == "__main__":
    # Specify the input file and target language
    input_file = '../../../../../Audioma2/audioma/src/messages/en.json'
    # translate_json(input_file, 'fr', 'french')
    translate_json(input_file, 'de', 'german')
    translate_json(input_file, 'it', 'italian')
    translate_json(input_file, 'ru', 'russian')
    translate_json(input_file, 'ja', 'japanese')
    translate_json(input_file, 'es', 'spanish')
    translate_json(input_file, 'pt', 'portuguese')
