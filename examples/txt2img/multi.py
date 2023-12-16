import os
import sys
from typing import Literal

import fire

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from wrapper import StreamDiffusionWrapper


def main(
    output: str = "output",
    model_id: str = "KBlueLeaf/kohaku-v2.1",
    prompt: str = "Girl with panda ears wearing a hood",
    width: int = 512,
    height: int = 512,
    frame_buffer_size: int = 2,
    acceleration: Literal["none", "xformers", "sfast", "tensorrt"] = "xformers",
):
    os.makedirs(output, exist_ok=True)

    stream = StreamDiffusionWrapper(
        model_id=model_id,
        t_index_list=[0, 16, 32, 45],
        frame_buffer_size=frame_buffer_size,
        width=width,
        height=height,
        warmup=10,
        acceleration=acceleration,
        is_drawing=True,
        mode="txt2img",
        use_denoising_batch=False,
        cfg_type="none",
    )

    stream.prepare(
        prompt=prompt,
        num_inference_steps=50,
    )

    output_images = stream()
    for i, output_image in enumerate(output_images):
        output_image.save(os.path.join(output, f"{i:02}.png"))


if __name__ == "__main__":
    fire.Fire(main)
