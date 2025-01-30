from telethon import TelegramClient, events
from telethon.tl.custom import Button
from dotenv import load_dotenv
from os import getenv
import json
import wolframalpha
from memory import Memory
from uuid import uuid4
from langchain_together import Together

load_dotenv()

# Initialize Together.ai client with specified parameters
together_client = Together(
#    model="mistralai/Mistral-7B-Instruct-v0.2",
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    max_tokens=256,
    temperature = 0.6,
    top_p = 0.7,
    repetition_penalty = 1,
)

memory = Memory('BotMemories')

api_id = getenv('API_ID')
api_hash = getenv('API_HASH')
bot_token = getenv('BOT_TOKEN')
wolframalpha_app_id = getenv('WOLFRAMALPHA_APP_ID')

if not api_id or not api_hash or not bot_token:
    raise Exception('API_ID, API_HASH and BOT_TOKEN must be set in .env file')

client = TelegramClient('bot', api_id, api_hash)

MISSIONS = False
PLUGINS = False
MEMORY = False
ROLE = ""
ADD_MEMORY_MODE = False

# Define mission prompts
mission_prompts = {
    "Teach": "Your mission is to teach the user about a topic they provide. Explain concepts clearly and provide examples.",
    "Assist": "Your mission is to assist the user with a task they provide. Offer helpful guidance and complete the task to the best of your ability.",
    "Conversate": "Your mission is to engage in a conversation with the user. Be informative, interesting, and entertaining."
}

# Define roles
roles = {
    "Lawyer": "You are a lawyer. Your responses should be legally sound and well-reasoned.",
    "Developer": "You are a developer. Your responses should be technical and focused on coding and software development.",
    "Marketer": "You are a marketer. Your responses should be creative and focused on promoting products or services."
}

plugins_dict = {
    "wolframalpha": "Wolframalpha plugin lets you perform math operations. If appropriate to use it, answer exactly with: \"[WOLFRAMALPHA <query> END]\" where query is the operation you need to solve. Examples: Input: Solve for x: 2x+3=5 Output: [WOLFRAMALPHA solve (2x+3=5) for x END] Input: A*2=B solve for B Output: [WOLFRAMALPHA solve (A*2=B) for B END]. Even if you got the input in a different language, always use english in the wolframalpha query.",
}
plugins_second_question = {
    "wolframalpha": "Explain the following wolframalpha results in a comprehensive way considering the user input was: <input> \n\nwolframalpha result: <result>. If no result is given, then try to answer the question on your own. After the answer, add the text: [Wolfram]",
}
plugins_string = ""
for plugin in plugins_dict:
    plugins_string += f"\n{plugin}: {plugins_dict[plugin]}"

async def AiAgent(prompt, system_prompt="", mission=None):
    """Sends a prompt to the language model and returns the response."""
    instruction = prompt
    if system_prompt:
        instruction = f"{system_prompt} {instruction}"
    if mission:
        instruction = f"{mission_prompts[mission]} {instruction}"

    messages = f"<s>[INST] {instruction} [/INST]"
    try:
        # Use together_client to generate response
        response = await together_client.agenerate(prompts=[messages])
        # Extract text from the response and remove leading/trailing spaces
        text = response.generations[0][0].text
        text = text.strip()
        return text  # Return only the extracted text
    except IndexError:
        keyboard = []
        for mission in mission_prompts:
            keyboard.append([Button.inline(mission, data=f'activate_mission_{mission}')])
        keyboard.append([Button.inline('Disable Missions', data='disable_missions')])
        # Assuming 'event' is defined in the broader scope (e.g., within a handler)
        # If 'event' is not available, you'll need to adapt this part
        await event.respond('Choose a mission:', buttons=keyboard) 
        return "Mission selection triggered." # Indicate that a mission selection has been prompted
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while generating the response."

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hey! I am a telegram chatbot powered by Together.ai. How can I help you today?')

@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond('Here are the available commands:\n'
                         '\n/missions - list all missions'
                         '\n/missions [MISSION NAME] - enable a mission'
                         '\n/plugins toggle - enable/disable plugins'
                         '\n/plugins list - list all plugins'
                         '\n/role [ROLE NAME] - enable a role'
                         '\n/role disable - disable current role'
                         '\n/memory - enable/disable memory'
                         '\n/addmemory - add something to the memory without receiving AI response')

@client.on(events.NewMessage(pattern='/plugins list'))
async def pls(event):
    pls = []
    for plugin in plugins_dict:
        pls.append(plugin)
    await event.respond("Available plugins are:\n{}".format("\n".join(pls)))

@client.on(events.NewMessage(pattern='/plugins toggle'))
async def pls_toggle(event):
    global PLUGINS
    PLUGINS = not PLUGINS
    if PLUGINS and not wolframalpha_app_id:
        await event.respond("You need to set a wolframalpha app id in the .env file to use plugins.")
        PLUGINS = False
        return
    await event.respond("Plugins enabled" if PLUGINS else "Plugins disabled")

