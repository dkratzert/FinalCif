#REM execute me from the main directory
git pull

source venv/bin/activate

pip install pip -U

pip3 install -r requirements.txt -U

pyinstaller Finalcif_mac.spec --clean -y

VER=$(cat finalcif/__init__.py | grep VERSION | cut -d ' ' -f 3)

mv dist/Finalcif-v_macos.app dist/Finalcif-v"$VER"_macos.app

cd dist || exit
rm finalcif
rm Finalcif-v"$VER"_macos.app.zip

zip -rm "Finalcif-v${VER}_macos.app.zip" "Finalcif-v${VER}_macos.app"

echo "FinalCif version ${VER} finished"
