# Give the model time to link

我们的第二个原则是给模型思考的时间。如果模型通过急于做出结论而出现推理错误，在模型在最终回答之前，您应该尝试重新构建查询请求相关推理的链或序列。

## Tactic 1: Specify the steps to complete a task.

我们的第一个策略是指定完成任务所需的步骤。

Step 1: ...
Step 2: ...
...
Step N: ...

先看示例：
```python
# 这是一段 Jack 和 Jill 的故事
text = f"""
In a charming village, siblings Jack and Jill set out on a quest to fetch water from a hilltop
well. As they climbed, singing joyfully, misfortune struck-Jack tripped on a stone and tumbled down the hill, with Jill following suit.
Though slightly battered, the pair returned home to comforting embraces. Despite the mishap, their adventurous spirits remained undimmed, and they continued exploring with delight.
"""
# example 1
prompt_1 = f"""
Perform the following actions:
1 - Summarize the following text delimited by triple backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
"""
response = get_completion(prompt_1)
print( "Completion for prompt 1:")
print(response)
```
我们的要求是：
1-用1句话总结以下由三个反调分隔的文本。
2-将摘要翻译成法语。
3-在法语摘要中列出每个名字。
4-输出一个json对象，该对象包含以下键：french_summary、num_names。

得到的结果为：
```text
Completion for prompt 1:
1 - Siblings Jack and Jill go on a quest to fetch water from a hilltop well, but misfortune strikes as Jack trips and tumbles down the hill, with Jill following suit, yet they return home slightly battered but with their adventurous spirits undimmed.
2 - Les frères et sœurs Jack et Jill partent en quête d'eau d'un puits au sommet d'une colline, mais la malchance frappe lorsque Jack trébuche sur une pierre et dévale la colline, suivi de Jill, mais ils rentrent chez eux légèrement meurtris mais avec leurs esprits aventureux intacts.
3 - Jack, Jill
4 - {
     "french_summary": "Les frères et sœurs Jack et Jill partent en quête d'eau d'un puits au sommet d'une colline, mais la malchance frappe lorsque Jack trébuche sur une pierre et dévale la colline, suivi de Jill, mais ils rentrent chez eux légèrement meurtris mais avec leurs esprits aventureux intacts.",
     "num_names": 2
   }
```
我把其中的法语改成中文，得到的结果为：
```text
Completion for prompt 1:
1 - Siblings Jack and Jill go on a quest to fetch water from a hilltop well, but misfortune strikes when Jack trips and tumbles down the hill, with Jill following suit, yet they return home slightly battered but with their adventurous spirits undimmed.
2 - 兄妹杰克和吉尔前往山顶井取水，但不幸的是，杰克绊倒在石头上滚下山，吉尔紧随其后，尽管他们受了些伤，但他们的冒险精神仍然不减，继续愉快地探索。
3 - 杰克，吉尔
4 - {
      "chinese_summary": "兄妹杰克和吉尔前往山顶井取水，但不幸的是，杰克绊倒在石头上滚下山，吉尔紧随其后，尽管他们受了些伤，但他们的冒险精神仍然不减，继续愉快地探索。",
      "num_names": 2
   }
```
在视频中的输出和我的并不相同，所以上面的例子没有下面这种好，下面的更明确，得到的答案也比较固定和统一。
我们看到结果是按照序号来回答的，也就是按照要求一点点回答的，这我觉得很好了，但是如果我们想要按照严格的格式，比如像下面这样：
总结： ...
翻译： ...
姓名： ...
输出 JSON ： ...
那么我们就需要使用另外一种方式来实现，看例子：
```python
# example 2, asking for output in a specified format
prompt_2 = f"""
Your task is to perform the following actions:
1 - Summarize the following text delimited by <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
response = get_completion(prompt_2)
print("InCompletion for prompt 2:")
print (response)
```
这里我使用视频中的语言，先来看看其结果：
```text
InCompletion for prompt 2:
Summary: Jack and Jill go on a quest to fetch water from a hilltop well, but misfortune strikes when Jack trips and tumbles down the hill with Jill following suit, yet they remain undeterred and continue exploring with delight.
Translation: Jack et Jill partent en quête d'eau d'un puits au sommet d'une colline, mais la malchance frappe quand Jack trébuche et dévale la colline avec Jill qui suit, mais ils restent indéfectibles et continuent à explorer avec plaisir.
Names: Jack, Jill
Output JSON: {"french_summary": "Jack et Jill partent en quête d'eau d'un puits au sommet d'une colline, mais la malchance frappe quand Jack trébuche et dévale la colline avec Jill qui suit, mais ils restent indéfectibles et continuent à explorer avec plaisir.", "num_names": 2}
```
下面我改成中文的，来看看其结果：
```text
总结: 兄妹俩在一个迷人的村庄里出发去山顶的井里取水，但不幸的是，Jack绊倒了，滚下了山，Jill也跟着摔了下来，但他们的冒险精神并没有因此而减弱。
翻译: 在一个迷人的村庄里，兄妹俩Jack和Jill出发去山顶的井里取水。他们唱着欢快的歌曲爬山，但不幸的是，Jack绊倒了，滚下了山，Jill也跟着摔了下来。尽管有些受伤，但他们回到家中得到了安慰的拥抱。尽管发生了不幸的事情，他们的冒险精神并没有因此而减弱，他们继续充满喜悦地探索着。
姓名: Jack, Jill
输出 JSON: {"chinese_summary": "在一个迷人的村庄里，兄妹俩Jack和Jill出发去山顶的井里取水。他们唱着欢快的歌曲爬山，但不幸的是，Jack绊倒了，滚下了山，Jill也跟着摔了下来。尽管有些受伤，但他们回到家中得到了安慰的拥抱。尽管发生了不幸的事情，他们的冒险精神并没有因此而减弱，他们继续充满喜悦地探索着。", "num_names": 2}
```

## Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion.

指示模型在匆忙做出结论之前思考解决方案。我们明确指示模型在做出结论之前先推理出自己的解决方案，可以获得更好的结果。即让模型说出答案是否正确之前，为模型提供足够时间去实际思考问题。

下面来看一个例子：
```python
prompt = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need help working out the financials.
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / square foot
What is the total cost for the first year of operations as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
response = get_completion(prompt)
print(response)
```
这是一道题，这上面的答案是错误的，下面我们看看结果：
```text
The student's solution is correct.
```
我们发现模型给出的答案是“正确”，很明显不是。

下面我们改善这个提示，让其先自己计算完成再得出结论，而不是匆忙的下结论：
```python
prompt = f"""
Your task is to determine if the student's solution is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem.
- Then compare your solution to the student's solution and evaluate if the student's solution is correct or not. Don't decide if the student's solution is correct until you have done the problem yourself.

Use the following format:
Question:
...
question here
...
Student's solution:
...
student's solution here
...
Actual solution:
...
steps to work out the solution and your solution here
...
Is the student's solution the same as actual solution just calculated:
...
yes or no
...
Student grade:
...
correct or incorrect
"""
# 下面就是上面的内容。
```
这样我们就可以看到其运算的过程，并且按照上面的格式进行输出：
```text
Actual Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 10x
Total cost: 100x + 250x + 100,000 + 10x = 360x + 100,000

Is the student's solution the same as actual solution just calculated:
No

Student grade:
Incorrect
```
这次我们得到的正确的答案。