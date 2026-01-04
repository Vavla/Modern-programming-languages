import enum
import subprocess
import re

t_print = r'System\.out\.println$.*$' 
t_class = r'\s*public class (?!MyClass)[A-Za-z]+'
t_if = r'\s*if\(.+\){?'
t_def_main = r'\s*(public static void main(String[] args)|public class MyClass)'
t_bracket_close = r'\s*}'
t_bracket_open = r'\s*{'
t_bracket_circle_open = r'\s*$'
t_bracket_circle_close = r'\s*$'
t_operation = r'\s*(== | != | >= | <= | \|\| | && | \+= | -= | \*= | = | [><!%\/])'
t_else = r'\s*else\(.+\){?'
t_special = r'\s*(public|private|protected|int|void|boolean|String|double|char)'
t_var = r'\s*\b(?!(public|private|protected|int|void|boolean|String|double|char|class|if|else|this|return))[a-zA-Z0-9_]+\b'
t_self = r'\s*this.'
t_enter = r'\n'

class_names = []
def_names = []
var_names = []

def parse_print(text):
    match = re.match(t_print,text)
    if match:
        text = text.replace(match.group(0)[:18],'print')
    else:
        return None
    return text

def parse_brackets(text):
    match = re.match(t_bracket_open,text)
    if  match:
        text = text.replace(match.group(0),':')
    elif (match := re.match(t_bracket_close,text[j:])) != None:
        text = text.replace(re.match(t_bracket_close,text).group(0),'')
        type.pop()
    else:
        return None
    return text

def parse_operations(text):
    if re.match(t_operation,text) is None:
        return None
    elif re.match(t_operation,text).group(0) == '&&':
        text = text.replace('&&','and')
    elif re.match(t_operation,text).group(0) == '||':
        text = text.replace('||','or')
    elif re.match(t_operation,text).group(0) == '!':
        text = text.replace('!','not')
    return text

def parse_self(text):
    match = re.match(t_self,text)
    if not match:
        return None
    text = text.replace(match.group(0),'self.')
    return text

def parse_var(text):
    if re.match(t_special,text):
            text = text.replace(re.match(t_special,text).group(0),'')
    match = re.match(t_var,text)
    if not match:
        return text
    elif match not in def_names and match not in class_names and re.search('\(',text):
        text = text.replace(match.group(0),'def ' + match.group(0))
        def_names.append(match.group(0))
        type.append(Type.DEF)
    return text
    
def parse_class(text):
    match = re.match(t_class, text)
    if not match:
        return None
    text = text[7:]
    end = text[6:].find(' ') + 6
    if type[-1] != Type.CLASS:
        type.append(Type.CLASS)
        class_names.append(text[6:end])
        class_names[-1] = class_names[-1].replace('{',"")
    return text

def parse_if(text):
    match = re.match(t_if, text)
    if not  match:
        return None
    type.append(Type.IF)
    return text

def parse_else(text):
    match = re.match(t_else, text)
    if not  match:
        return None
    type.append(Type.ELSE)
    return text

def parse_enter(text):
    match = re.match(t_enter, text)
    if not match:
        return None
    else:
        step = 0
        for i in type:
            if i == Type.CLASS or i == Type.DEF or i == Type.IF or i == Type.ELSE:
                step += 1
        text = text.replace(match.group(0),'\n'+'\t'*step)
    return text

class Type(enum.Enum):
    CLASS = 0
    CONSTRUCTOR = 1
    DEF = 2
    IF = 3
    ELSE = 4
    EMPTY = 5

type = [Type.EMPTY]
result = open("result.py",'w')
with open("C:\labs modern-programming\lab2\java.txt",'r') as file:
    for line in file:
        if parse_class(line) != None:
            result.write(parse_class(line))
        elif parse_if(line) != None:
            result.write(parse_if(line))
        elif parse_else(line) != None:
            result.write(parse_else(line))
        elif parse_print(line) != None:
            result.write(parse_print(line))
        else:
            list_line = line.split()
            for l in list_line:
                if re.match(t_special,l) != None:
                    pass
                elif parse_self(l) != None:
                    result.write(parse_self(l))
                elif parse_var(l) != None:
                    result.write(parse_var(l))
                elif parse_operations(l) != None:
                    result.write(parse_operations(l))
                elif parse_brackets(l) != None:
                    result.write(parse_brackets(l))
                elif parse_enter(l) != None:
                    result.write(parse_enter(l))
                else:
                    result.write(l)
        print(line)
result.close()
#output = subprocess.run(['python', 'result.py'], capture_output=True, text=True) #запуск команды для проигрывания кода из другого файла .py
 
#print(output.stdout)

