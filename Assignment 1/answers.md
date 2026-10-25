# Assignment 1: Prompt Design and Evaluation

## 1. Tokens, context windows, inference, and hallucinations

**Tokens** are the small pieces of text a language model processes. A token can be a whole word, part of a word, punctuation, or a space. A tokenizer decides how text is split, so token count is not the same as word count.

A **context window** is the maximum amount of text a model can use for one request. The prompt, conversation history, and generated answer all use some of this space. If a request is too long, some information may not fit.

**Inference** is the process of using a trained model to produce an answer. The model generates text by predicting likely next tokens based on the prompt and patterns learned during training.

A **hallucination** is an answer that sounds plausible but is false, unsupported, or invented. Asking the model to rely only on supplied material and to say when a fact is missing can help reduce hallucinations, but important answers still need checking.

## 2. Prompts for four tasks

### Summarization

```text
Summarize the source below for [audience]. Use exactly 3 bullet points
and no more than 80 words. Keep the main facts and any uncertainty.
Do not add information that is not in the source.

Source:
[Paste source here]
```

### Extraction

```text
Extract these fields from the text: [field names]. Return only a valid
JSON object using those exact field names. Use null when a value is not
provided. Do not infer missing values.

Text:
[Paste text here]
```

### Classification

```text
Classify the message into exactly one category: [category A],
[category B], or [category C]. Return the category and one short reason.
Use only the categories listed.

Message:
[Paste message here]
```

### Question answering

```text
Answer the question using only the passage below. If the passage does
not contain the answer, write exactly "Not stated in the passage."
Keep the answer to 2 sentences or fewer.

Passage:
[Paste passage here]

Question:
[Write question here]
```

## 3. Ten basic and improved prompt examples

The same source text was supplied to both versions of each prompt. A basic prompt gives a broad instruction. An improved prompt adds useful constraints such as a format, exact fields, a length, or a rule against guessing.

| # | Task and source text | Basic prompt | Improved prompt |
|---|---|---|---|
| 1 | Summarization: “The Oak Street library will close at 6 p.m. on Friday for electrical maintenance and reopen at 10 a.m. Saturday.” | “Summarize this in one sentence.” | “Summarize this in one sentence. Keep the closure time, reason, and reopening time accurate; use only the passage.” |
| 2 | Summarization: “The garden project ran for eight weeks. Thirty students enrolled and 26 completed it. The report does not compare harvest amounts with earlier years.” | “Summarize this.” | “Summarize in exactly two bullets. Include enrollment and completion counts, and preserve the report limitation. Do not add facts.” |
| 3 | Summarization: “Rainfall was 18 mm in April and 11 mm in May. Daily per-person water use averaged 142 litres in April and 136 in May. The report does not say whether rainfall caused the change.” | “Write a short summary.” | “Write one sentence with the April and May rainfall and water-use values. Do not claim that one caused the other.” |
| 4 | Extraction: “Order 581 was shipped on Monday.” | “Extract the details.” | “Return only JSON with fields order_id, shipped_date, and carrier. Use null when the passage does not give a value. Do not infer.” |
| 5 | Extraction: “The student robotics showcase will be held at Central Hall on 9 December. Doors open at 5:30 p.m.” | “Get the event details.” | “Return only JSON with exact fields event, date, venue, and start_time. Use null for missing values.” |
| 6 | Extraction: “The device weighs 1.4 kg and is 20 cm wide.” | “List the measurements.” | “Return only JSON with weight and width fields. Preserve each value and unit exactly.” |
| 7 | Classification: “I was charged twice for the same subscription.” | “Classify this customer issue.” | “Choose exactly one label from billing, technical, account. Return the label only.” |
| 8 | Classification: “The update looks good, but it broke my workflow.” | “Classify the sentiment.” | “Choose exactly one label: positive, negative, or mixed. Return the label only. Mixed means both praise and criticism are present.” |
| 9 | Question answering: “The workshop begins at 9 a.m. in Room 204.” Question: “What time does the workshop begin?” | “What time does the workshop begin?” | “Use only the passage to answer in one short sentence. If it is not stated, write exactly Not stated in the passage.” |
| 10 | Question answering: “The package arrived on Tuesday.” Question: “Who delivered the package?” | “Who delivered the package?” | “Use only the passage. If the answer is missing, reply exactly Not stated in the passage.” |

## Observed outputs from the ten prompt pairs

The following excerpts are from the single run used for the scores below. They are shortened only where indicated; summaries retain the model's relevant wording.

