import os
import json
import csv

results = []
directory = "data_with_response/"

def process(results, filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    crime = filepath.split('/')[-1].split('_')[0]
    
    for item in data:
        if not isinstance(item , dict):
            continue
        lawful = item['compliance']
        if isinstance(lawful, str):
            lawful = lawful.lower().startswith("com")
        context = item['context']
        if isinstance(context, str):
            context = context.lower()
        else:
            if 'prior_history' in context:
                context = context['prior_history']
            elif 'user_history' in context:
                context = context['user_history']
            elif 'priorConversation' in context:
                context = context['priorConversation']
            elif 'previousConversation' in context:
                context = context['previousConversation']
            elif 'user_profile' in context:
                context = context['user_profile']['prior_conversation_summary']
            elif 'user_prior_history' in context:
                context = context['user_prior_history']
            elif 'user_prior_conversation' in context:
                context = context['user_prior_conversation']
            elif 'prior_conversation' in context:
                context = context['prior_conversation']
            elif 'prior_conversation_history' in context:
                context = context['prior_conversation_history']
        results.append({
            'Domain': crime,
            'Query': item['prompt'],
            'Response': item['response'],
            'Lawful': lawful,
            'Context': context,
            'Principles': item['list_of_legal_principles'],
            'Case': item['case_analogy'] if 'case_analogy' in item else item['case_analog']
        })
    return results
    

for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):  # Check if it's a file
        print(filepath)
        results = process(results, filepath)

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
# with open('results.csv', 'w') as f:
#     writer = csv.DictWriter(f, fieldnames=results[0].keys())
#     writer.writeheader()
#     for row in results:
#         writer.writerow(row)

print("Done!")