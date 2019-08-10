

  spell run --mount runs/4/data:datasets \
    --machine-type V100 \
    --framework tensorflow \
    "bash ./runner.sh"

