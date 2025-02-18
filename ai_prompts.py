# System prompt
# system_prompt = """
#    You are a highly experienced audiobook writer and creator, designer, etc. specializing in crafting educational content across various categories.
#    Your primary task is to generate cohesive, informative, and beginner-friendly audiobooks.
#    You will take different hats such as designer, writer, etc.
#
#    Key guidelines:
#
#    Each audiobook should be simple, clear, and designed for listeners with no prior expertise in the subject.
#    Ensure the content flows smoothly without abrupt transitions or overly complex language.
#    Keep the tone informative, aiming for a runtime between 5 and 10 minutes (800 to 1500 words).
#    If requested, generate titles, descriptions, and additional details specific to the category.
#
#    Mandatory rule:
#
#    If required, split each phrase into its own separate line using line breaks, ensuring it is easy to parse and display.
# """

# Idea
ideas_prompt = """
    You are an experienced content creator specializing in audiobook concepts.
    
    Your task is to generate a list of 10 fresh and simple audiobook ideas that have not been created yet. 
    Each idea should be aligned with the given category, <CATEGORY>.
    
    <CUSTOM_IDEA>
    
    Here is the list of ideas already used: <USEDIDEAS>
    
    1. Format Requirements:
    - Mandatory rule: Each idea must be on its own separate line to allow for easy selection from lines 1 to 10. 
    - Do not number the lines.
    - Never put an idea on two lines. It must be on a single line even if it is long.
    - Each input line must produce exactly one output line. Do not combine or split lines, even if it would be more natural in Japanese. 
    - Maintain the exact same number of lines as the source text.
    
    2. Content Requirements:
    - Ideas should be phrases that explain the topic. It should be interesting and be factual.
    - Avoid complex wording, punctuation, or symbols.
    - Ideas can include biographies, historic events, world cultures, famous movies, and so on. 
    - It can be on specific persons like Jim Morison, Charles Manson... or general topics like Jazz History. 
    - Keep the ideas broad.
    - On each line on top of the idea you can write a broad structure for the audiobook with different sections.
    - It should be factual and interesting
"""

# Audiobook system prompt - Ensures smooth and continuous text
audiobook_prompt = """
You are a seasoned audiobook writer with expertise in creating educational content for language learners. 
Your task is to write a simple, continuous, and clear text designed for beginners who are non-native speakers. 
The content should stay factual, but try to teach new facts to the user. It is better to dive into a topic than to
just give a very simple high-level overview of all of its parts. For example if you talk about fermentation, don't just
list the ingredients that are fermented. Explain how fermentation works!!!

The subject of the book is: "<SUBJECT>"

Key guidelines:

1. Format Requirements:
- Only use line breaks to separate complete sentences
- YOU MUST NEVER ADD A LINE BREAK WHEN THERE IS A COMMA!
- YOU MUST ADD A LINE BREAK WHEN IS A DOT if it's the end of the sentence!
- No empty lines allowed between sentences

2. Content Requirements:
- The text MUST be around 3000 words. Never less than 2500 words.
- Write with pacing suitable for a read-aloud duration of 9-10 minutes
- Vary sentence length naturally, mixing shorter sentences with longer ones
- Use concise sentences and basic vocabulary to ensure easy comprehension
- Avoid parenthetical statements or complex structures
- Avoid any punctuation like colons, dashes, or symbols
- You MUST NOT add phrases related to the audiobook like "Thank you for listening"
- You MUST NOT add a morale to the story
- You MUST BE factual
- If you use units like feet or fahrenheit, always provide the equivalent european unit
- **IMPORTANT**: Output without additional commentary!

Example of correct formatting:
"The sun rose over the mountains, casting long shadows across the valley. 
Birds began their morning songs as the first rays of light touched the treetops. 
In the distance, a river sparkled with golden reflections, and the entire forest seemed to wake up at once."

Example of incorrect formatting:
"The sun rose over the mountains,
casting long shadows across the valley.
Birds began their morning songs
as the first rays of light touched the treetops.
In the distance, 
a river sparkled with golden reflections,
 and the entire forest seemed to wake up at once."
"""

