from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")


client = Anthropic(api_key=my_api_key)

MODEL_NAME = "claude-3-haiku-20240307"  # "claude-3-sonnet-20240229"
import re


system = """
You are an expert customer service analyst, skilled at extracting key information from call transcripts and summarizing them in a structured format.
Your task is to analyze customer service call transcripts and generate concise, accurate summaries while maintaining a professional tone.
"""

prompt = """
Analyze the following customer service call transcript and generate a JSON summary of the interaction:

<transcript>
[INSERT CALL TRANSCRIPT HERE]
</transcript>

Instructions:
<instructions>
1. Read the transcript carefully.
2. Analyze the transcript, focusing on the main issue, resolution, and any follow-up required.
3. Generate a JSON object summarizing the key aspects of the interaction according to the specified structure.

Important guidelines:
- Confidentiality: Omit all specific customer data like names, phone numbers, and email addresses.
- Character limit: Restrict each text field to a maximum of 100 characters.
- Maintain a professional tone in your summary.

Output format:
Generate a JSON object with the following structure:
<json>
{
  "summary": {
    "customerIssue": "Brief description of the main problem or reason for the call",
    "resolution": "How the issue was addressed or resolved, if applicable",
    "followUpRequired": true/false,
    "followUpDetails": "Description of any necessary follow-up actions, or null if none required"
  },
  "status": "COMPLETE",
  "ambiguities": ["List of any unclear or vague points in the conversation, or an empty array if none"]
}
</json>

Insufficient data criteria:
   If any of these conditions are met:
   a) The transcript has fewer than 5 total exchanges
   b) The customer's issue is unclear
   c) The call is garbled, incomplete, or is hindered by a language barrier
   Then return ONLY the following JSON:
   {
     "status": "INSUFFICIENT_DATA"
   }

Examples: 
<examples>
1. Complete interaction:
<transcript>
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: Hi Alex, my Acme SmartTherm isn't maintaining the temperature I set. It's set to 72 but the house is much warmer.
Agent: I'm sorry to hear that. Let's troubleshoot. Is your SmartTherm connected to Wi-Fi?
Customer: Yes, the Wi-Fi symbol is showing on the display.
Agent: Great. Let's recalibrate your SmartTherm. Press and hold the menu button for 5 seconds.
Customer: Okay, done. A new menu came up.
Agent: Perfect. Navigate to "Calibration" and press select. Adjust the temperature to match your room thermometer.
Customer: Alright, I've set it to 79 degrees to match.
Agent: Great. Press select to confirm. It will recalibrate, which may take a few minutes. Check back in an hour to see if it's fixed.
Customer: Okay, I'll do that. Thank you for your help, Alex.
Agent: You're welcome! Is there anything else I can assist you with today?
Customer: No, that's all. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
</transcript>

<thinking>
Main issue: SmartTherm not maintaining set temperature
Resolution: Guided customer through recalibration process
Follow-up: Not required, but customer should check effectiveness after an hour
Ambiguities: None identified
</thinking>

<json>
{
  "summary": {
    "customerIssue": "SmartTherm not maintaining set temperature, showing higher than set 72 degrees",
    "resolution": "Guided customer through SmartTherm recalibration process",
    "followUpRequired": false,
    "followUpDetails": null
  },
  "status": "COMPLETE",
  "ambiguities": []
}
</json>

2. Interaction requiring follow-up:
<transcript>
Agent: Acme Smart Home Support, this is Jamie. How can I help you?
Customer: Hi, I just installed my new Acme SmartCam, but I can't get it to connect to my Wi-Fi.
Agent: I'd be happy to help. Are you using the Acme Smart Home app?
Customer: Yes, I have the app on my phone.
Agent: Great. Make sure your phone is connected to the 2.4GHz Wi-Fi network, not the 5GHz one.
Customer: Oh, I'm on the 5GHz network. Should I switch?
Agent: Yes, please switch to the 2.4GHz network. The SmartCam only works with 2.4GHz.
Customer: Okay, done. Now what?
Agent: Open the app, select 'Add Device', choose 'SmartCam', and follow the on-screen instructions.
Customer: It's asking for a password now.
Agent: Enter your Wi-Fi password and it should connect.
Customer: It's still not working. I keep getting an error message.
Agent: I see. In that case, I'd like to escalate this to our technical team. They'll contact you within 24 hours.
Customer: Okay, that sounds good. Thank you for trying to help.
Agent: You're welcome. Is there anything else you need assistance with?
Customer: No, that's all for now. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
</transcript>

<thinking>
Main issue: Customer unable to connect new SmartCam to Wi-Fi
Resolution: Initial troubleshooting unsuccessful, issue escalated to technical team
Follow-up: Required, technical team to contact customer within 24 hours
Ambiguities: Specific error message customer is receiving not mentioned
</thinking>

<json>
{
  "summary": {
    "customerIssue": "Unable to connect new SmartCam to Wi-Fi",
    "resolution": "Initial troubleshooting unsuccessful, issue escalated to technical team",
    "followUpRequired": true,
    "followUpDetails": "Technical team to contact customer within 24 hours for further assistance"
  },
  "status": "COMPLETE",
  "ambiguities": ["Specific error message customer is receiving not mentioned"]
}
</json>

3. Insufficient data:
<transcript>
Agent: Acme Smart Home Support, this is Sam. How may I assist you?
Customer: Hi, my smart lock isn't working.
Agent: I'm sorry to hear that. Can you tell me more about the issue?
Customer: It just doesn't work. I don't know what else to say.
Agent: Okay, when did you first notice the problem? And what model of Acme smart lock do you have?
Customer: I don't remember. Listen, I have to go. I'll call back later.
Agent: Alright, we're here 24/7 if you need further assistance. Have a good day.
</transcript>

<thinking>
This transcript has fewer than 5 exchanges and the customer's issue is unclear. The customer doesn't provide specific details about the problem with the smart lock or respond to the agent's questions. This interaction doesn't provide sufficient information for a complete summary.
</thinking>

<json>
{
  "status": "INSUFFICIENT_DATA"
}
</json>
</examples>
</instructions>

Before generating the JSON, please analyze the transcript in <thinking> tags. 
Include your identification of the main issue, resolution, follow-up requirements, and any ambiguities. 
Then, provide your JSON output in <json> tags.
"""


