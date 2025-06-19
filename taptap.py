#!./.venv/bin/python
from openai import OpenAI
import os
import sys
import orjson

def clear_stdin():
    """Clear any pending input from the standard input buffer.

    This function ensures that no stale or unintended data remains in stdin
    before reading user input interactively. On Windows, it uses the msvcrt
    module to discard characters from the input buffer. On POSIX-compliant
    systems (e.g., Linux, macOS...), it uses select to check for available
    input without blocking and either discards the data by reading or flushes
    it using termios.tcflush if stdin is a terminal.
    """
    try:
        if os.name == "nt":
            import msvcrt  # pylint: disable=import-outside-toplevel

            # For Windows systems, Check if there is any pending input in the
            # buffer Discard characters one at a time until the buffer is empty.
            while msvcrt.kbhit():
                msvcrt.getch()
        elif os.name == "posix":
            import select  # pylint: disable=import-outside-toplevel

            # For Unix-like systems, check if there's any pending input in
            # stdin without blocking.
            stdin, _, _ = select.select([sys.stdin], [], [], 0)
            if stdin:
                if sys.stdin.isatty():
                    # pylint: disable=import-outside-toplevel
                    from termios import TCIFLUSH, tcflush

                    # Flush the input buffer
                    tcflush(sys.stdin.fileno(), TCIFLUSH)
                else:
                    # Read and discard input (in chunks).
                    while sys.stdin.read(1024):
                        pass
    except ImportError:
        pass

with open(os.path.expanduser("~/.taptap/clients.json"), "rb") as clientprofile:
    
    profile_dict = orjson.loads(clientprofile.read())
    profile = profile_dict["chat"]
    
    if len(sys.argv) > 2:
        profile = profile_dict[sys.argv[1]]
    
    response_creater = None
    content_get = None
    context = None


    if "messages" in profile["parameter"]:
        context = profile["parameter"]["messages"]
    elif "input" in profile["parameter"]:
        context = profile["parameter"]["input"]
    
    
    openai = OpenAI(api_key=profile["api_key"], base_url=profile['base_url'])
    match profile["type"]:
        case "DPSK":
            response_creater = openai.chat.completions.create
            if profile['parameter']['stream']:
                content_get = lambda response: response.choices[0].delta.content
            else:
                content_get = lambda response: response.choices[0].message.content
            
        case "OpenAI":
            response_creater = openai.responses.create
            if profile['parameter']['stream']:
                content_get = lambda response: response.output_text.delta
            else:
                content_get = lambda response: response.output_text
    
    if profile["oneshot"]:
        clear_stdin()
        context.append({"role": "user", "content": " ".join(sys.argv[2:])})
        response = response_creater(**profile["parameter"])
        ans = ""
        if profile["parameter"]["stream"]:
            for chunk in (response):
                char = content_get(chunk)
                ans += char
                print(char, end='', flush=True)
            print()
        else:
            ans = content_get(response)
            print(ans)

    else:
        while True:
            clear_stdin()
            prompt = input(">> ")
            ans = ""
            if (prompt == "exit"):
                break
            elif (prompt.isspace()):
                continue
            else:
                context.append({"role": "user", "content": prompt})
                
            response = response_creater(**profile["parameter"])
            if profile["parameter"]["stream"]:
                for chunk in (response):
                    char = content_get(chunk)
                    ans += char
                    print(char, end='', flush=True)
                print()
            else:
                ans = content_get(response)
                print(ans)
            context.append({"role": "assistant", "content": ans})

