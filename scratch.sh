

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