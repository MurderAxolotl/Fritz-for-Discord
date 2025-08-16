echo -e "Init service created"

cd /home/fritz/Fritz
echo -e "CWD: $(pwd)"

echo -e "\nHanding off to Fritz service\n"

python main.py
