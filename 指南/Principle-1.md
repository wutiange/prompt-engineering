# Write clear and specific instructions

现在让我们深入了解这一原则：即编写明确和具体的指令。
你应该通过提供尽可能明确和具体的指令来表达您想让模型做什么，这将指导模型朝着所需的输出方向并减少您获得无关或不正确的响应的机会，不要将编写明确提示与编写简短提示混淆，因为在很多情况下，更长的提示实际上提供了更多的清晰度和上下文，这实际上可以得到更详细与之相关的输出。

## Tactic 1: Use delimiters

帮助您编写明确和具体的指令的第一个策略是使用分隔符清楚地指示输入的不同部分。

- Triple quotes: """
- Triple backticks: ```
- Triple dashes: ---
- Triple brackets: < >
- XML tags: <tag></tag>

让我给您展示一个例子：
```python
text = f"""
You should express what you went a model to do by providing instructions that are as clear and specific as you can possibly make them. This will guide the model towards the desired output, and reduce the chances of receiving irrelevant or incorrect response, Don't confuse writing a clear prompt with writing a short prompt. In many cases, longer prompts provide more clarity and context for the model, which can lead to more detailed and relevant outputs.
"""
prompt = f"""
Summarize the tet delimited by triple backticks into a single sentence.
```{text}```
"""
response = get_completion(prompt)
print(response)
```
我们有一个段落，我们想要实现的任务是对这个段落进行总结，因此在提示中，我用 ``` 来包裹要总结的文本，接着我们使用我们的 get_completion 函数来获取响应：
```text
Clear and specific instructions should be provided to guide the model towards the desired output, and longer prompts can provide more clarity and context for the model.
```

## Tactic 2: Ask for structured output

这一策略是结构话输出，为了使解析模型输出更容易，可以请求使用 HTML 或 JSON 等结构化输出。

- HTML
- JSON

接下来让我们看一个例子：
```python
prompt = f"""
Generate a list of three made-up book titles alone with their authors and genres. Provide them in JSON format with the following keys: book_id, title, author, genre.
"""
response = get_completion(prompt)
print(response)
```
我们说要生成三个虚构的书名以及它们的作者和类型的列表，并以 JSON 格式提供以下 keys ，即 book_id, title, author, genre 。
得到的结果为：
```json
[
  {
    "book_id": 1,
    "title": "The Lost City of Zorath",
    "author": "Aria Blackwood",
    "genre": "Fantasy"
  },
  {
    "book_id": 2,
    "title": "The Last Hope",
    "author": "Ethan Stone",
    "genre": "Science Fiction"
  },
  {
    "book_id": 3,
    "title": "The Secret of the Haunted Mansion",
    "author": "Lila Rose",
    "genre": "Mystery"
  }
]
```

## Tactic 3: Check whether conditions are satisfied

这个策略是要求模型检查是否满足条件；因此假设结论是不成立的，那么我们可以告诉模型首先检查这些假设，如果不满足则输出建设不成立；您还可以考虑潜在的边缘情况以及模型应如何处理它们以避免意外错误或结果，这样当不符合的时候就会按照你想的那样输出。

Check assumptions required to do the task.

接下来看例子：
```python
text_1 = f"""
Making a cup of tea is easy! First, you need to get some water boiling. While that's happening, grab a cup and put a tea bag in it. Once the water is hot enough, just pour it over the tea bag. Let it sit for a bit so the tea can steep. After a few minutes, take out the tea bag. If you like, you can add some sugar or milk to taste. And that's it! You've got yourself a delicious cup of tea to enjoy.
"""
prompt_1 = f"""
You will be provided with text delimited by triple quotes.
If it contains a sequence of instructions, re-write those instructions in the following format:
Step 1 - ...
Step 2 - ...
...
Step N -
If the text does not contain a sequence of instructions, then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
response = get_completion (prompt_1)
print ("Completion for Text 1:")
print (response)
```
这是一段描述制作茶的步骤；下面的 prompt 则是告诉 chatGPT 在引号中俄内容如果有对应步骤的提示，那么就使用 `Step 1` 这样的方格式重新编写；否则输出 `No steps provided` 。
得到的结果为：
```text
Completion for Text 1:
Step 1 - Get some water boiling.
Step 2 - Grab a cup and put a tea bag in it.
Step 3 - Once the water is hot enough, pour it over the tea bag.
Step 4 - Let it sit for a bit so the tea can steep.
Step 5 - After a few minutes, take out the tea bag.
Step 6 - Add some sugar or milk to taste.
Step 7 - Enjoy your delicious cup of tea!
```

下面看一个输出为 “ No steps provided ” 的例子：
```python
text_2 = f"""
The sun is shining brightly today, and the birds are singing. It's a beautiful day to go for a walk in the park. The flowers are blooming, and the trees are swaying gently in the breeze. People are out and about, enjoying the lovely weather. Some are having picnics, while others are playing games or simply relaxing on the grass. It's a perfect day to spend time outdoors and appreciate the beauty of nature.
"""
prompt_2 = f"""
You will be provided with text delimited by triple quotes.
If it contains a sequence of instructions, re-write those instructions in the following format:
Step 1 - ...
Step 2 - ...
...
Step N -
If the text does not contain a sequence of instructions, then simply write \"No steps provided.\"

\"\"\"{text_2}\"\"\"
"""
response = get_completion (prompt_2)
print ("Completion for Text 2:")
print (response)
```

其结果为：
```text
Completion for Text 2:
No steps provided.
```