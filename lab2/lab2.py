import enum
import subprocess
import re

t_print = r'\s*System\.out\.println\(\s*.*\s*\)'
t_class = r'\s*public class (?!MyClass)[A-Za-z]+'
t_if = r'\s*if'
t_def_main = r'\s*(public static void main\s*\(\s*String args\[\]\)|public class MyClass)'
t_bracket_close = r'\s*}'
t_bracket_open = r'\s*{'
t_operation = r'\s*(==|!=|>=|<=|\|\||&&|\+=|-=|\*=|=|[><!%\/])'
t_else = r'\s*(else|else if)\s*{?'
t_special = r'\s*\b(public|private|protected|int|void|boolean|String|double|char|new)\b'
t_var = r'\s*\b(?!(public|private|protected|int|void|boolean|String|double|char|class|if|else|this|return))[a-zA-Z][a-zA-Z0-9_]+\b'
t_self = r'\s*this.'
t_enter = r'\n'

class_names = []
def_names = []
var_names = []

def parse_print(text):
    match = re.match(t_print,text)
    if match:
        text = text.replace("System.out.println",'print')
    else:
        return None
    return text

def parse_brackets(text):
    match = re.match(t_bracket_open,text)
    if  match:
        text = text.replace(match.group(0),':')
        if(typeVar[-1] == TypeVAR.PARAM_DEF):
            typeVar.pop()
    elif (match := re.match(t_bracket_close,text)) != None:
        text = text.replace(re.match(t_bracket_close,text).group(0),'')
        if(type[len(type)-1] != Type.EMPTY):
            type.pop()
    else:
        return None
    return text

def parse_operations(text):
    if re.search(t_operation,text) is None:
        return None
    elif re.search(t_operation,text).group(0) == '&&':
        text = text.replace('&&','and')
    elif re.search(t_operation,text).group(0) == '||':
        text = text.replace('||','or')
    elif re.search(t_operation,text).group(0) == '!':
        text = text.replace('!','not')
    return text

def parse_self(text):
    match = re.match(t_self,text)
    if not match:
        return None
    text = text.replace(match.group(0),'self.')
    var_names.append(text[:5])
    return text

def parse_special(text):
    if re.match(t_special,text):
        return ''
    else:
        return None

def search_def(text):
    for i in def_names:
        if(i.split('/')[0] == text and ((i.split('/')[1] == class_names[-1]) or i.split('/')[1] == '')):
            return True
    return False

def parse_var(text):
    match = re.search(t_var,text)
    if not match:
        return text
    elif re.search('\(',text) and not search_def(match.group(0).replace('(','')) and match.group(0).replace('(','') not in class_names and text.count('.') == 0:
        text = text.replace(match.group(0),'def ' + match.group(0))
        if (type[-1] == Type.CLASS):
            text = text.replace('(','(self,')
        if (type.count(Type.CLASS) != 0):
            def_names.append(match.group(0)+'/'+ class_names[-1])
        else:
            def_names.append(match.group(0) + '/')
        type.append(Type.DEF)
        typeVar.append(TypeVAR.PARAM_DEF)
    elif match.group(0).replace('(','') in class_names and type[-1] == Type.CLASS:
        text = text.replace(match.group(0),'def __init__')
        if (type[-1] == Type.CLASS):
            text = text.replace('(','(self,')
        type.append(Type.CONSTRUCTOR)
        typeVar.append(TypeVAR.PARAM_DEF)
    else:
        var_names.append(match.group(0))
        if (type.count(Type.CLASS) > 0 and typeVar[-1] == TypeVAR.VAR and not (type[-1] == Type.CONSTRUCTOR or type[-1] == Type.CLASS)):
            text = text.replace(match.group(0),'self.' + match.group(0))
    text = text.replace('{',':')
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
    text = text.replace('{',':')
    return text

def parse_if(text):
    match = re.match(t_if, text)
    if not  match:
        return None
    type.append(Type.IF)
    text = text.replace('(','( ').replace('{',':')
    text = text[:2] + get_tokens(text[2:])
    return text

def parse_else(text):
    match = re.match(t_else, text)
    if not  match:
        return None
    type.append(Type.ELSE)
    text = text.replace('{',':').replace('else if','elif').replace('(','( ')
    text = text[:4] + get_tokens(text[4:])
    return text

def parse_enter(text):
    match = re.match(t_enter, text)
    if not match:
        return None
    else:
        step = 0
        for i in type:
            if i == Type.CLASS or i == Type.DEF or i == Type.IF or i == Type.ELSE or i == Type.CONSTRUCTOR:
                step += 1
        text = text.replace(match.group(0),'\n'+'\t'*step)
        if (typeVar[-1] == TypeVAR.PARAM_DEF):
            typeVar.pop()
    return text

def parse_main_def(text):
    if (re.match(t_def_main,text) != None):
        return True
    return False

def get_tokens(line):
    result_line = ''
    list_line = line.split()
    for l in list_line:
        if (re.search(t_special,l) != None and parse_special(l) == None):
            l = l.replace(re.search(t_special,l).group(0),'')
        if parse_special(l) != None or l in class_names:
            pass
        elif re.match(t_bracket_open,l) != None or re.match(t_bracket_close,l) != None:
            result_line += (parse_brackets(l))
        elif parse_self(l) != None:
            result_line += (parse_self(l) + ' ')
        elif re.search(t_var,l) != None:
            result_line += (parse_var(l) + ' ')
        elif parse_operations(l) != None:
            result_line += (parse_operations(l) + ' ')
        else:
            result_line += (l + ' ')
    return result_line

class Type(enum.Enum):
    CLASS = 0
    CONSTRUCTOR = 1
    DEF = 2
    IF = 3
    ELSE = 4
    EMPTY = 5
class TypeVAR(enum.Enum):
    PARAM_DEF = 0
    VAR = 1

type = [Type.EMPTY]
typeVar = [TypeVAR.VAR]
result = open("result.py",'w')
with open("C:\labs modern-programming\lab2\java.txt",'r') as file:
    for line in file:
        line = line.replace(';','').replace('\n','')
        if(parse_main_def(line)):
            pass
        elif re.match(t_print,line) != None:
            result.write(parse_print(line.strip()))
        elif re.match(t_class,line) != None:
            result.write(parse_class(line.strip()))
        elif re.match(t_if, line) != None:
            result.write(parse_if(line.strip()))
        elif re.match(t_else, line) != None:
            result.write(parse_else(line.strip()))
        else:
            result.write( get_tokens(line) )
        if parse_enter('\n') != None:
            result.write(parse_enter('\n'))
result.close()
print(class_names)
print(def_names)
print(var_names)
print(type)
output = subprocess.run(['python', 'result.py'], capture_output=True, text=True) #запуск команды для проигрывания кода из другого файла .py
 
print(output.stdout)

