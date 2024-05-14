import json , re

# Sample string
original_string = """```json [
 {
  "Question_name": "Question 1",
  "Question": "Explain the process of photosynthesis in plants. How does it contribute to the oxygen-carbon dioxide cycle? Describe the role of chlorophyll in this process.",
  "Answer": "Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy in the form of glucose. During this process, carbon dioxide and water are converted into glucose and oxygen in the presence of sunlight and chlorophyll pigment present in the chloroplasts of plant cells. The equation for photosynthesis is:\n\\[ 6CO_2 + 6H_2O + light \\rightarrow C_6H_{12}O_6 + 6O_2  \\] \nThe oxygen produced during photosynthesis is released into the atmosphere, contributing to the oxygen-carbon dioxide cycle. Chlorophyll, a green pigment found in chloroplasts, absorbs light energy required for photosynthesis and plays a crucial role in capturing sunlight and converting it into chemical energy.",
  "Question_mark": "10"
 },
 {
  "Question_name": "Question 2",
  "Question": "What are the differences between prokaryotic and eukaryotic cells? Provide examples of organisms for each cell type and describe their unique characteristics.",
  "Answer": "Prokaryotic cells lack a distinct nucleus and membrane-bound organelles, while eukaryotic cells have a well-defined nucleus and membrane-bound organelles such as mitochondria and endoplasmic reticulum. Examples of prokaryotic organisms include bacteria and archaea, which are unicellular and lack membrane-bound organelles. On the other hand, examples of eukaryotic organisms include plants, animals, fungi, and protists. Eukaryotic cells are typically larger and more complex than prokaryotic cells, with compartmentalization allowing for specialized cellular functions.",
  "Question_mark": "20"
 }
]
```"""

# Remove triple backticks and "json" specifier
original_string = re.sub(r'^```json\s*', '', original_string)
original_string = re.sub(r'```$', '', original_string)


print(original_string)
print(type(original_string))
# Convert the JSON string to a Python object
python_obj = json.loads(original_string)

# Print the Python object
# print(python_obj)
