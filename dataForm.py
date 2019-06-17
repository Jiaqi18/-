
def chuli(file_name):
    g = open('./data/semi/test/baidu_neu_fenci_label.txt', 'w', encoding='utf8')

    with open(file_name,"r",encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line + "#label#:neutral" + "\n"
            g.write(line)

if __name__ == '__main__':
    chuli('./data/semi/test/baidu_neu_fenci.txt')
