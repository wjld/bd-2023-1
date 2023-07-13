def avaTexto(s: str) -> bool:
    return len(s) <= 200

def avaNota(s: str) -> bool:
    try:
        return int(s) > 0 and int(s) < 5
    except:
        return False

def proMatricula(s: str) -> bool:
    return len(s) == 9 and s.isdigit()

def primNome(s: str) -> bool:
    return bool(s) and len(s) <= 15 and s.isalpha()

def sobrenome(s: str) -> bool:
    return bool(s) and len(s) <= 60 and s.replace(' ','').isalpha()

def disCodigo(s: str) -> bool:
    return bool(s) and len(s) <= 15 and s.isalnum()

def disNome(s: str) -> bool:
    return bool(s) and len(s) <= 150

def denJustificativa(s: str) -> bool:
    return len(s) <= 100

def usuMatricula(s: str) -> bool:
    return len(s) == 9 and s.isdigit()

def usuSenha(s: str) -> bool:
    return len(s) >= 8 and len(s) <= 100

def usuEmail(s: str) -> bool:
    sep: str = '.-_'
    if (len(s) >= 5 and len(s) <= 100 and '@' in s
        and '..' not in s and '.' in s):
        try:
            n: str = s.split('@')[0]
            d: str = s.split('@')[1]
            validN: bool = (len(n) >= 1 and not n.startswith('.') 
                            and not n.endswith('.'))
            for c in n:
                validN = validN and (c.isalnum() or c in sep)
            validD: bool = (len(d) >= 3 and '.' in d and not d.startswith('.')
                            and not d.endswith('.')
                            and d.replace('.','').isalnum())
            for c in n:
                validN = validN and (c.isalnum() or c in sep)
            return validN and validD
        except:
            pass
    return False

def usuCurso(s: str) -> bool:
    return bool(s) and len(s) <= 50 and s.replace(' ','').isalpha()

def depCodigo(s: str) -> bool:
    return len(s) == 4 and s.isdigit()

def depNome(s: str) -> bool:
    return bool(s) and len(s) <= 150

def turNumero(s: str) -> bool:
    return bool(s) and len(s) <= 5 and s.replace(' ','').isalnum()

def turSemestre(s: str) -> bool:
    if len(s) == 6:
        try:
            return len(s.split('.')[1]) == 1 and s.replace('.','').isdigit()
        except:
            pass
    return False