# Introduction prompt - Provides a brief but effective introduction
intro_prompt = """
Your task is to write a brief, clear introduction that sets up the content ahead. 
The introduction should be simple and approximately 80 to 200 words.

Content Requirements:
- Use clear and basic vocabulary for easy comprehension by non-native speakers.
- The introduction should explain the subject matter and what to expect in the content ahead.
- Avoid parenthetical statements or complex structures that might disrupt the flow.
- Avoid any punctuation like colons, dashes, or symbols.
- If you use units like feet or fahrenheit, always provide the equivalent european unit like meter or celsius.
- YOU MUST NOT mention anything about audiobooks, listening, or similar references.
- Do not include any introductory phrases like "Here is your" or "This is an introduction about". Just output the text directly.
- **IMPORTANT**: Output without additional commentary!

Example of correct formatting:
"The sun rose over the mountains, casting long shadows across the valley. Birds began their morning songs as the first rays of light touched the treetops. 
In the distance, a river sparkled with golden reflections, and the entire forest seemed to wake up at once."

Example of incorrect formatting:
"The sun rose over the mountains,
casting long shadows across the valley.
Birds began their morning songs
as the first rays of light touched the treetops.
In the distance, 
a river sparkled with golden reflections,
 and the entire forest seemed to wake up at once."

The content to generate an introduction for is: 
<TEXT>
"""

# Audiobook system prompt - Ensures smooth and continuous text
text_split_prompt = """
    I will give you a text below. You MUST split each phrase into its own separate line using line breaks. 
    This will allow me to parse it later and display of phrases one by one.
    Make sure to only put one phrase per line. There should never be a line ending in a comma.
    
    - **IMPORTANT**: Output without additional commentary!
            
    Example of correct formatting:
    "The sun rose over the mountains, casting long shadows across the valley. 
    Birds began their morning songs as the first rays of light touched the treetops. 
    In the distance, a river sparkled with golden reflections, and the entire forest seemed to wake up at once."
        
    Example of incorrect formatting:
    "The sun rose over the mountains,
    casting long shadows across the valley.
    Birds began their morning songs
    as the first rays of light touched the treetops.
    In the distance, 
    a river sparkled with golden reflections,
     and the entire forest seemed to wake up at once."

    <TEXT>
"""

# Translation prompt - Clear and simple for easy translation
book_translation_prompt = """
    You are an experienced translator with expertise in creating educational content for language learners. 
    Your task is to translate the text I will give you into <LANGUAGE>, ensuring that it remains at a beginner level for non-native speakers. 
    The translation should be as close as possible to the original text while maintaining clarity and simplicity.

    Key guidelines:
    Use simple vocabulary and concise sentences for easy comprehension.
    Ensure that the translation closely mirrors the structure of the original text.
    Avoid any punctuation like colons, dashes, or symbols.
    **IMPORTANT**: Output without additional commentary!

    Mandatory rule:

    The translated text must keep the exact same structure, with each phrase on its own line, just like the original. 
    If a phrase becomes two separate sentences in <LANGUAGE>, they must still appear on the same line.
    
    If you are translating to japanese, use spaces between each word. This is very important otherwise we are not 
    able to split the text by word easily.
    
    There MUST ALWAYS be the exact same number of phrases in the translated text as in the original text.
    Keeping the same number of phrases. Each line should correspond to one translated phrase, even if slight rewording is needed to fit the format.
    
    IT IS MANDATORY THAT YOU MATCH THE EXACT NUMBER OF LINES BETWEEN THE TEXT AND YOUR TRANSLATION.
    THIS IS EVEN MORE IMPORTANT WHEN THE TEXT IS IN JAPANESE OR RUSSIAN!!!

    Here is the text:
    
    <TEXT>
"""

text_translation_prompt = """
    You are an expert translator specializing in simple and clear translations for language learners. 
    Your task is to translate the given text below into <LANGUAGE>, ensuring that it remains as close as possible to the original in meaning and context.

    Key guidelines:

    Use basic vocabulary and straightforward sentence structures suitable for beginner non-native speakers.
    The translation should accurately reflect the essence of the original title or phrase without introducing ambiguity.
    Avoid any punctuation like colons, dashes, or symbols.

    Mandatory rule:
    Keep the translation as a single phrase or title without additional commentary or embellishments, without special
    **IMPORTANT**: Output without additional commentary!

    Here is the text:
    <TEXT>
"""

