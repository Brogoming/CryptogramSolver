from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load model & tokenizer
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Example input (summarization task)
text = "summarize: Artificial intelligence is transforming various industries, including healthcare, finance, and education, by automating processes, enhancing decision-making, and improving efficiency."
inputs = tokenizer(text, return_tensors="pt")

# Generate output
output = model.generate(**inputs, max_length=50, min_length=10, length_penalty=2.0, num_beams=4)
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print(decoded_output)