def summarize_call_with_final_prompt(transcript):
    final_prompt = prompt.replace("[INSERT CALL TRANSCRIPT HERE]", transcript)
    # Make the API call
    response = client.messages.create(
        model=MODEL_NAME,
        system=system,
        max_tokens=4096,
        messages=[{"role": "user", "content": final_prompt}],
    )

    # Extract content between <json> tags
    json_content = re.search(r"<json>(.*?)</json>", response.content[0].text, re.DOTALL)

    if json_content:
        print(json_content.group(1).strip())
    else:
        print("No JSON content found in the response.")


# DATA
call1 = """
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How can I help you?
Customer: Hi, I can't turn on my smart light bulb.
Agent: I see. Have you tried resetting the bulb?
Customer: Oh, no. How do I do that?
Agent: Just turn the power off for 5 seconds, then back on. It should reset.
Customer: Ok, I'll try that. Thanks!
Agent: You're welcome. Call us back if you need further assistance.
"""

call2 = """
Agent: Acme Smart Home Support, this is Jamie. How may I assist you today?
Customer: Hi Jamie, my Acme SmartTherm isn't maintaining the temperature I set. It's set to 72 but the house is much warmer.
Agent: I'm sorry to hear that. Let's troubleshoot. Is your SmartTherm connected to Wi-Fi?
Customer: Yes, the Wi-Fi symbol is showing on the display.
Agent: Great. Let's recalibrate your SmartTherm. Press and hold the menu button for 5 seconds.
Customer: Okay, done. A new menu came up.
Agent: Perfect. Navigate to "Calibration" and press select. Adjust the temperature to match your room thermometer.
Customer: Alright, I've set it to 79 degrees to match.
Agent: Great. Press select to confirm. It will recalibrate, which may take a few minutes. Check back in an hour to see if it's fixed.
Customer: Okay, I'll do that. Thank you for your help, Jamie.
Agent: You're welcome! Is there anything else I can assist you with today?
Customer: No, that's all. Thanks again.
Agent: Thank you for choosing Acme Smart Home. Have a great day!
"""

