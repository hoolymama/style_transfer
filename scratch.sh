

  spell run --mount runs/4/data:datasets \
    --machine-type V100 \
    --framework tensorflow \
    "bash ./runner.sh"


./face -resolution 1024 

    parser.add_argument('-m', '--margin', type=int, default=0)
    parser.add_argument('-r', '--resolution', type=int, default=512)

    # args for neural style

    parser.add_argument('--style_image', type=str, default='kate.jpg')
    parser.add_argument('--main_style_weight', type=float, default=5000)
    parser.add_argument('--detail_style_weight', type=float, default=400)
    parser.add_argument('--max_iterations', type=int, default=500)
    # parser.add_argument('-l', '--local', action='store_true', default=False)
    parser.add_argument('-t', '--test_spell',
                        action='store_true', default=False)




for style in kateWithDetailOverlay.png kateWithDetailOverlayFract.png
do
for weight in 10000 100000 1000000
do
./face --resolution 1024 --style_image $style --main_style_weight $weight extras/julian_grade/hockne-001.png
done
done
for img
./face --resolution 1024 --style_image kateWithDetailOverlayFract.png --main_style_weight 30000 extras/julian_grade/hockne-001.png


./face --resolution 1024 --style_image kateWithDetail.jpg --detail_style_weight 400 
--main_sty/Users/julian/projects/bot/style_transfer/styles/kateWithDetailOverlay.png /styles/kateWithDetailOverlayFract.png le_weight 20000 extras/julian_grade/hockne-001.png

for f in /Volumes/SSD/projects/bot/style_transfer/extras/emily/1k/*
do
./face --resolution 1400 --style_image kateWithDetailOverlayFract.png --max_iterations 100 --main_style_weight 10000 $f
done