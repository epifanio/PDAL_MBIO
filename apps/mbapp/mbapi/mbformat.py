from subprocess import Popen, PIPE

def getFormats(format_name=None):
    p1 = Popen(["mbformat"], stdout=PIPE)
    mbf = p1.communicate()[0]

    mbformat = [i.strip() for i in mbf.decode().strip().split('\n\n') if i != ''][1:]

    #print(test)

    record = {j.split('\n')[1].split(':')[1].strip():{i.split(':')[0].strip():i.split(':')[1].strip() for i in j.split('\n') if ':' in i} for j in mbformat}
    if format_name:
        return list(record.keys())
    else:
        return record
    
    
    