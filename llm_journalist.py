from huggingface_hub import InferenceClient

def cycling_journalist(HF_Token, data, competition_name, competition_code = None, approx_length = 500, model = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8", additional_requests =  None):

  article = ''

  request = request_builder(data, competition_name, competition_code, approx_length, additional_requests)

  # Performing LLM Request

  ## Specify the inference client
  client = InferenceClient(provider="novita", api_key=HF_Token) # "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" or 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

  # Send messages to a specific model hosted on the inference client, specifying system-level instructions
  completion = client.chat.completions.create(
      model=model,
      messages=[
          {
              "role": "user",
              "content": request
          }
        ]
      )
  article = completion.choices[0].message.content
  return article


def request_builder(data, competition_name, competition_code = None, approx_length = 500, additional_requests = None):

  # Generic request building
  request = f"You are a sports journalist, write an article about the cycling competition '{competition_name} of about {approx_length} words'. In the output provide only the body of the article without any text formatting, emojis or additional phrases. The article must be enjoyable to read and must contain only the information provided below, do not include invented data or data from any other source. Here is the data to input along with some context, skip where 'None' is provided:\n-----Data-----\n"
  request += "GENERAL INFORMATION\n"
  request += "Track Information:\n"
  request += f" Starting location of the race: {data['General'][0]['Start']}\n Ending location of the race: {data['General'][0]['Finish']}\n Type of race ('Mountain', 'Hill', 'Flat', 'Chrono'): {data['General'][0]['Type']}\n Difficulty: {data['General'][0]['Difficulty']}\n Length: {data['General'][0]['Lenght']}\n Altitude Gain: {data['General'][0]['Altitude Gain']}\n Technical Info: {data['General'][0]['Technical Info']}\n"
  request += "Weather Conditions at start:\n"
  request += f" Temperature in Celsius: {data['General'][1].loc['Start']['Temperature']}\n Conditions (data in italian translate in english if used in the article): {data['General'][1].loc['Start']['Conditions']}\n Precipitations (in mm): {data['General'][1].loc['Start']['Precipitation']}\n Wind Speed (in Km/h): {data['General'][1].loc['Start']['Wind - Speed']}\n Wind Direction: {data['General'][1].loc['Start']['Wind - Direction']}\n"
  request += "Weather Conditions at finish:\n"
  request += f" Temperature in Celsius: {data['General'][1].loc['Finish']['Temperature']}\n Conditions (data in italian translate in english if used in the article): {data['General'][1].loc['Finish']['Conditions']}\n Precipitations (in mm): {data['General'][1].loc['Finish']['Precipitation']}\n Wind Speed (in Km/h): {data['General'][1].loc['Finish']['Wind - Speed']}\n Wind Direction: {data['General'][1].loc['Finish']['Wind - Direction']}\n"
  request += f"Number of Riders that finished the race: {len(data['General'][2])}\n"
  request += "Order of Arrival, top 15:\n"
  for i in range(min(15,len(data['General'][2]))):
    request += f" Position: {data['General'][2].iloc[i]['Position']}, Rider: {data['General'][2].iloc[i]['Rider']}, Team: {data['General'][2].iloc[i]['Team']}, Time: {data['General'][2].iloc[i]['Time']}, Gap to leader: {data['General'][2].iloc[i]['Gap']}\n"

  # Specialization for non generic competitions
  if competition_code:

    ## Giro d'Italia
    if competition_code == 'G':

      ### Maglia Rosa
      request += "Maglia Rosa Standings after this race, top 15:\n"
      for i in range(min(15,len(data['Maglia Rosa Standing'][0]))):
        request += f" Position: {data['Maglia Rosa Standing'][0].iloc[i]['Position']}, Rider: {data['Maglia Rosa Standing'][0].iloc[i]['Rider']}, Team: {data['Maglia Rosa Standing'][0].iloc[i]['Team']}, Time (total sum): {data['Maglia Rosa Standing'][0].iloc[i]['Time']}\n"

      ### King of the Mountain
      request += "\nKING OF THE MOUNTAINS INFORMATION\n"

      #### Maglia Azzurra
      request += "Maglia Azzurra Standings after this race, top 15:\n"
      for i in range(min(15,len(data['King of the Mountains'][0]))):
        request += f" Position: {data['King of the Mountains'][0].iloc[i]['Position']}, Rider: {data['King of the Mountains'][0].iloc[i]['Rider']}, Team: {data['King of the Mountains'][0].iloc[i]['Team']}, Points (total sum): {data['King of the Mountains'][0].iloc[i]['Points']}\n"

      #### KOMs Current Stage
      for j in range(len(data['King of the Mountains'][1:])):
        request += f"KOM climb {j+1} of this stage standings:\n"
        for i in range(min(15,len(data['King of the Mountains'][j+1]))):
          request += f" Position: {data['King of the Mountains'][j+1].iloc[i]['Position']}, Rider: {data['King of the Mountains'][j+1].iloc[i]['Rider']}, Team: {data['King of the Mountains'][j+1].iloc[i]['Team']}, Points: {data['King of the Mountains'][j+1].iloc[i]['Points']}\n"

      ### Points Classification
      request += "\nPOINTS CLASSIFICATION INFORMATION\n"

      #### Maglia Ciclamino
      request += "Maglia Ciclamino Standings after this race, top 15:\n"
      for i in range(min(15,len(data['Intermediate Sprints'][0]))):
        request += f" Position: {data['Intermediate Sprints'][0].iloc[i]['Position']}, Rider: {data['Intermediate Sprints'][0].iloc[i]['Rider']}, Team: {data['Intermediate Sprints'][0].iloc[i]['Team']}, Points (total sum): {data['Intermediate Sprints'][0].iloc[i]['Points']}\n"

      #### KOMs Current Stage
      for j in range(len(data['Intermediate Sprints'][1:])):
        request += f"KOM climb {j+1} of this stage standings:\n"
        for i in range(min(15,len(data['Intermediate Sprints'][j+1]))):
          request += f" Position: {data['Intermediate Sprints'][j+1].iloc[i]['Position']}, Rider: {data['Intermediate Sprints'][j+1].iloc[i]['Rider']}, Team: {data['Intermediate Sprints'][j+1].iloc[i]['Team']}, Points: {data['Intermediate Sprints'][j+1].iloc[i]['Points']}\n"

      ### Official Withdrawals
      request += "\nOFFICIAL WITHDRAWALS INFORMATION\n"
      for i in range(len(data['Official Withdrawals'][0])):
        request += f" Rider: {data['Official Withdrawals'][0].iloc[i]['Rider']}, Team: {data['Official Withdrawals'][0].iloc[i]['Team']}\n"

      ### Previous Standings
      request += "\nPREVIOUS STANDINGS INFORMATION\n"
      for j in range(len(data['Previous Standings'])):
        n = 5
        if j == 0:
          n = 10
          request += "Maglia Rosa Standings before this race, top 10:\n"
        elif j == 1:
          request += "Maglia Azzurra Standings before this race, top 5:\n"
        elif j == 2:
          request += "Maglia Ciclamino Standings before this race, top 5:\n"
        for i in range(min(n,len(data['Previous Standings'][j]))):
          request += f" Position: {data['Previous Standings'][j].iloc[i]['Position']}, Rider: {data['Previous Standings'][j].iloc[i]['Rider']}, Team: {data['Previous Standings'][j].iloc[i]['Team']}\n"
      request += "-----Data End-----\nDo not mention retirements if they are not in top 15 of any standing and consider talking about the variations of the three standings.\n"

  else:
    print('Competition code not specified or recognised, the article will be generic')
    request += "-----Data End-----\n"
  request += "Use only the most relevant data to make the article as interesting as possible.\n"

    # Additional Requests
  if additional_requests:
    request += f"additionally, {additional_requests}"
  return request


def title_request_builder(article):
  request = "Write a title for the following article. In the output provide only the title without any text formatting, emojis or additional phrases.\n\n"
  request += article
  return request


def title_creator(HF_Token, article, model = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"):

  title = ''

  request = title_request_builder(article)

  # Performing LLM Request

  ## Specify the inference client
  client = InferenceClient(provider="novita", api_key=HF_Token) # or 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

  # Send messages to a specific model hosted on the inference client, specifying system-level instructions
  completion = client.chat.completions.create(
      model=model,
      messages=[
          {
              "role": "user",
              "content": request
          }
        ]
      )
  title = completion.choices[0].message.content
  return title