@client.on(events.NewMessage(pattern='/missions'))
async def missions_command(event):
    try:
        mission = event.text.split(' ')[1]
        if mission in mission_prompts:
            global MISSIONS
            MISSIONS = mission
            await event.respond(f'{mission} mission activated.')
        elif mission == 'disable':
            MISSIONS = False
            await event.respond('Missions disabled.')
        else:
            await event.respond('Invalid mission. Available missions are:\n\n' + '\n'.join(mission_prompts.keys()) + '\ndisable')
    except IndexError:
        keyboard = [] # Initialize keyboard as a list
        for mission in mission_prompts:
            keyboard.append([Button.inline(mission, data=f'activate_mission_{mission}')])
        keyboard.append([Button.inline('Disable Missions', data='disable_missions')])
        await event.respond('Choose a mission:', buttons=keyboard)

@client.on(events.NewMessage(pattern="/role"))
async def role_command(event):
    global ROLE
    try:
        role_name = event.text.split(" ")[1]
        if role_name == "disable":
            ROLE = ""
            await event.respond("Role disabled")
        elif role_name in roles:
            ROLE = roles[role_name]
            await event.respond("Role set")
        else:
            await event.respond("Role not found")
    except IndexError:
        keyboard = [] # Initialize keyboard as a list
        for role in roles:
            keyboard.append([Button.inline(role, data=f'activate_role_{role}')])
        keyboard.append([Button.inline('Disable Role', data='disable_role')])
        await event.respond('Choose a role:', buttons=keyboard)

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    global MISSIONS, ROLE
    if event.data.startswith(b'activate_mission_'):
        MISSIONS = event.data.decode().split('_')[-1]
        await event.edit(f'{MISSIONS} mission activated.')
    elif event.data == 'disable_missions':
        MISSIONS = False
        await event.edit('Missions disabled.')
    elif event.data.startswith(b'activate_role_'):
        ROLE = roles[event.data.decode().split('_')[-1]]
        await event.edit('Role set.')
    elif event.data == 'disable_role':
        ROLE = ""
        await event.edit('Role disabled.')

@client.on(events.NewMessage(pattern='/memory'))
async def memory_command(event):
    global MEMORY
    MEMORY = not MEMORY
    await event.respond("Memory enabled" if MEMORY else "Memory disabled")

@client.on(events.NewMessage(pattern='/addmemory'))
async def addmemory(event):
    global ADD_MEMORY_MODE
    global MEMORY

    ADD_MEMORY_MODE = True
    await event.respond("What do you want to add to the memory?")

@client.on(events.NewMessage())
async def handler(e):
    global MISSIONS, PLUGINS, wolframalpha_app_id, client, plugins_string, plugins_second_question, ROLE, MEMORY, memory, ADD_MEMORY_MODE

    # Check if the message is a command and ignore it
    if e.text.startswith('/'):
        return

    # Check if in ADD_MEMORY_MODE and respond accordingly
    if ADD_MEMORY_MODE:
        memory.insert(e.text, str(uuid4()))
        await e.respond("Memory added")
        ADD_MEMORY_MODE = False
        return

    my_id = await client.get_me()
    my_id = my_id.id
    my_username = await client.get_me()
    my_username = my_username.username
    if e.sender_id == my_id:
        return
    if e.is_private:
        prompt = e.text
    else:
        if not e.text.startswith(f'@{my_username}'):
            return
        prompt = e.text.replace(f'@{my_username}', '')
    msg = await e.respond('Thinking...')
    system_prompt = ""
    mission = None
    if MISSIONS:
        mission = MISSIONS
    if ROLE:
        system_prompt = ROLE
    if MEMORY:
        res = memory.find(prompt)
        if len(res) > 0 and res[0]:
            system_prompt += " To answer the next question these data may be relevant: "
            for i in res:
                if len(i) > 0:
                    system_prompt += i[0]
    if PLUGINS:
        result = await AiAgent(prompt, system_prompt, mission)
        if "[WOLFRAMALPHA" in result:
            query = result.replace("[WOLFRAMALPHA ", "").replace(" END]", "")
            wf_client = wolframalpha.Client(app_id=wolframalpha_app_id)
            res = wf_client.query(query)
            if not res["@success"]:
                result = "No results"
            else:
                result = next(res.results).text
            result = await AiAgent(plugins_second_question["wolframalpha"].replace("<input>", prompt).replace("<result>", result), mission=mission)
            if MEMORY:
                memory.insert(prompt, str(uuid4()))
                memory.insert(result, str(uuid4()))
            await msg.edit(result)
            return
        if MEMORY:
            memory.insert(prompt, str(uuid4()))
            memory.insert(result, str(uuid4()))
        await msg.edit(result)
    else:
        result = await AiAgent(prompt, system_prompt, mission)
        if result:
            result = result.replace("[INST]", "").replace("[/INST]", "").strip()
            await msg.edit(result)
        else:
            await msg.edit("Sorry, I couldn't generate a response.")

client.start(bot_token=bot_token)
client.run_until_disconnected()
