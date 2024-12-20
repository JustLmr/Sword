import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "gen-lang-client-0908696813"
output_file = "input-image.png"

vertexai.init(project=PROJECT_ID, location="us-central1")

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

images = model.generate_images(
    prompt="The white cat",
    number_of_images=1,
    language="en",
    aspect_ratio="1:1",
    safety_filter_level="block_some",
    person_generation="allow_adult",
)

# Görüntüyü kaydet
images[0].save(location=output_file, include_generation_parameters=False)

print(f"Created output image using {len(images[0]._image_bytes)} bytes")
