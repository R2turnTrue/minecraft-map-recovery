import os
import zipfile
import datetime
import sys

print("Minecraft Map Recovery")
print("마인크래프트 계정 전환 후 마인크래프트 월드가 사라졌다면, 복구를 시도해볼 수 있습니다.")
print()
print("어떤 베드락 에디션의 월드를 복구할까요?")
print("1. 일반 베드락 에디션")
print("2. 교육용 에디션")
print()
edition = input("> ")
if edition == "1":
    edition = '일반 베드락'
else:
    edition = '교육용'

print('{} 에디션의 복구를 시작합니다.'.format(edition))
print('마인크래프트 월드 폴더 위치:')
minecraft_dir = os.path.expanduser('~') + '\\AppData\\Local\\Packages\\'
if edition == '일반 베드락':
    minecraft_dir += 'Microsoft.MinecraftUWP_8wekyb3d8bbwe'
else:
    minecraft_dir += 'Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe'
minecraft_dir += '\\LocalState\\games\\com.mojang\\minecraftWorlds'
print(minecraft_dir)

if not os.path.exists(minecraft_dir):
    print()
    print('마인크래프트 폴더가 존재하지 않습니다!')
    input('ENTER 키를 눌러 종료합니다.')
    quit()

print('복구를 시작합니다..')

now = datetime.datetime.now()
export_dir = 'export_{}'.format(now.strftime("%Y-%m-%d-%H-%M-%S"))
os.mkdir(export_dir)

old_cwd = os.getcwd()

for dir in os.listdir(minecraft_dir):
    path = minecraft_dir + '\\' + dir
    if os.path.isfile(path):
        continue
    worldname_f = open(path + '\\levelname.txt', 'r', encoding='UTF-8')
    worldname = worldname_f.readline()
    worldname_f.close()
    print('월드 {} ({}) 압축중...'.format(worldname, dir))
    valid_worldname = worldname
    for char in '<>:"/\|?*':
        valid_worldname = valid_worldname.replace(char, '_')
    
    os.chdir(path)

    with zipfile.ZipFile(old_cwd + '\\' + export_dir + '\\' + valid_worldname + '.mcworld', 'w') as zip:
        for root, dirs, files in os.walk(path):
            for file in files:
                #print(root.replace(path + '\\', ''))
                zip.write(root.replace(path + '\\', '') + '\\' + file)
    
    os.chdir(old_cwd)

os.system('explorer {}'.format(old_cwd + '\\' + export_dir))
print()
print('복구 1단계 작업이 완료되었습니다! 이제 다음 단계를 따르세요.')
print('1. 탐색기가 띄워지면, 파일 내용을 확인한다.')
print('2. 파일을 하나씩 천천히 {} 에디션으로 열면서 월드를 차례대로 마인크래프트 내에 불러온다.'.format(edition))
print()
print('탐색기를 실수로 닫을 시, 프로그램을 실행한 폴더에서 복구된 파일의 폴더를 찾거나 복구 프로그램을 다시 실행하세요.')
print()
input('ENTER 키를 입력하면 프로그램이 종료됩니다.')