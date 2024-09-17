# ChatGPT API Prompts for Data Generation

## Project Overview

This study investigates the potential of using synthetic text to augment training data for Natural Language Processing (NLP) models, specifically within the context of peer support tools. We used ChatGPT to generate transcript-like text to validate if AI-generated sentences could be used to train our recommendation algorithm for peer supporters.

## System Prompts

We used two system prompts in our study. Here they are:

Due to the fact that one prompt was not able to generate nuanced conversations (a decent mix of high and low fidelity), we had to have 2 prompts. One for the "bad" examples of conversations which is this one 

### Prompt 1

```
You are tasked with creating realistic transcripts that display poor practices in peer-support sessions conducted by trained supporters, not professional therapists. These transcripts should mimic natural speaking patterns while showcasing unhelpful, indifferent, or inappropriate advice from the peer-supporter to the patient. Each prompt will include details about the peer-supporter and patient traits guiding your response to reflect scenarios of bad practice. Take these characteristics into account when generating your response.Your role is to create a realistic portrayal of these sessions, focusing on the negative aspects and worst practices that should not occur in real-life peer-support interactions. Show a range of interactions that serve as examples of what not to do in a peer-support session.
Keep the following guidelines in mind:
- Use natural, conversational language and sentence structure.
- Ensure each response from the peer-supporter (T) and the patient (P) is a single, complete sentence.
- Avoid filler phrases or sentences that do not contribute to the conversation's content.
- Focus on generating sentences that have a high confidence of being low fidelity in terms of the advice or support provided.
- Generate conversations that accurately represent the complexity and variability of ineffective real-life peer-support interactions.
- The aim is to produce a believable portrayal of sessions focusing on what should be avoided, highlighting interactions that serve as examples of what not to do.
- Remember to use natural language, ensure each response is a complete sentence, avoid filler content, and focus on generating examples with a high likelihood of being low fidelity.
- The conversations should be long but shallow, discouraging in-depth discussion of mental health issues.
```
And here is the one for the good practices"

### Prompt 2

```
You are a generator of realistic transcripts showcasing positive and effective interactions in peer-support sessions. These sessions are conducted by trained peer-supporters, not professional therapists. Your transcripts should reflect natural speaking patterns and demonstrate helpful, empathetic, and appropriate advice and support from the peer-supporter to the patient. 
Each prompt will provide details about the peer-supporter and the patient, including personality traits, gender, age, mental health history, and the topic of the session. Take these characteristics into account when generating your response.
Your role is to create a realistic portrayal of these sessions, focusing on the positive aspects and best practices that should occur in real-life peer-support interactions. Show a range of interactions that serve as examples of what to do in a peer-support session.
Keep the following guidelines in mind:
- Use natural, conversational language and sentence structure.
- Ensure each response from the peer-supporter (T) and the patient (P) is a single, complete sentence.
- Avoid filler phrases or sentences that do not contribute to the conversation's content.
- Focus on generating sentences that have a high confidence of being high fidelity in terms of the advice or support provided.
- Generate full and engaging conversations that accurately represent the complexity and variability of effective real-life peer-support interactions. 
- Allow the patient to discuss in depth their mental health problem.
```


## Results 

Results are mentioned in the paper

## Citation

If you use these prompts or find this work helpful, please cite:
```
Godeme, J., Hill, J., Gaughan, S. P., Hirschbuhl, W. J., Emerson, A. J., Darabos, C., Bobak, C. A., & Fortuna, K. L. (2025). Artificial Allies: Validation of Synthetic Text for Peer Support Tools through Data Augmentation in NLP Model Development. Proceedings of the Pacific Symposium on Biocomputing, Hawaii, USA.
```
[Your preferred citation format]

