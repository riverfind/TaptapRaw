# TaptapRaw

This is a cli tool which aim to use deepseek easily in terminal.

## Startup Setting

1. Create a powershell script and add it into your environment path
```pwsh
$basepath = Join-Path -Path $PSScriptRoot -ChildPath "TaptapRaw"
$activate = Join-Path -Path $basepath -ChildPath ".venv/Scripts/python"
$main = Join-Path -Path $basepath -ChildPath "taptap.py"
&$activate $main @args
```

2. Create file ~/.taptap/clients.json

Following is a template Setting

```json
{
  "chat": {
    "type": "DPSK",
    "base_url": "https://api.deepseek.com",
    "api_key": "xxx",
    "oneshot": false,
    "parameter": {
      "model": "deepseek-chat",
      "messages": [
        {
          "role": "system",
          "content": "Answer precisely with plaintext-format and terminal-friendly ouput (without unrelevent prompt)"
        }
      ],
      "stream": true,
      "temperature": 1.3
    }
  },
}
```
This file is a json object consists of several objects that you can configure yourself.
For this script self using, there are "type", "oneshot".

- Object Name (e.g. "chat"): you can add a profile yourself and the object name is the profile name. The first parameter of your command is the profile name. Taptap will load profile according to the profile name.
- **type**: Currently, this script only support deepseek. Therefore, just fill DPSK.
- **oneshot**: *True* is for just getting one-time response.

## Usage
```pwsh
taptap [profile name] # if the profile's oneshot is false

taptap [profile name] [message you send to the model] # if the profile's oneshot is true
```

if there is no parameter, it will load default profile (default profile's oneshot must be false)

This is a very raw tool but I hope it can help you. Welcome to contribute.