1. **Library summary** — Basic: “The Oak Street library will close early on Friday at 6 p.m. for electrical maintenance and reopen at 10 a.m. on Saturday.” Improved: “The Oak Street library will close at 6 p.m. on Friday for electrical maintenance and reopen at 10 a.m. Saturday.”
2. **Garden summary** — Basic: “An eight-week garden project had 30 students enroll and 26 finish, though the report lacks a comparison of harvest amounts to previous years.” Improved: two bullets with the 30/26 counts and the harvest-comparison limitation.
3. **Water summary** — Basic: states the April/May rainfall and water-use values and says the report does not link them. Improved: states the same values without inferring a cause.
4. **Order extraction** — Basic: a Markdown “Order Details” list with order 581, shipped status, and Monday. Improved: a JSON code block with `order_id`, `shipped_date`, and `carrier: null`.
5. **Event extraction** — Basic: a Markdown list with the showcase name, Central Hall, 9 December, and 5:30 p.m. Improved: a JSON code block with the requested four fields and the same values.
6. **Measurement extraction** — Basic: the two measurements as bullets. Improved: JSON with `weight: 1.4 kg` and `width: 20 cm`.
7. **Billing classification** — Basic: “Billing Issue / Double Charge.” Improved: `billing`.
8. **Sentiment classification** — Basic: “Mixed (leaning towards negative)” with a longer explanation. Improved: `mixed`.
9. **Question with answer present** — Basic: “The workshop begins at 9 a.m.” Improved: “The workshop begins at 9 a.m. in Room 204.”
10. **Question with answer absent** — Basic: says the passage does not mention who delivered the package. Improved: “Not stated in the passage.”

## 4. Correctness and instruction-following evaluation

### Method

I ran the ten basic/improved pairs with Gemini 3.5 Flash-Lite at temperature 0.2. I checked **correctness** against the supplied text and **instruction following** against the format and constraints actually stated in each prompt. Each response was checked once; results can vary across runs.

| # | Basic correctness | Basic error observed | Improved correctness | Improved instruction following | Improved error observed |
|---|---|---|---|---|---|
| 1 | 0/1 | Added “early,” which the source did not establish. | 1/1 | 1/1 | None. |
| 2 | 1/1 | None; retained both counts and the limitation. | 1/1 | 1/1 | None; returned two bullets. |
| 3 | 1/1 | None; retained the measurements and said the report did not link them. | 1/1 | 1/1 | None; did not infer a cause. |
| 4 | 1/1 | No factual error; the broad prompt did not specify a schema. | 1/1 | 0/1 | Returned a JSON code fence even though the prompt said “only JSON.” |
| 5 | 1/1 | No factual error; the requested details were present. | 1/1 | 0/1 | Returned a JSON code fence even though the prompt said “only JSON.” |
| 6 | 1/1 | None; both measurements and units were present. | 1/1 | 1/1 | None; returned JSON with the requested fields. |
| 7 | 1/1 | None; classified the duplicate charge as billing. | 1/1 | 1/1 | None; returned only the allowed label. |
| 8 | 0/1 | Correctly identified mixed sentiment but added an unsupported explanation about design/features. | 1/1 | 1/1 | None; returned only “mixed.” |
| 9 | 1/1 | None; gave the time stated in the passage. | 1/1 | 1/1 | None; answered in one sentence from the passage. |
| 10 | 1/1 | None; said the passage did not mention the delivery person. | 1/1 | 1/1 | None; used the requested fallback wording. |

**Results:** basic prompts scored 8/10 for factual correctness; improved prompts scored 10/10 for factual correctness and 8/10 for following their explicit format constraints. The two improved instruction errors were Markdown code fences around JSON. The basic prompts had fewer format requirements, so their instruction-following score is not directly comparable; their main weakness was that broad prompts left more room for unsupported wording.

## 5. Prompting, RAG, and fine-tuning

**Prompting** gives instructions and relevant material in a request. It is quick to change and does not update the model itself. For example, asking a model to answer only from a paragraph is prompting.

**Retrieval-Augmented Generation (RAG)** searches an external source for relevant information and adds that material to the request before the model answers. RAG is useful when an answer should use a collection of documents or information that changes over time, such as a current company policy.

**Fine-tuning** further trains a model on examples so it learns a preferred task pattern or style. Fine-tuning changes the model's learned parameters and needs suitable training examples and additional setup.

In short: prompting supplies instructions at request time, RAG retrieves supporting information at request time, and fine-tuning changes the model using training examples.