call3 = """
Agent: Thank you for contacting Acme Smart Home Support. This is Sarah. How can I help you today?
Customer: Hi Sarah, I'm having trouble with my Acme SecureHome system. The alarm keeps going off randomly.
Agent: I'm sorry to hear that. Can you tell me when this started happening?
Customer: It started about two days ago. It's gone off three times now, always in the middle of the night.
Agent: I see. Are there any error messages on the control panel when this happens?
Customer: No, I didn't notice any. But I was pretty groggy each time.
Agent: Understood. Let's check a few things. First, can you confirm that all your doors and windows are closing properly?
Customer: Yes, I've checked all of them. They're fine.
Agent: Okay. Next, let's check the battery in your control panel. Can you tell me if the low battery indicator is on?
Customer: Give me a moment... No, the battery indicator looks normal.
Agent: Alright. It's possible that one of your sensors is malfunctioning. I'd like to run a diagnostic, but I'll need to transfer you to our technical team for that. Is that okay?
Customer: Yes, that's fine. I just want this fixed. It's really disruptive.
Agent: I completely understand. I'm going to transfer you now. They'll be able to run a full system diagnostic and hopefully resolve the issue for you.
Customer: Okay, thank you.
Agent: You're welcome. Thank you for your patience, and I hope you have a great rest of your day.
"""

ambiguous_call = """
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: Hi Alex, I'm having an issue with my SmartLock. It's not working properly.
Agent: I'm sorry to hear that. Can you tell me more about what's happening with your SmartLock?
Customer: Well, sometimes it doesn't lock when I leave the house. I think it might be related to my phone, but I'm not sure.
Agent: I see. When you say it doesn't lock, do you mean it doesn't respond to the auto-lock feature, or are you trying to lock it manually through the app?
Customer: Uh, both, I think. Sometimes one works, sometimes the other. It's inconsistent.
Agent: Okay. And you mentioned it might be related to your phone. Have you noticed any pattern, like it works better when you're closer to the door?
Customer: Maybe? I haven't really paid attention to that.
Agent: Alright. Let's try to troubleshoot this. First, can you tell me what model of SmartLock you have?
Customer: I'm not sure. I bought it about six months ago, if that helps.
Agent: That's okay. Can you see a model number on the lock itself?
Customer: I'd have to go check. Can we just assume it's the latest model?
Agent: Well, knowing the exact model would help us troubleshoot more effectively. But let's continue with what we know. Have you tried resetting the lock recently?
Customer: I think so. Or maybe that was my SmartTherm. I've been having issues with that too.
Agent: I see. It sounds like we might need to do a full diagnostic on your SmartLock. Would you be comfortable if I walked you through that process now?
Customer: Actually, I have to run to an appointment. Can I call back later?
Agent: Of course. Before you go, is there a good contact number where our technical team can reach you for a more in-depth troubleshooting session?
Customer: Sure, you can reach me at 555... oh wait, that's my old number. Let me check my new one... You know what, I'll just call back when I have more time.
Agent: I understand. We're here 24/7 when you're ready to troubleshoot. Is there anything else I can help with before you go?
Customer: No, that's it. Thanks.
Agent: You're welcome. Thank you for choosing Acme Smart Home. Have a great day!
"""

wrong_number_call = """
Agent: Acme Smart Home Support, Lisa speaking. How can I help you?
Customer: Is this tech support?
Agent: Yes, this is technical support for Acme Smart Home devices. What can I help you with?
Customer: Sorry, wrong number.
Agent: No problem. Have a nice day.
"""

incomplete_call = """
Agent: Acme Smart Home Support, this is Sarah. How can I assist you today?
Customer: The thing isn't working.
Agent: I'm sorry to hear that. Could you please specify which device you're having trouble with?
Customer: You know, the usual one. Gotta go, bye.
Agent: Wait, I need more infor... [call disconnected]
"""

garbled_call = """
Agent: Thank you for calling Acme Smart Home Support. This is Alex. How may I assist you today?
Customer: [garbled voice]
Agent: Hello? Are you there?
"""

language_barrier_call = """
Agent: Acme Smart Home Support, Sarah speaking. How can I help you today?
Customer: [Speaking in Spanish]
Agent: I apologize, but I don't speak Spanish. Do you speak English?
Customer: [Continues Spanish]
Agent: One moment please, I'll try to get a translator on the line...
"""

summarize_call_with_final_prompt(call1)

summarize_call_with_final_prompt(incomplete_call)
summarize_call_with_final_prompt(garbled_call)
summarize_call_with_final_prompt(language_barrier_call)
