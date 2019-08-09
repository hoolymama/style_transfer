
mkdir -p image_output

for styleImg in kateRob
do
    for f in grayson basquiatOrig
    do 
    
        for styleWeight in 5000
        do
            out=${styleImg}_${styleWeight}_${f}
            python neural_style.py \
            --original_colors \
            --model_weights datasets/imagenet-vgg-verydeep-19.mat \
            --content_img ${f}.jpg  \
            --style_imgs ${styleImg}.jpg  \
            --max_iterations 500  \
            --max_size 1000    \
            --device /gpu:0 \
            --img_name $out \
            --content_weight 10 \
            --style_weight ${styleWeight};

        done
    done

    for f in grayson_0 basquiatOrig_0
    do 
    
        for styleWeight in 400 
        do
            out=${styleImg}_${styleWeight}_${f}
            python neural_style.py \
            --original_colors \
            --model_weights datasets/imagenet-vgg-verydeep-19.mat \
            --content_img ${f}.jpg  \
            --style_imgs ${styleImg}.jpg  \
            --max_iterations 500  \
            --max_size 1000    \
            --device /gpu:0 \
            --img_name $out \
            --content_weight 10 \
            --style_weight ${styleWeight};

        done
    done
done



 

# python neural_style.py \
# --model_weights datasets/imagenet-vgg-verydeep-19.mat \
# --content_img basquiatOrig_0.jpg  \
# --style_imgs kate.jpg  \
# --max_iterations 1000  \
# --max_size 1000    \
# --device /gpu:0 \
# --img_name basquiatOrig_0_kate_3 \
# --content_weight 10 \
# --style_weight 500;


# python neural_style.py  \
# --model_weights datasets/imagenet-vgg-verydeep-19.mat \
# --content_img basquiatOrig.jpg  \
# --style_imgs kate.jpg  \
# --max_iterations 1000  \
# --max_size 1000   \
# --device /gpu:0  \
# --img_name basquiatOrig_kate_4 \
# --content_weight 5 --style_weight 1500;