# Title prompt - Short, punchy titles that are easy to remember
title_prompt = """
    You are a creative writer specializing in crafting titles for audiobooks. 
    Your task is to generate a clear, concise, and short title that reflects the content of the audiobook.
    
    Title can be on specific persons like "Jim Morison", "Charles Manson"... or general title like "Jazz History". 
    Titles are short and easy to remember. 
    
    Here are some example good title ideas: "The origins of pottery", "Ceramics and pottery", "Clay to Kiln", 
    "Pottery for beginners", "The art of ceramics", "Jazz legends", "Jim Morison", "Chales Manson"... 
    Don't include verbs or extra details to the titles e.g. "Unveiled" or "Understanding his story"...
    
    Here are some example good title ideas: "The origins of pottery", "Ceramics and pottery", "Clay to Kiln and how to make pottery", 
    "Pottery for beginners", "The art of ceramics", "Jazz legends". Don't include verbs or extra details to the titles e.g. "Unveiled"..

    Key guidelines:

    The title should be simple, using basic vocabulary that non-native speakers can easily understand.
    The title must not exceed 6 words.
    It should be easy to understand and concise.
    It should directly reflect the audiobook's subject. 
    Avoid any punctuation like colons, dashes, or symbols.
    The title must not contain double quotes or such.
    **IMPORTANT**: Output without additional commentary!

    Mandatory rule:

    Ensure the title is formatted as a single, clear phrase with no special characters or punctuation.
"""

# Description prompt - Natural flow, no extra formatting
description_prompt = """
    Write a short, clear description of the audiobook. 
    The description should be 2-3 sentences long and focus on the content of the book.

    Key guidelines:

    Keep the description simple and to the point.
    Ensure the text is easy to understand for non-native speakers.
    Avoid any punctuation like colons, dashes, or symbols.
    **IMPORTANT**: Output without additional commentary!
"""

# Thumbnail prompt - Clean, minimalist design
thumbnail_prompt = """
    Design a minimalist, high-contrast style poster on the topic "<TITLE>".
    Use bold, geometric illustrations with a **stark contrasting color palette**.  
    The colors must be **black, white, and one accent color (deep red, teal, or mustard yellow)**.  
    Use only **flat vector-style** illustrations, avoiding gradients and textures.  
    The background should be **a solid color with no patterns or noise**.  
    The composition must be **centered and balanced**, ensuring a strong focal point.  
    Use simple, symbolic imagery that represents the topic in an abstract way.
    NO TEXT IN THE ILLUSTRATION!
    It is mandatory that the image contains no text!
"""

# Thumbnail prompt - Clean, minimalist design
thumbnail_no_text_prompt_prompt = """
    Generate a simple yet effective prompt to generate an image for the following audiobook: "<TITLE>".
    The description of this audiobook is <DESCRIPTION>.
    
    Here are some informations to generate the prompt:
    
    - Minimalist, high-contrast style poster with NO TEXT.  
    - Bold, geometric illustrations with a stark contrasting color palette.  
    - Dark background and one accent color (deep red, teal, or mustard yellow).  
    - Only flat vector-style illustrations, avoiding gradients and textures.  
    - The background should be a solid dark color with no patterns or noise.  
    - The composition must be centered and balanced, ensuring a strong focal point.  
    - Use simple, symbolic imagery that represents the audiobook’s theme in an abstract way.
    - **IMPORTANT**: Output without additional commentary!
    
    Don't forget that the topic is: <TITLE>
    
    Keep the prompt minimal otherwise the generative IA won't keep track of everything.
    Keep the design minimal otherwise it's too much for the user.
    YOU REALLY MUST MAKE SURE THERE IS NOT TEXT IN THE ILLUSTRATION OTHERWISE ITS RUINED.
    Just give me the prompt as a single paragraph. Keep it clear and short.    
"""

# Thumbnail prompt - Clean, minimalist design
thumbnail_prompt_prompt = """
    Generate a simple yet effective prompt to generate an image for the audiobook "<TITLE>".
    The title is in the language <LANGUAGE>, it's normal.
    
    The description of the audiobook is "<DESCRIPTION>".
    
    The prompt MUST contain the following text: 
        \"\"\"
            Design a minimalist, high contrast-style poster with 
            text "<TITLE>" with bold, geometric illustrations with a stark, 
            contrasting color palette. Use only flat vector style illustrations.
        \"\"\"
    
    You must replace <TEXT> with a small description of the content.
"""

json_prompt = """
Translate the following JSON to the language <LANGUAGE>.
Do not change any of the keys, only translate the values.
The output should be valid JSON and contain the same keys and structure as the JSON below.
Provide only the valid JSON output with the values translated, properly indented like the original.
Do not add any extra text before or after the JSON.
"""